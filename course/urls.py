from django.urls import path
from course.views import  new_course


urlpatterns = [
	#Course - Classroom Views
	path('newcourse/', new_course, name='newcourse'),
]