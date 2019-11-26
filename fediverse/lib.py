import json
from datetime import datetime
from json.decoder import JSONDecodeError
from dateutil.parser import parse
import logging

from Crypto.PublicKey import RSA
from Crypto import Random

import requests

from urllib.parse import urlparse

from requests_http_signature import HTTPSignatureHeaderAuth

from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

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

def parse_signature(signature_header):
    return {i.split("=", 1)[0]: i.split("=", 1)[1].strip('"') for i in signature_header.split(",")}

def addDefaultHeader(header={}, isGETMethod=False):
    header.update({
        "User-Agent": f"CrossPlan/{str(settings.CP_VERSION)} (https://{settings.CP_ENDPOINT}/)",
    })
    if isGETMethod:
        header.update({
            "Accept": "application/activity+json"
        })
    else:
        header.update({
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
        resRaw = requests.get(
            uri,
            headers=addDefaultHeader(isGETMethod=True)
        )
        resRaw.raise_for_status()
        res = resRaw.json()
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
        
        if res.get("sharedInbox") == None:
            if res.get("endpoints") != None and res["endpoints"].get("sharedInbox") != None:
                sharedInbox = res["endpoints"].get("sharedInbox")
            else:
                sharedInbox = None
        else:
            sharedInbox = res["sharedInbox"]

        return models.FediverseUser(
            username=res["preferredUsername"],
            display_name=res.get("name"),
            description=res.get("summary"),
            Host=host,
            Inbox=res["inbox"],
            Outbox=res.get("outbox"),
            SharedInbox=sharedInbox,
            Featured=res.get("featured"),
            Followers=res.get("followers"),
            Following=res.get("following"),
            Uri=res["id"],
            Url=res.get("url"),
            publicKey=publicKey,
            keyId=keyId,
            is_manualFollow=res.get("manuallyApprovesFollowers", False)
        )

def newPostFromObj(objUrl):
    res = requests.get(
        objUrl,
        headers=addDefaultHeader(isGETMethod=True)
    )
    res.raise_for_status()
    try:
        resJ = res.json()
    except json.decoder.JSONDecodeError:
        logging.warning("Json decode ERROR. Abort fetch post object.")
        return False

    if not isAPContext(resJ):
        return False
    
    if not resJ.get("type") in ["Note", "Question"]:
        logging.warning("This url is not Note Type. Abort.")
        return False

    try:
        parentUser = models.FediverseUser.objects.get(Uri=resJ["attributedTo"]) # pylint: disable=no-member
    except ObjectDoesNotExist:
        parentUser = registerFediUser(resJ["attributedTo"])
        if parentUser == False:
            return False
        parentUser.save()

    newPost = models.Post(
        fediID=resJ["id"],
        body=resJ["content"],
        parentFedi=parentUser,
        posted=parse(resJ["published"])
    )

    return newPost
