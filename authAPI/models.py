from django.contrib.auth.models import User
from django.db import models


class Employee(User):
    mobile = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="authAPI/media/images", default=None)
