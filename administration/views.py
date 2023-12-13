from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, IntegerField
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.cache import never_cache
from acuser.models import Wallet
from product.models import *
from order.models import OrderItem, Order, ReturnedProduct
from .form import OfferForm, CouponForm
from .models import Banners, Offer, Coupon
from django.core.mail import EmailMessage


# Create your views here.
@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')
        pass
    else:
        return render(request, 'admin_manage/sign_in.html')


def admin_login_perform(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Username or password is not correct')
            return redirect('admin_login')
        else:
            if User.objects.get(username=username).is_superuser:
                request.session['username'] = username
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Authentication denied')
                return redirect('admin_login')
    else:
        messages.error(request, 'Method not allowed')
        return redirect('admin_login')


@login_required
def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        customers = User.objects.exclude(is_superuser=True).count()
        products = Product.objects.count()
        brands = Brand.objects.count()
        categories = Category.objects.count()
        subcategories = Subcategory.objects.count()
        orders = Order.objects.all().order_by("-created_at")
        banners = Banners.objects.all()
        order = orders.filter(status=Order.DELIVERED, paid=True)
        total_sales = sum(order.paid_amount_total() for order in order)
        context = {
            'customers': customers,
            'products': products,
            'brands': brands,
            'categories': categories,
            'subcategories': subcategories,
            'orders': orders,
            'banners': banners,
            'total_sales': total_sales,
        }
        return render(request, 'admin_manage/adm/dashboard.html', context)
    else:
        return redirect('admin_login')

#-----------------------------------------------Banners----------------------------------------

def bannersAdd(request):
    if request.method == 'POST':
        banner = Banners(
            bm_1 = request.FILES.get('bm1'),
            bm_2 = request.FILES.get('bm2'),
            bm_3 = request.FILES.get('bm3'),
            bs_1 = request.FILES.get('bm4'),
            bs_2 = request.FILES.get('bm5'),
            bs_3 = request.FILES.get('bm6'),
            bs_4 = request.FILES.get('bm7')
        )
        banner.save()
        return redirect('dashboard')
    else:
        return redirect('dashboard')

# ----------------------------------------------customer---------------------------------------

def customer_view(request):
    if request.user.is_authenticated:
        customers = User.objects.all().exclude(is_superuser=True)
        context = {
            'customers': customers
        }
        return render(request, 'admin_manage/adm/customer.html', context)
    else:
        return redirect('admin_login')


def customer_block(request, uid):
    user = User.objects.get(id=uid)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('customer_view')


# -------------------------------------------Category---------------------------------------------

def categoryView(request):
    category = Category.objects.all()
    sub = Subcategory.objects.all()
    context = {
        'category': category,
        'sub': sub,
    }
    return render(request, 'admin_manage/category/categories.html', context)


def categoryAdd_perform(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        if Category.objects.filter(name__icontains=category).exists():
            messages.error(request, 'Category already exists')
            return redirect('categoryAdd')
        else:
            Category.objects.create(name=category)
            return redirect('categoryView')
    else:
        return redirect('categoryView')


def subcategoryAdd_perform(request):
    if request.method == 'POST':
        sub = request.POST.get('subcategory')
        cat = request.POST.get('category')
        img = request.FILES.get('img')
        if Category.objects.filter(name__icontains=sub).exists():
            messages.error(request, 'Sub-Category already exists')
            return redirect('subcategoryAdd')
        else:
            Subcategory.objects.create(name=sub, category_id=cat, image=img)
            return redirect('categoryView')
    else:
        return redirect('categoryView')


def categoryEdit(request, uid):
    category = Category.objects.get(id=uid)
    return render(request, 'admin_manage/category/categoryEdit.html', {'category': category})


def categoryEdit_perform(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        id = request.POST.get('id')
        category_obj = Category.objects.get(id=id)
        category_obj.name = category
        category_obj.save()
        return redirect('categoryView')
    else:
        return redirect('categoryView')


def subcategoryEdit(request, uid):
    sub = Subcategory.objects.get(id=uid)
    cat = Category.objects.all()
    context = {
        'sub': sub,
        'cat': cat,
    }
    return render(request, 'admin_manage/category/subcatEdit.html', context)


def subcategoryEdit_perform(request):
    if request.method == 'POST':
        sub = request.POST.get('subcategory')
        cat = request.POST.get('category')
        img = request.FILES.get('img')
        id = request.POST.get('id')
        if Category.objects.filter(name__icontains=sub).exists():
            messages.error(request, 'Sub-Category already exists')
            return redirect('subcategoryEdit')
        else:
            subcategory = Subcategory.objects.get(id=id)
            subcategory.name = sub
            subcategory.category_id = cat
            if img:
                subcategory.image = img
            subcategory.save()
            return redirect('categoryView')
    else:
        return redirect('categoryView')


def categoryDelete(request, uid):
    category = Category.objects.get(id=uid)
    category.delete()
    return redirect('categoryView')


def subcategoryDelete(request, uid):
    sub = Subcategory.objects.get(id=uid)
    sub.delete()
    return redirect('categoryView')


def subcategoryBlock(request, uid):
    sub = Subcategory.objects.get(id=uid)
    if sub.active:
        sub.active = False
    else:
        sub.active = True
    sub.save()
    return redirect('categoryView')


# ------------------------------------Brand-----------------------------------

def brandView(request):
    brand = Brand.objects.all()
    context = {
        'brand': brand
    }
    return render(request, 'admin_manage/brand/brands.html', context)


def brandAdd_perform(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        logo = request.FILES.get('logo')
        if Brand.objects.filter(name__icontains=brand).exists():
            messages.error(request, 'Brand already exists')
            return redirect('brandAdd')
        else:
            Brand.objects.create(name=brand, image=logo)
            return redirect('brandView')
    else:
        return redirect('brandView')


def brandEdit(request, uid):
    brand = Brand.objects.get(id=uid)
    return render(request, 'admin_manage/brand/brandEdit.html', {'brand': brand})


def brandEdit_perform(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        logo = request.FILES.get('logo')
        id = request.POST.get('id')
        brand_obj = Brand.objects.get(id=id)
        brand_obj.name = brand
        if logo:
            brand_obj.image = logo
        brand_obj.save()
        return redirect('brandView')
    else:
        return redirect('brandView')


def brandBlock(request, uid):
    brand = Brand.objects.get(id=uid)
    if brand.active:
        brand.active = False
    else:
        brand.active = True
    brand.save()
    return redirect('brandView')


def brandDelete(request, uid):
    brand = Brand.objects.get(id=uid)
    brand.delete()
    return redirect('brandView')


# ----------------------------------------Product--------------------------------------------

def productView(request):
    product = Product.objects.all()
    brand = Brand.objects.exclude(active=False)
    subcategory = Subcategory.objects.exclude(active=False)
    context = {
        'product': product,
        'brand': brand,
        'subcategory': subcategory,
    }
    return render(request, 'admin_manage/product/products.html', context)


def productAdd_perform(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        sub = request.POST.get('category')
        stock = request.POST.get('stock')
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')
        product = Product(name=name, description=description, price=price, brand_id=brand, subcategory_id=sub,
                          stock=stock, image_1=img1, image_2=img2, image_3=img3, image_4=img4)
        product.save()
        return redirect('productView')
    else:
        return redirect('productView')


def productDetails(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'admin_manage/product/productDetail.html', {'product': product})


def productEdit(request, uid):
    product = Product.objects.get(id=uid)
    brand = Brand.objects.all()
    subcategory = Subcategory.objects.all()
    context = {
        'product': product,
        'brand': brand,
        'subcategory': subcategory
    }
    return render(request, 'admin_manage/product/productEdit.html', context)


def productEdit_perform(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        stock = request.POST.get('stock')
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')

        product = Product.objects.get(id=id)
        slug = product.slug

        product.name = name
        product.description = description
        product.price = price
        product.brand_id = brand
        product.subcategory_id = category
        product.stock = stock

        if img1 is not None:
            product.image_1 = img1
        if img2 is not None:
            product.image_2 = img2
        if img3 is not None:
            product.image_3 = img3
        if img4 is not None:
            product.image_4 = img4

        product.save()
        return redirect('productDetails', slug=slug)
    else:
        return redirect('productView')


def productDelete(request, uid):
    product = Product.objects.get(id=uid)
    product.delete()
    return redirect('productView')


def productBlock(request, uid):
    product = Product.objects.get(id=uid)
    if product.active:
        product.active = False
    else:
        product.active = True
    product.save()
    return redirect('productView')

#---------------------------------------------------Order---------------------------------------------------------------

def orders(request):
    order = Order.objects.all()
    returned = ReturnedProduct.objects.all()
    return render(request, 'admin_manage/order/orders.html', {'order': order, 'returned': returned})


def orderDetail(request, id):
    orders = Order.objects.get(id=id)
    return render(request, 'admin_manage/order/orderDetail.html', {'orders': orders})


def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('id')
        status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        request.session['order'] = order_id
        request.session['status'] = status
        request.session['email'] = order.address.Email
        if status:
            if status == order.DELIVERED:
                order.paid = True
            if status == order.CANCEL:
                Wallet.objects.create(user=order.user, amount=order.paid_amount)
            order.status = status
            order.save()
            print(order.status)
            user_order_update(request)
    return redirect('orderDetail', id=order_id)


def return_order(request, id):
    returns = ReturnedProduct.objects.get(id=id)
    context = {
        'returns': returns,
    }
    return render(request, 'admin_manage/order/returned_orders.html', context)


def update_return_status(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        status = request.POST.get('status')
        returned_order = ReturnedProduct.objects.get(id=id)
        if returned_order:
            returned_order.return_status = status
            returned_order.received_at = timezone.now()
            returned_order.save()
        ordered_item = returned_order.order
        for item in ordered_item.ordered_products.all():
            pro = item.product
            pro.stock += item.quantity
            pro.save()
        if returned_order.return_status == returned_order.RETURNED:
            Wallet.objects.create(user=returned_order.order.user, amount=returned_order.order.paid_amount)
    return redirect('return_order', id=id)


def user_order_update(request):
    order_id = request.session.get('order')
    status = request.session.get('status')
    mail = request.session.get('email')

    order = Order.objects.get(id=order_id)

    subject = 'Your Order is updated.!'
    # message = f'Your order on {order.product.name} is {status} successfully'
    message = "Order Updated"
    from_email = 'm.gouse7736@example.com'
    recipient_email = [mail]

    try:
        email = EmailMessage(subject, message, from_email, recipient_email)
        email.send()
    except Exception as e:
        print(f"Failed to send OTP email: {str(e)}")

# -------------------------------------------------Offers---------------------------------------------------------------

def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            offer = Offer.objects.filter(product=product)
            if offer:
                discount_type = form.cleaned_data['discount_type']
                discount_value = form.cleaned_data['discount_value']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                offer = Offer.objects.get(product=product)
                offer.discount_type = discount_type
                offer.discount_value = discount_value
                offer.start_date = start_date
                offer.end_date = end_date
                offer.save()
            else:
                form.save()
            return redirect('offers')
    else:
        form = OfferForm()

    return render(request, 'admin_manage/offers/addOffer.html', {'form': form})


def offers(request):
    offers = Offer.objects.all()
    return render(request, 'admin_manage/offers/offers.html', {'offers': offers})


def delete_offer(request, id):
    Offer.objects.get(pk=id).delete()
    return redirect('offers')

# --------------------------------------------Coupon---------------------------------------------------------------

def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('coupons')
    else:
        form = CouponForm()
    return render(request, 'admin_manage/coupon/add_coupon.html', {'form': form})


def coupons(request):
    coupons = Coupon.objects.all()
    return render(request, 'admin_manage/coupon/coupons.html', {'coupons': coupons})


def edit_coupon(request, id):
    coupon = Coupon.objects.get(id=id)
    if request.method == 'POST':
        coupon.code = request.POST.get("code")
        coupon.discount = request.POST.get("discount")
        coupon.valid_from = request.POST.get("valid_from")
        coupon.valid_to = request.POST.get("valid_to")
        coupon.save()
        return redirect('coupons')
    return render(request, 'admin_manage/coupon/edit_coupon.html', {'coupon': coupon})


def delete_coupon(request, id):
    Coupon.objects.get(id=id).delete()
    return redirect('coupons')


def block_coupon(request, id):
    coupon = Coupon.objects.get(id=id)
    if coupon.active:
        coupon.active = False
    else:
        coupon.active = True
    coupon.save()
    return redirect('coupons')


def sales_report(request):
    orders = Order.objects.filter(status=Order.DELIVERED, paid=True)
    total_sales = sum(order.paid_amount_total() for order in orders)
    order_items = OrderItem.objects.filter(order__in=orders)
    total_quantity_sold = sum(item.quantity for item in order_items)

    context = {
        'total_sales': total_sales,
        'total_quantity_sold': total_quantity_sold,
        'orders': orders,
    }

    return render(request, 'admin_manage/adm/sales_report.html', context)


def sales_chart(request):
    sales_data = Order.objects.annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(
        total_sales=Count(Case(When(status='Delivered', then=1), output_field=IntegerField())),
        total_canceled=Count(Case(When(status='Cancel', then=1), output_field=IntegerField())),
    )

    labels = [str(data['month']) for data in sales_data]
    sales_values = [data['total_sales'] for data in sales_data]
    canceled_values = [data['total_canceled'] for data in sales_data]

    chart_data = {'labels': labels, 'sales_values': sales_values, 'canceled_values': canceled_values}

    return render(request, 'admin_manage/adm/sales_chart.html', {'chart_data': chart_data})
