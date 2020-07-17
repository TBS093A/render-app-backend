from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class RenderConsumer(WebsocketConsumer):

    def connect(self):
        """
        connect to rendering zone
        """
        self.render_name = self.scope['url_route']['kwargs']['render_name']
        self.render_model = self.scope['url_route']['kwargs']['render_model']
        self.render_group = f'render_{self.render_name}_{self.render_model}'

        

        pass

    def disconnect(self, close_code):
        """
        disconnect from rendering zone
        """
        pass

    def receive(self, progress):
        """
        get info (index) about render image
        
        where index is a `frame_id`/`image_id`/`camera_id`
        """
        pass

    def check_render(self, event):
        """
        send info about rendered image
        """
        pass