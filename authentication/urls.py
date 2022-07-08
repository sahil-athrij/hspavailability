from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GroupList, UserApiViewSet, UserSearchApiViewSet

# Setup the URLs and include login URLs for the browsable API.
router = DefaultRouter()
router.register(r'users', UserApiViewSet)
router.register(r"search_users", UserSearchApiViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('social/', include('rest_framework_social_oauth2.urls')),
    path('groups/', GroupList.as_view()),
    # ...
]
