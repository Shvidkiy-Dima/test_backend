from django.contrib.auth.models import AbstractUser
from core.model_fields import PhoneNumberField


class CustomUser(AbstractUser):
    phone = PhoneNumberField(null=True, blank=True)
