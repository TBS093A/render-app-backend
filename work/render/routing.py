from django.conf.urls import url

from djangochannelsrestframework.consumers import view_as_consumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from .views import *

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(
                r"^render/$", 
                view_as_consumer(RenderViewSet),
            ),
            url(
                r"^render/angle/(?P<angle>[^/]+)/$", 
                view_as_consumer(RenderEverySetsViewSet),
            ),
            url(
                r"^render/angle/(?P<angle>[^/]+)/letter/(?P<letter_id>[^/]+)/$", 
                view_as_consumer(RenderSingleSetViewSet),
            ),
            url(
                r"^render/angle/(?P<angle>[^/]+)/letter/(?P<letter_id>[^/]+)/camera/(?P<camera_id>[^/]+)$",
                view_as_consumer(RenderSingleImageViewSet),
            ),
        ])
    ),
 })