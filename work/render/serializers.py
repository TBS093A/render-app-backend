from rest_framework import serializers

from .models import *


class RenderSetAbstractSerializer(serializers.ModelSerializer):
    """
    start rendering a every sets / single set (hand sign letter) / single image 
    
    subclasses can start rendering simply

    just use `create()` method inside subclass
    """

    class Meta:
        model = RenderSet

class RenderEverySetsSerializer(RenderSetAbstractSerializer):
    """
    every sets - `angle` - all hand sign positions
    """


    class Meta:
        fields = []

class RenderSingleSetSerializer(RenderSetAbstractSerializer):
    """
    single set - `letter_id` + `angle`

    (default `angle` is 12)
    """

    class Meta:
        fields = []   

class RenderSingleImageSerializer(RenderSetAbstractSerializer):
    """
    single image - `letter_id` + `angle` + `camera_id`

    (default `angle` is 12)
    """

    class Meta:
        fields = []


class ModelSerializer(serializers.ModelSerializer):
    pass