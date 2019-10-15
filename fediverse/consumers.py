import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class TimelineConsumer(WebsocketConsumer):
    def connect(self):
        self.tlMethod = self.scope['url_route']['kwargs']['stream_name']
        self.tlId = f"timeline_{self.tlMethod}"
        if self.tlMethod == "local" or self.tlMethod == "global" or self.tlMethod == "home":
            async_to_sync(self.channel_layer.group_add)(
                self.tlId,
                self.tlMethod
            )
            self.accept()
            return
        else:
            self.disconnect(1)
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.tlId,
            self.tlMethod
        )
