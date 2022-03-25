from calendar import c
from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, EditProfileForm
from course.forms import InscriptionForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from authy.models import Profile
from course.models import Course,Course_User
from pprint import pprint
from inspect import getmembers

from django.template import loader
from django.http import HttpResponse


# Create your views here.

def side_nav_info(request):
	user = request.user
	nav_profile = None

	if user.is_authenticated:
		nav_profile = Profile.objects.get(user=user)
	
	return {'nav_profile': nav_profile}

def user_profile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)


	template = loader.get_template('profile.html')

	context = {
		'profile':profile,

	}

	return HttpResponse(template.render(context, request))

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('edit-profile')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'registration/signup.html', context)

@login_required
def edit_profile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	user_basic_info = User.objects.get(id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.banner = form.cleaned_data.get('banner')
			user_basic_info.first_name = form.cleaned_data.get('first_name')
			user_basic_info.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			user_basic_info.save()
			return redirect('index')
	else:
		form = EditProfileForm(instance=profile)

	context = {
		'form':form,
	}

	return render(request, 'registration/edit_profile.html', context)

@login_required
def inscription(request):
	# courses = Course.objects.filter()
	# foo = 'vaca';
	# pprint(request.code)
	# pprint(foo)
	# data = {
	# 	'form' : InscriptionForm() 
	# }
	# form = Inscription()
	# mensaje = ''
	# if request.GET['code']:
	# 	mensaje = 'Buscaodr: %r' %request.GET['code']
	# 	courseForm = request.GET['code']
	# 	# course = Course.objects.get(title='Santuron')
	# 	course = Course.objects.filter(title__icontrains=courseForm)
	# 	return render(request,'courses/allCourses.html',{'course':course, 'mensaje':mensaje})
	# else:
	# 	mensaje = 'No hay nada'
	# mensaje = 'Buscaodr: %r' %request.GET['code']
	# courseForm = request.GET['code']
	# coursa= Course.objects.get(title='Santuron')
	# course = Course.objects.filter(title='Santuron')
	# course_1 = course.Course_User.all()
	# coursa=Course_User.objects.filter(user=request.user.id)
	# course = coursa.course_set.all()
	course = Course.objects.filter(course_user__user=request.user.id)
	# course = coursa.course_user_set.all()
	# vaca = 
	return render(request,'courses/allCourses.html',{'course_inscription':course})
 
	course = request.user.id; 
	return render(request,'courses/allCourses.html',{})
@login_required
def inscriptionProcess(request):
	mensaje = ''
	if request.GET['code']:
		mensaje = 'Buscaodr: %r' %request.GET['code']
		courseForm = request.GET['code']
		# course = Course.objects.get(title='Santuron')
		course = Course.objects.filter(title__icontrains=courseForm)
		return render(request,'courses/allCourses.html',{'course':course, 'mensaje':mensaje})
	else:
		mensaje = 'No hay nada'
	course = request.user.id;
	return HttpResponse(course)