from django.contrib import admin

# Register your models here.
from .models import Order, OrderGoods


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'total_price', 'order_status', 'order_profit']


class OrderGoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'goods', 'count', 'price', 'totalPrice']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderGoods, OrderGoodsAdmin)
