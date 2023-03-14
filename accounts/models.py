from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    balance = models.BigIntegerField(default=0, null=True )
    image = models.ImageField(blank=True)
    special_til = models.DateTimeField(null=True)

