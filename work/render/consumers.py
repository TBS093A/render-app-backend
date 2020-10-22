from abc import ABC, abstractmethod
from channels.generic.websocket import AsyncWebsocketConsumer
import json

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
        await elf.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    class Meta:
        abstract = True


class RenderSingleImageConsumer(AbstractConsumer):

    async def render(self):
        renderSingleImage = RenderSingleImage(
            self.params['fileName'] + '.blend'
        )
        await renderSingleImage.render(
            int(self.params['setID']),
            float(self.params['rotate']),
            int(self.params['nameSeries']),
            int(self.params['cameraID']),
            resolution=(
                int(self.params['resolutionX']), 
                int(self.params['resolutionY'])
            )
        )
        await self.send({
            'info': 'render success',
            'details': self.params
        })


class RenderSingleSetConsumer(AbstractConsumer):

    async def render(self):
        renderSingleSet = RenderSingleSet(
            self.params['fileName'] + '.blend'
        )
        for renderImage in renderSingleSet(
            int(self.params['setID']),
            int(self.params['cameraID']),
            resolution=(
                int(self.params['resolutionX']), 
                int(self.params['resolutionY'])
            ),
            angle=float(self.params['angle'])
        ):
            await self.send({
                'info': renderImage,
                'details': self.params
            })


class RenderAllConsumer(AbstractConsumer):

    async def render(self):
        renderAllSets = RenderAllSets(
            self.params['fileName'] + '.blend'
        )
        for renderSet in renderAllSets(
            resolution=(
                int(self.params['resolutionX']), 
                int(self.params['resolutionY'])
            ),
            angle=float(self.params['angle'])
        ):
            await self.send({
                'info': renderSet,
                'details': self.params
            })