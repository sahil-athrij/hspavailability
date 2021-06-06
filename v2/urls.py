

from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('login/', signin),
    path('logout/', log_out),
    path('signup/', signup),
    path('search/', search, name='search'),
    path('getlocation/', get_location),
    path('details/<int:hospital_id>', details),
    path('help/',help)
]
