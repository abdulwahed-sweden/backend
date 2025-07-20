# apps/apis/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'profiles', views.ProfileViewSet, basename='profile')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')

app_name = 'apis'

urlpatterns = [
    # API router URLs
    path('', include(router.urls)),
    
    # Authentication URLs
    path('auth/', include('rest_framework.urls')),
]