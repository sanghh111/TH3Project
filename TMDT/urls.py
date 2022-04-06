from django.urls import re_path

from . import views

urlpatterns = [
    # re_path('',views.index,name='index'),
    re_path(r'^login+/', views.login,name='login'),
    # re_path(r'^product+/add',views.view_product,name='view_product'),
    re_path(r'^products/$',views.list_product,name="list_product"),
    re_path(r'add-product/$',views.add_product,name="add_product"),
    re_path(r'^products\/(?P<product_id>[0-9]+)$',views.product_detail,name="product_detail"),
]