from dateutil.parser import parse

from django.http.response import HttpResponse

from CrossPlan.tasks import APSend

from fediverse.models import Post

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject

def _CreateActivity(body, fromUserObj, targetObj):
    newPost = Post(
        fediID=body["object"]["id"],
        body=body["object"]["content"],
        parentFedi=fromUserObj,
        posted=parse(body["object"]["published"])
    )
    newPost.save()

    APSend.delay(
        fromUserObj.inbox,
        targetObj.username,
        RenderAccept(
            targetObj.username,
            body
        )
    )

    return HttpResponse(status=202)
