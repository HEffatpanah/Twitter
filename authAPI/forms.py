from django.contrib.auth.models import User
from django.forms import ModelForm

from authAPI.models import Employee


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)


class EmployeeForm(UserForm):
    class Meta:
        model = Employee
        fields = UserForm.Meta.fields + ('mobile',)
