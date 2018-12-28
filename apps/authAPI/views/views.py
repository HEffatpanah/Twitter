import requests
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.authAPI.forms import *
from apps.authAPI.logics import OnlyOneUserMiddleware, IDS
from apps.authAPI.models import *


@IDS
def signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('home')
    else:
        form = ProfileForm()
        form.fields['avatar'].widget = forms.HiddenInput()

    return render(request, 'authAPI/signup.html', {'form': form})


@IDS
def mainPage(request):
    return render(request, 'authAPI/mainPage.html')


@IDS
def tweets(request):
    tweet = Tweet.objects.all()

    return render(request, 'authAPI/tweets.html', {'tweets': tweet})


@IDS
def login_page(request):
    if request.user.is_authenticated:
        return render(request, 'authAPI/login.html', {'login': True})
    form = LoginForm()
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('login_success')
        else:
            return render(request, 'authAPI/login.html', {'form': form, 'login': False, 'auth': False})
    else:

        return render(request, 'authAPI/login.html', {'form': form, 'login': False, 'auth': True})


@login_required
def login_success(request):
    user = request.user
    print(user)
    prof = Profile.objects.filter(username=user)
    if prof.count() is 0:
        u = User.objects.get(username=user)
        p = Profile(user_ptr_id=u.pk)
        p.__dict__.update(u.__dict__)
        p.save()
    a = OnlyOneUserMiddleware()
    a.process_request(request)
    return redirect('profile')


@IDS
@login_required
def profile(request):
    user = request.user
    employee = Profile.objects.get(username=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=employee)
        print('fuck img django\n', form.instance.avatar.name)
        if form.is_valid():
            print('fuck img django\n', form.instance.avatar.name)
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
    form = ProfileForm(instance=employee)
    form.fields['password'].widget = forms.HiddenInput()
    form.fields['username'].widget = forms.HiddenInput()
    form.fields['first_name'].widget = forms.HiddenInput()
    form.fields['last_name'].widget = forms.HiddenInput()
    form.fields['email'].widget = forms.HiddenInput()
    tweet = TweetForm()
    return render(request, 'authAPI/profilepage.html', {'form': form, 'tweet': tweet, 'personsTweet': persons_tweet})


@IDS
def logoutUser(request):
    # a = OnlyOneUserMiddleware()
    # a.clearSession(request)
    logout(request)
    return redirect('home')


@login_required
def home(request):
    return render(request, 'authAPI/home.html')
