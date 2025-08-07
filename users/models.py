from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver

USERS_TYPE = [("PUB", "publisher"), ("SUB", "viewer"), ("NaN", "NO-ACTIVE")]

# Create your models here.
class App_users(AbstractUser):
    user_type = models.TextField(max_length=20, choices=USERS_TYPE, default=USERS_TYPE[1])

    @property
    def is_publisher(self):
        return self.user_type == "PUB"

    def clean(self):
        if not self.is_active and self.user_type == "NaN":
            return ValidationError("inactive user can't be anything else 'NO-ACTIVE' ")
        return super().clean()

    def __str__(self):
        return super().get_full_name()

    class Meta:
        pass

@receiver(pre_save, sender=App_users)
def set_user_type_inactive(sender, instance, **kwargs):
    if instance.is_active is False and instance.user_type !="NaN":
        instance.user_type = "NaN"
