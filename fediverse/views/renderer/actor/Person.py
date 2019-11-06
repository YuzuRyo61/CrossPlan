import os

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.urls import reverse

from fediverse.models import User
from fediverse.views.renderer.object.Key import RenderKey

def RenderUser(username):
    target = get_object_or_404(User, username__iexact=username)

    return {
        "type": "Service" if target.is_bot else "Person",
        "id": f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': target.username})}",
        "name": target.display_name if target.display_name != '' else None,
        "preferredUsername": target.username,
        "summary": target.description,
        "inbox": f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:Inbox', kwargs={'username': target.username})}",
        "outbox": f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:Outbox', kwargs={'username': target.username})}",
        "following": f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:Following', kwargs={'username': target.username})}",
        "followers": f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:Followers', kwargs={'username': target.username})}",
        "url": f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': target.username})}",
        "manuallyApprovesFollowers": target.is_manualFollow,
        "publicKey": RenderKey(target.username, False)
    }
