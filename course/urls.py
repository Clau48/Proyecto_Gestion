from django.urls import path
from course.views import  *


urlpatterns = [
	#Course - Classroom Views
	path('newcourse/', new_course, name='newcourse'),
	path('mycourses/', show_mycourses, name='mycourses'),
]