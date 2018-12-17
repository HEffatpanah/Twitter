from django.contrib.auth.models import User
from django.db import models


class Employee(User):
    mobile = models.CharField(max_length=100)

    # def create_user(self, mobile, username, email, password, first_name, last_name):
    #     self.objects.create_user(username=username,
    #                              email=email,
    #                              password=password,
    #                              first_name=first_name,
    #                              last_name=last_name
    #                              )
    #     self.mobile = mobile
