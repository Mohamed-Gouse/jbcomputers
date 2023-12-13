from django.db import models
from django.contrib.auth.models import User
from acuser.models import UserAddress
from product.models import Product

# Create your models here.
class Order(models.Model):
    COD = 'COD'
    PAYPAL = 'PAYPAL'
    WALLET = 'WALLET'

    PAYMENT_CHOICES = (
        (COD, 'COD'),
        (PAYPAL, 'PAYPAL'),
        (WALLET, 'WALLET')
    )
    ORDERED = 'Ordered'
    SHIPPED = 'Shipped'
    CANCEL = 'Cancel'
    DELIVERED = 'Delivered'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped'),
        (CANCEL, 'Cancel'),
        (DELIVERED, 'Delivered')
    )

    user = models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True, default=0)
    pay_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=COD)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order ID: {self.id}"

    def paid_amount_total(self):
        if self.paid_amount:
            return self.paid_amount
        else:
            return 0


class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='ordered_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='ordered_products', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.order.id} - {self.product.name}"


class ReturnedProduct(models.Model):
    RETURN_PENDING = 'Return Pending'
    RETURNED = 'Returned'

    RETURN_STATUS_CHOICES = (
        (RETURN_PENDING, 'Return Pending'),
        (RETURNED, 'Returned')
    )

    order = models.ForeignKey(Order, related_name='returned_products', on_delete=models.CASCADE)
    reason = models.TextField()
    return_status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default=RETURN_PENDING)
    returned_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.order.id} - {self.return_status}"


class Applied_coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    coupon = models.CharField(max_length=20, null=True, blank=True, unique=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.coupon}"
