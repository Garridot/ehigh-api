# Generated by Django 4.0.4 on 2022-05-30 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_order_orderdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('stock', 'Stock'), ('out-of-stock', 'Out-of-stock')], default='stock', max_length=100),
        ),
    ]
