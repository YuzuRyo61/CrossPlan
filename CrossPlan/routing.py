from channels.routing import ProtocolTypeRouter, ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from fediverse import routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})
