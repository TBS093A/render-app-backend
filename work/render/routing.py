from django.conf.urls import url

from djangochannelsrestframework.consumers import view_as_consumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from .views import *

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^general/$", view_as_consumer(RenderViewSet)),
            url(r'^render/all/$', view_as_consumer(RenderEverySetsViewSet)),
            url(r'^render/set/$', view_as_consumer(RenderSingleSetViewSet)),
            url(r'^render/image/$', view_as_consumer(RenderSingleImageViewSet)),
        ])
    ),
 })

# from django.urls import re_path

# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/frame/(?P<frame_id>[^/]+)/image/(?P<image_id>[^/]+)/camera/(?P<camera_id>[^/]+)/$', consumers.RenderConsumer),
# ]