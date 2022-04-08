from django.urls import path
from course.views import  *


urlpatterns = [
	#Course - Classroom Views
	path('', showCourse, name='show_courses'),
	path('newcourse/', new_course, name='newcourse'),
	path('mycourses/', show_mycourses, name='mycourses'),
	path('<course_id>/', show_course_description, name='show_description'),
	path('<course_id>/posts', show_posts, name='show_posts'),
	path('<course_id>/posts/newpost', NewPost, name='new-post'),
	path('<course_id>/<post_id>/entrega', send_homework, name='send_homework'), 
 	path('<course_id>/<post_id>/entrega/process', send_homework_post, name='send_homework_post'), 
	path("<course_id>/users/", usersInCourse, name="users_in_course"),
	path("<course_id>/send_invitation", sendInscriptionLink, name="send_inscription"),
	path("inscription/<codeInvitation>/", inscriptionLink, name="url_inscription"),
]