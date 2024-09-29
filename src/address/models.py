from django.db import models

from django.conf import settings


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    locality = models.CharField(max_length=25)
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)