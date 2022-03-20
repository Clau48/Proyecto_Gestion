from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, EditProfileForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from authy.models import Profile


from django.template import loader
from django.http import HttpResponse


# Create your views here.

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

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			new_user = authenticate(username=username, password=password)

			login(request, new_user)
			profile = Profile.objects.get(user=request.user)
			edit_form = EditProfileForm(instance=profile)
			messages.success(request, '¡La cuenta ha sido creada con éxito!')
			return render(request, 'registration/edit_profile.html', {'form': edit_form})
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