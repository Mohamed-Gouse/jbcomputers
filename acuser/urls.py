from django.urls import path
from django.contrib.auth import views
from acuser.views import *

urlpatterns = [
    path('sign_up', sign_up, name='sign_up'),
    path('sign_up_action', sign_up_action, name='sign_up_action'),
    path('otp', otp, name='otp'),
    path('otp_perform', otp_perform, name='otp_perform'),
    path('resend_otp', resend_otp, name='resend_otp'),
    path('login/', loginView.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('change_password', change_password, name='change_password'),
    path('add_address', add_address, name='add_address'),
    path('add_address_checkout', add_address_checkout, name='add_address_checkout'),
    path('delete_address/<int:id>', delete_address, name='delete_address'),
    path('edit_address/<int:id>', edit_address, name='edit_address'),
    path('order_summary/<int:order_id>', order_summary, name='order_summary'),
    path('cancelOrder/<int:id>', cancelOrder, name='cancelOrder'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('wishlist', wish_list, name='wishlist'),
    path('add_wishlist/<int:id>', add_wishlist, name='add_wishlist'),
    path('remove_from_wishlist/<int:id>', remove_from_wishlist, name='remove_from_wishlist'),
]