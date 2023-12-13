import uuid
from django.db import models
from django.contrib.auth.models import User

from product.models import Product


# Create your models here.
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=250)
    zipcode = models.CharField(max_length=6)
    place = models.CharField(max_length=250)

    def __str__(self):
        return self.user.username

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_address(self):
        return f"{self.address}, {self.place}"


class Wallet(models.Model):
    DEBIT = 'Debit'
    CREDIT = 'Credit'

    BALANCE_TYPE = (
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit')
    )
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(default=0)
    balance_type = models.CharField(max_length=15, choices=BALANCE_TYPE, default=CREDIT)
    balance_returned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    def total_balance(self):
        balance = 0
        if self.balance_type == Wallet.DEBIT:
            balance -= self.amount
        else:
            balance += self.amount
        return balance


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
