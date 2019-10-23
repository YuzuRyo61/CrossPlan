from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from CrossPlan.tasks import APSend

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Undo import RenderUndo
from fediverse.views.renderer.activity.Follow import RenderFollow

from fediverse.models import Follow

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
