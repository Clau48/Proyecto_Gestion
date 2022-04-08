from django.test import TestCase
# from .models import Profile
from django.contrib.auth.models import User

from django.http import HttpRequest
from course.views import NewPost, show_posts
from .models import Course, Post
from django.contrib.auth import authenticate
from django.contrib.sessions.middleware import SessionMiddleware
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
# from .views import (side_nav_info, register, edit_profile)
from django.test.client import RequestFactory
from .views import send_link_course, usersInCourse

class CourseTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user',
                                            email='test.user@gmail.com',
                                            password='test.password',
                                            )
        self.course = Course.objects.create(picture=None,
                                            title='test_course',
                                            description='test',
                                            day='LU',
                                            time_start='10:00',
                                            time_end='11:00',
                                            syllabus='Syllabus',
                                            user=self.user,
                                            )
        self.post = Post.objects.create(title='testpost',
                                        content='postcontent',
                                        file='None',
                                        course_id=self.course.id
        )
    #def test_login(self):
    #    user = authenticate(username='luiggi', password='luiggi')
    #    self.assertNotEqual(user, None)
    

    def test_newpost(self):
        course = Course.objects.get(title='test_course')
        req = self.factory.post(f'{course.id}/posts/newpost')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'test_post_title',
                'content': 'test_post_content',
                'file': None,
                'course_id': course.id
                }

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        NewPost(req,course.id)
        post = Post.objects.get(title = info['title'])
        assert post

    def test_showpost(self):
        req = self.factory.get(f'{self.course.id}/posts')
        req.user = self.user
        try:
            show_posts(req,self.course.id)
            assert True
        except:
            assert False

    def test_send_link_course(self):
        user_owner =  self.user
        course = self.course
        to_email = 'fisiversity@gmail.com'
        
        result = send_link_course(user_owner, 'http://localhost:8000/', course, to_email)

        self.assertEqual(result, 1)

    def test_usersInCourse(self):
        request = HttpRequest()
        assert usersInCourse(request, self.course.id)