from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login,logout
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from .models import User
# Create your views here.


# 登陆功能



class LoginView(View):
    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 与数据库对象做比较
        user = authenticate(username=username, password=password)

        if not user is None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)

                # 判断用户是否已登录(使用login_required函数，若未登陆则该函数返回一个next参数记录想访问但被屏蔽的路径)
                # 使用该函数时应注意在login.html中的表单的action属性删去，否则会硬编码导致action不能传递next参数给后端
                # form表单的action属性不填写时Django默认将表单传给当前地址（即点击提交按钮页面的当前地址）
                next_url = request.GET.get('next')
                if next_url is None or next_url == '/user/' or next_url == '/user/loginOut/':
                    next_url = reverse('goods:index')  # reverse函数为url前加上绝对路径
                # 跳转到首页
                return redirect(reverse('goods:index'))

                # return redirect(next_url)
            else:
                return render(request, 'login.html', {'errmsg': '用户未激活！'})
        else:
            return redirect(reverse('user:login_fail'))


# 登录失败显示弹窗提示
class LoginFailView(View):

    def get(self, request):
        return render(request, 'login_fail.html')


class MemberShowView(View):
    '''用户个人信息页展示'''
    def get(self, request):
        return render(request, 'member-show.html')


class LoginOutView(View):
    '''注销功能'''
    def get(self, request):
        logout(request)
        return redirect(reverse('user:login'))

@method_decorator(csrf_exempt, name='dispatch')
class ReSetPasswordView(View):
    """忘记密码功能"""
    def get(self, request):
        return render(request, 'user-password-reset.html')

    def post(self, request):
        username = request.POST.get('username')
        if username is None or username == '':
            return HttpResponse('请输入用户名！')
        user = None
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print(repr(e))
        if user is None:
            return HttpResponse('该用户不存在！')

        # 发送邮件给该用户注册时的邮箱
        email = user.email
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode()  # token是byte类型 在网页传值给后端时后端不能接收，在此将它转化为str类型。
        # 发送邮件
        subject = '雷哥'
        message = ''
        html_message = '</h1>请点击下面链接来重置您的密码！</br><a href="http://127.0.0.1:8000/user/login_reset_pwd/%s">http://127.0.0.1:8000/user/login_reset_pwd/%s</a>' % (
        token, token)
        sender = settings.EMAIL_FROM
        receiver = [email]
        send_mail(subject, message, sender, receiver, html_message=html_message)
        return HttpResponse('已发送邮件到您的邮箱!请查看您注册时的邮箱以重置密码！')


@method_decorator(csrf_exempt, name='dispatch')
class ReSetPwdView(View):
    """
    忘记密码重设密码功能
    """
    def get(self, request, token):
        return render(request, 'user-reset-pwd.html')

    def post(self, request, token):
        password = request.POST.get('password12')
        serializer1 = Serializer(settings.SECRET_KEY, 900)  # 解密信息900秒过期
        try:
            info = serializer1.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.set_password(raw_password=password)
            user.save()
        except Exception as e:
            print(repr(e))
        return HttpResponse('密码修改成功！')


class UpdateUserInfoView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
