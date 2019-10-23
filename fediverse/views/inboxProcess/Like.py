from django.http.response import HttpResponse

from fediverse.views.renderer.activity.Accept import RenderAccept
from fediverse.views.renderer.activity.Reject import RenderReject
from fediverse.views.renderer.activity.Undo import RenderUndo
from fediverse.views.renderer.activity.Like import RenderLike

def _LikeActivity(body, fromUserObj, targetObj, undo=False):
    pass
