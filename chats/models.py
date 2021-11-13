from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True, auto_now_add=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    ip = models.GenericIPAddressField(verbose_name=_('IP'), null=True, blank=True)
