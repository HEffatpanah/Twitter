from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from apps.authAPI.views import views, APIviews

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('loginp', views.login_page, name='login'),
    path('logoutPage', views.logoutUser, name='logout'),
    path('api/v1/login', APIviews.login_page, name='index'),
    path('api/v1/tweet', APIviews.tweet, name='tweet'),
    path('', views.mainPage, name='home'),
    path('profile', views.profile, name='profile'),
    path('login_success', views.login_success, name='login_success'),
    path('tweets', views.tweets, name='tweets'),
    path('api/v2/profile', APIviews.generate_token, name='profile+token'),
    # path('api/v2/login', APIviews.login_page, name='login+token'),
    path('api/v2/logout', APIviews.logoutUser, name='logout'),
    path('api/v2/tweet', APIviews.tweet, name='tweet+token'),

    # url(r'^$', views.home, name='home'),
    # url(r'^login/$', auth_views.LogoutView.as_view(), name='login'),
    # url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),  # <--
    # url(r'^admin/', admin.site.urls),
]
