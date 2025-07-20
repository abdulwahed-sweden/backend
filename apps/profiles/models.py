# apps/profiles/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse
from PIL import Image
import os

class Profile(models.Model):
    """User profile model"""
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, help_text='Tell us about yourself')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_public = models.BooleanField(default=True, help_text='Make profile visible to others')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        return reverse('profiles:detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize avatar if it exists
        if self.avatar and hasattr(self.avatar, 'path'):
            try:
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)
            except Exception:
                pass

class SocialLink(models.Model):
    """Social media links for profiles"""
    
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'social_links'
        unique_together = ['profile', 'platform']
        verbose_name = 'Social Link'
        verbose_name_plural = 'Social Links'
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.get_platform_display()}"