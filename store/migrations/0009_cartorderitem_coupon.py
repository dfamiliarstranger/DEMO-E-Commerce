# Generated by Django 4.2.7 on 2024-10-12 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorderitem',
            name='coupon',
            field=models.ManyToManyField(blank=True, to='store.coupon'),
        ),
    ]