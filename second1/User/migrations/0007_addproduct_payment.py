# Generated by Django 3.1.7 on 2021-06-22 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='addproduct',
            name='payment',
            field=models.CharField(default='not paid', max_length=50),
        ),
    ]