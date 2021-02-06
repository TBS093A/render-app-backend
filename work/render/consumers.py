from abc import ABC, abstractmethod
from channels.generic.websocket import AsyncWebsocketConsumer
import json
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

    async def connect(self):
        self.params = self.scope['url_route']['kwargs']
        self.group_name = 'render'
        
        for param, value in self.params.items():
            self.group_name += f'_{param}{value}'
        
        self.channel_layer

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.render()

    @abstractmethod
    async def render(self):
        pass

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    class Meta:
        abstract = True

# test:
# ws://localhost:9090/render/testHand/single/image/set-id/0/rotate/0.2/name-series/0/camera-id/1/resolution/X/50/Y/33/

class RenderSingleImageConsumer(AbstractConsumer):

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
# ws://localhost:9090/render/testHand/single/set/set-id/50/camera-id/1/resolution/X/50/Y/33/angle/0.2

class RenderSingleSetConsumer(AbstractConsumer):

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
# ws://localhost:9090/render/testHand/all/resolution/X/50/Y/33/angle/0.2

class RenderAllConsumer(AbstractConsumer):

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

# test
# ws://localhost:9090/render/testHand/single/image/set-id/0/rotate/0.2/name-series/0/camera-id/1/vectors/{"IK_nadgarstek_R":{"head":{'x': 0.1445000171661377,'y': 0.06353862583637238,'z': -0.0073097944259643555},"tail":{'x': -0.08322930335998535,'y': 0.06281907856464386,'z': -0.009127259254455566}}}/resolution/X/50/Y/33/

