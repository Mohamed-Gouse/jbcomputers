from django.db import models
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
