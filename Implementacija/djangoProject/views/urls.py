from django.urls import path, include

from views import views

urlpatterns = [
    path('allwines', views.viewWines, name='viewWines'),
    path('wine/<str:value>', views.wine, name='wine'),
    path('detour', views.detour, name='detour'),
    path('detours/<str:value>', views.oneDetour, name='oneDetour'),
    path('celebration', views.celebration, name='celebration'),
    path('celebration/<str:value>', views.oneCelebration, name='oneCelebration')
]