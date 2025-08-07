from django.db import models
from django.contrib.auth.models import AbstractUser


USERS_TYPE = [("publisher", "PUB"), ("viewer", "SUB")]

# Create your models here.
class App_users(AbstractUser):
    is_publisher = models.BooleanField(default=False)
    user_type = models.TextField(max_length=20, choices=USERS_TYPE, default="viewer")

    def __str__(self):
        return super().get_full_name()

    class Meta:
        pass