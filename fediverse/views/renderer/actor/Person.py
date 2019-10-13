import os

from django.http.response import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from fediverse.models import User

def RenderUser(username):
    try:
        target = User.objects.get(username__iexact=username) # pylint: disable=no-member
    except ObjectDoesNotExist:
        raise Http404("Specified user was not Found")

    return {
        "type": "Service" if target.is_bot else "Person",
        "id": f"https://{settings.CP_ENDPOINT}/user/{target.username}",
        "name": target.display_name if target.display_name != '' else None,
        "preferredUsername": target.username,
        "summary": target.description,
        "inbox": f"https://{settings.CP_ENDPOINT}/AP/user/{target.username}/inbox",
        "outbox": f"https://{settings.CP_ENDPOINT}/AP/user/{target.username}/outbox",
        "following": f"https://{settings.CP_ENDPOINT}/AP/user/{target.username}/following",
        "followers": f"https://{settings.CP_ENDPOINT}/AP/user/{target.username}/followers",
        "url": f"https://{settings.CP_ENDPOINT}/user/{target.username}",
        "manuallyApprovesFollowers": False,
        "publicKey": {
            "id": f"https://{settings.CP_ENDPOINT}/AP/user/{target.username}/publickey",
            "type": "Key",
            "owner": f"https://{settings.CP_ENDPOINT}/user/{target.username}",
            "publicKeyPem": target.publicKey
        }
    }
