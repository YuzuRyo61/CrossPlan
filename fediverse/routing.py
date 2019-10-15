from django.urls import path
from . import consumers

# to-do: https://qiita.com/massa142/items/cbd508efe0c45b618b34 https://poyo.hatenablog.jp/entry/2018/05/17/233000

websocket_urlpatterns = [
    path('streaming/<slug:stream_name>', consumers.TimelineConsumer, name="Streaming-Local")
]
