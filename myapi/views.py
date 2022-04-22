from django.shortcuts import render
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from TMDT.models import *
from . import serializers


#SHOW ALL LIST CATEGORY (GET) AND ADD A NEW CATEGORY(POST)

class APIListCategory(APIView):
    
    # permission_classes = [IsAuthenticated]
    #doc du lieu list category
    def get(self,request):
        # print(type(request.user))
        category = Category.objects.all()
        serializer = serializers.CategorySerializer(category,many = True)
        return Response(
            data=serializer.data,
            status=200)
    
    #Them du lieu moi
    def post(self,request):
        try:
            Category.objects.get(name = request.data['name'])
            return  Response(
                data = {
                    'error' : f'Cateogory name: {request.data["name"]}  existed ' 
                },
                status= 409
            )   
        except Category.DoesNotExist:
            serializer = serializers.CategorySerializer().create(validated_data= request.data)
            return Response(
                data = {
                    'message': "add proucts sucess" 
                },
                status = 201
            )

class APIDetailCategory(APIView):

    # 
    #CHI TIẾT CATEGORY
    def get(self,request,cateogry_id):
        try:
            category = Category.objects.get(id = cateogry_id)
            serializer = serializers.CategorySerializer(category)
            return Response(
                data=serializer.data,
                status=200)
        except Category.DoesNotExist:
            return  Response(
                data = {
                    'error' : f'Cateogory id: {request.data["name"]} does not exist ' 
                },
                status= 404
            ) 

    #chỉnh sửa category
    def put(self, request,cateogry_id):
        try:
            category = Category.objects.get(id = cateogry_id)
            try:
                Category.objects.get( name = request.data['name'])
                if category.name == request.data['name']:
                    serializers.CategorySerializer().update(category,request.data)
                    return Response(
                    data = {
                        'message': f'update proucts with id = {category.id} sucess' 
                    },
                    status = 200
                )
                else:
                    return  Response(
                data = {
                    'error' : f'Cateogory name: {request.data["name"]} existed ' 
                },
                status= 409
            ) 
            except Category.DoesNotExist:
                serializers.CategorySerializer().update(category,request.data)
                return Response(
                    data = {
                        'message': f'update proucts with id = {request.data["id"]} sucess' 
                    },
                    status = 200
                )
        except Category.DoesNotExist:
            return  Response(
                data = {
                    'error' : f'Cateogory id: {request.data["name"]} does not exist ' 
                },
                status= 404
            ) 


    def delete(self,request,cateogry_id):
        try:
            category = Category.objects.get(id = cateogry_id)
            category.delete()
            return Response(
                data =  {
                    'message': f'Delete success'
                },
                status= 200
            )
        except Category.DoesNotExist:
            return  Response(
                data = {
                    'error' : f'Cateogory id: {cateogry_id} does not exist ' 
                },
                status= 404
            ) 

class APIListProduct(APIView):

    # permission_classes = [IsAuthenticated]
    #doc du lieu list category
    def get(self,request):
        product = Product.objects.all()

        data = request.data
        print('data: ', type(data))
        serializer = serializers.ProductSerializer(product,many = True)
        return Response(
            data=serializer.data,
            status=200)
    
    #Them du lieu moi
    def post(self,request):
        try:
            Product.objects.get(name = request.data['name'])
            return  Response(
                data = {
                    'error' : f'Product name: {request.data["name"]}  existed ' 
                },
                status= 409
            )   
        except Product.DoesNotExist:
            try: 
                request.data['category_id'] = Category.objects.get(id = request.data['category_id'])
                data = request.data
                data.update(user = request.user)
                
                serializer = serializers.ProductSerializer().create(validated_data= request.data)
                return Response(
                    data = {
                        'message': "add proucts sucess" 
                    },
                    status = 201
                )
            except Category.DoesNotExist:
                return  Response(
                data = {
                    'error' : f'Category_id: {request.data["category_id"]}  does not exist ' 
                },
                status= 404
            )   

class APIDetailProduct(APIView):
    
    # permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        try:
            product = Product.objects.get( id = product_id)
            data = serializers.ProductSerializer(product).data
            
            try:
                product_detail = ProductDetail.objects.get(product_id = product_id)
                serializer_product_detail = serializers.ProductDetailSerializer(product_detail).data
                data.update(product_detail= serializer_product_detail)
            except ProductDetail.DoesNotExist:
                pass
            except ProductDetail.MultipleObjectsReturned:
                product_detail = ProductDetail.objects.filter(product_id = product_id)
                serializer_product_detail = serializers.ProductDetailSerializer(product_detail, many =True).data
                data.update(product_detail= serializer_product_detail)

            return Response(
                data = data,
                status= 200
            )
        except Product.DoesNotExist :
            return Response(
                data =  {
                    'error' : f'prodcut id {product_id} does not exist'
                },
                status= 404
            )

    def put(self, request, product_id):
        try:
            product = Product.objects.get(id = product_id)
            try: 
                request.data['category_id'] = Category.objects.get(id = request.data['category_id']) 
                serializer = serializers.ProductSerializer().update( instance=product,validated_data= request.data)
                return Response(
                    data = {
                        'message': f'update product with id: {product_id}'
                    },
                    status= 200
                )
            except Category.DoesNotExist:
                return  Response(
                data = {
                    'error' : f'Category_id: {request.data["category_id"]}  does not exist ' 
                },
                status= 404
            )   
            except KeyError:
                serializer = serializers.ProductSerializer().update( instance=product,validated_data= request.data)
                return Response(
                    data = {
                        'message': f'update product with id: {product_id}'
                    },
                    status= 200
                )
        except Product.DoesNotExist:
            return Response(
                data =  {
                    'error' : f'prodcut id {product_id} does not exist'
                },
                status= 404
            )

    def delete(self,request,product_id):
        try:
            product = Product.objects.get(id = product_id)
            product.delete()
            return Response(
                data =  {
                    'message' : f'Delete OK'
                },
                status= 200
            )
        except Product.DoesNotExist:
            return Response(
                data =  {
                    'error' : f'prodcut id {product_id} does not exist'
                },
                status= 404
            )   

