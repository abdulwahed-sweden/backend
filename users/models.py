# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


# Add these fields to the User model
class User(AbstractUser):
    personnummer = models.CharField(max_length=12, blank=True, verbose_name="Personnummer")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telefonnummer")
    address = models.TextField(blank=True, verbose_name="Adress")
    postnummer = models.CharField(max_length=6, blank=True, verbose_name="Postnummer")
    ort = models.CharField(max_length=50, blank=True, verbose_name="Ort")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name="Profilbild")
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client_secret = models.CharField(max_length=128, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"