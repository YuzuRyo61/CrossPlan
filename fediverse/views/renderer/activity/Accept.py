from django.conf import settings
from django.urls import reverse

from fediverse.models import User

def RenderAccept(actor, obj):
    target = User.objects.get(username__iexact=actor)
    return {
        "type": "Accept",
        "actor": f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': target.username})}",
        "object": obj
    }