class APIListProductDetail(APIView):
    
    # permission_classes = [IsAuthenticated]

    #Hiện thị list ProductDetail
    #KHONG PHAI NG BAN KHONG DUOC THEM SAN PHAM VAO
    def get(self, request):
        product_detail = ProductDetail.objects.all()
        serializer = serializers.ProductDetailSerializer(product_detail,many  = True) # show all
        return Response(
            data = serializer.data,
            status= 200
        )

    # THÊM PRODUCT DETAIL VÀO PRODUCT ?
    def post(self, request):
        data = request.data
        try:   
            data['product_id'] = Product.objects.get(id  = data['product_id'])
            try:
                serializers.ProductDetailSerializer().create(data)
                return Response(
                    data = { 
                        'message': 'ProductDeatil add success'
                    },
                    status= 201
                )
            except Exception as e:
                return Response(
                    data =  {
                        'message' : f'{e}'
                        },
                    status= 400
                )
        except Product.DoesNotExist:
            return Response(
                data = {
                    'message' : f'Product id: {data["product_id"]} does not exist'
                },
                status= 404
            )
        except KeyError:
            return Response(
                data = {
                    'message' : "Missing data",
                },
                status= 400
            )

class APIDetailProduct(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self,requet,product_detail_id):
        try:
            product_detail = ProductDetail.objects.get(id = product_detail_id)
            serializer = serializers.ProductDetailSerializer(product_detail)
            return Response(
                data = serializer.data,
                status= 200
            )
        except ProductDetail.DoesNotExist:
            return Response(
                data = {
                    'error' : f"Product detail {product_detail_id} does not exist",
                },
                status= 404
            )
        except KeyError:
            return Response(
                data = {
                    'message' : "Missing data",
                },
                status= 400
            )
    
    def put(self,request,product_detail_id):
        data = request.data
        try:
            product_detail = ProductDetail().objects.get(id = product_detail_id)
            try:
                data['product_id'] = Product.objects.get(id = data['product_id'])        
                serializers.ProductDetailSerializer().update(
                                instance=product_detail,
                                validated_data= data
                                )
                return Response(
                    data= {
                        'message': f'Product Deltail {product_detail_id} update sucess'
                    },
                    status = 200)
            except Product.DoesNotExist:
                return Response(
                    data = {
                        'error' : f'Product  {data["product_id"]} does not exist',
                    },
                    status= 404
                )
            except KeyError:
                serializers.ProductDetailSerializer().update(
                                instance=product_detail,
                                validated_data= data
                                )
                return Response(
                    data= {
                        'message': f'Product Deltail {product_detail_id} update sucess'
                    },
                    status = 200
                )
        except ProductDetail.DoesNotExist:
            return Response(
                data = {
                    'error' : f"Product detail {product_detail_id} does not exist",
                },
                status= 404
            )

    def delete(self,request,product_detail_id):
        try:
            product_detail = ProductDetail().objects.get(id = product_detail_id)
            product_detail.delete()
            return Response(
                    data= {
                        'message': f'Product Deltail {product_detail_id} delete success'
                    },
                    status = 200
                ) 
        except ProductDetail.DoesNotExist:
            return Response(
                data = {
                    'error' : f"Product detail {product_detail_id} does not exist",
                },
                status= 404
            )
    






# Create your views here.
#API có liên quan tới DATABAE -> áp dụng CURD
#REST API: Cần biết url + HTTP method   
#HTTP method:  các method thông dụng GET, POST, PUT, PATCH, DELETE, OPTIONS,..........
#ỨNG với mỗi METHOD:
# GET: Lấy thông tin từ APIs. Lấy hết hoặc 1 : READ
# POST: Tạo mới 1 dữ liệu, thêm mới add, :ADD
# PUT: Cập nhập, chỉnh sửa dữ liệu (Thường là gửi tất cả dữ liệu  của đối tượng, thường gửi thông tin củ cái gì muốn thay đổi)+     thông tin để xác định đối tượng chỉnh sửa: UPDATE
# PATCH: Cập nhập, chỉnh sửa (Chỉ gửi những cái gì muốn đổi)+ thông tin để xác định đối tượng chỉnh sửa
# DELETE: Xóa, destroy dữ liệu +Thông tin cần xóa, đối tượng cần xóa: DELETE
# OPTIONS: Xác định trên URL hỗ trợ METHOD nào. 