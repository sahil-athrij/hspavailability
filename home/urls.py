

from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import index, modify, add_review, suspicious, MarkerApiViewSet
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()
router.register(r'marker', MarkerApiViewSet)
urlpatterns = [
    path('', index),
    path('modify/', modify),
    path('add_review/',add_review),
    path('suspicious/',suspicious),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns+=[path(r'', include(router.urls))]