from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from .consumers import (
    RenderAllConsumer,
    RenderSingleSetConsumer,
    RenderSingleImageConsumer,
    RenderSingleImageByVectorConsumer,
    RenderSingleSetByVectorConsumer
)


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(
                r'^render/all/(?P<room_uuid>[^/]+)', 
                RenderAllConsumer,
            ),
            url(
                r'^render/single/set/(?P<room_uuid>[^/]+)', 
                RenderSingleSetConsumer,
            ),
            url(
                r'render/single/image/(?P<room_uuid>[^/]+)',
                RenderSingleImageConsumer,
            ),
            url(
                r'^render/single/set/vectors/(?P<room_uuid>[^/]+)', 
                RenderSingleSetByVectorConsumer,
            ),
            url(
                r'render/single/image/vectors/(?P<room_uuid>[^/]+)',
                RenderSingleImageByVectorConsumer,
            )
        ])
    ),
 })

# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             url(
#                 r"^render/angle/(?P<angle>[^/]+)/$", 
#                 view_as_consumer(RenderEverySetsViewSet),
#             ),
#             url(
#                 r"^render/angle/(?P<angle>[^/]+)/letter/(?P<letter_id>[^/]+)/$", 
#                 view_as_consumer(RenderSingleSetViewSet),
#             ),
#             url(
#                 r"^render/angle/(?P<angle>[^/]+)/letter/(?P<letter_id>[^/]+)/camera/(?P<camera_id>[^/]+)$",
#                 view_as_consumer(RenderSingleImageViewSet),
#             ),
#         ])
#     ),
#  })