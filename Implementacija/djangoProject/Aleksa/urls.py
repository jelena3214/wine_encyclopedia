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
    path('removeTourType/<str:value>/',views.removeTourType,name='removeTourType'),
    path('removeSommelier/<str:value>/',views.removeSommelier,name='removeSommelier'),
    path('ad',views.viewAds),
    path('unsubscribeAd/<str:ad_id>',views.unsubscribeAd),
    path('subscribeAd/<str:ad_id>',views.subscribeAd)
]

