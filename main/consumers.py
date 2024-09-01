import json
from channels.generic.websocket import WebsocketConsumer

class CommentsConsumer(WebsocketConsumer):
    async def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'Connection_established',
            'message': 'Welcome to the world'
        }))