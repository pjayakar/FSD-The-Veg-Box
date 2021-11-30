from django.contrib import admin
from .models import Register,Product, Profile, Order,OrderItem, Transaction,Product_Veggie,Product_Dairy
# Register your models here.
admin.site.register(Register)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(Product_Veggie)
admin.site.register(Product_Dairy)