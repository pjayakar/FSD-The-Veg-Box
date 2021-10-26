from django.urls import path
from vegbox_app import views
urlpatterns = [
    path('', views.home,name='home'),
]
