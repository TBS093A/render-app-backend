from abc import ABC, abstractmethod
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import base64
import sys
import asyncio

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

    async def connect(self):
        self.params = self.scope['url_route']['kwargs']
        self.group_name = 'render_room_' + self.params['room_uuid']
        
        # for param, value in self.params.items():
        #     self.group_name += f'_{param}{value}'
        
        self.channel_layer

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send('type a json')

    @abstractmethod
    async def render(self):
        pass

    async def receive(self, **kwargs):
        self.params = json.loads(
            kwargs['text_data']
        )
        try:
            await self.send(f'Render { self.group_name } Has Been Started!')
            await self.render()
        except Exception as error:
            await self.send(f'Render { self.group_name } Has Been Terminated!')
            await self.send(f'Bad Parameter! Type JSON like this: {json.dumps(self.schema)}')
            await self.send(f'Error: { str(error) }')
            await self.send(f'Error: { repr(error) }')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

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
        await self.send(json.dumps({
            'info': 'render success',
            'details': self.params,
            'group': self.group_name
        }))

# test:
# ws://localhost:9090/render/single/set/<room_uuid>
# {
#     "fileName": "testHand", 
#     "setID": 0,
#     "nameSeries": 0, 
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
            await self.send(json.dumps(
                    {
                        'info': renderImage,
                        'details': self.params,
                        'group': self.group_name
                    }
                )
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
            await self.send(json.dumps(
                    {
                        'info': renderSet,
                        'details': self.params,
                        'group': self.group_name
                    }
                )
            )

# test:
# ws://localhost:9090/render/vector/single/image/<room_uuid>
# {
#     "fileName": "testHand", 
#     "setID": 0, 
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
            'IK_nadgarstek_R': {
                'head': {
                    'x': 0.1445000171661377, 
                    'y': 0.06353862583637238, 
                    'z': -0.0073097944259643555
                }, 
                'tail': {
                    'x': -0.08322930335998535, 
                    'y': 0.06281907856464386, 
                    'z': -0.009127259254455566
                }
            }, 
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
        renderSingleImage.render(
            float(self.params['rotate']),
            int(self.params['nameSeries']),
            int(self.params['cameraID']),
            self.params['vectors'],
            resolution=(
                int(self.params['resolutionX']), 
                int(self.params['resolutionY'])
            )
        )
        await self.send(json.dumps({
            'info': 'render success',
            'details': self.params,
            'group': self.group_name
        }))

# test:
# ws://localhost:9090/render/vector/single/set/<room_uuid>
# {
#     "fileName": "testHand", 
#     "setID": 0,
#     "nameSeries": 0, 
#     "cameraID": 1,
#     "vectors": {}, 
#     "resolutionX": 1920, 
#     "resolutionY": 1080,
#     "angle": 0.2
# }

class RenderSingleSetByVectorConsumer(AbstractConsumer):

    schema = {
        'fileName': 'fileName',
        'rotate': 0.0,
        'nameSeries': 0,
        'cameraID': 0,
        'vectors': {
            'IK_nadgarstek_R': {
                'head': {
                    'x': 0.1445000171661377, 
                    'y': 0.06353862583637238, 
                    'z': -0.0073097944259643555
                }, 
                'tail': {
                    'x': -0.08322930335998535, 
                    'y': 0.06281907856464386, 
                    'z': -0.009127259254455566
                }
            }, 
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
        for renderImage in renderSingleSet.render(
            int(self.params['cameraID']),
            self.params['vectors'],
            resolution=(
                int(self.params['resolutionX']), 
                int(self.params['resolutionY'])
            ),
            angle=float(self.params['angle'])
        ):
            await asyncio.sleep(0.5)
            await self.send(json.dumps(
                    {
                        'info': renderImage,
                        'details': self.params,
                        'group': self.group_name
                    }
                )
            )

# example vectors
# 
# General
#
# {
#     "IK_nadgarstek_R":      {"y": float, "x": float, "z": float}, 
#     "IK_joint3_R":          {"y": float, "x": float, "z": float},
#     "IK_maly_1_R":          {"y": float, "x": float, "z": float},
#     "IK_maly_2_R":          {"y": float, "x": float, "z": float},
#     "IK_maly_3_R":          {"y": float, "x": float, "z": float},
#     "IK_joint4_R":          {"y": float, "x": float, "z": float}, 
#     "IK_serdeczny_1_R":     {"y": float, "x": float, "z": float}, 
#     "IK_serdeczny_2_R":     {"y": float, "x": float, "z": float}, 
#     "IK_serdeczny_3_R":     {"y": float, "x": float, "z": float}, 
#     "IK_joint5_R":          {"y": float, "x": float, "z": float}, 
#     "IK_srodkowy_1_R":      {"y": float, "x": float, "z": float}, 
#     "IK_srodkowy_2_R":      {"y": float, "x": float, "z": float}, 
#     "IK_srodkowy_3_R":      {"y": float, "x": float, "z": float}, 
#     "IK_joint6_R":          {"y": float, "x": float, "z": float}, 
#     "IK_wskazujacy_1_R":    {"y": float, "x": float, "z": float}, 
#     "IK_wskazujacy_2_R":    {"y": float, "x": float, "z": float}, 
#     "IK_wskazujacy_3_R":    {"y": float, "x": float, "z": float}, 
#     "IK_kciuk_0_R":         {"y": float, "x": float, "z": float},
#     "IK_kciuk_1_R":         {"y": float, "x": float, "z": float}, 
#     "IK_kciuk_2_R":         {"y": float, "x": float, "z": float}
# }
#
# Without extremals
#
# {
#     "IK_maly_1_R":          {"y": float, "x": float, "z": float},
#     "IK_maly_2_R":          {"y": float, "x": float, "z": float},
#     "IK_maly_3_R":          {"y": float, "x": float, "z": float},
#  
#     "IK_serdeczny_1_R":     {"y": float, "x": float, "z": float}, 
#     "IK_serdeczny_2_R":     {"y": float, "x": float, "z": float}, 
#     "IK_serdeczny_3_R":     {"y": float, "x": float, "z": float}, 
#
#     "IK_srodkowy_1_R":      {"y": float, "x": float, "z": float}, 
#     "IK_srodkowy_2_R":      {"y": float, "x": float, "z": float}, 
#     "IK_srodkowy_3_R":      {"y": float, "x": float, "z": float}, 
#
#     "IK_wskazujacy_1_R":    {"y": float, "x": float, "z": float}, 
#     "IK_wskazujacy_2_R":    {"y": float, "x": float, "z": float}, 
#     "IK_wskazujacy_3_R":    {"y": float, "x": float, "z": float}, 
#     "IK_kciuk_0_R":         {"y": float, "x": float, "z": float},
#     "IK_kciuk_1_R":         {"y": float, "x": float, "z": float}, 
#     "IK_kciuk_2_R":         {"y": float, "x": float, "z": float}
# }
#
# With example values
#
# {
#     "IK_maly_1_R":          {"y": 0.2, "x": 0.0, "z": 0.7},
#     "IK_maly_2_R":          {"y": 0.0, "x": 0.0, "z": 0.0},
#     "IK_maly_3_R":          {"y": 0.0, "x": 0.0, "z": 0.0},
 
#     "IK_serdeczny_1_R":     {"y": 0.2, "x": 0.0, "z": 0.6},
#     "IK_serdeczny_2_R":     {"y": 0.0, "x": 0.0, "z": 0.0}, 
#     "IK_serdeczny_3_R":     {"y": 0.0, "x": 0.0, "z": 0.0}, 

#     "IK_srodkowy_1_R":      {"y": 0.2, "x": 0.0, "z": 0.5},
#     "IK_srodkowy_2_R":      {"y": 0.0, "x": 0.0, "z": 0.0}, 
#     "IK_srodkowy_3_R":      {"y": 0.0, "x": 0.0, "z": 0.0},

#     "IK_wskazujacy_1_R":    {"y": 0.2, "x": 0.0, "z": 0.4},
#     "IK_wskazujacy_2_R":    {"y": 0.0, "x": 0.0, "z": 0.0},
#     "IK_wskazujacy_3_R":    {"y": 0.0, "x": 0.0, "z": 0.0},

#     "IK_kciuk_0_R":         {"y": 0.5, "x": 0.5, "z": 0.6},
#     "IK_kciuk_1_R":         {"y": 0.0, "x": 0.0, "z": 0.7}, 
#     "IK_kciuk_2_R":         {"y": 0.0, "x": 0.0, "z": 0.7}
# }