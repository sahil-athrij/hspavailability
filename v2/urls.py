from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from v2.views import index, signin, log_out, addHospital, signup, search, get_location, details, Google_login, csrf, \
    ping, help_page

urlpatterns = [
    path('', index),
    path('login/', signin),
    path('logout/', log_out),
    path('add_hospital/', addHospital),
    path('signup/', signup),
    path('search/', search, name='search'),
    path('getlocation/', get_location),
    path('details/<int:hospital_id>', details),
    path('help/', help_page),
    path('google-login/', Google_login),
    path('csrf/', csrf),
    path('ping/', ping),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)