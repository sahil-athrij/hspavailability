

from django.urls import path
from .views import index, modify, more_info, add_review, search_marker

urlpatterns = [
    path('', index),
    path('modify/', modify),
    path('more_info/<int:key_id>/', more_info,name='more_info'),
    path('add_review/',add_review),
    path('search/',search_marker)
]
