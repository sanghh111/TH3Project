from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.


def index(request):
    web = HttpResponse()
    web.write('<p>Hello WORLD</p>')
    return web



def login(request):
    return render(request,'login.html')