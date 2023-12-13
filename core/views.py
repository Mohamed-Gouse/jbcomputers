from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from product.models import *

# Create your views here.
def frontpage(request):
    product = Product.objects.exclude(active=False)[:10]
    category = Subcategory.objects.exclude(active=False)[:6]
    context = {
        'product': product,
        'category': category,
    }
    return render(request, 'core/frontpage.html', context)


def sign_up(request):
    return render(request, 'account/register.html')

