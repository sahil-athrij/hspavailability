import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','maps.settings')
import django
django.setup()
from django.contrib.gis.geos import Point
from home.models import Markers

oblist = Markers.objects.all()

for ob in oblist:
    ob.position = Point(ob.lng,ob.lat)
    print(ob.id,ob.position)
    ob.save()