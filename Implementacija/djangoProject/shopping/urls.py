from django.urls import path
from shopping import views

"""
    Author: Bojana Malesevic 2020/0235
    Defined urls for this part of the application.
"""

urlpatterns = [
    path('shoppingCart', views.shoppingCart, name='shoppingCart'),
    path('addToCart', views.addToCart, name='addToCart'),
    path('shoppingCart/deleteItem', views.deleteItemCart, name='deleteItemCart'),
    path('shoppingCart/changeQuantity', views.changeQuantity, name='changeQuantity'),
    path('shoppingCart/emptyCart', views.emptyCart, name='emptyCart'),
    path('shoppingDone', views.shoppingDone, name='shoppingDone'),
    path('reservationCelebrationDone', views.reservationCelebrationDone, name='reservationCelebrationDone'),
    path('reservationVisitDone', views.reservationVisitDone, name='reservationVisitDone'),
    path('questionnaire', views.questionnaire, name='questionnaire'),
    path('questionnaireQ', views.questionnaireQ, name='questionnaireQ'),
    path('questionnaireRes', views.questionnaireRes, name='questionnaireRes'),
    path('questionnaireHist', views.questionnaireHist, name='questionnaireHist')
]
