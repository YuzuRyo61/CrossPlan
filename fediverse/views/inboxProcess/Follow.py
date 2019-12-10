import json

from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from CrossPlan.tasks import APSend

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Undo import RenderUndo
from fediverse.views.renderer.activity.Follow import RenderFollow

from fediverse.models import Follow

def _FollowActivity(body, fromUserObj, targetObj, undo=False):
    if not undo:
        if not Follow.objects.filter(target=targetObj, fromFediUser=fromUserObj).count() != 0: # pylint: disable=no-member
            newFollow = Follow(
                target=targetObj,
                fromFediUser=fromUserObj,
                is_pending=targetObj.is_manualFollow
            )
            if targetObj.is_manualFollow:
                newFollow.pendingObj = json.dumps(body)
            newFollow.save()
        
        if targetObj.is_manualFollow == False:
            APSend.delay(
                fromUserObj.Inbox,
                targetObj.username,
                RenderAccept(
                    targetObj.username,
                    body
                )
            )

        return HttpResponse(status=202)
    else:
        try:
            unFollow = Follow.objects.get(target=targetObj, fromFediUser=fromUserObj) # pylint: disable=no-member
            unFollow.delete()
        except ObjectDoesNotExist:
            pass
        APSend.delay(
            fromUserObj.Inbox,
            targetObj.username,
            RenderUndo(
                targetObj.username,
                body["object"]
            )
        )
        return HttpResponse(status=202)
