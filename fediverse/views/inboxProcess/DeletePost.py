import logging

from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from CrossPlan.tasks import APSend

from fediverse.models import Post

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject

def _DeletePostActivity(body, fromUserObj, targetObj):
    try:
        deletePost = Post.objects.get(fediID=body['object']['id'], parentFedi=fromUserObj) # pylint: disable=no-member
    except ObjectDoesNotExist:
        logging.warn(f"Target FediID is not found: {body['object']['id']}")
    else:
        deletePost.delete()
    finally:
        APSend.delay(
            fromUserObj.inbox,
            targetObj.username,
            RenderAccept(
                targetObj.username,
                body
            )
        )
    return HttpResponse(status=202)
