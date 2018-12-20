import requests
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from authAPI.forms import ProfileForm, LoginForm, UserForm, TweetForm
from authAPI.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


class HelloView(APIView):
    def get(self, request):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token 5b009eb4691fee9787442273b2a72e9d74299ecb'}
        content = {'message': 'Hello, World!'}
        return Response(content, headers=headers)


@csrf_exempt
@api_view(["GET"])
def sample_api(APIView):
    data = {'sample_data': 123}
    print('\n\nsalam\n\n')
    # return Response(data, status=HTTP_200_OK)
    content = {'message': 'Hello, World!'}
    return Response(content)


def test(requset):
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token 5b009eb4691fee9787442273b2a72e9d74299ecb'}
    r = requests.get('http://127.0.0.1:8000/authAPI/api/sampleapi', headers=headers)
    print('\n\nsalam\n\n', r, '\n\n')
    # response = HttpResponseRedirect('http://127.0.0.1:8000/authAPI/api/sampleapi')
    # return redirect('api/sampleapi', headers=headers)
    return HttpResponse('salam')


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def my_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


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
            # token = Token.objects.get_or_create(user=user)# ---------------------< here
            # print(token[0].key, '\n\n\n\n\n')#------------------------------< here
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

        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
        # Employee.objects.filter(username=user).update()
        # user.refresh_from_db()
        # form = ProfileForm(instance=user)

        tweet = TweetForm(request.POST, request.FILES)
        if tweet.is_valid():
            t = tweet.save(commit=False)
            t.user = Profile.objects.get(username=request.user)
            t.save()
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
