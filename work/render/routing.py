from django.conf.urls import url

from djangochannelsrestframework.consumers import view_as_consumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from .views import *

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^general/$", view_as_consumer(RenderViewSet)),
        ])
    ),
 })

# from django.urls import re_path

# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/frame/(?P<frame_id>[^/]+)/image/(?P<image_id>[^/]+)/camera/(?P<camera_id>[^/]+)/$', consumers.RenderConsumer),
# ]