from operator import truediv
from django.test import TestCase
# from .models import Profile
from django.contrib.auth.models import User
from django.http import HttpRequest
from course.views import *
from .models import Assignment, Course, Post
from datetime import datetime
import pytz
from django.http.request import QueryDict
from django.middleware.csrf import get_token
# from .views import (side_nav_info, register, edit_profile)
from django.test.client import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from .views import send_link_course, usersInCourse, send_notification_new_asignement

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
        self.assignment = Assignment.objects.create(title='test_asgmt',
                                                    content='assignmentcontent',
                                                    file='None',
                                                    course_id=self.course.id,
                                                    is_asgmt=True,
                                                    due_datetime=datetime(2022, 4, 30, 17, 45, 0, 127325, tzinfo=pytz.UTC),

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

    def test_delete_course(self):
        req = self.factory.get(f'course/{self.course.id}/deletecourse')
        req.user = self.user

        setattr(req, 'session', 'session')
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)

        self.course.deleted = True

        delete_course(req, self.course.id)

        self.assertEqual(self.course.deleted, True)
        
    def test_edit_post(self):
        req = self.factory.post(f'{self.course.id}/posts/{self.post.id}/editpost')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'new_title_post',
                'content': 'new_post_content',
                }

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        edit_post(req,self.course.id,self.post.id)

        post = Post.objects.get(title = info['title'])
        assert post

    def test_send_link_course(self):
        user_owner =  self.user
        course = self.course
        to_email = 'fisiversity@gmail.com'
        
        result = send_link_course(user_owner, 'http://localhost:8000/', course, to_email)

        self.assertEqual(result, 1)

    def test_usersInCourse(self):
        request = HttpRequest()
        assert usersInCourse(request, self.course.id)

    def test_new_assignment(self):
        course = Course.objects.get(title='test_course')
        req = self.factory.post(f'{course.id}/posts/newassignment')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'test_post_title',
                'content': 'test_post_content',
                'file': None,
                'course_id': course.id,
                'is_asgmt': True,
                'due_datetime': '2022-04-30 17:45:00.000000'
                }

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        new_assignment(req,course.id)
        assignment = Assignment.objects.get(title = info['title'])
        assert assignment

    def test_edit_assignment(self):
        req = self.factory.post(f'{self.course.id}/posts/{self.assignment.id}/editassignment')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'new_asgmt_title',
                'content': 'new_asgmt_content',
                'file': None,
                'due_datetime': datetime(2022, 4, 20, 20, 8, 7, 127325, tzinfo = pytz.UTC),
                'is_asgmt': True,
        }

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        edit_assignment(req, self.course.id, self.assignment.id)
        asgmt = Assignment.objects.all().filter(title = info['title'])
        assert asgmt

    def test_edit_course(self):
        req = self.factory.post(f'{self.course.id}/editcourse')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'picture': 'picture',
                'title':'test_course',
                'description':'test',
                'day':'LU',
                'time_start':'10:00',
                'time_end':'11:00',
                'syllabus':'Syllabus',
                'title': 'curso',
                'picture': 'new_asgmt_content',
                'file': None,
                'user': self.user,
        }

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        edit_course(req, self.course.id)

        self.assertEqual(self.course.title, 'test_course')
    def test_send_notification_new_asignement(self):
        send_mail = send_notification_new_asignement(self.user, 'http://localhost:8000', self.course, [self.user])
        self.assertEqual(send_mail, 1)
