from django.urls import path
from authy.views import signup, edit_profile

from django.contrib.auth import views as authViews 


urlpatterns = [
    
    path('profile/edit', edit_profile, name='edit-profile'),
   	path('signup/', signup, name='signup'),

]