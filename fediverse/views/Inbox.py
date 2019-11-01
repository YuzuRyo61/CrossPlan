import logging
import json

from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse, HttpResponseNotAllowed, HttpResponseGone, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from CrossPlan.tasks import APSend

from fediverse.views.inboxProcess.Follow import _FollowActivity
from fediverse.views.inboxProcess.Like import _LikeActivity
from fediverse.views.inboxProcess.Create import _CreateActivity
from fediverse.views.inboxProcess.DeletePost import _DeletePostActivity
from fediverse.views.inboxProcess.Block import _BlockActivity

from fediverse.models import User, FediverseUser, Follow

from fediverse.lib import registerFediUser, isAPContext

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

    try:
        apbody = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest()

    if not isAPContext(apbody):
        return HttpResponseBadRequest()

    logging.info("ActivityPub Recieved: ")
    logging.info(pformat(apbody))

    try:
        fromUser = FediverseUser.objects.get(Uri=apbody["actor"]) # pylint: disable=no-member
    except ObjectDoesNotExist:
        fromUser = registerFediUser(apbody["actor"])
        if fromUser == False:
            return HttpResponseBadRequest()
        else:
            fromUser.save()

    if apbody.get("type") == None or type(apbody.get("type")) != str:
        return HttpResponseBadRequest()

    if apbody["type"] == "Follow":
        return _FollowActivity(apbody, fromUser, target)
    elif apbody["type"] == "Create":
        return _CreateActivity(apbody, fromUser)
    elif apbody["type"] == "Like":
        return _LikeActivity(apbody, fromUser, target)
    elif apbody["type"] == "Accept":
        logging.info("Activity was accepted")
        return HttpResponse(status=202)
    elif apbody["type"] == "Block":
        return _BlockActivity(apbody, fromUser, target)
    elif apbody["type"] == "Delete":
        if apbody["object"].get("type") == "Tombstone":
            return _DeletePostActivity(apbody, fromUser)
    elif apbody["type"] == "Undo":
        if apbody["object"]["type"] == "Follow":
            return _FollowActivity(apbody, fromUser, target, True)

    return HttpResponse(status=501)
    
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
