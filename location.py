import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maps.settings')
import django

django.setup()
from django.contrib.gis.geos import Point
from home.models import Markers

oblist = Markers.objects.all()

for ob in oblist:
    ob.location = Point(x=ob.lng, y=ob.lat, srid=4326)
    print(ob.id, ob.location)
    ob.save()
