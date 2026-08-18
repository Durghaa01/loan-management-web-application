from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect

IDLE_TIMEOUT = timedelta(minutes=30)

def idle_timeout_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            now = timezone.now()
            last = request.session.get("last_activity_ts")

            if last:
                try:
                    last_dt = timezone.datetime.fromisoformat(last)
                    if timezone.is_naive(last_dt):
                        last_dt = timezone.make_aware(last_dt)
                except Exception:
                    last_dt = now

                if now - last_dt > IDLE_TIMEOUT:
                    logout(request)
                    request.session.flush()
                    return redirect("/login/")

            request.session["last_activity_ts"] = now.isoformat()

        return get_response(request)

    return middleware