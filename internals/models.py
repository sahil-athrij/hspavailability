from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from home.models import Markers, Reviews
from datetime import timedelta


class Equipment_Name(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Department_Name(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to="pic", blank=True, null=True)

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
    rating = models.FloatField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    hospital = models.ForeignKey(Markers, related_name='departments', on_delete=models.CASCADE)
    floor = models.ForeignKey(Floors, null=True, blank=True, related_name='departments', on_delete=models.PROTECT)


class Equipment(models.Model):
    name = models.ForeignKey(Equipment_Name, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, related_name='equipment', on_delete=models.CASCADE)


class WorkingTime(models.Model):
    days = (
    (1, "monday"), (2, "tuesday"), (3, "Wednesday"), (4, "Thursday"), (5, "friday"), (6, "saturday"), (7, "sunday"))
    day = models.IntegerField(default=1, choices=days)
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    # time = models.DurationField(null=True, blank=True, validators=[])

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     self.time = timedelta(self.starting_time)


class HospitalWorkingTime(models.Model):
    working_time = models.ForeignKey(WorkingTime, on_delete=models.RESTRICT, blank=True, null=True)
    hospital = models.ForeignKey(Markers, on_delete=models.CASCADE, blank=True, null=True)
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE, related_name="working_time")


class Doctor(models.Model):
    choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=14)
    hospital = models.ManyToManyField(Markers, related_name='doctors', through=HospitalWorkingTime, )
    department = models.ManyToManyField(Department, related_name='doctors')
    user = models.OneToOneField(User, related_name='doctor', on_delete=models.PROTECT, default=None, null=True,
                                blank=True)
    about = models.TextField(blank=True, null=True, max_length=1000)
    rating = models.FloatField(default=0)
    patients = models.PositiveIntegerField(default=0)
    experience = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to="pic", null=True, blank=True)

    def __str__(self):
        return f"Dr: {self.name}"


class DoctorReviews(models.Model):
    content = models.TextField(max_length=3000)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="doctor_reviews")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reviews")


class Images(models.Model):
    image = models.ImageField(upload_to="pic", blank=True)
    review = models.ForeignKey(Reviews, default=None, null=True, blank=True, related_name='images',
                               on_delete=models.PROTECT)
    hospital = models.ForeignKey(Markers, related_name='images', on_delete=models.CASCADE,null=True, blank=True)
    department = models.ForeignKey(Department, related_name='images', on_delete=models.PROTECT, default=None, null=True,
                                   blank=True)
    equipment = models.ForeignKey(Equipment, related_name='images', on_delete=models.PROTECT, default=None, null=True,
                                  blank=True)
    useinmarker = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='uploaded_images', blank=True, null=True)
