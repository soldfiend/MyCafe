from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} (Chat ID: {self.telegram_chat_id})"
