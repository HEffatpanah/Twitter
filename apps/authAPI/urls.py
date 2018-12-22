from django.urls import path

from apps.authAPI.views import views ,APIviews

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login_page, name='index'),
    path('api/v1/login', APIviews.login_page, name='index'),
    path('api/v1/tweet', APIviews.tweet, name='tweet'),
    path('', views.mainPage, name='home'),
    path('profile', views.profile, name='profile'),
    path('tweets', views.tweets, name='tweets'),
    path('logoutPage', views.logoutUser, name='logout'),
    path('api/v2/profile', APIviews.generate_token, name='profile+token'),
    path('api/v2/login', APIviews.login_page, name='login+token'),
    path('api/v2/tweet', APIviews.tweet, name='tweet+token'),



]