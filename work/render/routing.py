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
                r'^render/(?P<fileName>[^/]+)/all/resolution/X/(?P<resolutionX>[^/]+)/Y/(?P<resolutionY>[^/]+)/angle/(?P<angle>[^/]+)', 
                RenderAllConsumer,
            ),
            url(
                r'^render/(?P<fileName>[^/]+)/single/set/set-id/(?P<setID>[^/]+)/camera-id/(?P<cameraID>[^/]+)/resolution/X/(?P<resolutionX>[^/]+)/Y/(?P<resolutionY>[^/]+)/angle/(?P<angle>[^/]+)', 
                RenderSingleSetConsumer,
            ),
            url(
                r'render/(?P<fileName>[^/]+)/single/image/set-id/(?P<setID>[^/]+)/rotate/(?P<rotate>[^/]+)/name-series/(?P<nameSeries>[^/]+)/camera-id/(?P<cameraID>[^/]+)/resolution/X/(?P<resolutionX>[^/]+)/Y/(?P<resolutionY>[^/]+)',
                RenderSingleImageConsumer,
            ),
            url(
                r'^render/(?P<fileName>[^/]+)/single/set/set-id/(?P<setID>[^/]+)/camera-id/(?P<cameraID>[^/]+)/vectors/(?P<vectors>[^/]+)/resolution/X/(?P<resolutionX>[^/]+)/Y/(?P<resolutionY>[^/]+)/angle/(?P<angle>[^/]+)', 
                RenderSingleSetByVectorConsumer,
            ),
            url(
                r'render/(?P<fileName>[^/]+)/single/image/set-id/(?P<setID>[^/]+)/rotate/(?P<rotate>[^/]+)/name-series/(?P<nameSeries>[^/]+)/camera-id/(?P<cameraID>[^/]+)/vectors/(?P<vectors>[^/]+)/resolution/X/(?P<resolutionX>[^/]+)/Y/(?P<resolutionY>[^/]+)',
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