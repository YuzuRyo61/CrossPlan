from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode

from fediverse.views.renderer.response import APResponse
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.object.OrderedCollection import RenderOrderedCollection
from fediverse.views.renderer.object.OrderedCollectionPage import RenderOrderedCollectionPage

from fediverse.models import User

def Outbox(request, username):
    target = get_object_or_404(User, username__iexact=username)
    if "page" in request.GET:
        return APResponse(APRender(
            RenderOrderedCollectionPage(
                "".join([reverse('Fediverse:Outbox', kwargs={"username": target.username}), '?', urlencode({'page': 'true'})]),
                reverse('Fediverse:Outbox', kwargs={"username": target.username}),
                []
            )
        ))
    else:
        return APResponse(APRender(
            RenderOrderedCollection(
                reverse('Fediverse:Outbox', kwargs={"username": target.username}),
                0,
                "".join([reverse('Fediverse:Outbox', kwargs={"username": target.username}), '?', urlencode({'page': 'true'})])
            )
        ))
