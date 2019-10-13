from django.shortcuts import get_object_or_404

from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.head import APRender

from fediverse.models import User

def InboxUser(request, username):
    target = get_object_or_404(User, username__iexact=username)
    

def InboxPublic(request):
    pass
