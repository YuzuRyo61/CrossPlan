from django.urls import path
from . import consumers

# to-do: https://qiita.com/massa142/items/cbd508efe0c45b618b34

websocket_urlpatterns = [
    path('streaming', consumers.TimelineConsumer, name="Streaming-Local")
]
