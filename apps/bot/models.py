from typing import TYPE_CHECKING
from django.db import models

from apps.common.models import BaseModel

if TYPE_CHECKING:
    from apps.user.models import User


class TelegramUser(BaseModel):
    chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    user: "User" = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
