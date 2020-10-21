from channels.generic.websocket import AsyncWebsocketConsumer
import json


class RenderConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.params = self.scope['url_route']['kwargs']
        self.group_name = 'render'
        
        for param, value in self.params.items():
            self.group_name += f'_{param}{value}'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await elf.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json

    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             'type': 'renderProgress',
    #             'progress': percentage
    #         }
    #     )

    # async def renderProgress(self, event):
    #     message = event['message']

    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))