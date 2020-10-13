from rest_framework import serializers

from .models import *


renderSerializerFields = ['id', 'name', 'images_width', 'images_height', 'images_count', 'model_id', 'user_id' ]


class RenderSetSerializer(serializers.ModelSerializer):
    """
    start rendering a every sets / single set (hand sign letter) / single image 
    
    subclasses can start rendering simply

    just use `create()` method inside subclass
    """
    id = serializers.IntegerField(read_only=True)
    
    name = serializers.CharField(max_length=30)
    images_width = serializers.IntegerField()
    images_height = serializers.IntegerField()
    
    model_id = serializers.IntegerField()
    user_id = serializers.IntegerField()


    def create(self, validated_data):
        pass


    class Meta:
        model = RenderSet
        fields = renderSerializerFields

class RenderAllSetsSerializer(RenderSetSerializer):
    """
    every sets - `angle` - all hand sign positions
    
    (default `angle` is 12)
    """
    angle = serializers.FloatField()


    def create(self, validated_data):
        pass


    class Meta:
        model = RenderSet
        fields = renderSerializerFields + ['angle']

class RenderSingleSetSerializer(RenderAllSetsSerializer):
    """
    single set - `letter_id` + `angle`

    (default `angle` is 12)
    """
    letter_id = serializers.IntegerField()


    def create(self, validated_data):
        pass


    class Meta:
        model = RenderSet
        fields = renderSerializerFields + ['letter_id']   

class RenderSingleImageSerializer(RenderSingleSetSerializer):
    """
    single image - `letter_id` + `angle` + `camera_id`

    (default `angle` is 12)
    """
    camera_id = serializers.IntegerField()


    def create(self, validated_data):
        pass


    class Meta:
        model = RenderSet
        fields = renderSerializerFields + ['camera_id']


class ModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Model
        fields = ['id', 'name', 'file']