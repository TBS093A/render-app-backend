from rest_framework.response import Response
from rest_framework import viewsets, mixins, parsers

from work.settings import RENDER_DIR
from .models import *
from .serializers import *
from .scripts.render import *
# from .renderAsync.GreenletTask import *

import os
import zipfile
import shutil


class ZipUtils():

    def __init__(self, directory):
        self.name = directory + '.zip'
        self.path = RENDER_DIR + '/' + directory

    def zipDir():
        archive = zipfile.ZipFile(self.name, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, images in os.walk(self.path):
            for image in images:
                archive.write(os.path.join(root, image))
        archive.close()


class RenderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
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

    def list(self, request):
        pass

    def retrieve(self, request, **kwargs):
        print(kwargs)
        archive = ZipUtils(kwargs['set'])
        pass


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
    parser_classes = (parsers.FileUploadParser,)

    def create(self, request, filename, format='blend'):
        model = request.FILES['file']
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']
        sets = serializer.validated_data['sets']
        cameras = serializer.validated_data['cameras']
        user = serializer.validated_data['user_id']
        return Response(ModelSerializer.create(
                {
                    'model': model,
                    'name': name,
                    'sets': sets,
                    'cameras': cameras,
                    'user_id': user
                }
            )
        )
