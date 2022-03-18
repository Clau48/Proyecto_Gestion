
from django.urls import path

from django.contrib.auth.views import (LoginView, LogoutView)
# from authapp.views import loginView

urlpatterns = [
	# path('login/', loginView, name="login"),
	path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='registration/logged_out.html') , name="logout"),
]
