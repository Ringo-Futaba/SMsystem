from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login,logout
from django.conf import settings
from .models import Goods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

# Create your views here.


class IndexView(View):
    def get(self, request):
        user = request.user
        return render(request, 'index.html', {'user': user})


class WelcomeView(View):
    def get(self, request):
        return render(request, 'welcome.html')


class GoodsShowView(View):
    """展示商品信息到表上（分页）"""
    def get(self, request):

        goods = Goods.objects.all().exclude(is_delete=1)
        for good in goods:
            if good.image is None or good.image == '':
                good.image = '/goods/default_product.jpg'

        total = Goods.objects.exclude(is_delete=1).count()

        return render(request, 'product-list.html', {'goods': goods, 'total': total})


class GoodsUpdateStatus(View):
    """产品的上下架功能"""
    def get(self, request):
        # 获取前端操作物品的ID
        goodId = request.GET.get('goodId')
        # 根据ID去数据库查询该对象
        good = Goods.objects.get(id=goodId)
        # from django.shortcuts import get_object_or_404
        good = get_object_or_404(Goods, pk=goodId)
        # 对该对象进行操作
        if good.status == 1:
            good.status = 0
        else:
            good.status = 1
        good.save()

        return redirect(reverse('goods:show'))


class GoodsDeleteView(View):
    """删除产品功能（假删除）"""
    def get(self, request):
        # 获取前端操作物品的ID
        goodId = request.GET.get('goodId')
        # 根据ID去数据库查询该对象
        good = Goods.objects.get(id=goodId)
        # 对该对象进行操作
        if good.is_delete == 1:
            good.is_delete = 0
        else:
            good.is_delete = 1
        good.save()
        return JsonResponse({'res': 1})


# 防止前端ajax传值不会被服务器端拦截
@method_decorator(csrf_exempt, name='dispatch')
class GoodsInsertView(View):
    """添加产品功能"""
    def get(self, request):

        return render(request, 'product-add.html')

    def post(self, request):
        # 接收页面传来的数据
        pname = request.POST.get('pname')
        desc = request.POST.get('desc')

        stock = request.POST.get('stock')
        if stock is None or stock == '' or float(stock) < 1:
            stock = 1
        purchase = request.POST.get('purchase')
        price = request.POST.get('price')
        unite = request.POST.get('unite')
        img_path = request.session.get('img_path')

        print([pname, desc, purchase, price, unite])
        # 校验数据
        if not all([pname, desc, purchase, price]) or unite == '请选择' or unite is None or pname == '':
            print('数据不完整！')
            return HttpResponse('数据不完整！')
        else:
            # 创建good实例
            good = Goods()
            good.name = pname
            good.desc = desc
            good.stock = int(stock)
            good.purchase = float(purchase)
            good.price = float(price)
            good.unite = unite
            good.image = img_path
        try:
            good.save()
            del request.session['img_path']
        except Exception as e:
            print("数据写入失败")
        return JsonResponse({'msg': '添加成功！'})


@method_decorator(csrf_exempt, name='dispatch')
class GoodsImgUpView(View):
    '''添加产品上传图片功能'''
    def get(self, request):
        return render(request, 'product-add.html')

    def post(self, request):

        # 接收页面传来的图片文件
        file = request.FILES.get('file')
        print(type(file))  # 测试能否接收到文件
        # 若图片文件合法，则将文件写入工程下的media/goods里面
        path = ''
        if file != None and file.size > 1 and file.size < 20480000:
            path = default_storage.save('./goods/' + file.name, ContentFile(file.read()))
            # 获取文件的绝对路径
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            img_path = '/goods/'+file.name
        request.session['img_path'] = img_path

        return JsonResponse({'img_path': img_path})


# 防止前端ajax传值不会被服务器端拦截
@method_decorator(csrf_exempt, name='dispatch')
class GoodsUpdateInfoView(View):
    """编辑产品信息功能"""
    def get(self, request):

        goodId = request.GET.get('goodId')
        if goodId is None:
            return HttpResponse('未知错误！')
        good = Goods.objects.get(id=goodId)
        if good.image is None or good.image == '':
                good.image = '/goods/default_product.jpg'
        return render(request, 'product-edit.html', {'good': good})


    def post(self, request):

        goodId = request.POST.get('goodId')
        if goodId is None:
            return HttpResponse('未知错误！')
        good = Goods.objects.get(id=goodId)
        pname = request.POST.get('pname')
        if pname is None or pname == '':
            pname = good.name
        desc = request.POST.get('desc')
        if desc is None or desc == '':
            desc = good.desc
        stock = request.POST.get('stock')
        purchase = request.POST.get('purchase')
        try:
            if stock is None or stock == '' or float(stock) < 1:
                stock = good.stock
            if purchase is None or purchase == '' or float(purchase) < 0:
                purchase = good.purchase
        except Exception as e:
            print(repr(e))
        price = request.POST.get('price')
        if price is None or price == '':
            price = good.price
        img_path = request.session.get('img_path')
        if img_path is None or img_path == '':
            img_path = good.image
        if not all([pname, desc, purchase, price]):
            print('数据不完整！')
            return HttpResponse('数据不完整！')
        else:
            # 创建good实例

            good.name = pname
            good.desc = desc
            good.stock = stock
            good.purchase = purchase
            good.price = price

            good.image = img_path
        try:
            good.save()
            del request.session['img_path']
        except Exception as e:
            print(repr(e))
        return JsonResponse({'msg': '修改成功'})



