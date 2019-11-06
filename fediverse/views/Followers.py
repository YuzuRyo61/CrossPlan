from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.http.response import HttpResponseGone

from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.object.OrderedCollection import RenderOrderedCollection
from fediverse.views.renderer.object.OrderedCollectionPage import RenderOrderedCollectionPage

from fediverse.models import User

def Followers(request, username):
    target = get_object_or_404(User, username__iexact=username)
    if target.is_active == False:
        return HttpResponseGone()
    followers = target.followers.filter(is_pending=False)
    if "page" in request.GET:
        offset = int(request.GET.get("offset", 1))
        if offset <= 0:
            offset = 1
        pagenated = followers[settings.USER_PER_PAGE * (offset - 1):settings.USER_PER_PAGE * offset]
        output = []
        for follower in pagenated:
            if follower.fromUser != None:
                output.append(f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': follower.fromUser.username})}")
            elif follower.fromFediUser != None:
                output.append(follower.fromFediUser.Uri)

        return APResponse(APRender(
            RenderOrderedCollectionPage(
                str(request.get_full_path()),
                reverse('Fediverse:Followers', kwargs={"username": target.username}),
                followers.count(),
                output,
                "".join([reverse('Fediverse:Followers', kwargs={"username": target.username}), '?', urlencode({'page': 'true', 'offset': offset + 1})]) if (followers.count() - settings.USER_PER_PAGE * offset) > 0 else None,
                "".join([reverse('Fediverse:Followers', kwargs={"username": target.username}), '?', urlencode({'page': 'true', 'offset': offset - 1})]) if (offset - 1) > 0 else None,
            )
        ))
    else:
        return APResponse(APRender(
            RenderOrderedCollection(
                reverse('Fediverse:Followers', kwargs={"username": target.username}),
                followers.count(),
                "".join([reverse('Fediverse:Followers', kwargs={"username": target.username}), '?', urlencode({'page': 'true'})])
            )
        ))
