import datetime

from django.contrib.sessions.models import Session
from django.utils import timezone

from apps.authAPI.models import Profile, Request, IP, IDSvar


def IDS(f):
    def attack_check(*args):
        h = 10
        n = 4
        x_forwarded_for = args[0].META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = args[0].META.get('REMOTE_ADDR')
        browser = args[0].user_agent.browser.family
        current_time = timezone.now()
        authenticated = args[0].user.is_authenticated
        conf = IDSvar.objects.last()
        if conf is None:
            IDSvar.objects.create(h=h, n=n)
        else:
            h = conf.h
            n = conf.n
        ip = IP.objects.filter(ip=ip_address).first()
        if ip is None:
            ip = IP.objects.create(ip=ip_address, number_of_unAuthenticated=0 if authenticated else 1,
                                   number_of_sequential_requests=1)
            Request.objects.create(ipInfo=ip, browser=browser,
                                   time=current_time)
            return f(*args)
        old_request = Request.objects.filter(ipInfo=ip).last()
        new_request = Request.objects.create(ipInfo=ip, browser=browser, time=current_time)
        if old_request is None:
            return f(*args)
        if current_time.timestamp() - old_request.time.timestamp() < h:
            ip.number_of_sequential_requests += 1
        elif current_time.timestamp() - old_request.time.timestamp() >= h:
            new_request.ipInfo.number_of_sequential_requests = 1
        if not authenticated:
            ip.number_of_unAuthenticated += 1
        if authenticated:
            ip.number_of_unAuthenticated = 0
        ip.save()
        if new_request.ipInfo.number_of_sequential_requests >= n or \
                ip.number_of_unAuthenticated >= n:
            print("Attack!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        new_request.browser = browser
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
