

from django.urls import path
from .views import index,signin,signup,get_location

urlpatterns = [
    path('', index),
    path('login/',signin),
    path('signup/',signup),

    path('getlocation/',get_location)
]
