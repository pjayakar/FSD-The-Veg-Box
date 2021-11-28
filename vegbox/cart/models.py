from django.db import models
from django.conf import settings
from django import forms

# from products.models import Product
# from checkout.models import ShippingAddress
# from checkout.models import Payment

from django.db import models
from django import forms
from django_countries.fields import CountryField
from django.urls import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    country = CountryField()
    phone = models.CharField(max_length=30)
    current_address = models.BooleanField(default=False)

    def __str__(self):
        return f'Shipping address for {self.user.username}: {self.street} {self.street_number}, {self.city}'

    def get_absolute_url(self):
        return reverse('profile')


class ShippingAddressForm(forms.ModelForm):
    save_address = forms.BooleanField(required=False, label='Save the billing addres')

    class Meta:
        model = ShippingAddress
        fields = [
            'first_name',
            'last_name',
            'street',
            'street_number',
            'zip_code',
            'city',
            'country',
            'phone'
        ]


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_id = models.CharField(max_length=60)
    amount = models.FloatField()
    issued_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} payment: {self.amount}'


class PromotionCode(models.Model):
    code = models.CharField(max_length=50)
    percentage_discount = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    def __str__(self):
        return self.code


class PromotionCodeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].required = False

    class Meta:
        model = PromotionCode
        fields = ['code']
        labels = {
            'code': 'Promotion Code'
        }

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    IMG_DIMENSION = 540

    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='products/')

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name

    def save(self):
        super().save()

        with Image.open(self.thumbnail.path) as img:
            if img.height > self.IMG_DIMENSION or img.width > self.IMG_DIMENSION:
                img.thumbnail((self.IMG_DIMENSION, self.IMG_DIMENSION))
                img.save(self.thumbnail.path)

    def get_product_url(self):
        return reverse("sumiaproducts:product-detail", kwargs={
            'pk': self.pk
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item.name}: {self.quantity}'

    def get_total(self):
        return round(self.item.price * self.quantity, 2)


class Order(models.Model):
    order_id = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    promo_code_applied = models.BooleanField(default=False)
    promo_code_discount = models.FloatField(default=0)
    # refund_requested = models.BooleanField(default=False)
    # refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.get_all_items()}'

    def get_all_items(self):
        return [item for item in self.items.all()]

    def get_total_amount(self):
        total = sum(item.get_total() for item in self.items.all())
        return total - self.promo_code_discount

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


# class Refund(models.Model):
#     reason = models.TextField()
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
#     granted = models.BooleanField(default=False)

#     def __str__(self):
#         return f'Refund for order {self.order.order_id}'


# class RefundForm(forms.ModelForm):
#     order_id = forms.CharField()

#     class Meta:
#         model = Refund
#         fields = ['order_id', 'reason']