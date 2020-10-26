from rest_framework import permissions, routers
from django.urls import path, include, re_path

from .views import *
from .routing import *

router = routers.DefaultRouter()

router.register(r'model', ModelViewSet, basename='model')
router.register(r'render/(?P<setName>\w+)', RenderViewSet, basename='render')

urlpatterns = [
    path('', include( router.urls ))
]