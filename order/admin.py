from django.contrib import admin
from order.models import OrderItem, Order, ReturnedProduct, Applied_coupon

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ReturnedProduct)
admin.site.register(Applied_coupon)
