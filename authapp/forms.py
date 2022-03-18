from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authapp.models import (Teacher, Student)

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