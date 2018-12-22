from django.contrib.sessions.models import Session

from apps.authAPI.models import Profile


class OnlyOneUserMiddleware(object):
    def process_request(self, request):
        p = Profile.objects.get(username=request.user)
        cur_session_key = p.session_key
        if cur_session_key and cur_session_key != request.session.session_key:
            Session.objects.get(session_key=cur_session_key).delete()
        # the following can be optimized(do not save each time if value not changed)
        p.session_key = request.session.session_key
        p.save()
