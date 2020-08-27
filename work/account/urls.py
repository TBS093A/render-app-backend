from rest_framework import permissions, routers
from django.urls import path, include, re_path

from .views import AccountViewSet, AccountAuth

router = routers.DefaultRouter()

router.register(r'user', AccountViewSet, basename='user')

urlpatterns = [
    path('', include( router.urls )),
    re_path(r'user/auth', AccountAuth.as_view()),
]
