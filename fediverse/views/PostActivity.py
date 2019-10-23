from django.shortcuts import get_object_or_404

from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.activity.Create import RenderCreate
from fediverse.views.renderer.object.Note import RenderNote

from fediverse.models import Post

def PostActivity(request, uuid):
    postObj = get_object_or_404(Post, uuid=uuid)
    return APResponse(APRender(RenderCreate(
        postObj.uuid,
        postObj.parent.username,
        RenderNote(
            postObj.uuid,
            postObj.posted.isoformat(),
            postObj.parent.username,
            postObj.body,
            ["https://www.w3.org/ns/activitystreams#Public"],
            [f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:Followers', kwargs={'username': postObj.parent.username})}"]
        )
    )))
