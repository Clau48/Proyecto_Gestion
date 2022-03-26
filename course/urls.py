from django.urls import path
from course.views import  *


urlpatterns = [
	#Course - Classroom Views
	path('', showCourse, name='show_courses'),
	path('newcourse/', new_course, name='newcourse'),
	path('mycourses/', show_mycourses, name='mycourses'),
	path('<course_id>/posts', show_posts, name='show_posts'),
	path('<course_id>/posts/newpost', NewPost, name='new-post'),
]