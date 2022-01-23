import random
import string

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

from home.models import Tokens


class Message(models.Model):
    data = models.JSONField(blank=True, null=True)
    to_user = models.ForeignKey('ChatUser', related_name='messages', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)


class Bundle(models.Model):
    data = models.JSONField(blank=True, null=True)
    user = models.ForeignKey('ChatUser', on_delete=models.CASCADE, related_name='bundle')
    deviceId = models.CharField(max_length=20)
    # token = models.OneToOneField(Tokens, on_delete=models.CASCADE, related_name='bundle', blank=True, null=True)

    def __str__(self):
        return f'{self.user.user} {self.deviceId}'


class Devices(models.Model):
    data = models.JSONField(blank=True, null=True)
    username = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.username}/ {self.data}'


def user_id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_user_id():
    not_unique = True
    unique_id = user_id_generator()
    while not_unique:
        unique_id = user_id_generator()
        if not ChatUser.objects.filter(id=unique_id):
            not_unique = False
    return str(unique_id)


class ChatUser(models.Model):
    id = models.CharField(default=create_user_id, primary_key=True, max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    device_ids = ArrayField(models.PositiveIntegerField(), blank=True, null=True)

    def __str__(self):
        return f"{self.id} {self.user.username}"
