import logging
import json
import re

from urllib.parse import urlparse

from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse, HttpResponseNotAllowed, HttpResponseGone, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.conf import settings

from CrossPlan.tasks import APSend

from fediverse.views.inboxProcess.Follow import _FollowActivity
from fediverse.views.inboxProcess.Like import _LikeActivity
from fediverse.views.inboxProcess.Create import _CreateActivity
from fediverse.views.inboxProcess.Announce import _AnnounceActivity
from fediverse.views.inboxProcess.DeletePost import _DeletePostActivity
from fediverse.views.inboxProcess.Block import _BlockActivity

from fediverse.views.renderer.activity.Reject import RenderReject

from fediverse.models import User, FediverseUser, Follow, BlackDomain

from fediverse.lib import registerFediUser, isAPContext, parse_signature

from pprint import pformat

# todo: sendable websocket

@csrf_exempt
def InboxUser(request, username):
    target = get_object_or_404(User, username__iexact=username)
    if target.is_active == False:
        return HttpResponseGone()
    
    if request.META.get('HTTP_SIGNATURE') == None:
        return HttpResponseNotFound()
    
    if request.META.get("CONTENT_TYPE").startswith("application/activity+json") or request.META.get("CONTENT_TYPE").startswith("application/ld+json"):
        pass
    else:
        return HttpResponseBadRequest()

    signature = parse_signature(request.META.get("HTTP_SIGNATURE"))
    host = urlparse(signature["keyId"])

    try:
        apbody = json.loads(request.body.decode('utf-8'))
        apbody.pop("@context")
    except json.JSONDecodeError:
        return HttpResponseBadRequest()

    if not isAPContext(apbody):
        return HttpResponseBadRequest()

    try:
        fromUser = FediverseUser.objects.get(Uri=apbody["actor"]) # pylint: disable=no-member
    except ObjectDoesNotExist:
        fromUser = registerFediUser(apbody["actor"])
        if fromUser == False:
            logging.warn("Fediverse user fetch failed.")
            return HttpResponseBadRequest()
        else:
            fromUser.save()
            
    if fromUser.is_suspended == True:
        logging.warn("This user is suspended in this server.")
        if apbody["type"] == "Follow":
            APSend.delay(
                fromUser.Inbox,
                target.username,
                RenderReject(
                    target.username,
                    apbody["object"]
                )
            )
        return HttpResponse(status=202)

    for bd in BlackDomain.objects.all(): # pylint: disable=no-member
        if host.netloc == bd.targetDomain:
            logging.warn(f"ActivityPub Received, but it is blacklisted domain: {host.netloc}")
            if apbody["type"] == "Follow":
                APSend.delay(
                    fromUser.Inbox,
                    target.username,
                    RenderReject(
                        target.username,
                        apbody["object"]
                    )
                )
            return HttpResponse(status=202)

    logging.info("ActivityPub Recieved: ")
    logging.info(pformat(apbody))

    if apbody.get("type") == None or type(apbody.get("type")) != str:
        return HttpResponseBadRequest()

    if apbody["type"] == "Follow":
        return _FollowActivity(apbody, fromUser, target)
    elif apbody["type"] == "Create":
        return _CreateActivity(apbody, fromUser)
    elif apbody["type"] == "Like":
        return _LikeActivity(apbody, fromUser, target)
    elif apbody["type"] == "Accept":
        if apbody["object"].get("type") == "Follow":
            res = re.search(f"^https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': '(.+)'})}#follow_(.+)", apbody["object"]["id"])
            if res == None:
                logging.error("Follow parse error.")
                return HttpResponse(status=202)
            uuid = res.group(2)
            try:
                followObj = Follow.objects.get(uuid=uuid) # pylint: disable=no-member
                followObj.is_pending = False
                followObj.save()
                logging.info("Follow was accepted")
                return HttpResponse(status=202)
            except ObjectDoesNotExist:
                logging.warn("Follow object was not found")
                return HttpResponse(status=202)
        else:
            logging.info("Accept activity recieved, but type work is unknown.")
        return HttpResponse(status=202)
    elif apbody["type"] == "Reject":
        if apbody["object"].get("type") == "Follow":
            res = re.search(f"^https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': '(.+)'})}#follow_(.+)", apbody["object"]["id"])
            if res == None:
                logging.error("Follow parse error.")
                return HttpResponse(status=202)
            uuid = res.group(2)
            try:
                followObj = Follow.objects.get(uuid=uuid) # pylint: disable=no-member
                followObj.delete()
                logging.info("Follow was rejected")
                return HttpResponse(status=202)
            except ObjectDoesNotExist:
                logging.warn("Follow object was not found")
                return HttpResponse(status=202)
        else:
            logging.info("Reject activity recieved, but type work is unknown.")
        return HttpResponse(status=202)
    elif apbody["type"] == "Announce":
        return _AnnounceActivity(apbody, fromUser, target)
    elif apbody["type"] == "Block":
        return _BlockActivity(apbody, fromUser, target)
    elif apbody["type"] == "Delete":
        if apbody["object"].get("type") == "Tombstone":
            return _DeletePostActivity(apbody, fromUser, target)
    elif apbody["type"] == "Undo":
        if apbody["object"]["type"] == "Follow":
            return _FollowActivity(apbody, fromUser, target, True)
        elif apbody["object"]["type"] == "Like":
            return _LikeActivity(apbody, fromUser, target, True)
        elif apbody["object"]["type"] == "Block":
            return _BlockActivity(apbody, fromUser, target, True)

    logging.error(f"Sorry, this type is not implemented!: {apbody['type']}")
    return HttpResponse(status=202)
    
    # to-do: Inbox methods

@csrf_exempt
def InboxPublic(request):
    if request.META.get('HTTP_SIGNATURE') == None:
        return HttpResponseNotFound()
    
    if request.META.get("CONTENT_TYPE").startswith("application/activity+json") or request.META.get("CONTENT_TYPE").startswith("application/ld+json"):
        pass
    else:
        return HttpResponseBadRequest()

    try:
        apbody = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest()

    if not isAPContext(apbody):
        return HttpResponseBadRequest()

    logging.info("ActivityPub Recieved: ")
    logging.info(pformat(apbody))
    
    return HttpResponse(status=501)
    
    # to-do: Inbox methods
