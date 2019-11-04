import re
from urllib.parse import urlparse

from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.urls import reverse

from fediverse.models import Like

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject
from fediverse.views.renderer.activity.Undo import RenderUndo
from fediverse.views.renderer.activity.Like import RenderLike

def _LikeActivity(body, fromUserObj, targetObj, undo=False):
    if not undo:
        try:
            # existLike = Like.objects.get(target=, fromFediUser=fromUserObj)
            pass
        except ObjectDoesNotExist:
            pass
        else:
            pass
        finally:
            return HttpResponse(status=202)
    else:
        pass
