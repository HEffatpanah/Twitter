from django.conf.urls import url
from django.urls import path
from notebook.auth import logout

from twitter import settings
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login_page, name='index'),
    path('', views.mainPage, name='home'),
    path('profile', views.profile, name='profile'),
    path('tweets', views.tweets, name='tweets'),
    # path('logoutPage', views.logout, name='logout'),
    path('logoutPage', views.logoutUser, name='logout'),
    path('api/login', views.my_login),
    path('api/sampleapi', views.sample_api),



]