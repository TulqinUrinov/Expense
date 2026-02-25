from typing import TYPE_CHECKING
from django.db import models

from apps.common.models import BaseModel

if TYPE_CHECKING:
    from apps.user.models import User


class TelegramUser(BaseModel):
    class States(models.TextChoices):
        START = "START", "Start"
        NAME = "NAME", "Name"
        PHONE = "PHONE", "Phone"
        DONE = "DONE", "Done"

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

    state = models.CharField(
        max_length=20,
        choices=States.choices,
        default=States.START
    )

    def __str__(self):
        return self.name or str(self.chat_id)
