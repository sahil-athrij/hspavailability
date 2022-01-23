from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ChatUserApiViewSet

router = DefaultRouter()
router.register(r'user', ChatUserApiViewSet)

urlpatterns = [path(r'', include(router.urls))]
