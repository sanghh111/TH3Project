from cmath import exp
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from Project.settings import DATABASES
from TMDT.models import *
from . import serializers
from django.contrib.auth.models import User as AuthUser
from django.db.models import F

class APIListProductSaler(APIView):

    permission_classes = [IsAuthenticated]


    def get(self,request):
        product = Product.objects.filter(user_id = request.user.id)
        print('product: ', product)
        # try:
        data = serializers.ProductSerializer(product,many = True).data
        print('data: ', data)
        return Response(
            data = data,
            status= 200
        )

    def post(self, request):
        
        data = request.data
        
        try:

            try:
                data['category_id'] = Category.objects.get(id= data['category_id'])
                Product.objects.get(name= data['name'], user = request.user.id)
                return Response(
                    data = {
                        'error': f'category name: {data["name"]} existed'
                    }
                )
            except Product.DoesNotExist:
                data.update(user_id = request.user.id)
                serializers.ProductSerializer().create(validated_data=data)
                return Response(
                    data = {
                        'message' : "Add product success"
                    }, 
                    status= 201
                )
            except KeyError:
                return Response(
                data = {
                    'error': f'Missing data'
                },
                status=400
            )

        except Category.DoesNotExist:
            return Response(
                data = {
                    'error' : f'Category {data["category_id"]} not already'
                },
                status= 404
            )
        

class APISalerDetaiProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        
    
        #product detail
        #product image
        try:
            product = Product.objects.get( pk = product_id, user = request.user.id)
            data = serializers.ProductSerializer(product ).data
            product_detail =  ProductDetail.objects.filter(product_id = product_id)
            print('product_detail: ', product_detail)
            if product_detail.exists():
                data_prodcut_detail = serializers.ProductDetailSerializer(product_detail,many = True).data
                data.update( product_detail =  data_prodcut_detail)
            
            product_image = ProductImage.objects.filter(product_id = product_id)
            if product_image.exists():
                data_product_image = serializers.ProductImageSerializer(product_image,many = True).data
                data.update(product_image =data_product_image)
            return  Response(
                data = data,
                status=404
            )            
        except Product.DoesNotExist:
            return Response(
                data = {
                    'error': f'product does not exist'
                },
                status=404
            )

    def put(self, request, product_id):
        try:
            product = Product.objects.get( pk = product_id, user = request.user.id)
            data_request = request.data

            try:
                query = Product.objects.filter(name = data_request['name'],user = request.user.id)
                query.exclude(id = product.id)
                if not query.exists:
                    return Response(
                data = {
                    'error': f'Can not update {data_request["name"]}'
                },
                status=409
            )
            except KeyError:
                pass

            serializers.ProductSerializer().update( 
                                instance = product,
                                validated_data = data_request
                                )
            return Response(
                data = {
                    'message': f'Update success product id {product_id}'
                },
                status=200
            )
        except Product.DoesNotExist:
            return Response(
                data = {
                    'error': f'product does not exist'
                },
                status=404
            )

    def delete(self, request , product_id):
        try:
            product = Product.objects.get( pk = product_id, user = request.user.id)
            product.delete()
            return Response(
                data = {
                    'message': f'Delete sucesss'
                },
                status = 200
            )
        except Product.DoesNotExist:
            return Response(
                data = {
                    'error': f'product does not exist'
                },
                status=404
            )
        except Exception as e:
            return Response(
                data = {
                    'error': f'{e}'
                },
                status=400
            )


class APISalerListProductDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        products  = Product.objects.filter(user = request.user.id).values('id')
        product_details = ProductDetail.objects.prefetch_related('product_id').filter(product_id_id__in = products)
        data = serializers.ProductDetailSerializer(product_details,many = True).data
        return Response(
            data = data ,
            status= 200
        )

    def post(self,request):
        try:
            data = request.data
            data['product_id'] = Product.objects.get(user = request.user.id, id = data['product_id'])
            serializers.ProductDetailSerializer().create(data)  
            return Response(
                data = {
                    'message': "Add product sucess"
                },
                status= 201
            )      
        except Product.DoesNotExist:
            return Response(
                data = {
                    'error': f'product does not exist'
                },
                status=404
            )
        except KeyError:
                return Response(
                data = {
                    'error': f'Missing data'
                },
                status=400
            )
      

