from django.contrib import admin
from product.models import Category, Subcategory, Product, Brand

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Brand)