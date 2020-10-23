from rest_framework import serializers

from .models import (
    Model,
    RenderSet
)


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

    @staticmethod
    def create(self, validated_data):
        pass


    class Meta:
        model = RenderSet
        fields = renderSerializerFields


class ModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    sets = serializers.IntegerField()
    cameras = serializers.IntegerField()

    user_id = serializers.IntegerField()

    @staticmethod
    def create(self, **kwargs) -> dict:
        newModel = Model(kwargs)
        newModel.save()
        return { 'info': 'model has been saved' }

    @staticmethod
    def update(self, **kwargs) -> dict:
        model = Model.objects.get(id=kwargs['id'])
        model.__dict__.update(kwargs)
        model.save()
        return { 'info': 'model has been updated' }

    class Meta:
        model = Model
        fields = ['id', 'name', 'sets', 'cameras' 'file']