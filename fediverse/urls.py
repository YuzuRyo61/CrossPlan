from django.urls import path

from fediverse.views.publickey import Key

app_name = "Fediverse"

urlpatterns = [
    path('user/<username>/publickey', Key, name="publicKey")
]
