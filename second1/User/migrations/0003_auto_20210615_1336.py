# Generated by Django 3.1.7 on 2021-06-15 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_bidding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproduct',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='addproduct',
            name='p_price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='bidding',
            name='Bid_Price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='bidding',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
