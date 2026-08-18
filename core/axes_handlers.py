from django.http import HttpResponse

def lockout_response(request, credentials=None, *args, **kwargs):
    # Return empty response so Axes does NOT inject its own message
    return HttpResponse(status=204)