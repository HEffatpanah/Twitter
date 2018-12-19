from django import forms
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from authAPI.forms import ProfileForm, LoginForm, UserForm, TweetForm
from authAPI.models import *


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
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return HttpResponse('false')
    else:
        form = LoginForm()
        return render(request, 'authAPI/login.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        employee = Profile.objects.get(username=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            form.fields['password'].widget = forms.HiddenInput()
        # Employee.objects.filter(username=user).update()
        # user.refresh_from_db()
        # form = ProfileForm(instance=user)
        tweet = TweetForm(request.POST, request.FILES)
        if tweet.is_valid():
            t = tweet.save(commit=False)
            t.user = Profile.objects.get(username=request.user)
            t.save()

    user = request.user
    user = Profile.objects.get(username=user)
    form = ProfileForm(instance=user)
    form.fields['password'].widget = forms.HiddenInput()
    tweet = TweetForm()
    return render(request, 'authAPI/profilepage.html', {'form': form, 'tweet': tweet})
