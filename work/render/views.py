# make normal rest first
# connect websocked after rest done
from rest_framework.response import Response

from rest_framework import viewsets

from .models import *
# from .serializers import *

class RenderViewSet(viewsets.ModelViewSet):
    """
    A RenderSet CRUD (abstract from `viewsets.ModelViewSet`):
        `GET`: `list()`
        `GET`: `retrieve()` /parameter {id}
        `POST`: `create()`
        `PUT`&`PATCH`: `update()` /parameter {id}
        `DELETE`: `destroy()` /parameter {id}
    """

    def create(self, request):
        """
        start rendering a every sets / single set (hand sign letter) / single image 
        
        every sets - `angle` - all hand sign positions

        single set - `letter_id` + `angle`

        single image - `letter_id` + `angle` + `camera_id`

        (default `angle` is 12)
        """
        
        pass

class ModelViewSet(viewsets.ModelViewSet):
    """
    A Model CRUD (abstract from `viewsets.ModelViewSet`):
        `GET`: `list()`
        `GET`: `retrieve()` /parameter {id}
        `POST`: `create()`
        `PUT`&`PATCH`: `update()` /parameter {id}
        `DELETE`: `destroy()` /parameter {id}
    """
    pass