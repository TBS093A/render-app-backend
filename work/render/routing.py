from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/frame/(?P<frame_id>[^/]+)/image/(?P<image_id>[^/]+)/camera/(?P<camera_id>[^/]+)/$', consumers.RenderConsumer),
]