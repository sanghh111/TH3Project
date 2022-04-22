from itertools import product
from pyexpat import model
from typing import Dict
from django.db import models
from django.contrib.auth.models import User as auth_user

# Create your models here.

# app_model

class User(models.Model):   

    # id = models.IntegerField()
    username =  models.TextField(max_length=50,primary_key=True)
    email = models.EmailField(max_length=50)
    address = models.TextField(max_length=100)
    name  = models.TextField(max_length=100, default='1')
    password = models.TextField(max_length=168)
    birthday  = models.TextField(max_length=20)
    gender = models.CharField(max_length=5,default="Nam")

    class Meta():
        db_table = "User"

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()
    # parent = models.ForeignKey(Category)

    class Meta():
        db_table =  "Category"

    def __str__(self) -> str:
        return self.name

class Product(models.Model):   
    
    name = models.CharField(max_length=50)
    stock = models.IntegerField()
    price = models.IntegerField()
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(auth_user,on_delete=models.CASCADE)
    class Meta():
        db_table =  "Product"

    def __str__(self):
        return self.name
        
class ShoppingCart(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(auth_user,on_delete=models.CASCADE)
    quality = models.IntegerField()
    unit_price = models.IntegerField()
    total_price = models.IntegerField()

    class Meta():
        db_table = "ShoppingCart"

class ProductImage(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField()

    class Meta():
        db_table = "ProductImage"

class ProductDetail(models.Model):
    product_id = models.ForeignKey(Product,on_delete= models.CASCADE)
    header = models.TextField(max_length=50)
    content = models.TextField(max_length=50)

    class Meta():
        db_table = "ProductDetail"
    
class Review(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete= models.CASCADE)
    vote = models.IntegerField()# write trigger from 0 to 5 
    content = models.CharField(max_length=200)

    class Meta():
        db_table = "Review"

class Vote(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    vote = models.FloatField()

    class Meta():
        db_table = "Vote"

class Order(models.Model):

    date = models.DateTimeField()
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    total_amount = models.FloatField(null=True)

    class Meta():
        db_table = "Order"

class OrderDetail(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    quality = models.IntegerField()
    amount = models.IntegerField(default=1)
    


    class Meta():
        db_table = "OrderDetail"

class Promotion(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    day_start = models.DateField()
    day_end = models.DateField()
    discount = models.IntegerField()

    class Meta():
        db_table = "Promotion"

