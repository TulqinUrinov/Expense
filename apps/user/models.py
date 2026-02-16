from django.db import models

from apps.common.models import BaseModel


class User(BaseModel):
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )
