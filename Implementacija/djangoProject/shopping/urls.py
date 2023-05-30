from django.urls import path, include

from shopping import views

urlpatterns = [
    path('shoppingCart', views.shoppingCart, name='shoppingCart'),
    path('addToCart', views.addToCart, name='addToCart'),
    path('shoppingCart/deleteItem', views.deleteItemCart, name='deleteItemCart'),
    path('shoppingCart/changeQuantity', views.changeQuantity, name='changeQuantity'),
    path('shoppingCart/emptyCart', views.emptyCart, name='emptyCart'),
    path('shoppingDone', views.shoppingDone, name='shoppingDone'),
    path('reservationCelebrationDone', views.reservationCelebrationDone, name='reservationCelebrationDone'),
    path('reservationVisitDone', views.reservationVisitDone, name='reservationVisitDone'),
    path('mejlProba', views.mejlProba, name='mejlProba')
]