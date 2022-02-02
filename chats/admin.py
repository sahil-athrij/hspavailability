from django.contrib import admin
from . import models

admin.site.register(models.Bundle)
admin.site.register(models.Message)
admin.site.register(models.Devices)
