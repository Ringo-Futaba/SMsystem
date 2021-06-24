from django.contrib import admin

# Register your models here.
from .models import Goods


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]


admin.site.register(Goods, GoodsAdmin)
