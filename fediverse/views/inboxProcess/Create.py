import datetime

from django.http.response import HttpResponse

from fediverse.models import Post

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject

def _CreateActivity(body, fromUserObj):
    newPost = Post(
        fediId=body["object"]["id"],
        body=body["object"]["content"],
        parentFedi=fromUserObj,
        posted=datetime.date.fromisoformat(body["object"]["published"])
    )
    newPost.save()
    return HttpResponse(status=202)
