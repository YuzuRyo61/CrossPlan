import logging

from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from fediverse.models import Post

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject

def _DeletePostActivity(body, fromUserObj):
    try:
        deletePost = Post.objects.get(fediID=body['object']['id'], parentFedi=fromUserObj) # pylint: disable=no-member
    except ObjectDoesNotExist:
        logging.warn(f"Target FediID is not found: {body['object']['id']}")
    else:
        deletePost.delete()
    return HttpResponse(status=202)
