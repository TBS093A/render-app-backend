from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json

class RenderConsumer(WebsocketConsumer):

    def connect(self):
        """
        connect to rendering zone
        """
        self.render_name = self.scope['url_route']['kwargs']['render_name']
        self.render_model = self.scope['url_route']['kwargs']['render_model']
        self.render_group = f'render_{self.render_name}_{self.render_model}'

        # save render object

        async_to_sync(self.chennel_layer.group_add)(
            self.render_group,
            self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code):
        """
        disconnect from rendering zone
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.render_group,
            self.channel_name
        )

    def receive(self, command):
        """
        start rendering a every sets / single set (hand sign letter) / single image 
        
        every sets - `angle` - all hand sign positions

        single set - `letter_id` + `angle`

        single image - `letter_id` + `angle` + `camera_id`

        (default `angle` is 12)
        """
        
        # render start. Async send percentage progress 

        command_json = json.loads(command)

        render_single_image = command_json['command'] == 'single_image'
        render_customize_set = command_json['command'] == 'customize_set'
        render_set = command_json['command'] == 'set'

        if render_single_image:
            self.render_single_image(command_json)
        elif render_customize_set:
            self.render_customize_set(command_json)
        elif render_set:
            self.render_set(command_json)
        

    def render_single_image(self, command):
        """
        one hand sign image [ `set_id` + `angle` + `(width, height)` ]
        """
        pass

    def render_customize_set(self, command):
        """
        one hand sign [ `set_id` + `step` + `angle` + `(width, height)` ] 
        
        or [ `list: [ step_id ]` + `step` + `angle` + `(width, height)` ]
        """
        pass

    def render_set(self, command):
        """
        general render (all hand signs) [ `angle` + `(width, height)` ]
        """
        pass