from django.urls import path
from vegbox_app import views
from users import views as user_views
urlpatterns = [
    path('', views.home,name='vegbox-home'),
    path('fruits/', views.fruits,name='vegbox-fruits'),
    path('dairy/', views.dairy,name='vegbox-dairy'),
    path('register/', user_views.register, name='register'),
    path('register_details/', user_views.register_details, name='vegbox-details'),

]
