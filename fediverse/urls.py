from django.urls import path

from fediverse.views.publickey import Key
from fediverse.views.Inbox import InboxUser, InboxPublic
from fediverse.views.Outbox import Outbox
from fediverse.views.PostActivity import PostActivity
from fediverse.views.Followers import Followers

app_name = "Fediverse"

urlpatterns = [
    path('inbox', InboxPublic, name="InboxPublic"),
    path('post/<uuid>/activity', PostActivity, name="PostActivity"),
    path('user/<username>/publickey', Key, name="publicKey"),
    path('user/<username>/inbox', InboxUser, name="Inbox"),
    path('user/<username>/outbox', Outbox, name="Outbox"),
    path('user/<username>/followers', Followers, name="Followers"),
]
