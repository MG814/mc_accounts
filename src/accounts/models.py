from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=15)
    role = models.CharField(
        max_length=10,
        choices=[('Patient', 'Patient'), ('Doctor', 'Doctor')],
    )
    specialization = models.CharField(max_length=200, blank=True, null=True)
