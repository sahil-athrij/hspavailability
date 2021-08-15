from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from home.models import Markers, Reviews


class Equipment_Name(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Department_Name(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=200)
    floor_plan = models.ImageField(upload_to="building", blank=True)
    hospital = models.ForeignKey(Markers, related_name='buildings', on_delete=models.CASCADE)


class Floors(models.Model):
    number = models.IntegerField()
    building = models.ForeignKey(Building, related_name='floors', on_delete=models.CASCADE)


class Department(models.Model):
    name = models.ForeignKey(Department_Name, on_delete=models.PROTECT)
    x = models.IntegerField()
    y = models.IntegerField()
    hospital = models.ForeignKey(Markers, related_name='departments', on_delete=models.CASCADE)
    floor = models.ForeignKey(Floors, related_name='departments', on_delete=models.PROTECT)


class Equipment(models.Model):
    name = models.ForeignKey(Equipment_Name, on_delete=models.PROTECT)
    department = models.ForeignKey(Department,related_name='equipment', on_delete=models.CASCADE)


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=14)
    hospital = models.ManyToManyField(Markers, related_name='doctors')
    department = models.ManyToManyField(Department, related_name='doctors')
    user = models.OneToOneField(User, related_name='doctor', on_delete=models.PROTECT, null=True, blank=True)


class Images(models.Model):
    image = models.ImageField(upload_to="pic", blank=True)
    review = models.ForeignKey(Reviews, default=None, null=True, blank=True, related_name='images',
                               on_delete=models.PROTECT)
    hospital = models.ForeignKey(Markers, related_name='images', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='images', on_delete=models.PROTECT, default=None, null=True,
                                   blank=True)
    equipment = models.ForeignKey(Equipment, related_name='images', on_delete=models.PROTECT, default=None, null=True,
                                  blank=True)
    useinmarker = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='uploaded_images', blank=True, null=True)
