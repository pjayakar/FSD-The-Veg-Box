from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vegbox_app.urls')),
    path('register/', users_views.register, name='vegbox-register'),
]
