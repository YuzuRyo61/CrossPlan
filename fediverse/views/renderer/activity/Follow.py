from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings

from fediverse.models import User

def RenderFollow(username, uuid, actor, obj):
    target = get_object_or_404(User, username__iexact=username)
    return {
        "type": "Follow",
        "actor": actor,
        "object": obj,
        "id": f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': target.username})}#follow_{str(uuid)}"
    }
