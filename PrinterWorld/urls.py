from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('acuser.urls')),
    path('', include('administration.urls')),
    path('', include('cart.urls')),
    path('', include('core.urls')),
    path('', include('order.urls')),
    path('', include('product.urls')),
    path('', include('product.urls')),

    path('accounts/', include('allauth.urls')),
    path('', include('paypal.standard.ipn.urls')),

    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
