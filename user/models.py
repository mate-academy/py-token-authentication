# user/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass  # Add any custom fields if needed

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
