from datetime import datetime

from Crypto.PublicKey import RSA
from Crypto import Random

from httpsig import HeaderSigner

from django.conf import settings
from django.urls import reverse

from fediverse import models

def generate_key():
    rsa = RSA.generate(4096, Random.new().read)
    return (rsa.exportKey().decode('utf-8'), rsa.publickey().exportKey().decode('utf-8'))

def sign_header(username):
    userInfo = models.User.objects.get(username__iexact=username)
    sign = HeaderSigner(
        f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': userInfo.username})}",
        bytes(userInfo.privateKey, "UTF-8"),
        algorithm="rsa-sha256"
    ).sign({"Date": datetime.now().isoformat()})
    auth = sign.pop("authorization")
    sign["Signature"] = auth[len("Signature "):] if auth.startswith("Signature ") else ''
    return sign

def get_header(username):
    sign = sign_header(username)
    sign.update({"Accept": "application/ld+json; profile=\"https://www.w3.org/ns/activitystreams\""})
    return sign
