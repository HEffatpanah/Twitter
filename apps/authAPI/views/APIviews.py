import requests
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
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
    authenticated = request.user.is_authenticated
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    ip = IP.objects.filter(ip=ip_address).first()
    if ip is None:
        ip = IP.objects.create(ip=ip_address, number_of_unAuthenticated=0 if authenticated else 1,
                               number_of_sequential_requests=1)
    if not authenticated:
        ip.number_of_unAuthenticated += 1
    if authenticated:
        ip.number_of_unAuthenticated = 0
    ip.save()
    if ip.number_of_unAuthenticated >= 18:
        return Response('‫‪Request‬‬ ‫‪Blocked‬‬')
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


@permission_classes((IsAuthenticated,))
def generate_token(request):
    user = Profile.objects.get(username=request.user)
    if request.method == 'POST':
        Token.objects.filter(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)
        return render(request, 'authAPI/profilePage+token.html', {'token': token})
    else:
        token, _ = Token.objects.get_or_create(user=user)
        return render(request, 'authAPI/profilePage+token.html', {'token': token})
