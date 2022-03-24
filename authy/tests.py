from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.sessions.middleware import SessionMiddleware
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from .views import side_nav_info, signup, edit_profile  
from django.test.client import RequestFactory
from .utils import send_email_confirmation

# Create your tests here.

class ProfileTestCase(TestCase):

	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='luiggi',
											 email='luiggi.pasache.lopera@gmail.com',
											 password='luiggi',
											 )

	def test_register(self):
		req = self.factory.post('user/signup')

		info = {'csrfmiddlewaretoken': get_token(req),
				'username': 'test_user',
				'email': 'test_user@gmail.com',
				'password1': 'test_user',
				'password2': 'test_user',
				'action': '',
				}

		user = User.objects.create_user('test_user', 'test_user@gmail.com', 'test_user')

		middleware = SessionMiddleware(get_response='')
		middleware.process_request(req)
		req.session.save()

		q = QueryDict('', mutable=True)
		q.update(info)
		req.POST = q
		req.user = user
		signup(req)
		user = User.objects.get(username='test_user')
		assert user

	def test_edit_profile(self):
		req = self.factory.post('user/profile/edit')
		req.user = self.user

		info = {'csrfmiddlewaretoken': get_token(req),
				'first_name': 'test',
				'last_name': 'user',
				'location': 'test location',
				'url': 'testurl.com',
				'profile_info': 'test profile info',
				'action': '',
				}

		q = QueryDict('', mutable=True)
		q.update(info)
		req.POST = q

		edit_profile(req)
		profile = Profile.objects.get(user=self.user)
		assert profile.location

	def test_side(self):
		req = self.factory.post('login')
		req.user = self.user
		side_nav_info(req)
		user = User.objects.get(username=self.user)
		assert user

	def test_login(self):
		user = authenticate(username='luiggi', password='luiggi')
		self.assertNotEqual(user, None)
	
	def test_send_email(self):
		req = self.factory.post('user/signup')
		user = authenticate(username='luiggi', password='luiggi')
		send_email = send_email_confirmation(req, user)
		self.assertEqual(send_email, 1)
