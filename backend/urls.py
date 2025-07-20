# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/', include('apps.apis.urls')),
    
    # Authentication
    path('accounts/', include('allauth.urls')),
    
    # App URLs
    path('users/', include('apps.users.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path('posts/', include('apps.posts.urls')),
    
    # Home page
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)