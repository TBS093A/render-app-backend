from django.conf.urls import url

from djangochannelsrestframework.consumers import view_as_consumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from .views import *
from .consumers import *


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(
                r'^render/all/resolution/X/(?P<resolutionX>[^/]+)/Y/(?P<resolutionY>[^/]+)/angle/(?P<angle>[^/]+)', 
                RenderConsumer,
            ),
            url(
                r'^render/single/set/set-id/(?P<setID>[^/]+)/camera-id/(?P<cameraID>[^/]+)/resolution/X/(?P<resolutionX>[^/]+)/Y/(?P<resolutionY>[^/]+)/angle/(?P<angle>[^/]+)', 
                RenderConsumer,
            ),
            url(
                r'render/single/image/set-id/(?P<setID>[^/]+)/rotate/(?P<rotate>[^/]+)/name-series/(?P<nameSeries>[^/]+)/camera-id/(?P<cameraID>[^/]+)/resolution/X/(?P<resolutionX>[^/]+)/Y/(?P<resolutionY>[^/]+)',
                RenderConsumer,
            ),
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