class APISalerDetailProductDetail(APIView):

    permission_classes = [IsAuthenticated]

    #ID PRODUCTDETAIL Làm soa liên kết Product với Product Detail
    #  để lấy ra user thích hợp + với id 
    def get(self,request,id):
        product_detail = ProductDetail.objects.annotate(user = F('product_id__user'))
        try:
            product_detail = product_detail.get(user = request.user.id, id = id)
        except ProductDetail.DoesNotExist:
            return Response(
            data = {
                'error' : f'Product detail  does not exist' 
            },
            status = 404
        )
        data = serializers.ProductDetailSerializer(product_detail).data
        return Response(
            data = data,
            status = 200
        )
        
    def put(self,request,id):
        product_detail = ProductDetail.objects.annotate(user = F('product_id__user'))
        try:
            product_detail = product_detail.get(user = request.user.id, id = id)
        except ProductDetail.DoesNotExist:
            return Response(
            data = {
                'error' : f'Product detail  does not exist' 
            },
            status = 404)


        # if request have 'product_id'
        data = request.data
        try:
            data['product_id'] = Product.objects.get(id = data['product_id'], user = request.user.id)
        except Product.DoesNotExist:
            return Response(
                data = {
                    'error': f'Product id {data["product_id"]} does not exist' 
                },
                status= 404
            )

        #check when update appear error ??
        try:
            serializers.ProductDetailSerializer().update(
                instance= product_detail,
                validated_data= data
                )
            return Response(
                data =  {
                    'message' : 'Update success',
                },
                    status= 200
            )
        except Exception as e:
            return Response(
                data = {
                    'error': e,
                },
                    status= 400
            )


    def delete(self,request,id):
        product_detail = ProductDetail.objects.annotate(user = F('product_id__user'))
        try:
            product_detail = product_detail.get(user = request.user.id, id = id)
        except ProductDetail.DoesNotExist:
            return Response(
            data = {
                'error' : f'Product detail  does not exist' 
            },
            status = 404)
        try:
            product_detail.delete()
            return Response(
                data = {
                    'message' : "Delete suceess",
                },
                status= 200
            )
        except Exception as e:
            return Response(
                data = {
                    "error" : e,
                    },
                status= 400
            )


class APISalerListProductImage(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self,request):
        product_image = ProductImage.objects.annotate(user = F('product_id__user'))
        product_image = product_image.filter(user = request.user.id)
        # products  = Product.objects.filter(user = request.user.id).values('id')
        # product_details = ProductDetail.objects.prefetch_related('product_id').filter(product_id_id__in = products)
        data = serializers.ProductDetailSerializer(product_image,many = True).data
        return Response(
            data = data ,
            status= 200
        )

    def post(self,request):
        try:
            data = request.data
            data['product_id'] = Product.objects.get(user = request.user.id, id = data['product_id'])
            serializers.ProductImageSerializer().create(data)  
            return Response(
                data = {
                    'message': "Add product sucess"
                },
                status= 201
            )      
        except Product.DoesNotExist:
            return Response(
                data = {
                    'error': f'product does not exist'
                },
                status=404
            )
        except KeyError:
                return Response(
                data = {
                    'error': f'Missing data'
                },
                status=400
            )


class APISalerDetailProductImage(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        product_image = ProductImage.objects.annotate(user = F('product_id__user'))
        try:
            product_image = product_image.get(user = request.user.id, id = id)
        except ProductImage.DoesNotExist:
            return Response(
            data = {
                'error' : f'Product image  does not exist' 
            },
            status = 404
        )
        data = serializers.ProductImageSerializer(product_image).data
        return Response(
            data = data,
            status = 200
        )
        
    def put(self,request,id):
        product_image = ProductImage.objects.annotate(user = F('product_id__user'))
        try:
            product_image = product_image.get(user = request.user.id, id = id)
        except ProductImage.DoesNotExist:
            return Response(
            data = {
                'error' : f'Product image  does not exist' 
            },
            status = 404)


        # if request have 'product_id'
        data = request.data
        try:
            data['product_id'] = Product.objects.get(id = data['product_id'], user = request.user.id)
        except Product.DoesNotExist:
            return Response(
                data = {
                    'error': f'Product id {data["product_id"]} does not exist' 
                },
                status= 404
            )

        #check when update appear error ??
        try:
            serializers.ProductImageSerializer().update(
                instance= product_image,
                validated_data= data
                )
            return Response(
                data =  {
                    'message' : 'Update success',
                },
                    status= 200
            )
        except Exception as e:
            return Response(
                data = {
                    'error': e,
                },
                    status= 400
            )


    def delete(self,request,id):
        product_image = ProductImage.objects.annotate(user = F('product_id__user'))
        try:
            product_image = product_image.get(user = request.user.id, id = id)
        except ProductImage.DoesNotExist:
            return Response(
            data = {
                'error' : f'Product imgae  does not exist' 
            },
            status = 404)
        try:
            product_image.delete()
            return Response(
                data = {
                    'message' : "Delete suceess",
                },
                status= 200
            )
        except Exception as e:
            return Response(
                data = {
                    "error" : e,
                    },
                status= 400
            )


