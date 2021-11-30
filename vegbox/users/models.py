
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
User = get_user_model()

class Register(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    number = models.CharField(max_length=10)

class Product(models.Model):
    name = models.CharField(max_length=120)
    product_img = models.ImageField(upload_to='images/')
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Product_Dairy(models.Model):
    name = models.CharField(max_length=120)
    product_img = models.ImageField(upload_to='images/')
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Product_Veggie(models.Model):
    name = models.CharField(max_length=120)
    product_img = models.ImageField(upload_to='images/')
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ebooks = models.ManyToManyField(Product, blank=True)
    def __str__(self):
        return self.user.username

def post_save_profile_create(sender, instance, created, *args, **kwargs):
    user_profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)

class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.name

class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)

class Transaction(models.Model):
        profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
        token = models.CharField(max_length=120)
        order_id = models.CharField(max_length=120)
        amount = models.DecimalField(max_digits=100, decimal_places=2)
        success = models.BooleanField(default=True)
        timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

        def __str__(self):
            return self.order_id

        class Meta:
            ordering = ['-timestamp']