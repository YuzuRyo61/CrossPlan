from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings

from fediverse.models import User

def RenderAnnounce(idReverse, actor, published, to, cc, obj):
    target = User.objects.get(username__iexact=actor)
    return {
        "id": f"https://{settings.CP_ENDPOINT}{idReverse}",
        "type": "Announce",
        "actor": f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': target.username})}",
        "published": published,
        "to": to,
        "cc": cc,
        "object": obj,
        "atomUri": f"https://{settings.CP_ENDPOINT}{idReverse}"
    }
