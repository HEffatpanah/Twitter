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
from apps.authAPI.models import *


def signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('index')
    else:
        form = ProfileForm()
        form.fields['avatar'].widget = forms.HiddenInput()

    return render(request, 'authAPI/signup.html', {'form': form})


def mainPage(request):
    return render(request, 'authAPI/mainPage.html')


def tweets(request):
    tweet = Tweet.objects.all()

    return render(request, 'authAPI/tweets.html', {'tweets': tweet})


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            token = Token.objects.get_or_create(user=user)  # ---------------------< here
            print(token[0].key, '\n\n\n\n\n')  # ------------------------------< here
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'authAPI/login.html', {'form': form, 'auth': False})
    else:

        return render(request, 'authAPI/login.html', {'form': form, 'auth': True})


def profile(request):
    user = request.user
    if request.method == 'POST':
        employee = Profile.objects.get(username=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=employee)
        print('fuck img django\n', form.instance.avatar.name)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token 5b009eb4691fee9787442273b2a72e9d74299ecb'}
        r = requests.get(url='http://localhost:8000/authAPI/api/sampleapi', headers=headers)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return redirect("profile")
        # Employee.objects.filter(username=user).update()
        # user.refresh_from_db()
        # form = ProfileForm(instance=user)

        tweet = TweetForm(request.POST, request.FILES)
        if tweet.is_valid():
            t = tweet.save(commit=False)
            t.user = Profile.objects.get(username=request.user)
            t.save()
            return redirect("profile")
    persons_tweet = Tweet.objects.filter(user=user)
    user = Profile.objects.get(username=user)
    form = ProfileForm(instance=user)
    form.fields['password'].widget = forms.HiddenInput()
    form.fields['username'].widget = forms.HiddenInput()
    form.fields['first_name'].widget = forms.HiddenInput()
    form.fields['last_name'].widget = forms.HiddenInput()
    form.fields['email'].widget = forms.HiddenInput()
    tweet = TweetForm()
    return render(request, 'authAPI/profilepage.html', {'form': form, 'tweet': tweet, 'personsTweet': persons_tweet})


def logoutUser(request):
    logout(request)
    print('hello\n\n\n\n ')
    return redirect('home')
