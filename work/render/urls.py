from rest_framework import permissions, routers
from django.urls import path, include, re_path

from .views import *

router = routers.DefaultRouter()

router.register(r'model', ModelViewSet, basename='model')

urlpatterns = [
    path('', include( router.urls ))
]