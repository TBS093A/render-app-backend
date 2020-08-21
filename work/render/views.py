# make normal rest first
# connect websocked after rest done
from rest_framework.response import Response

from rest_framework import viewsets

from .models import *
from .serializers import *


# make views for serializers -> do not swapping! use mixins

class RenderViewSet(viewsets.ModelViewSet):
    """
    A RenderSet CRUD (abstract from `viewsets.ModelViewSet`):
        `GET`: `list()`
        `GET`: `retrieve()` /parameter {id}
        `POST`: `create()`
        `PUT`&`PATCH`: `update()` /parameter {id}
        `DELETE`: `destroy()` /parameter {id}
    """
    queryset = RenderSet.objects.all()
    serializer_class = RenderSetSerializer

    def create(self, request):
        """
        start rendering a every sets / single set (hand sign letter) / single image 
        
        every sets - `angle` - all hand sign positions

        single set - `letter_id` + `angle`

        single image - `letter_id` + `angle` + `camera_id`

        (default `angle` is 12)
        """
        
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