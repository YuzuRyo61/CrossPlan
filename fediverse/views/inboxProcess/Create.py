from dateutil.parser import parse

from django.http.response import HttpResponse

from CrossPlan.tasks import APSend

from fediverse.models import Post

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject

def _CreateActivity(body, fromUserObj):
    newPost = Post(
        fediID=body["object"]["id"],
        body=body["object"]["content"],
        parentFedi=fromUserObj,
        posted=parse(body["object"]["published"])
    )
    newPost.save()
    return HttpResponse(status=202)
