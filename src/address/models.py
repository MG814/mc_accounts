from django.db import models
from accounts.models import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locality = models.CharField(max_length=25)
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)