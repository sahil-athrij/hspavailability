from django.contrib.auth.models import User
from django.contrib.gis.db import models



class Bundle(models.Model):
    data = models.JSONField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bundle')
    deviceId = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} {self.deviceId}'


class Devices(models.Model):
    data = models.JSONField(blank=True, null=True)
    username = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.username}/ {self.data}'

