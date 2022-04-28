from itertools import product
from rest_framework.decorators import api_view ,permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated ,IsAuthenticatedOrReadOnly , IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User as AuthUser
from django.db.models import F
from Project.settings import STATUS_ORDER
from rest_framework import status
from TMDT.models import *
from myapi.ModelViewSetMyCustom import ModelViewSetMyByUserID
from myapi.authorization import ExampleAutentication
from .serializers import *
from datetime import datetime
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# CHức năng người mua 

#XÂY DỰNG API VIEW
# CATEGORY (ADMIN LÀM GÌ, SALER LÀM GÌ, END_USER LÀM GÌ)
class APICategory(ModelViewSet):
    
    #Admin c


    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()
    # queryset = 

    serializer_class = CategorySerializer

# Product (ADMIN LÀM GÌ, SALER LÀM GÌ, END_USER LÀM GÌ)
    #THÊM PRODUCT AVALIABLE


class APIProdct(ReadOnlyModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    #ADMIN SALER CURD
    #CURD
    #LIST   list customer, saler, admin
    #CREATE create
    #UPDATE 
    #READ retrieve
    #DELTE destroy
    #END_USER: DETAIL
    def get_permissions(self):
        if self.action == 'product_detail':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else : 
            permission_classes = [IsAdminUser]
        return [auth() for auth  in  permission_classes]

    
    @action( detail=True, method = ['get'])
    def product_detail(self, request, pk):

    

        query = Product.objects.filter()
        instance = get_object_or_404(query,pk =pk)
        data = DetailProductSerializer(instance= instance).data
        

        return Response(data)
        # data.update()     

#ProductDetail ai laf nguoi tuong tac 
#Tuong tac nhung gi   

class APIProductDetail(ModelViewSetMyByUserID):

    queryset = ProductDetail.objects.annotate(user = F('product_id__user')).all() 

    permission_classes = [IsAdminUser]

    serializer_class = ProductDetailSerializer

    lookup_user = 'user'

class APIProductImage(ModelViewSetMyByUserID):
    
    queryset = ProductImage.objects.annotate(user = F('product_id__user')).all() 

    permission_classes = [IsAdminUser]

    serializer_class = ProductImageSerializer

    lookup_user = 'user'


class APIShoppingCart(ModelViewSetMyByUserID):

    permission_classes = [IsAuthenticated]

    serializer_class = ShoppingCartSerializer

    lookup_user = 'user'

    queryset = ShoppingCart.objects.all()


    #chinh serializaer_class

    #list ko caanf overide
    #retrive, create, destroy(Xem xét lại) 
    #Create so sanh dieu kien voi vaidation 


    def create(self, request, *args, **kwargs):
        data =  request.data


        #get prodcut_id 
        try:
            product = Product.objects.get(data['product_id'])
        except Product.DoesNotExist as error:
            return Response(
                data=  {
                    'message' : f'{error}'
                },
                status= status.HTTP_404_NOT_FOUND
            ) 

        data.update('user_id')
        super().create()

        