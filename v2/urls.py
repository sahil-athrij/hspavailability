from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from v2.views import index, signin, log_out, signup, Google_login, help_page

urlpatterns = [
    path('', index),
    path('login/', signin),
    path('logout/', log_out),
    path('signup/', signup),
    path('help/', help_page),
    path('google-login/', Google_login),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
