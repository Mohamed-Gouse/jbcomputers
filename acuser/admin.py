from django.contrib import admin
from .models import UserAddress,  Wallet, Wishlist

# Register your models here.
admin.site.register(UserAddress)
admin.site.register(Wallet)
admin.site.register(Wishlist)
