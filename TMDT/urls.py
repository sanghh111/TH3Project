from django.urls import re_path
from . import class_base_view
from . import views

urlpatterns = [
    # re_path('',views.index,name='index'),
    re_path(r'^login+/', views.login,name='login'),
    # re_path(r'^product+/add',views.list_product,name='view_product'),
    re_path(r'^products/$',views.list_product,name="list_product"),
    re_path(r'add-product/$',views.add_product,name="add_product"),
    re_path(r'^products\/(?P<product_id>[0-9]+)$',views.product_detail,name="product_detail"),
    re_path(r'^products\/update\/(?P<product_id>[0-9]+)$',views.product_update,name="product_update"),
    re_path(r'^products\/delete\/(?P<product_id>[0-9]+)$',views.delete_product,name="delete_product"),
    re_path(r'^list-product/products$',class_base_view.ProductListView.as_view(),name="list_class_product"),
    re_path(r'^detail-product\/(?P<pk>[0-9]+)$',class_base_view.ProductDetail.as_view(),name="detail_class_product"),
    re_path(r'^create-product$',class_base_view.PrductCreate.as_view(),name="create_class_product"),
    re_path(r'^update-product\/(?P<pk>[0-9]+)$',class_base_view.ProductUpdate.as_view(),name="update_class_product"),
]