from django.db import models
from user.models import User


class Message(models.Model):
    messages = models.TextField(max_length=120, default="")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.messages


class Time(models.Model):
    time = models.TextField(max_length=20, default="")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.time


class Taught(models.Model):
    taught = models.TextField(max_length=80, default="")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.taught
