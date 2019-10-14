from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings

from fediverse.models import User

def RenderLike(username, uuid, actor, obj):
    target = get_object_or_404(User, username__iexact=username)
    return {
        "type": "Like",
        "actor": actor,
        "object": obj,
        "id": f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': target.username})}#like_{str(uuid)}"
    }
