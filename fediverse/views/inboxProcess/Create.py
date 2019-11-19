import logging

from dateutil.parser import parse

from django.http.response import HttpResponse
from django.db.utils import IntegrityError

from CrossPlan.tasks import APSend

from fediverse.models import Post

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject

def _CreateActivity(body, fromUserObj):
    if Post.objects.filter(fediID=body["object"]["id"]).count() == 0: # pylint: disable=no-member
        newPost = Post(
            fediID=body["object"]["id"],
            body=body["object"]["content"],
            parentFedi=fromUserObj,
            posted=parse(body["object"]["published"])
        )
        newPost.save()
    else:
        logging.warn("This post is already created. Skipping.")
    return HttpResponse(status=202)
