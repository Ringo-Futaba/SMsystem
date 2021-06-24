import uuid

from django.db.models import QuerySet, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect ,reverse


from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from customer.models import Customer
from .models import Order, OrderGoods


# Create your views here.
from django.views.generic.base import View


class OrderListView(View):
    """显示订单"""
    def get(self, request):
        orders = Order.objects.all().exclude(is_delete=1)
        # 数据和
        total = Order.objects.exclude(is_delete=1).count()
        # 用于统计订单总价的数
        order_total_price = 0
        # 用于统计订单成本价的数
        order_purchase = 0
        # 由于无前台销售系统，订单数据由自己手动录入用于测试，故创建时没有订单项数据去计算订单成交价，反向创建订单项之后计算
        for order in orders:
            # 取出该订单中的订单项，将每个订单项小计相加得到订单总计
            order_set = order.ordergoods_set.all()
            for ordergood in order_set:
                # 每个订单的总价计算 计算方式为--统合订单项的小计 但小计数据靠录入，如未经计算数据可能不准
                #   order_total_price += ordergood.totalPrice
                # 故改变计算方式，数据从订单项的商品中取，与购买数量*商品价格（即为计算订单项小计）相叠加
                order_total_price += (ordergood.count*ordergood.goods.price)
                # 每个订单的成本价计算 订单项的数量*订单项物品的原价
                order_purchase += (ordergood.count*ordergood.goods.purchase)

            order.total_price = order_total_price
            # 订单利润计算
            order.order_profit = order.total_price - order_purchase
            # 清零，否则会多个订单总价相加
            order_total_price = 0
            order_purchase = 0
        # 组织上下文对象

        context = {'orders': orders, 'total': total}
        return render(request, 'order-list.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class OrderInsertView(View):
    """添加订单"""
    def get(self, request):
        customers = Customer.objects.all().exclude(is_delete=1)
        return render(request, 'order-add.html', {'customers': customers})


    def post(self, request):
        # 获取前台数据
        order_id = uuid.uuid4()
        total_price = request.POST.get('total_price')
        status = request.POST.get('status')
        if status == '请选择' or status is None:
            return HttpResponse('数据不完整！')
        profit = request.POST.get('profit')
        customer_id = request.POST.get('customer_id')

        # 将数据写入数据库
        order = Order()
        order.order_id = order_id
        order.total_price = total_price
        order.order_status = status
        order.order_profit = profit
        order.customer = Customer.objects.get(id=customer_id)
        try:
            order.save()
        except Exception as e:
            print('未知错误！')
        return HttpResponse('添加成功！')


@method_decorator(csrf_exempt, name='dispatch')
class OrderDelView(View):
    """删除订单"""
    def get(self, request):
        order_id = request.GET.get('order_id')
        order = Order.objects.get(order_id=order_id)
        if order.is_delete == 1:
            order.is_delete = 0
        else:
            order.is_delete = 1
        order.save()
        return redirect(reverse('order:list'))


class OrderInfoView(View):
    """订单详情页"""
    def get(self, request):
        order_id = request.GET.get('order_id')
        if order_id is None or order_id == '':
            return HttpResponse('未知错误！')
        order = Order.objects.get(order_id=order_id)
        # 对数据进行过滤 若good_id相同则合并为一条
        ordergoods = OrderGoods.objects.filter(order_id=order_id).exclude(is_delete=1)

        """ordergoods2 = OrderGoods.objects.filter(order_id=order_id).exclude(is_delete=1)
        for ordergood in ordergoods:        将相同商品数量相加 总价相加
            for ordergood2 in ordergoods2:
                if ordergood.goods_id == ordergood2.goods_id and ordergood.id != ordergood2.id:
                    ordergood.count += ordergood2.count
                    ordergood.totalPrice += ordergood2.totalPrice"""
        # 计算订单成本价(商品进价和)，应付价（商品售价和）
        purchase = 0
        total_price = 0
        for ordergood in ordergoods:
            # 订单项的price属性既是对应商品的售价
            ordergood.price = ordergood.goods.price
            # 订单项小计计算   购买数量*物品售价 反复相加得到订单总价
            ordergood.totalPrice = ordergood.goods.price * ordergood.count
            # 订单项成本价计算 同上
            purchase = purchase+(ordergood.goods.purchase*ordergood.count)
            total_price = total_price+ordergood.totalPrice
        #  由于没有前台销售系统，故订单项数据是靠自己导入来测试的 其中的price，totalPrice数据应经过计算得出而不是直接导入，
        #  所以有可能出现由于订单项的小计数据和price数据导入错误的情况，故填补该错误，数据全从商品中取，再重复导入到订单项中
        #  故现在补充导入，只为测试使用，实际上线应优化此行
            ordergood.save()

        # 计算利润率
        discount = 0
        try:
            discount = (abs(purchase-total_price)/purchase)*100
            discount = round(discount, 2)
        except Exception as e:
            print('除数为0')

        # 由于没有前台销售系统 故订单数据是靠自己导入来测试的 其中的利润属性由于没有数据故无法计算，现在计算并写入。
        # 但只为测试使用，实际上线应优化此行
        order.order_profit = total_price-purchase
        order.total_price = total_price
        # 若订单的total_price（订单应付价）属性和order_profit（订单利润）属性未经计算而导入错误数据，则在查看了订单详情后自动修正
        order.save()
        context = {'order': order, 'ordergoods': ordergoods, 'total_price': total_price,
                   'purchase': purchase, 'discount': discount}
        return render(request,  'order-info.html', context)


class OrderDelListView(View):
    """显示已删除的订单"""
    def get(self, request):
        orders = Order.objects.all().exclude(is_delete=0)
        total = Order.objects.exclude(is_delete=0).count()

        return render(request, 'order-del-list.html', {'orders': orders, 'total': total})


@method_decorator(csrf_exempt, name='dispatch')
class OrderSearchByDateView(View):
    """根据日期区间来查询订单"""
    def get(self, request):
        return redirect(reverse('order:list'))

    def post(self, request):
        date_min = request.POST.get('datemin')
        if date_min is None or date_min == '':
            date_min = '1000-01-01'
        date_min = datetime.strptime(date_min, "%Y-%m-%d")
        date_max = request.POST.get('datemax')
        if date_max is None or date_max == '':
            date_max = '9999-09-09'
        date_max = datetime.strptime(date_max, "%Y-%m-%d")

        orders = Order.objects.all().exclude(is_delete=1).filter(create_time__range=(date_min, date_max))
        # 数据和
        total = Order.objects.exclude(is_delete=1).filter(create_time__range=(date_min, date_max)).count()
        # 用于统计订单总价的数
        order_total_price = 0
        # 用于统计订单成本价的数
        order_purchase = 0
        # 由于无前台销售系统，订单数据由自己手动录入用于测试，故创建时没有订单项数据去计算订单成交价，反向创建订单项之后计算
        for order in orders:
            # 取出该订单中的订单项，将每个订单项小计相加得到订单总计
            order_set = order.ordergoods_set.all()
            for ordergood in order_set:
                # 每个订单的总价计算 计算方式为--统合订单项的小计 但小计数据靠录入，如未经计算数据可能不准
                #   order_total_price += ordergood.totalPrice
                # 故改变计算方式，数据从订单项的商品中取，与购买数量*商品价格（即为计算订单项小计）相叠加
                order_total_price += (ordergood.count * ordergood.goods.price)
                # 每个订单的成本价计算 订单项的数量*订单项物品的原价
                order_purchase += (ordergood.count * ordergood.goods.purchase)

            order.total_price = order_total_price
            # 订单利润计算
            order.order_profit = order.total_price - order_purchase
            # 清零，否则会多个订单总价相加
            order_total_price = 0
            order_purchase = 0
        # 组织上下文对象
        context = {'orders': orders, 'total': total}
        return render(request, 'order-list.html', context)


class CountChartsView(View):
    """统计图"""
    def get(self, request):

        year = request.GET.get('year')
        if year is None or year == '' or year == '请选择':
            year = 2019
        years = range(2000, 2030)
        data_list = []
        count = 0
        for i in range(1, 13):
            m = str(i)
            try:
                date_Min = str(year) + '-{0}-01'.format(m)
                date_Min = datetime.strptime(date_Min, "%Y-%m-%d")
                if m == '1' or m == '3' or m == '5' or m == '7' or m == '8' or m == '10' or m =='12':
                    date_Max = str(year) + '-{0}-31'.format(m)
                    date_Max = datetime.strptime(date_Max, "%Y-%m-%d")
                elif m == '2':
                    date_Max = str(year) + '-{0}-28'.format(m)
                    date_Max = datetime.strptime(date_Max, "%Y-%m-%d")
                else:
                    date_Max = str(year) + '-{0}-30'.format(m)
                    date_Max = datetime.strptime(date_Max, "%Y-%m-%d")
                orders = Order.objects.all().exclude(is_delete=1).filter(create_time__range=(date_Min, date_Max))
                for order in orders:
                    count = count + float(order.total_price)
            except Exception as e:
                print(repr(e))
            data_list.append(count)
            count = 0
        return render(request, 'count_charts.html', {'data_list': data_list, 'years': years, 'year': year})

    def post(self, request):
        pass
