from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.object.Key import RenderKey

def Key(request, username):
    return APResponse(APRender(RenderKey(username)))
