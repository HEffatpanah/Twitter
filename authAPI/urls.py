from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='index'),
    path('addUser', views.addUser, name='addUser'),
    path('', views.mainPage, name='addUser'),
    path('checkAuth', views.checkAuth, name='checkAuth'),
]