from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # --- Constants ---
    # User types
    DRIVER = 'driver'
    OWNER = 'owner'

    USER_TYPE_CHOICES = [
        (DRIVER, 'Driver'),
        (OWNER, 'Owner'),
    ]

    # --- Fields ---
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=DRIVER
    )

    phone_number = models.CharField(max_length=20)

    # --- Methods ---
    def __str__(self):
        return self.email
