import datetime

from django.contrib.sessions.models import Session

from apps.authAPI.models import Profile


def IDS(f):
    def attack_check(*args):
        x_forwarded_for = args[0].META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = args[0].META.get('REMOTE_ADDR')
        browser = args[0].user_agent.browser.family
        current_time = datetime.datetime.now()
        print(ip, browser, current_time, args[0].user.is_authenticated)
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
