import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from acuser.models import Wallet, UserAddress
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from order.models import Order, OrderItem, ReturnedProduct, Applied_coupon
from cart.models import CartItem
from administration.models import Notification
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail


# Create your views here.
def checkout(request):
    message = ''
    host = request.get_host()
    cart = CartItem.objects.filter(user=request.user)
    cart_total_price = sum(item.total_price() for item in cart)
    address = UserAddress.objects.filter(user=request.user)
    total_price = request.session.get('total_price')
    discount = request.session.get('discount')
    if request.method == 'POST':
        address = request.POST.get('address')
        if not address:
            return redirect('checkout')
        payment_method = request.POST.get('payment_method')
        request.session['email'] = request.user.email
        request.session['address'] = address
        if payment_method == 'COD':
            user = request.user
            coupon = request.session.get('coupon')
            order = Order.objects.create(user=user, address_id=address, paid_amount=total_price, paid=False, discount=discount)
            Applied_coupon.objects.create(user=user, coupon=coupon, order=order)
            request.session['order'] = order.id

            for item in cart:
                product = item.product
                price = item.total_price()
                quantity = item.quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
                pro = item.product
                pro.stock -= quantity
                pro.save()
                message = f"{user.username} place a new order on {item.product.name}"

            cart.delete()
            send_mail(request)
            Notification.objects.create(message=message)
            del request.session['email']
            del request.session['order']
            del request.session['discount']
            return redirect('profile')

        elif payment_method == 'WALLET':
            user = request.user
            wallets = Wallet.objects.filter(user=user)
            wallet_balance = sum(wallet.total_balance() for wallet in wallets)

            if wallet_balance > total_price:
                coupon = request.session.get('coupon')
                order = Order.objects.create(user=user, address_id=address, paid_amount=total_price, paid=True, pay_method=Order.WALLET, discount=discount)
                Applied_coupon.objects.create(user=user, coupon=coupon, order=order)
                Wallet.objects.create(user=user, amount=order.paid_amount, balance_type=Wallet.DEBIT)
                request.session['order'] = order.id

                for item in cart:
                    product = item.product
                    price = item.total_price()
                    quantity = item.quantity

                    item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
                    pro = item.product
                    pro.stock -= quantity
                    pro.save()
                    message = f"{user.username} place a new order on {item.product.name}"

                cart.delete()
                send_mail(request)
                Notification.objects.create(message=message)
                del request.session['email']
                del request.session['order']
                del request.session['discount']
                return redirect('profile')
            else:
                messages.error(request, "Insufficient balance")
                return redirect('checkout')
        else:
            address = UserAddress.objects.filter(user=request.user)
            items = []
            for item in cart:
                product = item.product
                price = item.total_price()
                quantity = item.quantity

                item_dict = {
                    'product': product,
                    'quantity': quantity,
                    'price': price,
                }
                items.append(item_dict)

            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": total_price,
                "currency_code": "USD",
                "item_name": items,
                "invoice": uuid.uuid4(),
                "notify_url": f"http://{host}{(reverse('paypal-ipn'))}",
                "return": f"http://{host}{(reverse('payment-success'))}",
                "cancel_return": f"http://{host}{(reverse('payment-failed'))}",
            }

            # Create the instance.
            form = PayPalPaymentsForm(initial=paypal_dict)
            context = {
                'address': address,
                'total_price': total_price,
                'cart_total_price': cart_total_price,
                'discount': discount,
                'form': form,
            }
            return render(request, 'cart/checkout.html', context)

    context = {
        'address': address,
        'total_price': total_price,
        'cart_total_price': cart_total_price,
        'discount': discount,
    }
    return render(request, 'cart/checkout.html', context)


def payment_success(request):
    user = request.user
    message = ''
    cart = CartItem.objects.filter(user=user)
    address = request.session.get('address')
    total_price = request.session.get('total_price')
    coupon = request.session.get('coupon')
    discount = request.session.get('discount')
    order = Order.objects.create(user=user, address_id=address, paid_amount=total_price, paid=True, pay_method=Order.PAYPAL, discount=discount)
    Applied_coupon.objects.create(user=user, coupon=coupon, order=order)
    request.session['order'] = order.id
    for item in cart:
        product = item.product
        price = item.total_price()
        quantity = item.quantity

        item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
        pro = item.product
        pro.stock -= quantity
        pro.save()
        message = f"{user.username} place a new order on {item.product.name}"

    cart.delete()
    send_mail(request)
    Notification.objects.create(message=message)
    del request.session['email']
    del request.session['order']
    del request.session['total_price']
    del request.session['discount']
    del request.session['address']
    return redirect('profile')


def payment_failed(request):
    return HttpResponse('Success')


def view_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_item = OrderItem.objects.filter(order=order)
    total_price = sum(item.price for item in order_item)
    context = {
        'order': order,
        'total_price': total_price,
    }
    return render(request, 'order/invoice.html', context)


def initiate_return(request, order_id):
    order = Order.objects.get(pk=order_id)
    existing_return = ReturnedProduct.objects.filter(order=order)
    if existing_return:
        existing_return = existing_return.get(order=order)
    else:
        if request.method == 'POST':
            reason = request.POST.get('reason')
            returned_product = ReturnedProduct.objects.create(order=order, reason=reason)
            messages.success(request, 'Return initiated successfully.')
            return redirect('profile')
    return render(request, 'order/return_product.html', {'orders': order, 'existing_return': existing_return})


@login_required
def wallet(request):
    wallet = Wallet.objects.filter(user=request.user)
    balance = sum(wallets.total_balance() for wallets in wallet)
    return render(request, 'account/wallet.html', {'wallet': wallet, 'balance': balance})


def send_mail(request):
    mail = request.session.get('email')
    order_id = request.session.get('order')
    order = Order.objects.get(id=order_id)
    subject = 'Your order is placed'
    message = f'Your Order on Order ID:{order.id} Ordered Successfully'
    from_email = 'm.gouse7736@example.com'
    recipient_email = [mail]

    try:
        email = EmailMessage(subject, message, from_email, recipient_email)
        email.send()
    except Exception as e:
        print(f"Failed to send OTP email: {str(e)}")
