from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Product
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators  import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.html import strip_tags
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.generic.edit import UpdateView

from .models import Payment, Product
from .models import Order, OrderItem, ShippingAddress, ShippingAddressForm, PromotionCodeForm,PromotionCode
class HomePage(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    paginate_by = 4


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_details.html'
class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False).first()
        if not order:
            return redirect('sumiacheckout:checkout')
        order_items = order.get_all_items()
        shipping_address = ShippingAddress.objects.filter(user=self.request.user, current_address=True)
        shipping_address = shipping_address.first() if shipping_address.exists() else None
        form = ShippingAddressForm(instance=shipping_address)
        promo_form = PromotionCodeForm()
        context = {
            'order': order,
            'order_items': order_items,
            'form': form,
            'promo_form': promo_form
        }
        return render(self.request, 'checkout/checkout.html', context)

    def post(self, *args, **kwargs):
        form = ShippingAddressForm(self.request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = self.request.user
            shipping_address.save()
            order = Order.objects.filter(user=self.request.user, ordered=False).first()
            order.shipping_address = shipping_address
            order.save()
            if form.cleaned_data['save_address']:
                current_shipping_address = ShippingAddress.objects.filter(user=self.request.user, current_address=True).first()
                if current_shipping_address:
                    current_shipping_address.current_address = False
                    current_shipping_address.save()
                shipping_address.pk = None
                shipping_address.current_address = True
                shipping_address.save()
        return redirect('sumiacheckout:payment')


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False).first()
        return render(self.request, 'checkout/payment.html', {'order': order})

    def post(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False).first()
        token = self.request.POST.get('stripeToken')
        try:
            charge = strip_tags.Charge.create(
              amount=round(float(order.get_total_amount() * 100)),
              currency="usd",
              source=token
            )
        except strip_tags.error.CardError:
            messages.error(self.request, 'Payment could not be made')
            return redirect('sumiaproducts:home-page')
        except Exception:
            messages.error(self.request, 'Internal server error')
            return redirect('sumiaproducts:home-page')

        payment = Payment(
            user=self.request.user,
            stripe_id=charge.id,
            amount=order.get_total_amount()
        )
        payment.save()
        order.order_id = get_random_string(length=20)
        order.payment = payment
        order.ordered = True
        order.save()

        messages.info(self.request, 'Payment was successfully issued')
        return redirect('sumiacheckout:checkout-success')


class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    form_class = ShippingAddressForm
    template_name = 'checkout/profile.html'
    success_message = "The address has been successfully updated"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.current_address = True
        return super().form_valid(form)

    def get_object(self):
        obj = ShippingAddress.objects.filter(user=self.request.user, current_address=True)
        return obj.first() if obj.exists() else None


class PromoCodeView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
            form = PromotionCodeForm(self.request.POST)
            if form.is_valid():
                order = Order.objects.filter(user=self.request.user, ordered=False).first()
                if order.promo_code_applied:
                    messages.warning(self.request, "The promotion code has been already applied")
                    return redirect('sumiacheckout:checkout')
                try:
                    code = PromotionCode.objects.get(code=form.cleaned_data.get('code'))
                except PromotionCode.DoesNotExist:
                    messages.warning(self.request, "Provided code does not exists")
                    return redirect('sumiacheckout:checkout')
                order.promo_code_discount = order.get_total_amount() * code.percentage_discount
                order.promo_code_applied = True
                order.save()
                return redirect('sumiacheckout:checkout')


def checkout_success(request):
    return render(request, 'checkout/success.html')

class OrdersListView(LoginRequiredMixin, ListView):
    """
        must define a template name for rendering
    """
    template_name = 'carts/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.request.user.order_set.filter(ordered=True)


class CartDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'order'
    template_name = 'carts/cart.html'

    def get_object(self, queryset=None):
        return self.request.user.order_set.filter(ordered=False).first()


class AddToCartAjax(View):
    def post(self, request, product_id, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return JsonResponse({
                'error': 'In order to add item to cart please create an account'
            }, status=401)
        if self.request.is_ajax:
            product = get_object_or_404(Product, pk=product_id)
            order, _ = Order.objects.get_or_create(user=self.request.user, ordered=False)
            if order.items.filter(item__pk=product_id).exists():
                order_item = order.items.get(item__pk=product_id)
                order_item.quantity += 1
                order_item.save()
            else:
                order_item = OrderItem.objects.create(user=self.request.user, item=product)
                order.items.add(order_item)
            return JsonResponse({
                'msg': "Product has been successfully added to cart",
                'quantity': order_item.quantity,
                'total_items': order.get_total_quantity()
            })


@login_required
def increase_product_in_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order, _ = Order.objects.get_or_create(user=request.user, ordered=False)
    if order.items.filter(item__pk=product_id).exists():
        order_item = order.items.get(item__pk=product_id)
        order_item.quantity += 1
        order_item.save()
    else:
        order.items.create(user=request.user, item=product)
    messages.success(request, 'Product has been added to cart.')
    return redirect('cart:show-cart')


@login_required
def decrease_product_in_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order:
        order_item = order.items.filter(user=request.user, item=product).first()
        if order_item:
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity <= 0:
                order.items.remove(order_item)
            messages.success(request, 'Product has been removed from cart.')
        else:
            messages.warning(request, 'This item is not in your cart.')
    else:
        messages.warning(request, 'Cart does not exists. Add some products to cart.')
        return redirect('products:home-page')
    return redirect('cart:show-cart')


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order:
        order_item = order.items.filter(user=request.user, item=product).first()
        if order_item:
            order.items.remove(order_item)
            messages.success(request, 'Product has been removed from cart.')
        else:
            messages.warning(request, 'This item is not in your cart.')
    else:
        messages.warning(request, 'Cart does not exists. First add products to cart.')
        return redirect('products:home-page')
    return redirect('cart:show-cart')