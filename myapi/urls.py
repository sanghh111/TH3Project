from django.urls import re_path
from . import views,views_saler 
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    re_path(r'^token$',view= jwt_views.TokenObtainPairView().as_view(),name='token'),
    re_path(r'^token$',view= jwt_views.TokenRefreshView().as_view(),name='token'),
    re_path(r'^categorys$',view = views.APIListCategory.as_view(), name = 'list-category'),
    re_path(r'^category/(?P<cateogry_id>[0-9]+)$',view = views.APIDetailCategory.as_view(), name = 'detail-category'),  
    re_path(r'^products$',view = views.APIListProduct.as_view(), name = 'list-product'),
    re_path(r'^product/(?P<product_id>[0-9]+)$',view = views.APIDetailProduct.as_view(), name = 'detail-product'),
    re_path(r'^product-details$',view = views.APIListProductDetail.as_view(), name = 'list-product-detail'),
    re_path(r'^saler-products$',view = views_saler.APIListProductSaler.as_view(), name = 'saler-list-product'),
    re_path(r'^saler-product/(?P<product_id>[0-9]+)$',view = views_saler.APISalerDetaiProduct.as_view(), name = 'saler-detail-product'),
    re_path(r'^saler-product-details$',view = views_saler.APISalerListProductDetail.as_view(), name = 'saler-list-product-detail'),
    re_path(r'^saler-product-detail/(?P<id>[0-9]+)$',view = views_saler.APISalerDetailProductDetail.as_view(), name = 'saler-detail-product-detail'),
]
