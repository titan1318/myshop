from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

CustomUser = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'avatar', 'phone_number', 'country']


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
