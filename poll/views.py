from django.contrib.auth.models import User
from django.http import HttpResponse
from poll.models import *


def index(request):
    user = Employee()
    user.create_user("09000")
    user.save()
    v = User.objects.get(username='john3')
    s = v.employee.mobile
    print(s)
    return HttpResponse("Hello, world. You're at the polls index.")
