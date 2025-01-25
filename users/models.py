# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    # Add Swedish-specific fields if needed
    personnummer = models.CharField(max_length=12, blank=True)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client_secret = models.CharField(max_length=128, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"