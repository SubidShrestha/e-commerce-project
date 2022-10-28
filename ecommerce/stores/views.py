from django.shortcuts import render,redirect,HttpResponse
from .models import *
from users.forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout

def getProducts(request):
    product = Product.objects.all()
    context = {
        "products" : product
    }
    return render(request,"pages/home.html",context)

def LoginPage(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse('Not Logged In')

    return render(request,"pages/login.html",{})
    
def register(request):
    forms = CustomUserCreationForm()

    if request.method == 'POST':
        forms = CustomUserCreationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('login-page')

    context = {
        "form" :forms
    }
    return render(request,"pages/register.html",context)

def LogoutPage(request):
    logout(request)
    return redirect('login-page')
