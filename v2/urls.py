

from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('login/',signin),
    path('signup/',signup),
    path('search/', search, name='search')
]
