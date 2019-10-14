from datetime import datetime

from Crypto.PublicKey import RSA
from Crypto import Random

from httpsig import HeaderSigner

from django.conf import settings

from fediverse import models

def generate_key():
    rsa = RSA.generate(4096, Random.new().read)
    return (rsa.exportKey().decode('utf-8'), rsa.publickey().exportKey().decode('utf-8'))

def sign_header(username, method, path):
    userInfo = models.User.objects.get(username__iexact=username)
    sign = HeaderSigner(
        "https://" + settings.SB_ENDPOINT + "/AP/user/" + userInfo.username + "/publickey",
        bytes(userInfo.privateKey, "UTF-8"),
        algorithm="rsa-sha256",
        headers=["(request-target)", "host", "date"]
    ).sign({"Date": datetime.now().isoformat(), "Host": settings.SB_ENDPOINT}, method=method, path=path)
    auth = sign.pop("authorization")
    sign["Signature"] = auth[len("Signature "):] if auth.startswith("Signature ") else ''
    return sign
