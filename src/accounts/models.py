from django.db import models


class User(models.Model):
    auth0_id = models.CharField(max_length=50)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    role = models.CharField(
        max_length=10,
        choices=[('Patient', 'Patient'), ('Doctor', 'Doctor')],
    )
    specialization = models.CharField(max_length=200, blank=True, null=True)
