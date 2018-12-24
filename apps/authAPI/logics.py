import datetime

from django.contrib.sessions.models import Session
from django.utils import timezone

from apps.authAPI.models import Profile, UserRequest


def IDS(f):
    def attack_check(*args):
        x_forwarded_for = args[0].META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = args[0].META.get('REMOTE_ADDR')
        browser = args[0].user_agent.browser.family
        current_time = timezone.now()
        authenticated = args[0].user.is_authenticated
        user_request = UserRequest.objects.get(ip=ip)
        h = 10
        n = 2
        if current_time.timestamp() - user_request.time.timestamp() < h:
            user_request.number_of_sequential_requests += 1
        elif current_time.timestamp() - user_request.time.timestamp() >= h:
            user_request.number_of_sequential_requests = 0
        if not authenticated:
            user_request.number_of_unAuthenticated += 1
        if authenticated:
            user_request.number_of_unAuthenticated = 0
        user_request.time = current_time
        user_request.save()
        if user_request.number_of_sequential_requests > n or user_request.number_of_unAuthenticated >= n and user_request.browser == browser:
            print("Attack!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        user_request.browser = browser
        return f(*args)

    return attack_check


class OnlyOneUserMiddleware(object):
    def process_request(self, request):
        p = Profile.objects.get(username=request.user)
        cur_session_key = p.session_key
        print("sess  ", cur_session_key)
        print("sess2  ", request.session.session_key)
        if cur_session_key and cur_session_key != request.session.session_key:
            try:
                Session.objects.get(session_key=cur_session_key).delete()
            except:
                pass
        p.session_key = request.session.session_key
        p.save()

    def clearSession(self, request):
        print(Session.objects.all())
        p = Profile.objects.get(username=request.user)
        p.session_key = None
        p.save()
        # Session.objects.all().delete()
