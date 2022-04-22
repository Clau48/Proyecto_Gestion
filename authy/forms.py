from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authy.models import Profile
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm)
import re

def forbidden_users(value):
    forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
    'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
    if value.lower() in forbidden_users:
        raise ValidationError('Invalid name for user, this is a reserverd word.')

def invalid_user(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def unique_email(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this email already exists.')

def unique_user(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this username already exists.')

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=True)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=True)
    picture = forms.ImageField(required=False)
    profile_info = forms.CharField(widget=forms.TextInput(), max_length=260, required=False)

    class Meta:
        model = Profile
        fields = ('picture', 'first_name', 'last_name', 'profile_info')

    def clean_first_name(self):
        fname_passed = self.cleaned_data.get("first_name")
        is_valid = re.search("[^a-z A-Z]", fname_passed)
        if is_valid is not None:
            raise forms.ValidationError("Los nombres solo puede contener letras y espacios")
        return fname_passed
    
    def clean_last_name(self):
        lname_passed = self.cleaned_data.get("last_name")
        is_valid = re.search("[^a-z A-Z]", lname_passed)
        if is_valid is not None:
            raise forms.ValidationError("Los apellidos solo puede contener letras y espacios")
        return lname_passed

# Registro con autentificacion de usuarios
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}), max_length=30, required=True,)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Email'}) , max_length=100, required=True,)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombres'}) , max_length=50, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Apellidos'}) , max_length=50, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}),max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirmar contraseña'}), required=True, label="Confirm your password.")

    class Meta:
        model = User
        fields =  ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email_passed = self.cleaned_data.get("email")
        email_already_registered = User.objects.filter(email = email_passed).exists()
        user_is_active = User.objects.filter(email = email_passed, is_active = 1)
        if email_already_registered and user_is_active:
            raise forms.ValidationError("Email ya se encuentra registrado")
        elif email_already_registered:
            User.objects.filter(email = email_passed).delete()

        return email_passed


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}), max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}),max_length=100, required=True)

    class Meta:
        fields = ('username', 'password')

    def clean_username(self):
        username_passed = self.cleaned_data.get("username")
        user_exists = User.objects.filter(username = username_passed).exists()
        email_is_authenticate = User.objects.filter(username = username_passed, is_active = 1).all()
        print(username_passed, user_exists, email_is_authenticate)
        if not user_exists:
            raise forms.ValidationError("Usuario no existe")
        if not email_is_authenticate:
            raise forms.ValidationError("Por favor, confirma tu email para completar el registro antes de iniciar sesión")
        return username_passed