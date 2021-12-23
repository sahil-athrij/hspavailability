from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import KeyExchangeViewSet, index

router = DefaultRouter()
router.register(r'key_exchange', KeyExchangeViewSet)

urlpatterns = [path(r'', include(router.urls)),
               path(r'chat', index)]
