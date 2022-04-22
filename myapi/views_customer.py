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
        data.update(user = request.user)
        try :
            data['product_id'] = Product.objects.get(id=data['product_id'])
        except Product.DoesNotExist:
            return Response(
              data =  {'error' : 'product does not exist'},
              stauts = 404
            )
        if data['product_id'].stock < data['quality']:
            return Response(
              data =  {'error' : 'product does not exist'},
              stauts = 404
            )

        data.update(unit_price = data['product_id'].price)
        data.update(total_price = data['product_id'].price* data['quality'] )
        serializers.ShoppingCartSerializer().create(data)
        return Response(
            data = {
                'message' : 'add success'
            },
            status= 201
        )


class APIDetailShoppingCart(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        pass

    def put(self,request,id):
        pass

    def delete(self,request,id):
        pass


#THANH TOÁN SANR PHẨM

#Tạo comment

#XEM HÓA ĐƠN

#XEM CHI TIẾT HÁO ĐƠN


