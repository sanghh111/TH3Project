import email
from django.shortcuts import render,redirect,get_object_or_404  
from .models import User
from .forms import RegisterForm
from .Backend import MyBackend
from django.contrib.auth import authenticate, login

#autheticate dùng để kiểm tra thông tin username và passowrd
# đúng trả về user. Sai thì none 

#login giữ trạng thái login của user khi autheticate thành công

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Khong Co loi")
            form.save()
            return redirect(to= 'login')
        # else:
        #     print('form.erro')
    else:
        form = RegisterForm()

    return render(
        request= request,
        template_name= 'user/register.html',
        context= {
            'form' : form
        }
    )   

def login_view(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = MyBackend.MyBackEnd().authenticate(request,email=email,password=password)
        # user = User.objects.get(email='sanghh 111@gmail.com')
        print('user: ', user)
        if user:
            print("xác thực thành công")
            login(request= request,user=user)

    return render(
        request= request,
        template_name= 'user/login.html',
    )       