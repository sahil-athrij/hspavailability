import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','maps.settings')
import django
django.setup()
import requests, json
from home.models import Markers

markers = Markers.objects.all()
for mkr in markers:
    url="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"+mkr