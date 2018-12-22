from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login_page, name='index'),
    path('', views.mainPage, name='home'),
    path('profile', views.profile, name='profile'),
    path('tweets', views.tweets, name='tweets'),
    # path('logoutPage', views.logout, name='logout'),
    path('logoutPage', views.logoutUser, name='logout'),
    path('api/login', views.my_login, name='mylogin'),
    path('api/sampleapi', views.sample_api, name='sampleapi'),
    path('api/test', views.test),



]