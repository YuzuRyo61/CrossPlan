from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse

from fediverse.models import User

def RenderCreate(uuid, actor, obj):
    target = User.objects.get(username__iexact=actor)
    return {
        "id": f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:PostActivity', kwargs={'uuid': str(uuid)})}",
        "type": "Create",
        "actor": f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': target.username})}",
        "object": obj
    }
