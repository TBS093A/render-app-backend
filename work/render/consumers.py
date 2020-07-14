from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class RenderConsumer(WebsocketConsumer):

    def connect(self):
        pass

    def disconnect(self, close_code):
        pass

    def receive(self, progress):
        pass

    def check_render(self, event):
        pass