from datetime import date

from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from administration.models import Offer
from cart.models import CartItem
from product.models import *

# Create your views here.
def search_bar(request):
    query = request.GET.get('query', '')
    product = Product.objects.exclude(active=False)
    if query:
        product = product.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'product/search.html', {'product': product})


def product(request):
    category = Subcategory.objects.all()
    brand = Brand.objects.all()
    product = Product.objects.exclude(active=False)

    active_category = request.GET.get('category', '')
    active_brand = request.GET.get('brand', '')

    product_filter = Q()


    if active_category:
        product_filter &= Q(subcategory__slug=active_category)

    if active_brand:
        product_filter &= Q(brand__slug=active_brand)

    # Apply the filter to the products
    product = product.filter(product_filter)

    context = {
        'category': category,
        'product': product,
        'brand': brand,
        'active_category': active_category,
        'active_brand': active_brand,

    }
    return render(request, 'core/productlist.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    today = date.today()
    active_offers = Offer.objects.filter(product=product, start_date__lte=today, end_date__gte=today)

    context = {'product': product, 'active_offers': active_offers}
    return render(request, 'product/productdetail.html', context)



def category(request, slug):
    product = Product.objects.filter(subcategory__slug=slug)
    return render(request, 'core/productlist.html', {'product': product})

