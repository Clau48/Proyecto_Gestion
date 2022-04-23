from django.urls import path
from course.views import  *


urlpatterns = [
	#Course - Classroom Views
	path('', showCourse, name='show_courses'),
	
	#Course routes
	path('newcourse/', new_course, name='newcourse'),
	path('<course_id>/editcourse', edit_course, name='edit_course'),
	path('mycourses/', show_mycourses, name='mycourses'),
	path('<course_id>/deletecourse', delete_course, name='deletecourse'),
	path('<course_id>/', show_course_description, name='show_description'),
	path('<course_id>/posts/notas', show_calification, name='show_calification'),

	#Post routes
	path('<course_id>/posts', show_posts, name='show_posts'),
	path('<course_id>/posts/newpost', NewPost, name='new-post'),
	path('<course_id>/posts/<post_id>/editpost', edit_post, name='edit-post'),

	#Homework routes
	path('<course_id>/<post_id>/entrega', send_homework, name='send_homework'), 
 	path('<course_id>/<post_id>/entrega/process', send_homework_post, name='send_homework_post'),

	#Auth routes
	path("<course_id>/users/", usersInCourse, name="users_in_course"),
	path("<course_id>/send_invitation", sendInscriptionLink, name="send_inscription"),
	path("inscription/<codeInvitation>/", inscriptionLink, name="url_inscription"),

	#Assignment routes
	path('<course_id>/posts/newassignment', new_assignment, name='new-assignment'),
	path('<course_id>/posts/<assignment_id>/editassignment', edit_assignment, name='edit-assignment'),
	path('<course_id>/posts/<assignment_id>/calificate', teacher_calificate, name='calification_assignment'), 
	path('homework/calificate', addCalification, name='addCalification'), 
	path('<course_id>/team/form', formTeams, name='formTeams'), 
	path('<course_id>/team/form/process', formTeamsProcess, name='formTeamsProcess'), 
	path('<course_id>/team/show', showTeams, name='showTeams'), 
]