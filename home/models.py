from django.db import models

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
    size = models.IntegerField(choices=sizes ,default=0)
    financial_rating = models.IntegerField(choices=rating,default=1)
    avg_cost = models.IntegerField(default=0)
    covid_rating = models.IntegerField(choices=rating,default=1)
    beds_available = models.IntegerField(default=0)
    care_rating = models.IntegerField(choices=rating,default=1)
    oxygen_rating = models.IntegerField(choices=rating,default=1)
    ventilator_availability = models.BooleanField(default=0)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)


class Reviews(models.Model):
    marker = models.ForeignKey(Markers,related_name="comment",on_delete=models.CASCADE)
    financial_rating = models.IntegerField(choices=rating,default=1)
    avg_cost = models.IntegerField(default=0)
    covid_rating = models.IntegerField(choices=rating,default=1)
    care_rating = models.IntegerField(choices=rating,default=1)
    oxygen_rating = models.IntegerField(choices=rating,default=1)
    beds_available = models.BooleanField(default=0)
    ventilator_availability = models.BooleanField(default=0)
    comment = models.TextField()
