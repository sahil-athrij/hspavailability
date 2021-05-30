

from django.urls import path
from .views import index, modify, more_info, add_review, filter_marker, marker_nearby, suspicious, getMarker
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index),
    path('modify/', modify),
    path('more_info/<int:key_id>/', more_info,name='more_info'),
    path('marker/', getMarker.as_view()),
    path('add_review/',add_review),
    path('filter/',filter_marker),
    path('markers/',marker_nearby),
    path('suspicious/',suspicious),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
