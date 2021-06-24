from django.db import models
from django.db import models
from db.base_model import BaseModel
# Create your models here.


class Customer(BaseModel):

    name = models.CharField(max_length=20, verbose_name='客户姓名')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    remark = models.CharField(max_length=255, verbose_name='客户备注')
    sex = models.CharField(max_length=20, verbose_name='性别', default='男')
    email = models.EmailField(max_length=50, verbose_name='邮箱', null=True, blank=True)

    class Meta:
        db_table = 'customer'
        verbose_name = '客户'
        verbose_name_plural = verbose_name
