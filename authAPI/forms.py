from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from authAPI.models import Employee


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)


class ProfileForm(UserForm):
    avatar = forms.ImageField()

    class Meta:
        model = Employee
        fields = UserForm.Meta.fields + ('mobile', 'avatar')


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        help_texts = {
            'username': None
        }
