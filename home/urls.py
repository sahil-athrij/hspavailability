from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MarkerApiViewSet, ReviewViewSet, SusViewSet, PatientViewSet, ImageViewSet

router = DefaultRouter()
router.register(r'marker', MarkerApiViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'suspicious', SusViewSet)
router.register(r'patient', PatientViewSet)
router.register(r'image', ImageViewSet)
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path(r'', include(router.urls))]
