from abc import ABC, abstractmethod
from channels.generic.websocket import AsyncWebsocketConsumer
import os
import json
import base64
import sys
import asyncio
from datetime import datetime

from work.settings import (
    RENDER_DIR
)

from .scripts.render import (
    RenderSingleImage,
    RenderSingleSet,
    RenderAllSets,

    RenderSingleImageByVector,
    RenderSingleSetByVector
)


class AbstractConsumer(AsyncWebsocketConsumer, ABC):

    schema = {
        'abstract': True
    }

    async def send_json(self, values: dict):
        await self.send( json.dumps( values ) ) 

    async def connect(self):
        self.params = self.scope['url_route']['kwargs']
        self.group_name = self.params['room_uuid'] # + '_' + str(datetime.now()).replace(' ','_').replace('.','_')
        
        # for param, value in self.params.items():
        #     self.group_name += f'_{param}{value}'
        
        self.channel_layer

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_json({ 'info': 'Ready to work. Get params' })

    @abstractmethod
    async def render(self):
        pass

    async def receive(self, **kwargs):
        self.params = json.loads(
            kwargs['text_data']
        )
        try:
            await self.send_json({ 'info': f'Render { self.group_name } Has Been Started!' }) 
            await self.render()
            await self.send_json({ 'info': f'Download Zip Named: { self.group_name } And Check Your Renders!' }) 
        except Exception as error:
            await self.send_json({ 'info': f'Render { self.group_name } Has Been Terminated!' })
            await self.send_json({ 'info': f'Bad Parameter! Type JSON like this: {json.dumps(self.schema)}' })
            await self.send_json({ 'error': str(error) })
            await self.send_json({ 'error': repr(error) })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    def get_render_image_base64(self, imageName: str):
        base64_image = b''
        with open(RENDER_DIR + '/' + self.group_name + '/' + imageName + '.png', 'rb') as image:
            base64_image = base64.b64encode(image.read())
        return base64_image.decode('utf-8')

    class Meta:
        abstract = True


# test:
# ws://localhost:9090/render/single/image/<room_uuid>
# {
#     "fileName": "testHand", 
#     "setID": 0, 
#     "rotate": 0.2, 
#     "nameSeries": 0, 
#     "cameraID": 1, 
#     "resolutionX": 1920, 
#     "resolutionY": 1080
# }

class RenderSingleImageConsumer(AbstractConsumer):

    schema = {
        'fileName': 'fileName',
        'setID': 0,
        'rotate': 0.0,
        'nameSeries': 0,
        'cameraID': 0,
        'resolutionX': 0,
        'resolutionY': 0
    }

    async def render(self):
        renderSingleImage = RenderSingleImage(
            self.params['fileName'] + '.blend'
        )
        renderSingleImage.render(
            int(self.params['setID']),
            float(self.params['rotate']),
            int(self.params['nameSeries']),
            int(self.params['cameraID']),
            resolution=(
                int(self.params['resolutionX']), 
                int(self.params['resolutionY'])
            )
        )
        await self.send_json(
            {
                'info': 'render success',
                'details': self.params,
                'group': self.group_name
            }
        )

# test:
# ws://localhost:9090/render/single/set/<room_uuid>
# {
#     "fileName": "testHand", 
#     "setID": 0,
#     "cameraID": 1, 
#     "resolutionX": 1920, 
#     "resolutionY": 1080,
#     "angle": 0.2
# }

class RenderSingleSetConsumer(AbstractConsumer):

    schema = {
        'fileName': 'fileName',
        'setID': 0,
        'cameraID': 0,
        'resolutionX': 0,
        'resolutionY': 0,
        'angle': 0.0
    }

    async def render(self):
        renderSingleSet = RenderSingleSet(
            self.params['fileName'] + '.blend'
        )
        for renderImage in renderSingleSet.render(
            int(self.params['setID']),
            int(self.params['cameraID']),
            resolution=(
                int(self.params['resolutionX']), 
                int(self.params['resolutionY'])
            ),
            angle=float(self.params['angle'])
        ):
            await asyncio.sleep(0.5)
            await self.send_json(
                {
                    'info': renderImage,
                    'details': self.params,
                    'group': self.group_name
                }
            )

# test
# ws://localhost:9090/render/all/<room_uuid>
# {
#     "fileName": "testHand",
#     "resolutionX": 1920, 
#     "resolutionY": 1080,
# }

