from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from .forms import ProfileUpdateForm, SecuritySettingsForm

User = get_user_model()


# ======================
# Template Views
# ======================

def home_view(request):
    return render(request, 'home.html')  # المسار الصحيح للقالب


def api_docs_view(request):
    return render(request, 'users/api_docs.html')


@login_required
def profile_view(request):
    """Render the user profile page."""
    return render(request, 'profile.html', {
        'profile': request.user.profile
    })


# ======================
# API Views
# ======================
class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Create and save a new user with a hashed password."""
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()


class ProfileView(generics.RetrieveAPIView):
    """Get client credentials and user profile."""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the profile of the authenticated user."""
        return self.request.user.profile


class CustomTokenObtainPairView(TokenObtainPairView):
    """Extended login endpoint to return profile data."""
    def post(self, request, *args, **kwargs):
        """Add profile data to the JWT token response."""
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = request.user
            profile = Profile.objects.get(user=user)
            response.data.update(ProfileSerializer(profile).data)
        return response


# ======================
# Profile Management Views
# ======================
class ProfileUpdateView(UpdateView):
    """Allow users to update their profile."""
    model = User
    form_class = ProfileUpdateForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        """Return the currently authenticated user."""
        return self.request.user


class SecuritySettingsView(UpdateView):
    """Allow users to update their security settings."""
    form_class = SecuritySettingsForm
    template_name = 'security_settings.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        """Return the currently authenticated user."""
        return self.request.user


# ======================
# Two-Factor Authentication Views
# ======================
def enable_2fa(request):
    """Enable Two-Factor Authentication for the user."""
    device = TOTPDevice.objects.create(user=request.user, confirmed=False)
    # Show QR code to user
    return render(request, 'enable_2fa.html', {'device': device})


def disable_2fa(request):
    """Disable Two-Factor Authentication for the user."""
    TOTPDevice.objects.filter(user=request.user).delete()
    return redirect('security_settings')