from django.contrib import admin

from .models import OrderItem
from .models import Order
from .models import Category
from .models import Product
from .models import ShippingAddress
from .models import Payment
from .models import PromotionCode

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'shipping_address',
                    'payment',
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'payment',
    ]
    list_filter = ['ordered',
                 ]
    search_fields = [
        'user__username',
        'order_id'
    ]
    actions = [make_refund_accepted]


admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(Payment)
admin.site.register(PromotionCode)