class RenderAllConsumer(AbstractConsumer):

    schema = {
        'fileName': 'fileName',
        'resolutionX': 0,
        'resolutionY': 0
    }

    async def render(self):
        renderAllSets = RenderAllSets(
            self.params['fileName'] + '.blend'
        )
        for renderSet in renderAllSets.render(
            resolution=(
                int(self.params['resolutionX']), 
                int(self.params['resolutionY'])
            ),
            angle=float(self.params['angle'])
        ):
            await asyncio.sleep(0.5)
            await self.send_json(
                {
                    'info': renderSet,
                    'details': self.params,
                    'group': self.group_name
                }
            )
            

# test:
# ws://localhost:9090/render/vector/single/image/<room_uuid>
# {
#     "fileName": "testHand",
#     "rotate": 0.2, 
#     "nameSeries": 0, 
#     "cameraID": 1,
#     "vectors": {}, 
#     "resolutionX": 1920, 
#     "resolutionY": 1080
# }

class RenderSingleImageByVectorConsumer(AbstractConsumer):

    schema = {
        'fileName': 'fileName',
        'rotate': 0.0,
        'nameSeries': 0,
        'cameraID': 0,
        'vectors': {
            'IK_nadgarstek_R': {"scale": 0.0, "y": 0.0, "x": 0.0, "z": 0.0}, 
            'IK_joint3_R': {},
            'IK_maly_1_R': {},
            'IK_maly_2_R': {},
            'IK_maly_3_R': {},
            'IK_joint4_R': {}, 
            'IK_serdeczny_1_R': {}, 
            'IK_serdeczny_2_R': {}, 
            'IK_serdeczny_3_R': {}, 
            'IK_joint5_R': {}, 
            'IK_srodkowy_1_R': {}, 
            'IK_srodkowy_2_R': {}, 
            'IK_srodkowy_3_R': {}, 
            'IK_joint6_R': {}, 
            'IK_wskazujacy_1_R': {}, 
            'IK_wskazujacy_2_R': {}, 
            'IK_wskazujacy_3_R': {}, 
            'IK_kciuk_0_R': {},
            'IK_kciuk_1_R': {}, 
            'IK_kciuk_2_R': {}
        },
        'resolutionX': 0,
        'resolutionY': 0
    }

    async def render(self):
        renderSingleImage = RenderSingleImageByVector(
            self.params['fileName'] + '.blend'
        )
        date = str(datetime.now()).replace(' ','_')
        renderSingleImage.render(
            float(self.params['rotate']),
            int(self.params['nameSeries']),
            int(self.params['cameraID']),
            self.params['vectors'],
            date,
            resolution=(
                int(self.params['resolutionX']), 
                int(self.params['resolutionY'])
            ),
            renderDir=str(self.group_name)
        )
        await self.send_json(
            {
                'info': 'render success',
                'details': self.params,
                'group': self.group_name,
                'image': self.get_render_image_base64(f'set{0}_deg{ str(float(self.params["rotate"]) * 62) }_customizeVector{ date }_camera{ self.params["cameraID"] }_size{ self.params["resolutionX"] }x{ self.params["resolutionY"] }')
            }
        )

# test:
# ws://localhost:9090/render/vector/single/set/<room_uuid>
# {
#     "fileName": "testHand",
#     "cameraID": 1,
#     "vectors": {}, 
#     "resolutionX": 1920, 
#     "resolutionY": 1080,
#     "angle": 0.2
# }

class RenderSingleSetByVectorConsumer(AbstractConsumer):

    schema = {
        'fileName': 'fileName',
        'cameraID': 0,
        'vectors': {
            'IK_nadgarstek_R': {"scale": 0.0, "y": 0.0, "x": 0.0, "z": 0.0}, 
            'IK_joint3_R': {},
            'IK_maly_1_R': {},
            'IK_maly_2_R': {},
            'IK_maly_3_R': {},
            'IK_joint4_R': {}, 
            'IK_serdeczny_1_R': {}, 
            'IK_serdeczny_2_R': {}, 
            'IK_serdeczny_3_R': {}, 
            'IK_joint5_R': {}, 
            'IK_srodkowy_1_R': {}, 
            'IK_srodkowy_2_R': {}, 
            'IK_srodkowy_3_R': {}, 
            'IK_joint6_R': {}, 
            'IK_wskazujacy_1_R': {}, 
            'IK_wskazujacy_2_R': {}, 
            'IK_wskazujacy_3_R': {}, 
            'IK_kciuk_0_R': {},
            'IK_kciuk_1_R': {}, 
            'IK_kciuk_2_R': {}
        },
        'resolutionX': 0,
        'resolutionY': 0,
        'angle': 0.0
    }

    async def render(self):
        renderSingleSet = RenderSingleSetByVector(
            self.params['fileName'] + '.blend'
        )
        date = str(datetime.now()).replace(' ','_')
        for renderImage in renderSingleSet.render(
            int(self.params['cameraID']),
            self.params['vectors'],
            date,
            resolution=(
                int(self.params['resolutionX']), 
                int(self.params['resolutionY'])
            ),
            angle=float(self.params['angle']),
            generalDir=str(self.group_name)
        ):
            await asyncio.sleep(0.5)
            await self.send_json(
                {
                    'info': renderImage,
                    'details': self.params,
                    'group': self.group_name
                }
            )
            

