from rest_framework.response import Response
from rest_framework import viewsets, mixins, parsers

from .models import *
from .serializers import *
from .scripts.render import *
# from .renderAsync.GreenletTask import *


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
