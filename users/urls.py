from django.urls import path
from .views import home_view, api_docs_view  # Import the view for API docs
from .views import (
    home_view,
    profile_view,
    RegisterView,
    ProfileView,
    CustomTokenObtainPairView,
    ProfileUpdateView,
    SecuritySettingsView,
    enable_2fa,
    disable_2fa,
    api_docs_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('profile/view/', ProfileView.as_view(), name='profile_api'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('security/', SecuritySettingsView.as_view(), name='security_settings'),
    path('enable-2fa/', enable_2fa, name='enable_2fa'),
    path('disable-2fa/', disable_2fa, name='disable_2fa'),
    path('api/docs/', api_docs_view, name='api_docs'),  # API documentation page
]