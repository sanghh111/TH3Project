import re
from unicodedata import category
from django.shortcuts import render,redirect,get_object_or_404  

from django.http import HttpResponse
# Create your views here.

from .models import Category, Product,ProductDetail

from .forms import ProductFrorm

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


#LIST

def list_product(request):
    products = Product.objects.all()
    return render(request,
    "product/list.html",
    {'products':products})


def add_product(request):

    form = ProductFrorm()
    # print(form)
    if request.method == "POST":
        form = ProductFrorm(request.POST)
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

def product_detail(request,product_id):
    product_detail = get_object_or_404(ProductDetail,id=product_id)
    return render(
        request=request,
        template_name='product/detail.html',
        context= {'product_detail': product_detail,}
    )