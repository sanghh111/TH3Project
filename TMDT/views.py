from ast import keyword
from cgitb import html
import re
from unicodedata import category
from django import template
from django.shortcuts import render,redirect,get_object_or_404  

from django.http import HttpResponse
from flask import template_rendered
# Create your views here.

from .models import Category, Product,ProductDetail

from .forms import ProductForm

def index(request):
    web = HttpResponse()
    web.write('<p>Hello WORLD</p>')
    return web



def login(request):
    return render(request,'login.html')



#CURD PRODUCT
# 
#
#CREATE 

# def view_product(request):
#     products = Product.objects.all()
#     return render(request,
#     "view_product.html",
#     {'products':products})

#CURD
#LIST
def list_product(request):
    keyword = request.GET.get('keyword')
    if keyword:
        products = Product.objects.filter(name__icontains = keyword)
        # if products:
            
    else:
        products = Product.objects.all()
    return render(request,
    "product/list.html",
    {'products':products})
#CREATE CURD
def add_product(request):

    form = ProductForm()
    # print(form)
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid(): # Hàm này sẽ gọi tất cả clean_name bên form. Bất kì lôi nào xuất hiện return False
            # name = request.POST.get('name')
            # price = request.POST.get('price')
            # stock = request.POST.get('stock')
            # category = Category.objects.get(pk=request.POST.get('category_id'))
            # Product.objects.create(name=name,price=price,stock=stock,category_id=category)
            print("KHOONG CO LOI")
            form.save()
            return redirect(
                to= 'list_product'
            )
        else:
            print(form.errors)

    categorys = Category.objects.all()
    return render(request = request,
    template_name= 'product/add.html',
    context= {'categorys':categorys,
                'form': form}
    )
#READ CURD
def product_detail(request,product_id):
    product_detail = get_object_or_404(ProductDetail,id=product_id)
    return render(
        request=request,
        template_name='product/detail.html',
        context= {'product_detail': product_detail,}
    )
#UPDATE CURD
def product_update(request,product_id):

    product = get_object_or_404(Product,id=product_id)
    form = ProductForm(instance=product)
    
    if request.method == "POST":
        # name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        # category = Category.objects.get(pk=request.POST.get('category_id'))
        product.price = price
        product.stock = stock
        product.save()
        return redirect(
                to= 'list_product'
            )    
    else: 
        return render(
            request=request,
            template_name='product/update.html',
            context= {'form': form,}
        )
#DELETE CURD
def delete_product(request,product_id):
    try:
        product = Product.objects.get(id= product_id)
        product.delete()
        return redirect(
            to='list_product'
            )
    except Product.DoesNotExist:
        return render(
            request = request,
            template_name = '404.html'
        )

# def search_product(request):
#     keyword = request.GET.get('keyword')
#     if keyword:
#         products = Product.objects.filter(name__icontains = 'keyword')
#         if products:
#             return render(
#                 request= request,
#                 template_name='product/list.html',
#                 context = {'products' : products})