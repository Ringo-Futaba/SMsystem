from django.db import models
from db.base_model import BaseModel

# Create your models here.


class Goods(BaseModel):
    '''商品模型类'''
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )

    name = models.CharField(max_length=20, verbose_name='商品名称')
    desc = models.CharField(max_length=256, verbose_name='商品简介')
    purchase = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品进价')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='商品状态')

    def __str__(self):
        return '产品ID:'+str(self.id)+'==>'+self.name

    class Meta:
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
