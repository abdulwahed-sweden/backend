# users/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer

class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()

class ProfileView(generics.RetrieveAPIView):
    """Get client credentials and user profile"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile

class CustomTokenObtainPairView(TokenObtainPairView):
    """Extended login endpoint to return profile data"""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = request.user
            profile = Profile.objects.get(user=user)
            response.data.update(ProfileSerializer(profile).data)
        return response