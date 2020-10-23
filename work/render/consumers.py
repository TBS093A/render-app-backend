from abc import ABC, abstractmethod
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import sys
import asyncio

from .scripts.render import (
    RenderSingleImage,
    RenderSingleSet,
    RenderAllSets
)


class AbstractConsumer(AsyncWebsocketConsumer, ABC):

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
            'details': self.params
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
                        'details': self.params
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
                        'details': self.params
                    }
                )
            )