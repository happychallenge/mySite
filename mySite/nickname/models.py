from django.db import models
from django.conf import settings


# Create your models here.
# from mySite.records.models import Person

class Nickname(models.Model):
    """docstring for Nickname"""
    nickname = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname




