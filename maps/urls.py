"""maps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, authentication

...

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",

        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sahilathrij@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
    authentication_classes=[authentication.SessionAuthentication]
)

urlpatterns = [

    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path(os.environ.get('ADMIN_URL'), admin.site.urls),
    path('api/', include('home.urls')),
    path('', include('v2.urls')),
    path('auth/', include('authentication.urls')),
    path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# curl -X POST -d "grant_type=convert_token&client_id=Ahn9ELq2nVTrWjnaKeDbbf1p7FWPyIGM4hxLeUvb&client_secret=eTkLmNzC2uJNkRSP9qPb5k8IR3OmueIa5KEVqDbTuRJ1GURzp9Jm3Vviz0qMCk73AzlW0TSM0n981JBYr2MEC8t0tsWSZFgaTIdaxN4eFvsjUROzSL3RoVlVdE2iaEHy&backend=google-oauth2&token=569002618626-kr65dimckmmdbgfuafrakqa0g6h18f55.apps.googleusercontent.com" http://localhost:8000/auth/convert-token
