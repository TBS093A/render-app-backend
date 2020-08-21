"""work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from work import settings
from .account.views import AccountViewSet, AccountAuth
from .render.views import RenderViewSet, ModelViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='0.1',
      description="API",
      contact=openapi.Contact(email="zukkamil.44@gmail.com"),
      license=openapi.License(name="All rights reserved"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

router.register(r'user', AccountViewSet, basename='user')
router.register(r'render', RenderViewSet, basename='render')
router.register(r'model', ModelViewSet, basename='model')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    re_path(r'user/auth', AccountAuth.as_view())
]

if settings.DEBUG:
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0))
    ]
