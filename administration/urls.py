from django.urls import path
from .views import *

urlpatterns = [
    path('admin_login', admin_login, name='admin_login'),
    path('admin_login_perform', admin_login_perform, name='admin_login_perform'),
    path('dashboard', dashboard, name='dashboard'),
    path('bannersAdd', bannersAdd, name='bannersAdd'),

#----------------------------------------customer---------------------------------------

    path('customer_view', customer_view, name='customer_view'),
    path('customer_block/<int:uid>', customer_block, name='customer_block'),

#---------------------------------------Category----------------------------------------

    path('categoryView', categoryView, name='categoryView'),
    path('categoryAdd_perform', categoryAdd_perform, name='categoryAdd_perform'),
    path('subcategoryAdd_perform', subcategoryAdd_perform, name='subcategoryAdd_perform'),
    path('categoryEdit/<int:uid>', categoryEdit, name='categoryEdit'),
    path('subcategoryEdit/<int:uid>', subcategoryEdit, name='subcategoryEdit'),
    path('categoryEdit_perform', categoryEdit_perform, name='categoryEdit_perform'),
    path('subcategoryEdit_perform', subcategoryEdit_perform, name='subcategoryEdit_perform'),
    path('categoryDelete/<int:uid>', categoryDelete, name='categoryDelete'),
    path('subcategoryDelete/<int:uid>', subcategoryDelete, name='subcategoryDelete'),
    path('subcategoryBlock/<int:uid>', subcategoryBlock, name='subcategoryBlock'),

#----------------------------------------Brand------------------------------------------

    path('brandView', brandView, name='brandView'),
    path('brandAdd_perform', brandAdd_perform, name='brandAdd_perform'),
    path('brandEdit/<int:uid>', brandEdit, name='brandEdit'),
    path('brandEdit_perform', brandEdit_perform, name='brandEdit_perform'),
    path('brandBlock/<int:uid>', brandBlock, name='brandBlock'),
    path('brandDelete/<int:uid>', brandDelete, name='brandDelete'),

#--------------------------------------Product-----------------------------------------

    path('productView', productView, name='productView'),
    path('productAdd_perform', productAdd_perform, name='productAdd_perform'),
    path('productDetails/<slug:slug>', productDetails, name='productDetails'),
    path('productEdit/<int:uid>', productEdit, name='productEdit'),
    path('productEdit_perform', productEdit_perform, name='productEdit_perform'),
    path('productDelete/<int:uid>', productDelete, name='productDelete'),
    path('productBlock/<int:uid>', productBlock, name='productBlock'),

#---------------------------------------Order------------------------------------------

    path('orders', orders, name='orders'),
    path('orderDetail/<int:id>', orderDetail, name='orderDetail'),
    path('return_order/<int:id>', return_order, name='return_order'),
    path('update_return_status', update_return_status, name='update_return_status'),
    path('update_order_status', update_order_status, name='update_order_status'),

# --------------------------------------Offers-----------------------------------------

    path('offers', offers, name='offers'),
    path('offer-create', create_offer, name='offer-create'),
    path('offer-delete/<int:id>', delete_offer, name='offer-delete'),

# -------------------------------------Coupons----------------------------------------

    path('coupons', coupons, name='coupons'),
    path('coupons-add', add_coupon, name='coupons-add'),
    path('coupon-edit/<int:id>', edit_coupon, name='coupon-edit'),
    path('coupon-block/<int:id>', block_coupon, name='coupon-block'),
    path('coupon-delete/<int:id>', delete_coupon, name='coupon-delete'),

# -------------------------------------sales-------------------------------------------

    path('sales-report/', sales_report, name='sales_report'),
    path('sales-chart/', sales_chart, name='sales-chart'),
]