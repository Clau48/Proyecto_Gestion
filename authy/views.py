from calendar import c
from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import *
from course.forms import InscriptionForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from authy.models import Profile
from course.models import Course,Course_User

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from .forms import (RegisterUserForm, EditProfileForm)

from .utils import send_email_confirmation

def side_nav_info(request):
	user = request.user
	nav_profile = None

	if user.is_authenticated:
		nav_profile = Profile.objects.get(user=user)
	
	return {'nav_profile': nav_profile}

@login_required
def user_profile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	template = loader.get_template('profile.html')

	context = {
		'profile':profile,
	}

	return HttpResponse(template.render(context, request))

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
			return redirect('login')
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
    # if request.method == 'POST':
    # 		form = InscriptionForm(request.POST)
	# 	if form.is_valid():
	# 		course = form.cleaned_data.get('course')
	# 		course_user = Course_User.objects.create(user=request.user, course=course)
	# 		return redirect('index')
	# else:
     
	if request.method == 'POST':
		already_inscription = Course_User.objects.filter(user=request.user.id, course=request.POST['code_inscription'])
		if already_inscription:
			messages.error(request, 'Ya estas inscripto en este curso')
			return redirect('/user/inscription/')
		else:
			idCourse = request.POST.get('code_inscription')
			course = Course.objects.get(id=idCourse)
			course_user = Course_User.objects.create(user=request.user, course=course)
			return redirect('/user/inscription/')

	# mensaje = ''
	# if request.GET['code']:
	# 	mensaje = 'Buscaodr: %r' %request.GET['code']
	# 	courseForm = request.GET['code']
	# 	# course = Course.objects.get(title='Santuron')
	# 	course = Course.objects.filter(title__icontrains=courseForm)
	# 	return render(request,'courses/allCourses.html',{'course':course, 'mensaje':mensaje})
	# else:
	# 	mensaje = 'No hay nada'
	# course = request.user.id;
	
	return HttpResponse(request.POST['code_inscription'])

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                send_email_confirmation(request, user)

                messages.success(request, 'Por favor, confirma tu email para completar el registro antes de iniciar sesión')
                return redirect('register')
            else:
                if form.errors:
                    for key, values in form.errors.as_data().items():
                            for error_value in values:
                                message = str(error_value).replace('[\'','').replace('\']','')
                                messages.info(request, message)

                return redirect('register')
        else:
            form = RegisterUserForm()

            context = {
                'form': form
            }
            return render(request, 'registration/signup.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Confirmación de email exitosa, puedes iniciar sesión')

        return redirect('login')
    else:
        return HttpResponse('Link de activación inválido')
