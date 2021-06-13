import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','maps.settings')
import django
django.setup()
from home.views import update_marker
from home.models import Markers

markers = Markers.objects.all()
for ob in markers:
    ob.financial_rating = 1
    ob.avg_cost = 1
    ob.covid_rating = 1
    ob.care_rating = 1
    ob.oxygen_rating = 0
    ob.beds_available = 0
    ob.ventilator_availability = 0
    ob.oxygen_availability = 0
    ob.icu_availability = 0
    ob.save()
    print(ob.id)