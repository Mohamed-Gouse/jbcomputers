from django.urls import path
from cart.views import *

urlpatterns = [
    path('cart_page/', cart_page, name='cart_page'),
    path('add_to_cart/<int:id>', add_to_cart, name='add_to_cart'),
    path('update_cart/<int:id>/<str:action>/', update_cart, name='update_cart'),
]