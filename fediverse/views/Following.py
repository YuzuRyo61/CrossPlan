from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode

from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.object.OrderedCollection import RenderOrderedCollection
from fediverse.views.renderer.object.OrderedCollectionPage import RenderOrderedCollectionPage

from fediverse.models import User

def Following(request, username):
    target = get_object_or_404(User, username__iexact=username)
    following = target.following.all()
    if "page" in request.GET:
        offset = int(request.GET.get("offset", 1))
        if offset <= 0:
            offset = 1
        pagenated = following[settings.USER_PER_PAGE * (offset - 1):settings.USER_PER_PAGE * offset]
        output = []
        for follow in pagenated:
            if follow.target != None:
                output.append(f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': follow.target.username})}")
            elif follow.targetFedi != None:
                output.append(follow.targetFedi.Uri)

        return APResponse(APRender(
            RenderOrderedCollectionPage(
                str(request.get_full_path()),
                reverse('Fediverse:Following', kwargs={"username": target.username}),
                following.count(),
                output,
                "".join([reverse('Fediverse:Following', kwargs={"username": target.username}), '?', urlencode({'page': 'true', 'offset': offset + 1})]) if (following.count() - settings.USER_PER_PAGE * offset) > 0 else None,
                "".join([reverse('Fediverse:Following', kwargs={"username": target.username}), '?', urlencode({'page': 'true', 'offset': offset - 1})]) if (offset - 1) > 0 else None,
            )
        ))
    else:
        return APResponse(APRender(
            RenderOrderedCollection(
                reverse('Fediverse:Following', kwargs={"username": target.username}),
                following.count(),
                "".join([reverse('Fediverse:Following', kwargs={"username": target.username}), '?', urlencode({'page': 'true'})])
            )
        ))
