import datetime

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Customer
from django.views.generic.base import View

# Create your views here.


class CustomerListView(View):
    """客户页面展示"""
    def get(self, request):

        customers = Customer.objects.all().exclude(is_delete=1).order_by('-id')
        total = Customer.objects.exclude(is_delete=1).count()
        return render(request, 'customer-list.html', {'customers': customers, 'total': total})


class CustomerDelListView(View):
    """显示被删除的客户"""
    def get(self, request):
        customers = Customer.objects.all().exclude(is_delete=0)
        total = Customer.objects.exclude(is_delete=0).count()
        return render(request, 'customer-del-list.html', {'customers': customers, 'total': total})


@method_decorator(csrf_exempt, name='dispatch')
class CustomerInsertView(View):
    """添加客户"""
    def get(self, request):

        return render(request, 'customer-add.html')

    def post(self, request):
        username = request.POST.get('username')
        sex = request.POST.get('sex')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        remark = request.POST.get('remark')
        if not all([username, sex, mobile]):
            return HttpResponse('数据不完整！')
        customer = Customer()
        customer.name = username
        customer.sex = sex
        customer.phone = mobile
        customer.remark = remark
        customer.sex = sex
        customer.email = email
        try:
            customer.save()
        except Exception as e:
            print('未知错误！')
        return JsonResponse({'msg': '添加成功！'})


@method_decorator(csrf_exempt, name='dispatch')
class CustomerUpdateView(View):
    """编辑客户"""
    def get(self, request):
        customer_id = request.GET.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        return render(request, 'customer-edit.html', {'customer': customer})


    def post(self, request):

        customer_id = request.POST.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        createtime = customer.create_time
        if customer_id is None or customer_id == '':
            return HttpResponse('未知错误！')
        username = request.POST.get('username')
        if username is None or username == '':
            username = customer.name
        mobile = request.POST.get('mobile')
        if mobile is None or mobile == '':
            mobile = customer.phone
        email = request.POST.get('email')
        if email is None or email == '':
            email = '123456@qq.com'
        sex = request.POST.get('sex')
        if sex is None or sex == '':
            sex = customer.sex
        remark = request.POST.get('remark')
        if remark is None or remark == '':
            remark = customer.remark
        # 将数据更改
        customer.name = username
        customer.sex = sex
        customer.phone = mobile
        customer.remark = remark
        # customer.sex = sex
        customer.email = email
        customer.updata_time = datetime.datetime.now()
        customer.create_time = createtime
        try:
            customer.save()
        except Exception as e:
            print('未知错误！')
        return JsonResponse({'msg': '添加成功！'})


@method_decorator(csrf_exempt, name='dispatch')
class CustomerDelView(View):
    """"删除客户"""
    def get(self, request):
        # 获取前端操作客户的ID
        customer_id = request.GET.get('customer_id')
        # 根据ID去数据库查询该对象
        customer = Customer.objects.get(id=customer_id)
        # 对该对象进行操作
        if customer.is_delete == 1:
            customer.is_delete = 0
        else:
            customer.is_delete = 1
        customer.save()
        return redirect(reverse('customer:List'))


class CustomerInfoView(View):
    """查看客户详细信息（包括与之相关联的订单详情）"""
    def get(self, request):
        customer_id = request.GET.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        if customer is None:
            return HttpResponse('用户不存在！')
        customer_orders = customer.order_set.all()
        return render(request, 'customer-info.html', {'customer': customer, 'customer_orders': customer_orders})

