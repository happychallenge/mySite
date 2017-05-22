from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    """docstring for Profile"""
    """ 설명 """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='user_profile/')
    created_at = models.DateTimeField(auto_now_add=True)

