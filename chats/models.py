import random
import string

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

from home.models import Tokens


class Message(models.Model):
    from_user = models.ForeignKey(User, related_name='msg_frm', on_delete=models.CASCADE, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    to_user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    to_send = ArrayField(ArrayField(models.CharField(max_length=10), default=list), default=list)


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

