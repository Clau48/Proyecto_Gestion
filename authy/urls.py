from django.urls import path
from authy import views

from django.contrib.auth.views import (LoginView, LogoutView)

urlpatterns = [
	path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
   	path('logout/', LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),

    path('signup/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('profile/edit', views.edit_profile, name='edit-profile'),
]
