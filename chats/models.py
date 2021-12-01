from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# class Message(models.Model):
#     sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
#     receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
#     message = models.TextField()
#     sent_at = models.DateTimeField(auto_now_add=True)
#     read_at = models.DateTimeField(null=True, blank=True)
#     ip = models.GenericIPAddressField(null=True, blank=True)

class KeyExchange(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="keyExchangeSender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="keyExchangeReceiver")
    sender_key_bundle = models.JSONField()
    receiver_key_bundle = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.sender} --> {self.receiver}"
