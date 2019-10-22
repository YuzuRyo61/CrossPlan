from datetime import datetime

from Crypto.PublicKey import RSA
from Crypto import Random

from requests_http_signature import HTTPSignatureAuth

from httpsig import HeaderSigner

from django.conf import settings
from django.urls import reverse

from fediverse import models

def generate_key():
    rsa = RSA.generate(4096, Random.new().read)
    return (rsa.exportKey().decode('utf-8'), rsa.publickey().exportKey().decode('utf-8'))

def sign_header(username):
    userInfo = models.User.objects.get(username__iexact=username)
    return HTTPSignatureAuth(
        algorithm="rsa-sha256",
        key=userInfo.privateKey,
        key_id=f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:publicKey', kwargs={'username': username})}"
    )

def addDefaultHeader(header={}):
    header.update({
        "User-Agent": f"CrossPlan/0.0.0 (https://{settings.CP_ENDPOINT}/)",
        "Content-Type": "application/activity+json"
    })
    return header
