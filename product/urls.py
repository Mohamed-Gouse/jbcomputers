from django.urls import path
from product.views import *

urlpatterns = [
    path('search_bar/', search_bar, name='search_bar'),
    path('product/', product, name='product'),
    path('product/<slug:slug>', product_detail, name='product_detail'),
    path('category/<slug:slug>', category, name='category'),
]