class RenderSingleImageByVectorConsumer(AbstractConsumer):

    async def render(self):
        renderSingleImage = RenderSingleImageByVector(
            self.params['fileName'] + '.blend'
        )
        renderSingleImage.render(
            int(self.params['setID']),
            float(self.params['rotate']),
            int(self.params['nameSeries']),
            int(self.params['cameraID']),
            json.loads(self.params['vectors']),
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
# ws://localhost:9090/render/testHand/single/set/set-id/50/camera-id/1/vectors/{"IK_nadgarstek_R":{"head":{'x': 0.1445000171661377,'y': 0.06353862583637238,'z': -0.0073097944259643555},"tail":{'x': -0.08322930335998535,'y': 0.06281907856464386,'z': -0.009127259254455566}}}/resolution/X/50/Y/33/angle/0.2

class RenderSingleSetByVectorConsumer(AbstractConsumer):

    async def render(self):
        renderSingleSet = RenderSingleSetByVector(
            self.params['fileName'] + '.blend'
        )
        for renderImage in renderSingleSet.render(
            int(self.params['setID']),
            int(self.params['cameraID']),
            json.loads(self.params['vectors']),
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
# in multiline
# 
# {
#     'IK_nadgarstek_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_joint3_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     },
#     'IK_maly_1_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     },
#     'IK_maly_2_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     },
#     'IK_maly_3_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     },
#     'IK_joint4_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_serdeczny_1_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_serdeczny_2_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_serdeczny_3_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_joint5_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_srodkowy_1_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_srodkowy_2_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_srodkowy_3_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_joint6_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_wskazujacy_1_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_wskazujacy_2_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_wskazujacy_3_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_kciuk_0_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     },
#     'IK_kciuk_1_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }, 
#     'IK_kciuk_2_R': {
#         'head': {
#             'x': 0.1445000171661377, 
#             'y': 0.06353862583637238, 
#             'z': -0.0073097944259643555
#         }, 
#         'tail': {
#             'x': -0.08322930335998535, 
#             'y': 0.06281907856464386, 
#             'z': -0.009127259254455566
#         }
#     }
# }
# 
# in one-liner
# 
# {'IK_nadgarstek_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_joint3_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_maly_1_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_maly_2_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_maly_3_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_joint4_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_serdeczny_1_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_serdeczny_2_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_serdeczny_3_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_joint5_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_srodkowy_1_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_srodkowy_2_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_srodkowy_3_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_joint6_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_wskazujacy_1_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_wskazujacy_2_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_wskazujacy_3_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_kciuk_0_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_kciuk_1_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}},'IK_kciuk_2_R':{'head':{'x':0.1445000171661377,'y':0.06353862583637238,'z':-0.0073097944259643555},'tail':{'x':-0.08322930335998535,'y':0.06281907856464386,'z':-0.009127259254455566}}}
# 
# in base64
# 
# eydJS19uYWRnYXJzdGVrX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfam9pbnQzX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfbWFseV8xX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfbWFseV8yX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfbWFseV8zX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfam9pbnQ0X1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfc2VyZGVjem55XzFfUic6eydoZWFkJzp7J3gnOjAuMTQ0NTAwMDE3MTY2MTM3NywneSc6MC4wNjM1Mzg2MjU4MzYzNzIzOCwneic6LTAuMDA3MzA5Nzk0NDI1OTY0MzU1NX0sJ3RhaWwnOnsneCc6LTAuMDgzMjI5MzAzMzU5OTg1MzUsJ3knOjAuMDYyODE5MDc4NTY0NjQzODYsJ3onOi0wLjAwOTEyNzI1OTI1NDQ1NTU2Nn19LCdJS19zZXJkZWN6bnlfMl9SJzp7J2hlYWQnOnsneCc6MC4xNDQ1MDAwMTcxNjYxMzc3LCd5JzowLjA2MzUzODYyNTgzNjM3MjM4LCd6JzotMC4wMDczMDk3OTQ0MjU5NjQzNTU1fSwndGFpbCc6eyd4JzotMC4wODMyMjkzMDMzNTk5ODUzNSwneSc6MC4wNjI4MTkwNzg1NjQ2NDM4Niwneic6LTAuMDA5MTI3MjU5MjU0NDU1NTY2fX0sJ0lLX3NlcmRlY3pueV8zX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfam9pbnQ1X1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfc3JvZGtvd3lfMV9SJzp7J2hlYWQnOnsneCc6MC4xNDQ1MDAwMTcxNjYxMzc3LCd5JzowLjA2MzUzODYyNTgzNjM3MjM4LCd6JzotMC4wMDczMDk3OTQ0MjU5NjQzNTU1fSwndGFpbCc6eyd4JzotMC4wODMyMjkzMDMzNTk5ODUzNSwneSc6MC4wNjI4MTkwNzg1NjQ2NDM4Niwneic6LTAuMDA5MTI3MjU5MjU0NDU1NTY2fX0sJ0lLX3Nyb2Rrb3d5XzJfUic6eydoZWFkJzp7J3gnOjAuMTQ0NTAwMDE3MTY2MTM3NywneSc6MC4wNjM1Mzg2MjU4MzYzNzIzOCwneic6LTAuMDA3MzA5Nzk0NDI1OTY0MzU1NX0sJ3RhaWwnOnsneCc6LTAuMDgzMjI5MzAzMzU5OTg1MzUsJ3knOjAuMDYyODE5MDc4NTY0NjQzODYsJ3onOi0wLjAwOTEyNzI1OTI1NDQ1NTU2Nn19LCdJS19zcm9ka293eV8zX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfam9pbnQ2X1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfd3NrYXp1amFjeV8xX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfd3NrYXp1amFjeV8yX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfd3NrYXp1amFjeV8zX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fSwnSUtfa2NpdWtfMF9SJzp7J2hlYWQnOnsneCc6MC4xNDQ1MDAwMTcxNjYxMzc3LCd5JzowLjA2MzUzODYyNTgzNjM3MjM4LCd6JzotMC4wMDczMDk3OTQ0MjU5NjQzNTU1fSwndGFpbCc6eyd4JzotMC4wODMyMjkzMDMzNTk5ODUzNSwneSc6MC4wNjI4MTkwNzg1NjQ2NDM4Niwneic6LTAuMDA5MTI3MjU5MjU0NDU1NTY2fX0sJ0lLX2tjaXVrXzFfUic6eydoZWFkJzp7J3gnOjAuMTQ0NTAwMDE3MTY2MTM3NywneSc6MC4wNjM1Mzg2MjU4MzYzNzIzOCwneic6LTAuMDA3MzA5Nzk0NDI1OTY0MzU1NX0sJ3RhaWwnOnsneCc6LTAuMDgzMjI5MzAzMzU5OTg1MzUsJ3knOjAuMDYyODE5MDc4NTY0NjQzODYsJ3onOi0wLjAwOTEyNzI1OTI1NDQ1NTU2Nn19LCdJS19rY2l1a18yX1InOnsnaGVhZCc6eyd4JzowLjE0NDUwMDAxNzE2NjEzNzcsJ3knOjAuMDYzNTM4NjI1ODM2MzcyMzgsJ3onOi0wLjAwNzMwOTc5NDQyNTk2NDM1NTV9LCd0YWlsJzp7J3gnOi0wLjA4MzIyOTMwMzM1OTk4NTM1LCd5JzowLjA2MjgxOTA3ODU2NDY0Mzg2LCd6JzotMC4wMDkxMjcyNTkyNTQ0NTU1NjZ9fX0
# 