from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('api/auth/', include('users.urls')),  # API authentication routes
    path('', include('users.urls')),  # Root path (home page)
]