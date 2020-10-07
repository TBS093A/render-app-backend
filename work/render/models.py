from django.db import models
from django.http import FileResponse

from rest_framework.response import Response

from work.account.models import Account

class Model(models.Model):
    name = models.CharField(max_length=255)
    model = models.FileField(upload_to='models/')

class RenderSet(models.Model):
    name = models.CharField(max_length=30)
    images_width = models.IntegerField()
    images_height = models.IntegerField()
    images_count = models.IntegerField()
    
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def share_archive_of_renders(self):
        file = open(f'renders/{self.name}.7z', 'r')
        file_download = FileResponse(file, content_type='archive/7zip')
        file_download['Content-Lenght']