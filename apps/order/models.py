from django.db import models
from db.base_model import BaseModel
# Create your models here.


class Order(BaseModel):
    """订单类"""
    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单id')
    customer = models.ForeignKey('customer.Customer', verbose_name='订单所属客户', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总价')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    order_profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单利润')

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name




class OrderGoods(BaseModel):
    '''订单商品模型类'''
    order = models.ForeignKey('Order', verbose_name='订单', on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.Goods', verbose_name='商品', on_delete=models.CASCADE)
    count = models.IntegerField(default=1, verbose_name='商品数目')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品小计')


    class Meta:
        db_table = 'order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name