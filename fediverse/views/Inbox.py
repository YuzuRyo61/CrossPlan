from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse, HttpResponseNotAllowed, HttpResponseGone
from django.views.decorators.csrf import csrf_exempt

from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.head import APRender

from fediverse.models import User

# todo: sendable websocket

@csrf_exempt
def InboxUser(request, username):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    target = get_object_or_404(User, username__iexact=username)

    if target.is_active == False:
        return HttpResponseGone()
    
    # to-do: Inbox methods

@csrf_exempt
def InboxPublic(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")
    
    # to-do: Inbox methods
