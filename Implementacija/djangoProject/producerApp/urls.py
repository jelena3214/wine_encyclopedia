from django.contrib import admin
from django.urls import path, include

from producerApp import views

urlpatterns = [
    path('wine',views.viewWine,name='viewWine'),
    path('tour',views.inputTour,name='inputTour'),
    path('addTourType',views.addTourType,name='addTourType'),
    path('inputTourPicture',views.inputTourPicture,name='inputTourPicture'),
    path('celebration',views.inputCelebration,name="inpurtCelebration"),
    path('myStore',views.myStore,name="myStore"),
    path('setTourDetails',views.setTourDetails),
    path('addSommelier',views.addSommelier),
    path('removeTourType/<str:value>/',views.removeTourType,name='removeTourType'),
    path('removeSommelier/<str:value>/',views.removeSommelier,name='removeSommelier'),
    path('ad',views.viewAds,name='viewAds'),
    path('unsubscribeAd/<str:ad_id>',views.unsubscribeAd,name='unsubscribeAd'),
    path('subscribeAd/<str:ad_id>',views.subscribeAd,name='subscribeAd'),
    path('removeWine/<str:wine_id>',views.removeWine,name='removeWine'),
    path('removeTourPicture/<str:picture_id>',views.removeTourPicture,name='removeTourPicture'),
    path('removeReservation/<str:reservation_id>',views.removeReservation,name='removeReservation')
]

