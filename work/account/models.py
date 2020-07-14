from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import serializers


class AbstractUser(models.Model):
    city = models.CharField(verbose_name='City', max_length=255)
    country = models.CharField(verbose_name='Country', max_length=255)
    ip = models.CharField(verbose_name='IP', max_length=15)

    class Meta:
        abstract = True


class Account(User, AbstractUser):

    def fromDict(self, dict):
        self.__dict__.update(dict)

    def toDict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'password': None,
            'email': self.email,
            'ip': self.ip,
            'city': self.city,
            'country': self.country
        }

    @staticmethod
    def register(userDict) -> dict:
        account = Account.objects.create_user(
            userDict['username'], 
            userDict['email'], 
            userDict['password'],
        )
        account.ip = userDict['ip']
        account.city = userDict['city'],
        account.country = userDict['country']
        account.save()
        return account.toDict()

    def update(self, userDict) -> dict:
        if 'password' in userDict:
            password = userDict.pop('password')
            self.set_password(password)
        self.fromDict(userDict)
        self.save()
        return self.toDict()

    def set_password(self, raw_password):
        return super().set_password(raw_password)

    
