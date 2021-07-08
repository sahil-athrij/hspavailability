import datetime
import random
import string

from django.contrib.auth.models import User
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

gender = [
    ('M', 'male'),
    ('F', 'female'),
    ('NB', 'Non Binary'),
    ('NP', 'Prefer Not to Say')
]

bed = [
    (1, 'normal'),
    (2, 'ventilator'),
    (3, 'ICU')
]


class Markers(models.Model):
    name = models.CharField(max_length=500)
    Phone = models.CharField(max_length=100)
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
    display_address = models.TextField(default="", max_length=3000, blank=True)
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
    comment = models.TextField(blank=True, max_length=3000)
    datef = models.DateField(default=datetime.date.today)
    day = models.IntegerField(default=0)
    size = models.IntegerField(choices=sizes, default=0)
    written_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.written_by.username + ',' + self.marker.name


class SuspiciousMarking(models.Model):
    marker = models.ForeignKey(Markers, on_delete=models.CASCADE)
    comment = models.TextField(max_length=30000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    datef = models.DateField(default=datetime.date.today)


class Images(models.Model):
    image = models.ImageField(upload_to="pic", blank=True)
    review = models.ForeignKey(Reviews, default=None, null=True, blank=True, related_name='images',
                               on_delete=models.CASCADE)
    hospital = models.ForeignKey(Markers, related_name='images', on_delete=models.CASCADE)
    useinmarker = models.BooleanField(default=False)


class Patient(models.Model):
    Name = models.CharField(max_length=40)
    age = models.IntegerField(default=0)
    gender = models.CharField(choices=gender, max_length=2)
    address = models.TextField(max_length=2048, default='',blank=True)

    symptoms = models.TextField(max_length=2048)
    symdays = models.DateField(blank=True, null=True)
    spo2 = models.IntegerField(default=0)
    oxy_bed = models.BooleanField(default=False)
    bedtype = models.IntegerField(choices=bed, default=0, blank=True, null=True)

    blood = models.CharField(max_length=2, blank=True, null=True)
    ct = models.BooleanField(default=False)
    covidresult = models.BooleanField(default=False)
    ctscore = models.TextField(max_length=20, blank=True, null=True)

    attendername = models.CharField(max_length=40, blank=True, null=True)
    attenderphone = models.CharField(max_length=20, blank=True, null=True)
    relation = models.CharField(max_length=30, blank=True, null=True)

    hospitalpref = models.CharField(max_length=300, blank=True, null=True)
    hospitalprefid = models.ForeignKey(Markers, related_name='hospital_preference', blank=True, null=True,on_delete=models.PROTECT)
    srfid = models.CharField(max_length=30, blank=True, null=True)
    bunum = models.CharField(max_length=40, blank=True, null=True)

    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_new_id():
    not_unique = True
    unique_id = id_generator()
    while not_unique:
        unique_id = id_generator()
        if not Tokens.objects.filter(private_token=unique_id):
            not_unique = False
    return str(unique_id)


class Tokens(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    private_token = models.CharField(max_length=10, unique=True, default=create_new_id)
    invited = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    reviews = models.IntegerField(default=0)
    reports = models.IntegerField(default=0)
    invite_token = models.CharField(max_length=10, blank=True, null=True)
