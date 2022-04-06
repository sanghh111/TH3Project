from django.contrib import admin

# Register your models here.

from TMDT.models import Category, Product,ProductDetail

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductDetail)