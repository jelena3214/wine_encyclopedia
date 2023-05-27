from django.contrib import admin
from django.urls import path, include

from Aleksa import views

urlpatterns = [
    path('wine',views.viewWine,name='viewWine'),
    path('tour',views.inputTour,name='inputTour'),
    path('addTourType',views.addTourType,name='addTourType'),
    path('inputTourPicture',views.inputTourPicture,name='inputTourPicture'),
    path('celebration',views.inputCelebration,name="inpurtCelebration"),
    path('myStore',views.myStore,name="myStore"),
    path('setTourDetails',views.setTourDetails),
    path('addSommelier',views.addSommelier),
    path('removeTourType<str:value>',views.removeTourType)
]