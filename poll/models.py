from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=100)

    def create_user(self, mobile):
        print("mamad")
        self.user = User.objects.create_user(username='john3',
                                             email='jlennon@beatles.com',
                                             password='glass onion',
                                             first_name='jigar',
                                             last_name='jila')
        self.mobile = mobile
