from django.db import models

from work.account.models import Account

class RenderSet(models.Model):
    name = models.CharField(max_length=30)
    images_width = models.IntegerField()
    images_height = models.IntegerField()
    images_count = models.IntegerField()
    
    model = models.ForeignKey(Model, on_delete=models.SET_NULL)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL)

    def check_or_save(self):
        for render in RenderSet.objects.all():
            if render.name == self.name:
                if render.images_width == self.images_width:
                    if render.images_height == self.images_height:
                        if render.images_count == self.images_count:
                            pass
                        elif render.images_count < self.images_count:
                            pass
                        elif render.images_count > self.images_count:
                            pass

class Model(models.Model):
    name = models.CharField(max_length=255)
    file = models.CharField(max_length=255)