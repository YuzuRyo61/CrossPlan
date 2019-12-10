from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.http.response import HttpResponseGone

from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.activity.Create import RenderCreate
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.object.Note import RenderNote
from fediverse.views.renderer.object.OrderedCollection import RenderOrderedCollection
from fediverse.views.renderer.object.OrderedCollectionPage import RenderOrderedCollectionPage

from fediverse.models import User

def Outbox(request, username):
    target = get_object_or_404(User, username__iexact=username)
    if target.is_active == False:
        return HttpResponseGone()
    posts = target.posts.all()
    if "page" in request.GET:
        offset = int(request.GET.get("offset", 1))
        if offset <= 0:
            offset = 1
        pagenated = posts[settings.OBJECT_PER_PAGE * (offset - 1):settings.OBJECT_PER_PAGE * offset]
        output = []
        for post in pagenated:
            output.append(RenderCreate(
                post.uuid,
                post.parent.username,
                RenderNote(
                    post.uuid,
                    post.posted.isoformat(),
                    post.parent.username,
                    post.body,
                    ["https://www.w3.org/ns/activitystreams#Public"],
                    [f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:Followers', kwargs={'username': post.parent.username})}"]
                )
            ))
        return APResponse(APRender(
            RenderOrderedCollectionPage(
                str(request.get_full_path()),
                reverse('Fediverse:Outbox', kwargs={"username": target.username}),
                posts.count(),
                output,
                "".join([reverse('Fediverse:Outbox', kwargs={"username": target.username}), '?', urlencode({'page': 'true', 'offset': offset + 1})]) if (posts.count() - settings.OBJECT_PER_PAGE * offset) > 0 else None,
                "".join([reverse('Fediverse:Outbox', kwargs={"username": target.username}), '?', urlencode({'page': 'true', 'offset': offset - 1})]) if (offset - 1) > 0 else None,
            )
        ))
    else:
        return APResponse(APRender(
            RenderOrderedCollection(
                reverse('Fediverse:Outbox', kwargs={"username": target.username}),
                posts.count(),
                "".join([reverse('Fediverse:Outbox', kwargs={"username": target.username}), '?', urlencode({'page': 'true'})])
            )
        ))
