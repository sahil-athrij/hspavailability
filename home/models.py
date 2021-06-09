from django.contrib.auth.models import User
from django.db import models
import datetime
from django.contrib.gis.db import models
# Create your models here.

rating = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]

sizes = [
    (0, 'small'),
    (1, 'medium'),
    (2, 'large'),
]


class Markers(models.Model):
    name = models.CharField(max_length=500)
    Phone = models.CharField(max_length=20)
    size = models.IntegerField(choices=sizes, default=0)
    financial_rating = models.FloatField(default=1)
    avg_cost = models.IntegerField(default=0)
    covid_rating = models.FloatField(default=1)
    beds_available = models.IntegerField(default=0)
    care_rating = models.FloatField(default=1)
    oxygen_rating = models.FloatField(default=1)
    ventilator_availability = models.FloatField(default=0)
    oxygen_availability = models.FloatField(default=0)
    icu_availability = models.FloatField(default=0)
    lat = models.FloatField()
    lng = models.FloatField()
    datef = models.DateField(default=datetime.date.today)
    place_id = models.CharField(max_length=60, default="")
    added_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    Suspicious = models.IntegerField(default=0)
    display_address = models.TextField(default="", blank=True)
    address = models.JSONField(blank=True)
    location = models.PointField(srid=4326, verbose_name='Location')

    def __str__(self):
        return self.name




class Reviews(models.Model):
    marker = models.ForeignKey(Markers, related_name="comment", on_delete=models.CASCADE)
    financial_rating = models.IntegerField(choices=rating, default=1)
    avg_cost = models.IntegerField(default=0)
    covid_rating = models.IntegerField(choices=rating, default=1)
    care_rating = models.IntegerField(choices=rating, default=1)
    oxygen_rating = models.IntegerField(choices=rating, default=1)
    beds_available = models.IntegerField(default=0)
    ventilator_availability = models.IntegerField(default=0)
    oxygen_availability = models.IntegerField(default=0)
    icu_availability = models.IntegerField(default=0)
    comment = models.TextField(blank=True)
    datef = models.DateField(default=datetime.date.today)
    day = models.IntegerField(default=0)
    written_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)


class SuspiciousMarking(models.Model):
    marker = models.ForeignKey(Markers, on_delete=models.CASCADE)
    comment = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    datef = models.DateField(default=datetime.date.today)


class Images(models.Model):
    image = models.ImageField(upload_to="pic", blank=True)
    review = models.ForeignKey(Reviews,default=None,related_name='images', on_delete=models.CASCADE)
    hospital = models.ForeignKey(Markers, related_name='images', on_delete=models.CASCADE)
    useinmarker = models.BooleanField(default=False)
