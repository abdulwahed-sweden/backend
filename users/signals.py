# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile
from django.utils.crypto import get_random_string

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create profile with client credentials for new users"""
    if created:
        secret = get_random_string(64)
        Profile.objects.create(user=instance, client_secret=secret)