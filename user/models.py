from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=64)
    picture = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.username