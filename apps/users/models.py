# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    """Custom User model with additional fields"""
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'pk': self.pk})
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def display_name(self):
        return self.full_name or self.username