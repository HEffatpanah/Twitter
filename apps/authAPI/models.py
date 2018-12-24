from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(User):
    mobile = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="images", null=True, blank=True,
                               default="images/user.png")
    session_key = models.CharField(max_length=1024, null=True, blank=True)


class Tweet(models.Model):
    tweet_title = models.CharField(max_length=50, default='no title')
    tweet_text = models.CharField(max_length=1024)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class UserRequest(models.Model):
    ip = models.CharField(max_length=20)
    browser = models.CharField(max_length=100, default=' ')
    time = models.DateTimeField(default=timezone.now)
    number_of_sequential_requests = models.IntegerField(default=0)
    number_of_unAuthenticated = models.IntegerField(default=0)


# class IDSvar(models.Model):
#     h = models.IntegerField()
#     n = models.IntegerField()
