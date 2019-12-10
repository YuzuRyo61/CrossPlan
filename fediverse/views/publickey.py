from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseGone

from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.object.Key import RenderKey

from fediverse.models import User

def Key(request, username):
    if get_object_or_404(User, username__iexact=username).is_active == False:
        return HttpResponseGone()
    return APResponse(APRender(RenderKey(username)))
