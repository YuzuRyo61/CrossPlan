import logging
import re
from urllib.parse import urlparse

from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.urls import reverse

from fediverse.models import Like, Post

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject
from fediverse.views.renderer.activity.Undo import RenderUndo
from fediverse.views.renderer.activity.Like import RenderLike

def _LikeActivity(body, fromUserObj, targetObj, undo=False):
    if not undo:
        logging.info("Do like")
        uuidRaw = re.match(f"^https://{settings.CP_ENDPOINT}" + reverse("PostDetail", kwargs={"uuid": r"(.+)"}), body["object"])
        try:
            logging.debug("is exist post data")
            LikeTargetObj = Post.objects.get(uuid=uuidRaw.group(1)) # pylint: disable=no-member
        except ObjectDoesNotExist:
            logging.warn(f"Target post object was not found. Ignoring.: {uuidRaw.group(1)}")
            return HttpResponse(status=202)
        
        try:
            logging.debug("is exist like data")
            isExist = Like.objects.get(target=LikeTargetObj, fromFediUser=fromUserObj) # pylint: disable=no-member
        except ObjectDoesNotExist:
            logging.debug("create like data")            
            newLike = Like(
                target=LikeTargetObj,
                fromFediUser=fromUserObj
            )
            newLike.save()
            logging.info(f"Like saved: {str(newLike.uuid)}")
            return HttpResponse(status=202)
        else:
            logging.warn(f"It has already been liked. Ignoring.: {str(isExist.uuid)}")
            return HttpResponse(status=202)
    else:
        logging.info("Undo like")
        uuidRaw = re.match(f"^https://{settings.CP_ENDPOINT}" + reverse("PostDetail", kwargs={"uuid": r"(.+)"}), body["object"]["object"])
        try:
            logging.debug("is exist post data")
            LikeTargetObj = Post.objects.get(uuid=uuidRaw.group(1)) # pylint: disable=no-member
        except ObjectDoesNotExist:
            logging.warn(f"Target post object was not found. Ignoring.: {uuidRaw.group(1)}")
            return HttpResponse(status=202)

        try:
            logging.debug("is exist like data")
            existLike = Like.objects.get(target=LikeTargetObj, fromFediUser=fromUserObj) # pylint: disable=no-member
            logging.info(f"Like delete: {str(existLike.uuid)}")
            existLike.delete()
            return HttpResponse(status=202)
        except ObjectDoesNotExist:
            logging.warn("Not liked Ignore it.")
            return HttpResponse(status=202)
