from datetime import datetime
from json.decoder import JSONDecodeError

from Crypto.PublicKey import RSA
from Crypto import Random

import requests

from urllib.parse import urlparse

from requests_http_signature import HTTPSignatureHeaderAuth

from httpsig import HeaderSigner

from django.conf import settings
from django.urls import reverse

from fediverse import models

def generate_key():
    rsa = RSA.generate(4096, Random.new().read)
    return (rsa.exportKey().decode('utf-8'), rsa.publickey().exportKey().decode('utf-8'))

def sign_header(username):
    userInfo = models.User.objects.get(username__iexact=username)
    return HTTPSignatureHeaderAuth(
        algorithm="rsa-sha256",
        key=bytes(userInfo.privateKey, 'UTF-8'),
        headers=["(request-target)", "host", "date"],
        key_id=f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:publicKey', kwargs={'username': userInfo.username})}"
    )

def addDefaultHeader(header={}):
    header.update({
        "User-Agent": f"CrossPlan/0.0.0 (https://{settings.CP_ENDPOINT}/)",
        "Content-Type": "application/activity+json"
    })
    return header

def isAPContext(apbody):
    if apbody.get("@context") != None and type(apbody.get("@context")) == str:
        if apbody["@context"] == "https://www.w3.org/ns/activitystreams":
            pass
        else:
            return False
    elif apbody.get("@context") != None and type(apbody.get("@context")) == list:
        if "https://www.w3.org/ns/activitystreams" in apbody["@context"]:
            pass
        else:
            return False
    else:
        return False
    
    return True

def registerFediUser(uri):
    try:
        res = requests.get(
            uri,
            headers={"Accept": "application/activity+json"}
        ).json()
        host = urlparse(uri).netloc
        if host == '':
            return False
        
        if not isAPContext(res):
            return False
    except JSONDecodeError:
        return False
    else:
        if res.get("publicKey") != None:
            publicKey = res["publicKey"].get("publicKeyPem")
            keyId = res["publicKey"].get("id")
        else:
            keyId = None
            publicKey = None

        return models.FediverseUser(
            username=res["preferredUsername"],
            display_name=res.get("name"),
            description=res.get("summary"),
            Host=host,
            Inbox=res["inbox"],
            Outbox=res.get("outbox"),
            SharedInbox=res.get("sharedInbox"),
            Featured=res.get("featured"),
            Followers=res.get("followers"),
            Following=res.get("following"),
            Uri=res["id"],
            Url=res.get("url"),
            publicKey=publicKey,
            keyId=keyId
        )
