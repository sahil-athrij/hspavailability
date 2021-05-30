

from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import index, modify, more_info, add_review, filter_marker, marker_nearby, suspicious, MarkerApiViewSet
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()
router.register(r'', MarkerApiViewSet)
urlpatterns = [
    path('', index),
    path('modify/', modify),
    path('more_info/<int:key_id>/', more_info,name='more_info'),
    path('add_review/',add_review),
    path('filter/',filter_marker),
    path('markers/',marker_nearby),
    path('suspicious/',suspicious),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns+=[path(r'marker/', include(router.urls))]