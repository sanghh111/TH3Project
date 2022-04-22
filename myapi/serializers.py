from rest_framework.serializers import ModelSerializer
from TMDT.models import *

class CategorySerializer(ModelSerializer):

    #Create và update tự động ở trong class nó đã quy định sẵnn

    #Create chỉ cần cùng validation_data

    #validation lafm the nao h 
    class Meta():
        model =  Category
        fields = '__all__'

class ProductSerializer(ModelSerializer):
    
    class Meta():
        model =  Product
        fields = '__all__'


class ProductDetailSerializer(ModelSerializer):
    
    class Meta():
        model =  ProductDetail
        fields = '__all__'


class ProductImageSerializer(ModelSerializer):
    
    class Meta():
        model =  ProductImage
        fields = '__all__'

class ShoppingCartSerializer(ModelSerializer):
    
    class Meta():
        model =  ShoppingCart
        fields = '__all__'

