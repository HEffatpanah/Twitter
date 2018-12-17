from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from authAPI.forms import UserForm, EmployeeForm
from authAPI.models import *


# def signup(request):
#     return render(request, 'authAPI/signup.html')

def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmployeeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save();
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse(form['password'].value())

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EmployeeForm()

    return render(request, 'authAPI/signup.html', {'form': form})



def mainPage(request):
    return render(request, 'authAPI/mainPage.html')


def login(request):
    return render(request, 'authAPI/login.html')


def checkAuth(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    # if User.objects.filter(username=request.POST['username'], password=request.POST['username']).exists():
    if user is not None:
        return HttpResponse('true')
    else:
        return HttpResponse('false')
