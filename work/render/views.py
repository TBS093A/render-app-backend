# make normal rest first
# connect websocked after rest done
from rest_framework.response import Response

from rest_framework import viewsets, mixins

from .models import *
from .serializers import *


# make views for serializers -> do not swapping! use mixins

class RenderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = RenderSet.objects.all()
    serializer_class = RenderSetSerializer


class RenderEverySetsViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    A RenderSet CRUD (abstract from `viewsets.ModelViewSet`):
        `GET`: `list()`
        `GET`: `retrieve()` /parameter {id}
        `POST`: `create()`
        `PUT`&`PATCH`: `update()` /parameter {id}
        `DELETE`: `destroy()` /parameter {id}
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
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
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
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
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