# from tkinter import Place
from webbrowser import BaseBrowser
from django.core.exceptions import ValidationError
from django.forms import  ModelForm, NumberInput, Select,TextInput
from .models import Product

#MODEL Form: Tạo HTML FORMS DỰA TRÊN MODEL CÓ SẴN
class ProductForm(ModelForm):
    


    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name'   : TextInput(attrs={'class' : "form-control"}),
            'stock' : NumberInput(attrs={'class' : "form-control"}),
            'price' : NumberInput(attrs={'class' : "form-control"}),
            'category_id' : Select(attrs={'class' : "form-control"}),
        }

    # Validation phía server
    # Step 1: chọn field/trường muốn validate
    # Step2: Tạo hàm có tên theo format : clean_<field>
    
    # Validate 'name' không được trùng nhau
    def clean_name(self):
        name = self.cleaned_data['name']
        #Kiểm tra 'name ' có tồn tại hay chưa
        #Bằng cách: thử lấy get qua name
        #Nếu mà trả kết quả thì 'name' tồn tại --> raise error và ngược lại được xài

        try:
            Product.objects.get(name = name) # Thử lấy cái name
            #raise cái error
            raise ValidationError(f"Name ({name}) đã tồn tại. Vui lòng chọn tên khác")
        except Product.DoesNotExist: # Bắt lỗi Product không tồn tại
            return name # được xài 


