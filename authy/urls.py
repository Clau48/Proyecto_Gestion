from django.urls import path
from authy.views import *
from authy import views
from .forms import LoginUserForm

from django.contrib.auth.views import (LoginView, LogoutView)

urlpatterns = [
	path('login/', LoginView.as_view(template_name='registration/login.html', authentication_form=LoginUserForm, redirect_authenticated_user=True), name='login'),
   	path('logout/', LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),

    path('inscription/', inscription, name='inscription'),
    path('inscription/process/', inscriptionProcess, name='inscription_process'),

    path('signup/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('profile/edit', views.edit_profile, name='edit-profile'),
    path('me/', views.show_profile, name='show-profile')
]
