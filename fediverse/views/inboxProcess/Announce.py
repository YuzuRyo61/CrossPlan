import re
from urllib.parse import urlparse
from dateutil.parser import parse

from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
from django.urls import reverse

from fediverse.lib import newPostFromObj
from fediverse.models import Post

from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject

def _AnnounceActivity(body, fromUserObj, targetObj, undo=False):
    if not undo:
        try:
            if urlparse(body["object"]).netloc == settings.CP_ENDPOINT:
                uuidRaw = re.match(reverse("PostDetail", kwargs={"uuid": "(.+)"}), body["object"])
                if uuidRaw == None:
                    raise ValueError("URL parse error.")
                announceObj = Post.objects.get(uuid=uuidRaw.group(1)) # pylint: disable=no-member
            else:
                announceObj = Post.objects.get(fediID=body["object"]) # pylint: disable=no-member
        except ObjectDoesNotExist:
            announceObj = newPostFromObj(body["object"])
            if announceObj == False:
                raise ValueError("Object fetch error.")
            announceObj.save()
        except MultipleObjectsReturned:
            return HttpResponse(status=202)
        
        newAnnounce = Post(
            fediID=body["object"],
            parentFedi=fromUserObj,
            announceTo=announceObj,
            posted=parse(body["published"])
        )
        newAnnounce.save()
        return HttpResponse(status=202)
    else:
        pass
