import logging
import traceback

from dateutil.parser import parse

from django.http.response import HttpResponse
from django.db import IntegrityError

from CrossPlan.tasks import APSend

from fediverse.models import Post

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject

def _CreateActivity(body, fromUserObj):
    try:
        newPost = Post(
            fediID=body["object"]["id"],
            body=body["object"]["content"],
            parentFedi=fromUserObj,
            posted=parse(body["object"]["published"])
        )
        newPost.save()
    except IntegrityError:
        logging.warn(f"This post is already created. Skipping.: {body['object']['id']}")
    except:
        logging.error("Create activity is raised error:")
        logging.error(traceback.format_stack())
    finally:
        return HttpResponse(status=202)
