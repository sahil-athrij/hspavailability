from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from .views import MarkerApiViewSet, ReviewViewSet, SusViewSet, PatientViewSet

schema_view = get_swagger_view(title='Need Medi API')

router = DefaultRouter()
router.register(r'marker', MarkerApiViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'suspicious', SusViewSet)
router.register(r'patient', PatientViewSet)
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path('', schema_view)]
urlpatterns += [path(r'', include(router.urls))]
