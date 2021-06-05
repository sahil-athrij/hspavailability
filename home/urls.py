

from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import index, modify, add_review, suspicious, MarkerApiViewSet, ReviewViewSet ,SusViewSet
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()
router.register(r'marker', MarkerApiViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'suspicious', SusViewSet)
urlpatterns = [
    path('', index),
    path('modify/', modify),
    path('add_review/',add_review),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns+=[path(r'', include(router.urls))]
