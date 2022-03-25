from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, EditProfileForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from authy.models import Profile

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from .forms import RegisterUserForm

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

def register(request):
    if request.user.is_authenticated:
        print('Already authenticated')
        return redirect('index')
    else:
        if request.method == 'POST':
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                print('Valid form')

                user = form.save(commit=False)
                user.is_active = False
                user.save()

                send_email_confirmation(request, user)

                messages.success(request, 'Please Confirm your email to complete registration before Login.')
                return redirect('register')
            else:
                if form.errors:
                    for key, values in form.errors.as_data().items():
                        if key == 'username':
                            messages.info(request, 'Error input fields')
                            break
                        else:
                            for error_value in values:
                                print(error_value)
                                messages.info(request, '%s' % (error_value.message))

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

        messages.success(request, 'Successful email confirmation, you can proceed to login.')

        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')