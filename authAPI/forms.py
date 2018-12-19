from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from authAPI.models import Profile, Tweet


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
        fields = ('tweet_text',)
