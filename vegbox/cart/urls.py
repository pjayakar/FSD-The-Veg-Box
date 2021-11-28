from django.urls import path
from .views import increase_product_in_cart, remove_from_cart, decrease_product_in_cart, CartDetailView, AddToCartAjax
from .views import HomePage
from .views import ProductDetailView
from . import views
app_name = 'core'

# app_name = "cart"

urlpatterns = [
    path('', CartDetailView.as_view(), name='show-cart'),
    path('add/<int:product_id>/', AddToCartAjax.as_view(), name='add-to-cart'),
    path('increase/<int:product_id>/', increase_product_in_cart, name='increase-product-in-cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('decrease/<int:product_id>/', decrease_product_in_cart, name='decrease-product-in-cart'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('success/', checkout_success, name='checkout-success'),
    path('add-promotion-code/', PromoCodeView.as_view(), name='promotion-code')
]