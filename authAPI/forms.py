from django import forms
from django.forms import ModelForm
from betterforms.multiform import MultiModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *


class profileForm(ModelForm):
    class Meta:
        model = User
        exclude = ('userName',)


class addUserMultiForm(MultiModelForm):
    form_classes = {
        'user': UserCreationForm,
        'profile': profileForm,
    }
