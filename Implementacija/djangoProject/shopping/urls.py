from django.urls import path, include

from shopping import views

urlpatterns = [
    path('shoppingCart', views.shoppingCart, name='shoppingCart'),
    path('shoppingDone', views.shoppingDone, name='shoppingDone'),
    path('reservationCelebrationDone', views.reservationCelebrationDone, name='reservationCelebrationDone'),
    path('reservationVisitDone', views.reservationVisitDone, name='reservationVisitDone'),
    path('mejlProba', views.mejlProba, name='mejlProba')
]