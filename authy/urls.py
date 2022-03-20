from django.urls import path
from authy.views import signup, edit_profile

from django.contrib.auth.views import (LoginView, LogoutView)

urlpatterns = [
	path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
   	path('logout/', LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),

    path('profile/edit', edit_profile, name='edit-profile'),
   	path('signup/', signup, name='signup'),
]
