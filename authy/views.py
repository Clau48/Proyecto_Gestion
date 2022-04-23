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
def show_profile(request):

	user = User.objects.get(id=request.user.id)
	profile = Profile.objects.get(user=user)

	context = {
		'profile': profile,
		'user': user,
	}
	return render(request,'registration/show_profile.html', context)

@login_required
def edit_profile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	user_basic_info = User.objects.get(id = user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			user_basic_info.first_name = form.cleaned_data.get('first_name')
			user_basic_info.last_name = form.cleaned_data.get('last_name')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			user_basic_info.save()
			messages.success(request, 'Perfil actualizado.')
			return redirect('show-profile')
	else:
		form = EditProfileForm(instance=profile)

	context = {
		'form':form,
	}

	return render(request, 'registration/edit_profile.html', context)

@login_required
def inscription(request):
	course = Course.objects.filter(course_user__user=request.user.id)
	return render(request,'courses/allCourses.html',{'course_inscription':course})


@login_required
def inscriptionProcess(request):     
	if request.method == 'POST':

		idInvitationRequest = request.POST.get('code_inscription')
		try:
			course = Course.objects.get(codeinvitation=idInvitationRequest)
			already_inscription = Course_User.objects.filter(user=request.user.id, course=course.id)     
			if already_inscription:
				messages.error(request, 'Ya estas inscripto en este curso')
				return redirect('/user/inscription/')
			else:  
				course_user = Course_User.objects.create(user=request.user, course=course)
				return redirect('/user/inscription/')
		except :
			messages.error(request, 'Codigo de invitacion no valido')
			return redirect('/user/inscription/')
	
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
