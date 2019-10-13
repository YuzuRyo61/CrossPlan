from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse

from fediverse.models import User

def RenderKey(username):
    target = get_object_or_404(User, username__iexact=username)
    return {
        "id": f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:publicKey', kwargs={'username': target.username})}",
        "type": "Key",
        "owner": f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': target.username})}",
        "publicKeyPem": target.publicKey
    }
