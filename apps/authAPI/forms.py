from django import forms
from django.forms import ModelForm

from apps.authAPI.models import *


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)


class ProfileForm(UserForm):

    class Meta:
        model = Profile
        fields = UserForm.Meta.fields + ('mobile', 'avatar')
        widgets = {
            'avatar': forms.FileInput(),
        }
        help_texts = {
            'username': None
        }


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        help_texts = {
            'username': None
        }


class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ('tweet_title', 'tweet_text')
