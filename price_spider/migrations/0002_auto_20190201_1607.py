# Generated by Django 2.1.5 on 2019-02-01 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('price_spider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='price_spider.Category', verbose_name='商品类型'),
        ),
        migrations.AlterField(
            model_name='price',
            name='goods',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='price_spider.Goods', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='price',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='price_spider.Unit', verbose_name='单位'),
        ),
    ]