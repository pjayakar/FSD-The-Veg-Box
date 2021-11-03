from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from users import views as users_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vegbox_app.urls')),
    path('register/', users_views.register, name='register'),
    path('register/', users_views.register_details, name='vegbox-registerdetails'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
