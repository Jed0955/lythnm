from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
class Goods(models.Model):
    name =  models.CharField(max_length=20, verbose_name=_('商品名称'))


class Category(models.Model):
    name = models.CharField(max_length=10, verbose_name=_('商品类型'))


class Unit(models.Model):
    name = models.CharField(max_length=10, verbose_name=_('单位'))


class LatestRecord(models.Model):
    date = models.DateField(verbose_name=_('最新数据日期'))


class Price(models.Model):
    date = models.DateField(verbose_name=_('数据日期'))
    goods = models.ForeignKey(Goods, verbose_name=_('商品'), blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_('商品类型'), blank=True, null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, verbose_name=_('单位'), blank=True, null=True, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name=_('均价'))
