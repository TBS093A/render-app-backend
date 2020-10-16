from rest_framework import permissions, routers
from django.urls import path, include, re_path

from .views import *

router = routers.DefaultRouter()

router.register(r'model', ModelViewSet, basename='model')
router.register(r'render', RenderViewSet, basename='render')
router.register(r'render/single/image/set-id/(?P<setID>[^/]+)/rotate/(?P<rotate>[^/]+)/name-series/(?P<nameSeries>[^/]+)/camera-id/(?P<cameraID>[^/]+)/resolution/X/(?P<resolutionX>[^/]+)/Y/(?P<resolutionY>[^/]+)', RenderSingleImageViewSet, basename='renderSingleImage')

urlpatterns = [
    path('', include( router.urls ))
]