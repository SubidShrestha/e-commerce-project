from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from .models import *
from users.forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import json

def getProducts(request):
    product = Product.objects.all()
    context = {
        "products" : product
    }
    return render(request,"pages/home.html",context)


@login_required(login_url='login-page')
def viewCart(request):
    if request.user.is_authenticated:
        customer = User.objects.get(id= request.user.id)
        cart, created = Cart.objects.get_or_create(user = customer,status = False)
        items = cart.cartitem_set.all()
    else:
        items=[]
        cart ={'cart_total':0, 'cart_items':0}
    context={
        "items":items,
        "cart":cart
    }
    return render(request,"pages/cart.html",context)

def createCartItem(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        customer = User.objects.get(id= request.user.id)
        product = Product.objects.get(id = productId)
        cart, created = Cart.objects.get_or_create(user = customer,status = False)

        cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if action == 'add':
            cartItem.quantity = (cartItem.quantity + 1)
        elif action == 'remove':
            cartItem.quantity = (cartItem.quantity - 1)

        cartItem.save()

        if cartItem.quantity <= 0:
            cartItem.delete()
    else:
        return JsonResponse({'status':500})

    return JsonResponse({'status': 200})

@login_required(login_url='login-page')
def checkout(request):
    user = User.objects.get(id = request.user.id)
    cart = Cart.objects.filter(user = user)
    if request.method == 'POST':
        city_data=request.POST['city']
        location_data=request.POST['location']
        state_data=request.POST['state']

        if city_data and location_data and state_data:
            ShippingLocation.objects.create(user = user,cart=cart[0],city = city_data, location= location_data, state = state_data,delivery_status=False)
            return redirect('payment')

    return render(request,"pages/checkout.html",{})

@login_required(login_url='login-page')
def payment(request):
    return render(request,"pages/payment.html",{})

def LoginPage(request):
    next = request.GET.get('next')
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                if next:
                    return redirect(next)
                else:
                    return redirect('home')
            else:
                return JsonResponse('Not Logged In')

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
