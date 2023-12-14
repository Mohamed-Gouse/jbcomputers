from django.db import models


# Create your models here.
class Banners(models.Model):
    bm_1 = models.ImageField(upload_to='banners', null=True, blank=True)
    bm_2 = models.ImageField(upload_to='banners', null=True, blank=True)
    bm_3 = models.ImageField(upload_to='banners', null=True, blank=True)
    bs_1 = models.ImageField(upload_to='banners', null=True, blank=True)
    bs_2 = models.ImageField(upload_to='banners', null=True, blank=True)
    bs_3 = models.ImageField(upload_to='banners', null=True, blank=True)
    bs_4 = models.ImageField(upload_to='banners', null=True, blank=True)


class Notification(models.Model):
    message = models.CharField(max_length=100)

    def __str__(self):
        return self.message


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
