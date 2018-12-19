from django import forms
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from authAPI.forms import ProfileForm, LoginForm, UserForm
from authAPI.models import *


def signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

            return HttpResponse(form['password'].value())
    else:
        form = ProfileForm()
        # form.fields['avatar'].widget = forms.HiddenInput()

    return render(request, 'authAPI/signup.html', {'form': form})


def mainPage(request):
    return render(request, 'authAPI/mainPage.html')


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
        employee = Employee.objects.get(username=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
        # Employee.objects.filter(username=user).update()
        # user.refresh_from_db()
        # form = ProfileForm(instance=user)
        form.fields['password'].widget = forms.HiddenInput()
        return render(request, 'authAPI/profilepage.html', {'form': form})
    else:
        user = request.user
        user = Employee.objects.get(username=user)
        form = ProfileForm(instance=user)
        form.fields['password'].widget = forms.HiddenInput()
        return render(request, 'authAPI/profilepage.html', {'form': form})
