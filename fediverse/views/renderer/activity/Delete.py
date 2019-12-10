from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings

from fediverse.models import User

def RenderDelete(actor, obj):
    target = get_object_or_404(User, username__iexact=actor)
    return {
        "type": "Delete",
        "actor": f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': target.username})}",
        "object": obj
    }
