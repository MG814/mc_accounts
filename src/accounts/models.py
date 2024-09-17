from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings


class User(AbstractUser):
    phone = models.CharField(max_length=15)
    role = models.CharField(
        max_length=10,
        choices=[('Patient', 'Patient'), ('Doctor', 'Doctor')],
    )


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    locality = models.CharField(max_length=25)
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)

