from django import forms
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render

from authAPI.forms import EmployeeForm
from authAPI.models import *


# def signup(request):
#     return render(request, 'authAPI/signup.html')

def signup(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

            return HttpResponse(form['password'].value())
    else:
        form = EmployeeForm()
        # form.fields['avatar'].widget = forms.HiddenInput()

    return render(request, 'authAPI/signup.html', {'form': form})


def mainPage(request):
    return render(request, 'authAPI/mainPage.html')


def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            return HttpResponse('true')
        else:
            return HttpResponse('false')
    else:
        return render(request, 'authAPI/login.html')