# example vectors
# 
# General
#
# {
#     "IK_nadgarstek_R":      {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_joint3_R":          {"scale": float, "y": float, "x": float, "z": float},
#     "IK_maly_1_R":          {"scale": float, "y": float, "x": float, "z": float},
#     "IK_maly_2_R":          {"scale": float, "y": float, "x": float, "z": float},
#     "IK_maly_3_R":          {"scale": float, "y": float, "x": float, "z": float},
#     "IK_joint4_R":          {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_serdeczny_1_R":     {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_serdeczny_2_R":     {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_serdeczny_3_R":     {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_joint5_R":          {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_srodkowy_1_R":      {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_srodkowy_2_R":      {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_srodkowy_3_R":      {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_joint6_R":          {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_wskazujacy_1_R":    {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_wskazujacy_2_R":    {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_wskazujacy_3_R":    {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_kciuk_0_R":         {"scale": float, "y": float, "x": float, "z": float},
#     "IK_kciuk_1_R":         {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_kciuk_2_R":         {"scale": float, "y": float, "x": float, "z": float}
# }
#
# Without extremals
#
# {
#     "IK_maly_1_R":          {"scale": float, "y": float, "x": float, "z": float},
#     "IK_maly_2_R":          {"scale": float, "y": float, "x": float, "z": float},
#     "IK_maly_3_R":          {"scale": float, "y": float, "x": float, "z": float},
#  
#     "IK_serdeczny_1_R":     {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_serdeczny_2_R":     {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_serdeczny_3_R":     {"scale": float, "y": float, "x": float, "z": float}, 
#
#     "IK_srodkowy_1_R":      {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_srodkowy_2_R":      {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_srodkowy_3_R":      {"scale": float, "y": float, "x": float, "z": float}, 
#
#     "IK_wskazujacy_1_R":    {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_wskazujacy_2_R":    {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_wskazujacy_3_R":    {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_kciuk_0_R":         {"scale": float, "y": float, "x": float, "z": float},
#     "IK_kciuk_1_R":         {"scale": float, "y": float, "x": float, "z": float}, 
#     "IK_kciuk_2_R":         {"scale": float, "y": float, "x": float, "z": float}
# }
#
# With example values
#
# {
#     "IK_maly_1_R":          {"scale": 0.9, "y": 0.2, "x": 0.0, "z": 0.7},
#     "IK_maly_2_R":          {"scale": 0.9, "y": 0.0, "x": 0.0, "z": 0.0},
#     "IK_maly_3_R":          {"scale": 0.9, "y": 0.0, "x": 0.0, "z": 0.0},
 
#     "IK_serdeczny_1_R":     {"scale": 0.9, "y": 0.2, "x": 0.0, "z": 0.6},
#     "IK_serdeczny_2_R":     {"scale": 0.9, "y": 0.0, "x": 0.0, "z": 0.0}, 
#     "IK_serdeczny_3_R":     {"scale": 0.9, "y": 0.0, "x": 0.0, "z": 0.0}, 

#     "IK_srodkowy_1_R":      {"scale": 0.9, "y": 0.2, "x": 0.0, "z": 0.5},
#     "IK_srodkowy_2_R":      {"scale": 0.9, "y": 0.0, "x": 0.0, "z": 0.0}, 
#     "IK_srodkowy_3_R":      {"scale": 0.9, "y": 0.0, "x": 0.0, "z": 0.0},

#     "IK_wskazujacy_1_R":    {"scale": 0.9, "y": 0.2, "x": 0.0, "z": 0.4},
#     "IK_wskazujacy_2_R":    {"scale": 0.9, "y": 0.0, "x": 0.0, "z": 0.0},
#     "IK_wskazujacy_3_R":    {"scale": 0.9, "y": 0.0, "x": 0.0, "z": 0.0},

#     "IK_kciuk_0_R":         {"scale": 0.9, "y": 0.5, "x": 0.5, "z": 0.6},
#     "IK_kciuk_1_R":         {"scale": 0.9, "y": 0.0, "x": 0.0, "z": 0.7}, 
#     "IK_kciuk_2_R":         {"scale": 0.9, "y": 0.0, "x": 0.0, "z": 0.7}
# }