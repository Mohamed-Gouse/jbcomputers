from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from acuser.form import SignupForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponse
from acuser.otp import send_otp
from django.contrib.auth.models import User
from acuser.models import UserAddress, Wallet, Wishlist
from datetime import datetime
import pyotp
from order.models import Order
from product.models import Product


# Create your views here.
def sign_up(request):
    if not request.user.is_authenticated:
        form = SignupForm()
        return render(request, 'account/register.html', {'form': form})
    else:
        return redirect('/')


class loginView(LoginView):
    template_name = 'account/sign_in.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)


def sign_up_action(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            request.session['mail'] = form.cleaned_data['email']
            request.session['user_data'] = form.cleaned_data
            send_otp(request)
            response_data = {
                "success": True,
                "otp_url": '/otp',
            }
            return JsonResponse(response_data)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors})
    else:
        return JsonResponse({"errors": "Invalid request"})


def otp(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        otp_valid_str = request.session.get('otp_valid', '')
        if otp_valid_str:
            otp_valid = datetime.strptime(otp_valid_str, '%Y-%m-%d %H:%M:%S')
            time_left = (otp_valid - datetime.now()).total_seconds()
            context = {
                'time_left': int(max(0, time_left)),
            }
            return render(request, 'account/otp.html', context)
        else:
            return HttpResponse("OTP validation data is missing. Please try again or contact support.")


def otp_perform(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_data = request.session.get('user_data')
        if user_data is not None:
            username = user_data['username']
            email = user_data['email']
            password = user_data['password1']
            otp_key = request.session.get('otp_key')
            otp_valid = request.session.get('otp_valid')
            if otp_key and otp_valid is not None:
                valid_otp = datetime.fromisoformat(otp_valid)
                if valid_otp > datetime.now():
                    totp = pyotp.TOTP(otp_key, interval=60)
                    if totp.verify(otp):
                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        clear_session(request)
                        return redirect('/')
                    else:
                        messages.error(request, 'Invalid OTP')
                        return redirect('otp')
                else:
                    clear_session(request)
                    messages.error(request, 'OTP expired')
                    return redirect('index')
            else:
                clear_session(request)
                messages.error(request, "Didn't get any OTP")
                return redirect('index')
        else:
            clear_session(request)
            messages.error(request, 'No registration data found in the session')
            return redirect('index')
    else:
        return redirect('otp')


def clear_session(request):
    keys_to_clear = ['otp_key', 'otp_valid', 'registration_data', 'mail']
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]


def resend_otp(request):
    send_otp(request)
    return redirect('otp')


@login_required
@never_cache
def profile(request):
    address = UserAddress.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'account/profile.html', {'address': address, 'orders': orders})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            messages.error(request, 'Username already exists')
            return redirect('edit_profile')
        if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            messages.error(request, 'Email already exists')
            return redirect('edit_profile')
        user = request.user
        user.username = username
        user.email = email
        user.save()
        return redirect('profile')
    return render(request, 'account/edit_profile.html')


@login_required
@never_cache
def change_password(request):
    user = request.user
    user_obj = User.objects.get(id=user.id)
    if request.method == "POST":
        prev = request.POST.get('prev_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if user_obj.check_password(prev):
            if password1 == prev:
                messages.error(request, 'Previous & new password should not be same')
            else:
                if password2 == password1:
                    user_obj.set_password(password1)
                    user_obj.save()
                    update_session_auth_hash(request, user_obj)
                    messages.success(request, "Password changed successfully!")
                    return redirect('profile')
                else:
                    messages.error(request, "New password and Repeat password must be same.!")
        else:
            messages.error(request, "Enter Old password correctly")
    return render(request, 'account/change_password.html')


def address_add(request):
    user = request.user
    fname = request.POST.get('first_name')
    lname = request.POST.get('last_name')
    email = user.email
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    place = request.POST.get('place')
    zipcode = request.POST.get('zipcode')
    UserAddress.objects.create(user=user, first_name=fname, last_name=lname, Email=email, phone=phone, address=address, place=place, zipcode=zipcode)


def add_address(request):
    if request.method == 'POST':
        address_add(request)
        return redirect('profile')
    return render(request, 'account/add_address.html')


def delete_address(request, id):
    address = UserAddress.objects.get(id=id)
    address.delete()
    return redirect('profile')


def edit_address(request, id):
    address = UserAddress.objects.get(id=id)
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        phone = request.POST.get('phone')
        adrs = request.POST.get('address')
        place = request.POST.get('place')
        zipcode = request.POST.get('zipcode')
        address.first_name = fname
        address.last_name = lname
        address.phone = phone
        address.address = adrs
        address.place = place
        address.zipcode = zipcode
        address.save()
        return redirect('profile')
    return render(request, 'account/edit_address.html', {'address': address})


def add_address_checkout(request):
    if request.method == 'POST':
        address_add(request)
        return redirect('checkout')
    return render(request, 'account/add_address.html')


def order_summary(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'account/order_summary.html', {'orders': order})


def cancelOrder(request, id):
    order = Order.objects.get(id=id)
    wallet = Wallet(user=request.user, amount=order.paid_amount)
    if order:
        order.status = order.CANCEL
        order.save()
        wallet.save()
        print('Wallet: ', wallet.amount)
    else:
        print('order not found')
    return redirect('order_summary', order_id=id)

# ----------------------------------------------Wishlist----------------------------------------------------------

def wishlist(request):
    wishlists = Wishlist.objects.all()
    return render(request, 'account/wishlist.html', {'wishlists': wishlists})


def add_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist_item.delete()
        message = f"{product} removed from wishlist."
    else:
        message = f"{product} added to wishlist."

    return JsonResponse({'message': message})
