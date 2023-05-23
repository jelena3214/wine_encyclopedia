from django.urls import path, include

from views import views

urlpatterns = [
    path('allwines', views.viewWines, name='viewWines'),
    path('wine', views.wine, name='wine'),
    path('detour', views.detour, name='detour'),
    path('celebration', views.celebration, name='celebration')
]