from _decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from order.models import  Applied_coupon
from administration.models import Coupon
from cart.models import CartItem
from core.form import CouponForm
from product.models import Product

@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    if CartItem.objects.filter(user=request.user, product_id=id).exists():
        default_url = '/'
        referer = request.META.get('HTTP_REFERER', default_url)
        try:
            return redirect(referer)
        except ValueError:
            return redirect(default_url)
    else:
        item = CartItem.objects.create(product=product, quantity=1)
        if request.user:
            item.user = request.user
            item.save()
        default_url = '/'
        referer = request.META.get('HTTP_REFERER', default_url)
        try:
            return redirect(referer)
        except ValueError:
            return redirect(default_url)


@login_required
def cart_page(request):

    cart = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart)
    original_price = sum(item.total_price() for item in cart)
    coupon_form = CouponForm(request.POST)
    coupon = ''
    request.session['discount'] = 0
    if coupon_form.is_valid():
        code = coupon_form.cleaned_data['code']
        if Applied_coupon.objects.filter(user=request.user, coupon=code).exists():
            messages.error(request, f"The Coupon {code} is Already used before")
        else:
            try:
                coupon = Coupon.objects.get(code=code, valid_from__lte=timezone.now(), valid_to__gte=timezone.now(), active=True)
                discount_price = int((total_price / 100) * coupon.discount)
                total_price -= discount_price
                request.session['coupon'] = code
                request.session['discount'] = discount_price
                messages.success(request, f'Coupon {code} applied successfully!')
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid coupon code.')
    request.session['total_price'] = int(total_price)
    return render(request, 'cart/cart.html', {'cart': cart, 'total_price': total_price, 'coupon_form': coupon_form, 'coupon': coupon, 'original_price': original_price})


def update_cart(request, id, action):
    cart = get_object_or_404(CartItem, product=id)
    if action == 'increment':
        cart.quantity += 1
    elif action == 'decrement':
        cart.quantity -= 1

    cart.save()
    if cart.quantity == 0:
        cart.delete()

    default_url = '/'
    referer = request.META.get('HTTP_REFERER', default_url)

    try:
        return redirect(referer)
    except ValueError:
        return redirect(default_url)


