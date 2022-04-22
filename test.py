# import email
# import imp
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
django.setup()


# from django.contrib.auth import login
# from TMDT.models import User
# from TMDT.Backend import MyBackend
from TMDT.models import Category,Product, ProductDetail,ProductImage
from myapi import serializers
from django.db.models import F

# from rest_framework.reverse import 
# user =  authenticate(
#     username = 'sangh',
#     password = '123')


# print(user)

# print(User.objects.get(email = 'sanghh111@gmail.com').email == 'sanghh111@gmail.com')

# test  =  MyBackend.MyBackEnd()
# H
# test.authenticate(HTTPResponse(),email='sanghh111@gmail.com',password='123')
# login( HTTPResponse ,user = test)

# product = Product.objects.get(id=1)

# # print(product[0].

# # product_image = ProductImage.objects.filter(product_id = 1)
# # print('product_image: ', product_image.exists())

# filter = Product.objects.filter(id = product.id ) 
# # print('filter: ', filter)
# # print('filter: ', filter[0].__dict__)

# serializer_category.data.append({123})
# print('serializer: ', (serializer_category.data))

# products  = Product.objects.filter(user = 2).values('id')
# print(Product.__dict__)
# print('products: ', list(products))
# product_details = products.productdetail_set.prefetch_related('category_id')
# print('product_details: ', product_details)
# product_details = ProductDetail.objects.select_related('product_id__user').filter(product_id_id__in = products)
# product_details = product_details.filter(product_id_id = products)/
# print('product_details: ', product_details[0].__dict__)

#Cách 1 dùng 3 dòng code 
#LẤY DỮ LIỆU MÌNH MONG MUỐN
# product_detail =  ProductDetail.objects.get(id=5)

#PRODUCT_ID LÀ NƠI TRUNG CHUYỂN GIỮA 2 TABLE
# product_id = product_detail.product_id

#TỪ PRODUCT_ID TA LIÊN KẾT ĐƯỢC BẢN PRODUCT NÊN GỌI ĐC USERx
# user = product_id.user

# print('user: ', user)


#Cách 2
# product_detail = ProductDetail.objects.prefetch_related("product_id__user").all()
# print('product_detail: ', product_detail[0].product_id.__dict__)



# project_detail = ProductDetail.objects.annotate(user = F('product_id__user')).values_list()
# print('project_detail: ', (project_detail))


#Querry expression
#Bài toán đặt ra 
# data = request.data
# data.update(user = request.user.id)
# try :
#     product = Product.objects.get(id=data['product_id'])
# except Product.DoesNotExist:
#     return Response(
#         data =  {'error' : 'product does not exist'},
#         stauts = 404
#     )
# if product.stock < data['quality']:
#     return Response(
#         data =  {'error' : 'product does not exist'},
#         stauts = 404
#     )

# data.update(unit_price = product.price)
# data.update(total_price = product.price* data['quality'] )