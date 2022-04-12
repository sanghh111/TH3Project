from django.views.generic import ListView, DetailView , CreateView , UpdateView 
from . models import Product , ProductDetail
from . forms import ProductForm
from django.urls import reverse_lazy
#R: CURD
class ProductListView(ListView):
    model = Product
    
    #format template <tenapp>/<ten model>_list.html
    #overide name template
    template_name = 'product/list.html'

    #phan trang
    paginate_by = 3

    #name varriable in the Html 
    #default "object_list" 
    context_object_name = 'products'

class ProductDetail(DetailView):
    #Tham them vao url là pk
    model = ProductDetail

    #template mặc định product/detail.html
    template_name = 'class_product/detail.html'

    context_object_name = 'product'


class PrductCreate(CreateView):

    model = Product

    #phải định nghĩa 'fields' với trường nào cần phỉa input vào 

    # fields = '__all__'

    # Sử dụng form trong CreateView sử dụng 'form_class'
    form_class = ProductForm

    # Khi dùng CreateView thì template mặc định là product/add.html
    template_name = "product/add.html"
    
    context_object_name = 'product'

    # Định nghĩa URL mà redirect tới khi add thành công

    success_url = reverse_lazy('list_class_product')



class ProductUpdate(UpdateView):

    model = Product

    # form ProductForm 
    # form_class =ProductForm

    fields = ('stock', 'price', 'category_id')

    #template root product/update.html
    template_name = "product/update.html"

    success_url = reverse_lazy('list_class_product')

    
