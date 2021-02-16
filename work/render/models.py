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
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

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


class RenderImageByVector(RenderImage):
    pass


class RenderSetByVector(RenderSet):
    pass


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

