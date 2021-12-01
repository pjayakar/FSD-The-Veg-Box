from django.conf.urls import url
from django.urls import path
from vegbox_app import views
from users import views as user_views
urlpatterns = [
    path('', views.product_list,name='vegbox-home'),
    path('fruits/', views.product_list_veggie,name='vegbox-fruits'),
    path('dairy/', views.product_list_dairy,name='vegbox-dairy'),
    path('register/', user_views.register, name='register'),
    path('register_details/', user_views.register_details, name='vegbox-details'),
    path('order_summary/',user_views.order_details,name='order_summary'),
    path('add_to_cart/(?P<item_id>[-\w]+)/$',user_views.add_to_cart,name='add_to_cart'),
    url('^item/delete/(?P<item_id>[-\w]+)/$',user_views.delete_from_cart,name='delete_item'),
    path('checkout/',user_views.order_details1,name='checkout'),
    path('invoice/',user_views.GeneratePdf.as_view(),name='invoice'),
]