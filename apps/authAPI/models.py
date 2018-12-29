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


class IP(models.Model):
    ip = models.CharField(max_length=20)
    number_of_sequential_requests = models.IntegerField(default=0)
    number_of_unAuthenticated = models.IntegerField(default=0)


class Request(models.Model):
    ipInfo = models.ForeignKey(IP, on_delete=models.CASCADE)
    browser = models.CharField(max_length=100, default=' ')
    time = models.DateTimeField(default=timezone.now)


class IDSvar(models.Model):
    h = models.IntegerField()
    n = models.IntegerField()

class UserRquests(models.Model):
    username = models.CharField(max_length=100, default=' ')
    number_of_requests = models.IntegerField(default=0)
