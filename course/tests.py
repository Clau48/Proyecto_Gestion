from django.test import TestCase
# from .models import Profile
from django.http import HttpRequest
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.sessions.middleware import SessionMiddleware
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from course.models import Course, Post, Course_User
# from .views import (side_nav_info, register, edit_profile)
from django.test.client import RequestFactory
from .views import send_link_course
import uuid

class CourseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=1, username='luiggi',
											 email='luiggi.pasache.lopera@gmail.com',
											 password='luiggi',
											 )
        self.course = Course.objects.create(id=1, picture='picture', title='test_curso', description='Este es un curso para tests', 
            time_start='09:00', time_end='12:00', syllabus='syllabus', user=self.user, codeinvitation=uuid.uuid4())
   
    def test_send_link_course(self):
        user_owner =  self.user
        course = self.course
        to_email = 'fisiversity@gmail.com'
        
        result = send_link_course(user_owner, 'http://localhost:8000/', course, to_email)

        self.assertEqual(result, 1)