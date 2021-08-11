from django.db import models
from django.contrib.auth.models import User
from Admin1.models import *


# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    number = models.CharField(max_length=10)

class addProduct(models.Model):
    p_name = models.CharField(max_length=255)
    p_desc = models.TextField()
    p_cate = models.ForeignKey(Add_Category,on_delete=models.CASCADE)
    p_price = models.DecimalField(decimal_places =2, max_digits =20)
    bid_ends= models.DateField(null=True)
    Seller = models.ForeignKey(Person,on_delete=models.CASCADE) 
    Main_image = models.ImageField(upload_to='mainimage/')
    secondary_image = models.ImageField(upload_to='secimage/')
    ter_image = models.ImageField(upload_to='terimage/')
    Status = models.CharField(max_length=50,default='some string')
    payment = models.CharField(max_length=50,default='not paid')


    @property
    def imageurl1(self):
        if self.Main_image == '':
            image = ''
        else:
            image = self.Main_image.url
        return image

    @property
    def imageurl2(self):
        if self.secondary_image == '':
            image = ''
        else:
            image = self.secondary_image.url
        return image

    @property
    def imageurl3(self):
        if self.ter_image == '':
            image = ''
        else:
            image = self.ter_image.url
        return image

class Bidding(models.Model):
    buyer = models.ForeignKey(Person,on_delete=models.CASCADE) 
    Products = models.ForeignKey(addProduct,on_delete=models.CASCADE) 
    Bid_Price = models.DecimalField(decimal_places=2, max_digits =20)

class User_Address(models.Model):
    Full_name = models.CharField(max_length=255)
    pinCode = models.PositiveIntegerField()
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    HouseName = models.CharField(max_length=150)
    landMark = models.CharField(max_length=150)
    user_address = models.ForeignKey(Person,on_delete=models.CASCADE)

class Order(models.Model):
    user_order = models.ForeignKey(Person,on_delete=models.CASCADE)
    Product = models.ForeignKey(addProduct,on_delete=models.CASCADE)
    address = models.ForeignKey(User_Address,on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=10,decimal_places=2)
    Status = models.CharField(max_length=50)
    PaymentMethod = models.CharField(max_length=20)
    Date = models.DateField(auto_now_add=True)  


