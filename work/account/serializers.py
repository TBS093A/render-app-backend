from .models import Account

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, logout as logoutDjango
from django.core.paginator import Paginator
from django.http import JsonResponse


class AccountGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    username = serializers.CharField(max_length = 100)
    email = serializers.EmailField()
    ip = serializers.CharField(max_length = 12)
    city = serializers.CharField(max_length = 255)
    country = serializers.CharField(max_length = 255)

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'ip', 'city', 'country']


class AccountSerializer(AccountGetSerializer):
    password = serializers.CharField(max_length = 100)

    def create(self, validated_data):
        return Account.register(validated_data)

    def update(self, instance, validated_data):
        return instance.update(validated_data)

    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'email', 'ip', 'city', 'country']

class AccountAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 100)
    password = serializers.CharField(max_length = 100)

    @staticmethod
    def login(username, password) -> dict:
        tryLogin = authenticate(username = username, password = password)
        if tryLogin is not None:
            user = Account.objects.get(username = username)
            try:
                token = Token.objects.get(user = user)
            except:
                token = Token.objects.create(user = user)
            return { 'Authorization': 'Token ' + token.key, 'user': user.toDict() }
        else:
            return { 'error': 'login failed'}

    @staticmethod
    def logout(request, format=None):
        logoutDjango(request)
        tokenStr = request.headers['Authorization'].split(' ')[1]
        token = Token.objects.get(key = tokenStr)
        token.delete()
        return { 'info': 'logout success' }

    class Meta:
        model = Account
        fields = ['username', 'password']
