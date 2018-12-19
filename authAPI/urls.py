from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login_page, name='index'),
    path('', views.mainPage, name='addUser'),
    path('profile', views.profile, name='profile'),
]