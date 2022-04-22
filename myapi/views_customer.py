from pickle import TRUE
from sys import exec_prefix
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User as AuthUser
from rest_framework.views import APIView
from django.db.models import F
from TMDT.models import *
from . import serializers

# CHức năng người mua 

# TÌM KIẾM SẢN PHẨM THEO DANH MỤC
@api_view(['GET'])
def sreach_category(request,id):
    product = Product.objects.filter(category_id = id)
    data = serializers.ProductSerializer(product ,many = True),data
    return Response(
        data = data,
        status= 200
    )



# TÌM KIẾM SẢN PHẨM THEO TỪ KHÓA LÀM SMART SREACH

#CURD GIỎ HÀNG
class APIListShoppingCart(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = ShoppingCart.objects.filter(user_id = request.user.id)
        data = serializers.ShoppingCartSerializer(cart , many =True).data
        return Response(
                data = data,
                status =200 

        )



    #POST TEMPLATE JSON
    #{
    # productID Connect Product get name unit_price 
    # total_Price = unit * quality
    # ammout <= stock
    # }
    def post(self,request):
        

        data = request.data
        data.update(request.user.id)
        try:
            product = Product.objects.get(id = data['product_ids'] )
        except Product.DoesNotExist:
            return Response(
                data = {
                    'error' : 'Product does not exist'
                },
                status = 404
            )
        try:
            if data['quality'] > product.stock:
                return Response(
                data = {
                    'error' : 'quality garther than stock'
                },
                status = 400
            )
            data.update(product.price)
        except KeyError:
            return Response(
                data = {
                    'error' : 'missing data'
                },
                status = 400
            )

#THANH TOÁN SANR PHẨM

#XEM HÓA ĐƠN

#XEM CHI TIẾT HÁO ĐƠN

#Tạo comment

