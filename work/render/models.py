from django.db import models
from django.http import FileResponse

from rest_framework.response import Response

from work.account.models import Account

class Model(models.Model):
    
    name = models.CharField(max_length=255)
    sets = models.IntegerField()
    cameras = models.IntegerField()
    model = models.FileField(upload_to='models/')

    user = models.ForeignKey(Account, on_delete=models.CASCADE)


class RenderAbstract(models.Model):
    name = models.CharField(max_length=30)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL)

    def share_archive_of_renders(self):
        file = open(f'renders/{self.name}.7z', 'r')
        file_download = FileResponse(file, content_type='archive/7zip')
        file_download['Content-Lenght']

    class Meta:
        abstract = True


class RenderAll(RenderAbstract):
    images_width = models.IntegerField()
    images_height = models.IntegerField()


class RenderImage(RenderAll):
    setID = models.IntegerField()
    cameraID = models.IntegerField()
    

class RenderSet(RenderImage):
    angle = models.FloatField()


class FingerVectorsDictAbstract(models.Model):
    pass

class FingerVectorsDict(FingerVectorsDict):
    render = models.ForeignKey(RenderImageByVector, on_delete=models.CASCADE)


class RenderImageByVector(RenderAbstract):
    pass