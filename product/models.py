from _decimal import Decimal
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files import File


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='brand')
    active = models.BooleanField(default=True)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Brand, self).save(*args, **kwargs)


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category')
    active = models.BooleanField(default=True)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Subcategories'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Subcategory, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    stock = models.IntegerField()
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    thumb = models.ImageField(upload_to='thumbnail')
    image_1 = models.ImageField(upload_to='product-img')
    image_2 = models.ImageField(upload_to='product-img')
    image_3 = models.ImageField(upload_to='product-img')
    image_4 = models.ImageField(upload_to='product-img')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def thumbnail(self):
        if self.thumb:
            return self.thumb.url
        else:
            self.thumb = self.make_thumbnail(self.image_1)
            self.save()
            return self.thumb.url

    def make_thumbnail(self, image, size=(150, 150)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_discounted_price(self):
        offers = Offer.objects.filter(product=self, start_date__lte=timezone.now(), end_date__gte=timezone.now())

        if offers.exists():
            offer = offers.first()
            if offer.discount_type == 'percentage':
                discount_amount = (offer.discount_value / Decimal(100)) * self.price
            else:
                discount_amount = offer.discount_value

            discounted_price = self.price - discount_amount
            return max(discounted_price, Decimal(0))
        else:
            return self.price


class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=10, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
