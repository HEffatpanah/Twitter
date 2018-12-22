import requests
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.views import APIView

from apps.authAPI.forms import *
from apps.authAPI.logics import OnlyOneUserMiddleware
from apps.authAPI.models import *


@api_view(["POST"])
@permission_classes((AllowAny,))
def login_page(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is None:
        return Response({'token': 'boooogh you are you kidding me?'},
                        status=HTTP_404_NOT_FOUND)
    else:
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({'token': token.key},
                        status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def tweet(request):
    the_tweet = Tweet(user=Profile.objects.get(username=request.user), tweet_title=request.POST['tweet_title'],
                      tweet_text=request.POST['tweet_text'])
    the_tweet.save()
    return Response('ok')


def logoutUser(request):
    logout(request)
    print('hello\n\n\n\n ')
    return redirect('home')


def generate_token(request):
    user = Profile.objects.get(username=request.user)
    if request.method == 'POST':
        Token.objects.filter(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)
        return render(request, 'authAPI/profilePage+token.html', {'token': token})
    else:
        token, _ = Token.objects.get_or_create(user=user)
        return render(request, 'authAPI/profilePage+token.html', {'token': token})


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            a = OnlyOneUserMiddleware()
            a.process_request(request)
            return redirect('profile+token')
        else:
            return render(request, 'authAPI/login.html', {'form': form, 'auth': False})
    else:

        return render(request, 'authAPI/login.html', {'form': form, 'auth': True})

