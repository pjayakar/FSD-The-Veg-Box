from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from users import views as users_views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', include('vegbox_app.urls')),
    path('register/', users_views.register, name='register'),
    path('register/', users_views.register_details, name='vegbox-registerdetails'),
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)