from django import forms
from .models import User

from django.contrib.auth import get_user_model

User = get_user_model()



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 
                 'address', 'postnummer', 'ort', 'profile_picture']
        labels = {
            'first_name': 'Förnamn',
            'last_name': 'Efternamn',
            'email': 'E-post',
            'phone_number': 'Telefonnummer',
            'address': 'Adress',
            'postnummer': 'Postnummer',
            'ort': 'Ort',
            'profile_picture': 'Profilbild'
        }

class SecuritySettingsForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, label="Nuvarande lösenord")
    new_password = forms.CharField(widget=forms.PasswordInput, label="Nytt lösenord")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Bekräfta nytt lösenord")

