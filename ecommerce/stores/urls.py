from atexit import register
from django.urls import path
from .views import *

urlpatterns = [
    path('',getProducts,name='home'),
    path('login',LoginPage,name='login-page'),
    path('register',register,name='register-page'),
    path('logout',LogoutPage,name='logout')
]
