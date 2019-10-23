import json

from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse, HttpResponseNotAllowed, HttpResponseGone, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from CrossPlan.tasks import APSend

from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.activity.Undo import RenderUndo
from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Follow import RenderFollow

from fediverse.models import User, FediverseUser, Follow

from fediverse.lib import registerFediUser, isAPContext

from pprint import pprint as pp

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
    
    pp(apbody)

    if not isAPContext(apbody):
        return HttpResponseBadRequest()

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
    elif apbody["type"] == "Undo":
        if apbody["object"]["type"] == "Follow":
            return _FollowActivity(apbody, fromUser, target, True)

    return HttpResponse(status=501)
    
    # to-do: Inbox methods

@csrf_exempt
def InboxPublic(request):
    pass
    
    # to-do: Inbox methods

def _FollowActivity(body, fromUserObj, targetObj, undo=False):
    if not undo:
        if Follow.objects.filter(target=targetObj, fromFediUser=fromUserObj).count() != 0: # pylint: disable=no-member
            # to-do: reject
            pass
        else:
            newFollow = Follow(
                target=targetObj,
                fromFediUser=fromUserObj
            )
            newFollow.save()
            APSend.delay(
                fromUserObj.Inbox,
                targetObj.username,
                RenderAccept(
                    targetObj.username,
                    RenderFollow(
                        targetObj.username,
                        newFollow.uuid,
                        body["actor"],
                        body["object"]
                    )
                )
            )
        return HttpResponse(status=202)
    else:
        try:
            unFollow = Follow.objects.get(target=targetObj, fromFediUser=fromUserObj) # pylint: disable=no-member
        except ObjectDoesNotExist:
            APSend.delay(
                fromUserObj.Inbox,
                targetObj.username,
                RenderUndo(
                    targetObj.username,
                    RenderFollow(
                        targetObj.username,
                        "null",
                        body["actor"],
                        body["object"]
                    )
                )
            )
        else:
            APSend.delay(
                fromUserObj.Inbox,
                targetObj.username,
                RenderUndo(
                    targetObj.username,
                    RenderFollow(
                        targetObj.username,
                        unFollow.uuid,
                        body["actor"],
                        body["object"]
                    )
                )
            )
            unFollow.delete()
        return HttpResponse(status=202)
