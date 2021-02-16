from django.db import models
from django.http import FileResponse

from rest_framework.response import Response

from work.account.models import Account

from work.settings import (
    STATIC_ROOT
)

class Model(models.Model):
    file_name = models.CharField(max_length=600)
    path = models.CharField(max_length=600)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'file_name': self.file_name,
            'path': self.path,
            'user_id': self.user.id
        }


class RenderAbstract(models.Model):
    name = models.CharField(max_length=30)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    
    resolution_x = models.IntegerField()
    resolution_y = models.IntegerField()

    def share_archive_of_renders(self):
        file = open(f'renders/{self.name}.7z', 'r')
        file_download = FileResponse(file, content_type='archive/7zip')
        file_download['Content-Lenght']

    class Meta:
        abstract = True


class RenderAll(RenderAbstract):
    pass


class RenderImage(RenderAbstract):
    set_id = models.IntegerField()
    rotate = models.FloatField()
    name_series = models.IntegerField()
    camera_id = models.IntegerField()
    

class RenderSet(RenderAbstract):
    set_id = models.IntegerField()
    rotate = models.FloatField()
    name_series = models.IntegerField()
    camera_id = models.IntegerField()
    angle = models.FloatField()


class RenderImageByVector(RenderAbstract):
    rotate = models.FloatField()
    name_series = models.IntegerField()
    camera_id = models.IntegerField()


class RenderSetByVector(RenderAbstract):
    name_series = models.IntegerField()
    camera_id = models.IntegerField()
    angle = models.FloatField()


default_vector = '{"scale": 0.0, "y": 0.0, "x": 0.0, "z": 0.0}'

class FingerVectorsDictAbstract(models.Model):
    IK_nadgarstek_R     = models.CharField(max_length=100, verbose_name=default_vector)
    IK_joint3_R         = models.CharField(max_length=100, verbose_name=default_vector)
    IK_joint4_R         = models.CharField(max_length=100, verbose_name=default_vector)
    IK_joint5_R         = models.CharField(max_length=100, verbose_name=default_vector)
    IK_joint6_R         = models.CharField(max_length=100, verbose_name=default_vector)
    IK_maly_1_R         = models.CharField(max_length=100, verbose_name=default_vector)
    IK_maly_2_R         = models.CharField(max_length=100, verbose_name=default_vector)
    IK_maly_3_R         = models.CharField(max_length=100, verbose_name=default_vector)
    IK_serdeczny_1_R    = models.CharField(max_length=100, verbose_name=default_vector)
    IK_serdeczny_2_R    = models.CharField(max_length=100, verbose_name=default_vector)
    IK_serdeczny_3_R    = models.CharField(max_length=100, verbose_name=default_vector)
    IK_srodkowy_1_R     = models.CharField(max_length=100, verbose_name=default_vector)
    IK_srodkowy_2_R     = models.CharField(max_length=100, verbose_name=default_vector)
    IK_srodkowy_3_R     = models.CharField(max_length=100, verbose_name=default_vector)
    IK_wskazujacy_1_R   = models.CharField(max_length=100, verbose_name=default_vector)
    IK_wskazujacy_2_R   = models.CharField(max_length=100, verbose_name=default_vector)
    IK_wskazujacy_3_R   = models.CharField(max_length=100, verbose_name=default_vector)
    IK_kciuk_0_R        = models.CharField(max_length=100, verbose_name=default_vector)         
    IK_kciuk_1_R        = models.CharField(max_length=100, verbose_name=default_vector)
    IK_kciuk_2_R        = models.CharField(max_length=100, verbose_name=default_vector)

    class Meta:
        abstract = True


class FingerVectorsDictImage(FingerVectorsDictAbstract):
    render = models.ForeignKey(RenderImageByVector, on_delete=models.CASCADE)


class FingerVectorsDictSet(FingerVectorsDictAbstract):
    render = models.ForeignKey(RenderSetByVector, on_delete=models.CASCADE)

