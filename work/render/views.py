from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets, mixins

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from work.settings import RENDER_DIR
from .models import *
from .serializers import *
from .scripts.render import *


from work.settings import (
    MODEL_DIR,
    RENDER_DIR
)

import os
import zipfile
import shutil


class ZipUtils():

    def __init__(self, directory):
        self.path = RENDER_DIR + '/' + directory
        self.name = self.path + '.zip'

    def zipDir(self):
        """
        create zip archive
        """
        with zipfile.ZipFile(self.name, 'w') as archive:
            for root, dirs, images in os.walk(self.path):
                for image in images:
                    archive.write(os.path.join(root, image))
            return archive

    def getSize(self):
        """
        archive size in bytes
        """
        return sum(
            os.path.getsize(file) for file in os.listdir(self.path) if os.path.isfile(file)
        )


class RenderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    A RenderSet CRUD (abstract from `viewsets.ModelViewSet`):
        `GET`: `list()`
        `GET`: `retrieve()` /parameter {id}'
        `DELETE`: `destroy()` /parameter {id}
    """
    queryset = RenderSet.objects.all()
    serializer_class = RenderSetSerializer

    def list(self, request):
        return Response(
            {
                'render_list': os.listdir(RENDER_DIR)
            }
        )

    def retrieve(self, request, **kwargs):
        # try:
        dir_id = int(kwargs['pk'])
        path = os.listdir(RENDER_DIR)[dir_id]
        archive = ZipUtils(path)
        archiveFile = archive.zipDir()

        # return Response(
        #     {
        #         'info': 'zip has been created'
        #     }
        # )

        response = FileResponse(archiveFile, content_type='zip')
        response['Content-Length'] = archive.getSize()
        response['Content-Disposition'] = f'attachment; filename={archive.name}'
        return response

        # except Exception as error:
        #     return Response(
        #         {
        #             'error': f'{repr(error)}: {str(error)}'
        #         }
        #     )


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

    # How to save textures in blend file:
    # "File"->"External Data"->"Pack All into .blend"

    def create(self, request, *args, **kwargs):
        blend_file = request.data['file']
        path = f'{MODEL_DIR}/{blend_file}'

        real_path = default_storage.save(path, ContentFile(blend_file.read()))

        request_effect = {
            'user_id': request.POST['user_id'],
            'path': str(real_path),
            'file_name': str(blend_file)
        }

        serializer = self.serializer_class(data=request_effect, context={'request': request})
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        
        result = serializer.create(
            **validated_data
        )
        
        return Response(
            {
                'info': f'add model',
                'result': result
            }
        )

# request.data:
# <QueryDict: {'filaname': ['testHnad.blend'], 'path': ['/static/testHand.blend'], 'user_id': ['1'], 'file': [<InMemoryUploadedFile: chess_board.blend (application/x-blender)>]}>
# request.POST
# <QueryDict: {'filaname': ['testHnad.blend'], 'path': ['/static/testHand.blend'], 'user_id': ['1']}>
# request.FILES
# <MultiValueDict: {'file': [<InMemoryUploadedFile: chess_board.blend (application/x-blender)>]}>
# print(request.data['file'])
# chess_board.blend