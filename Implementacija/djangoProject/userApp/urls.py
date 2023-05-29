from django.contrib import admin
from django.urls import path, include

from userApp import views

urlpatterns = [
    path('', views.loginUser, name='loginUser'),
    path('registerUser', views.registerUser, name='registerUser'),
    path('registerProducer', views.registerProducer, name='registerProducer'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('changeCompanyStuff', views.changeCompanyStuff, name='changeCompanyStuff'),
    path('resetPassword', views.resetPassword, name='resetPassword'),
    path('changeInfoUser', views.changeInfoUser, name='changeInfoUser'),
    path('userExists/<str:email>/', views.userExists, name='userExists'),

]