from django.urls import path
# from authy.views import signup, edit_profile
from authy.views import edit_profile
from authy import views

from django.contrib.auth.views import (LoginView, LogoutView)

urlpatterns = [
	path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
   	path('logout/', LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),

    path('signup/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('profile/edit', edit_profile, name='edit-profile'),
   	# path('signup/', signup, name='signup'),

	# path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
