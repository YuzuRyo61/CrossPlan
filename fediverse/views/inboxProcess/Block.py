import logging

from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from CrossPlan.tasks import APSend

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Undo import RenderUndo
from fediverse.models import Block, Follow

def _BlockActivity(body, fromUser, target, undo=False):
    if not undo:
        if not Block.objects.filter(target=target, fromFediUser=fromUser).count() != 0: # pylint: disable=no-member
            logging.info(f"New block: {str(fromUser)} => {str(target)}")
            newBlock = Block(
                target=target,
                fromFediUser=fromUser
            )
            newBlock.save()
            if Follow.objects.filter(targetFedi=fromUser, fromUser=target).count() != 0: # pylint: disable=no-member
                Follow.objects.get(targetFedi=fromUser, fromUser=target).delete() # pylint: disable=no-member
        return HttpResponse(status=202)
    else:
        try:
            blockingObj = Block.objects.get(target=target, fromFediUser=fromUser) # pylint: disable=no-member
            logging.info(f"Unblock: {str(fromUser)} => {str(target)}")
            blockingObj.delete()
        except ObjectDoesNotExist:
            logging.warn("No blocking object.")

        APSend.delay(
            fromUser.Inbox,
            target.username,
            RenderUndo(
                target.username,
                body["object"]
            )
        )
        return HttpResponse(status=202)
