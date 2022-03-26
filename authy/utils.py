from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from dotenv import load_dotenv
import os

def send_email_confirmation(request, user):
	if user.email is not None:
		current_site = get_current_site(request)
		subject = 'Activa tu cuenta en Fisiversity'
		message = render_to_string('registration/email_confirmation.html',
			{
				"domain": current_site.domain,
				"user": user,
				"uid": urlsafe_base64_encode(force_bytes(user.pk)),
				"token": default_token_generator.make_token(user),
			},
		)
		to_email = user.email
		return send_mail(subject, message, os.getenv('EMAIL_HOST_USER') , [to_email])
	else:
		print('Error: Usuario sin email, no se puede enviar')
		return 0