from django.contrib import admin
from django.urls import path, include

from userApp import views

urlpatterns = [
    path('', views.loginUser, name='loginUser'),
    path('registerUser', views.registerUser, name='registerUser'),

]