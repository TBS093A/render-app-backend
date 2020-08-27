# make normal rest first
# connect websocked after rest done
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from djangochannelsrestframework import permissions, mixins as channelMixins
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from .models import *
from .serializers import *


# make views for serializers -> do not swapping! use mixins

class RenderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DeleteModelMixin,
    viewsets.GenericViewSet,
):
    """
    A RenderSet CRUD (abstract from `viewsets.ModelViewSet`):
        `GET`: `list()`
        `GET`: `retrieve()` /parameter {id}
        `DELETE`: `destroy()` /parameter {id}
    """
    queryset = RenderSet.objects.all()
    serializer_class = RenderSetSerializer


class RenderEverySetsViewSet(
    channelMixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A RenderEverySets CRUD (abstract from `viewsets.ModelViewSet`):
        `POST`: `create()`
    """
    queryset = RenderSet.objects.all()
    serializer_class = RenderEverySetsSerializer

    def create(self, request):
        if 'angle' and 'letter_id' and 'camera_id' in request:
            # single image serializer swap
            pass
        elif 'angle' and 'letter_id' in request:
            # single set serializer swap
            pass
        elif 'angle' in request:
            # every sets serializer swap
            pass
        return Response()


class RenderSingleSetViewSet(
    channelMixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A RenderSingleSetSet CRUD (abstract from `viewsets.ModelViewSet`):
        `POST`: `create()`
    """
    queryset = RenderSet.objects.all()
    serializer_class = RenderSingleSetSerializer

    def create(self, request):
        if 'angle' and 'letter_id' and 'camera_id' in request:
            # single image serializer swap
            pass
        elif 'angle' and 'letter_id' in request:
            # single set serializer swap
            pass
        elif 'angle' in request:
            # every sets serializer swap
            pass
        return Response()


class RenderSingleImageViewSet(
    channelMixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A RenderSingleImage CRUD (abstract from `viewsets.ModelViewSet`):
        `POST`: `create()`
    """
    queryset = RenderSet.objects.all()
    serializer_class = RenderSingleImageSerializer

    def create(self, request):
        if 'angle' and 'letter_id' and 'camera_id' in request:
            # single image serializer swap
            pass
        elif 'angle' and 'letter_id' in request:
            # single set serializer swap
            pass
        elif 'angle' in request:
            # every sets serializer swap
            pass
        return Response()


class ModelViewSet(viewsets.ModelViewSet):
    """
    A  CRUD (abstract from `viewsets.ModelViewSet`):
        `GET`: `list()`
        `GET`: `retrieve()` /parameter {id}
        `POST`: `create()`
        `PUT`&`PATCH`: `update()` /parameter {id}
        `DELETE`: `destroy()` /parameter {id}
    """
    queryset = Model.objects.all()
    serializer_class = ModelSerializer