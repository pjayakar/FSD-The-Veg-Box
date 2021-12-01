from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Register,Product, Profile, Order,OrderItem, Transaction, Product_Dairy, Product_Veggie
from django.urls import reverse
import random
import string
from datetime import date
import datetime
#from shopping_cart.models import Order
@login_required
def product_list(request):
    object_list = Product.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, "vegbox_app/home.html", context)

def product_list_veggie(request):
    object_list = Product_Veggie.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, "vegbox_app/fruits.html", context)

def product_list_dairy(request):
    object_list = Product_Dairy.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, "vegbox_app/dairy.html", context)

from django.shortcuts import render, get_object_or_404

def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str

def my_profile(request):
	my_user_profile = Profile.objects.filter(user=request.user).first()
	my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
	context = {
		'my_orders': my_orders
	}

	return render(request, "vegbox_app/profile.html", context)

@login_required()
def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first() or Product_Veggie.objects.filter(id=kwargs.get('item_id', "")).first() or Product_Dairy.objects.filter(id=kwargs.get('item_id', "")).first()
    if product in request.user.profile.ebooks.all():
        messages.info(request, 'You already own this ebook')
        return redirect(reverse('product-list'))
    order_item, status = OrderItem.objects.get_or_create(product=product)
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('vegbox-home'))


    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('vegbox-home'))

@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('order_summary'))

def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'vegbox_app/cart.html', context)

@login_required()
def checkout(request, **kwargs):
    return render(request, 'vegbox_app/checkout.html')

@login_required()
def order_details1(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'vegbox_app/checkout.html', context)

from django.http import HttpResponse
from django.views.generic import View

#importing get_template from loader
from django.template.loader import get_template

#import render_to_pdf from util.py
from .utils import render_to_pdf

#Creating our view, it is a class based view
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        existing_order = get_user_pending_order(request)
        context = {
            'order': existing_order
        }
        #getting the template
        pdf = render_to_pdf('vegbox_app/invoice.html',context)

         #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vegbox-details')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def register_details(request):
    if request.method == 'POST':
        form1 = ProfileForm(request.POST)
        if form1.is_valid():
            form1.save()
            messages.success(request, f'Account has been created!')
            return redirect('login')
    else:
        form1 = ProfileForm()
    return render(request, 'users/register_details.html', {'form': form1})

