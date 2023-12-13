from django.urls import path
from order.views import *

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('payment-success', payment_success, name='payment-success'),
    path('payment-failed', payment_failed, name='payment-failed'),
    path('invoice/<int:order_id>/', view_invoice, name='view_invoice'),
    path('initiate-return/<int:order_id>/', initiate_return, name='initiate-return'),
    path('wallet', wallet, name='wallet'),
]
