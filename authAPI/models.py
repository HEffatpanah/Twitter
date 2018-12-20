from django.contrib.auth.models import User
from django.db import models


class Profile(User):
    mobile = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="authAPI/static/images", null=True, blank=True,
                               default="authAPI/static/images/user.png")


class Tweet(models.Model):
    tweet_title = models.CharField(max_length=50, default='no title')
    tweet_text = models.CharField(max_length=1024)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
