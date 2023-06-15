from django.db import models
from django.contrib.auth.models import User
import random


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_code = models.CharField(max_length=6, default='')
    telegram_username = models.CharField(max_length=32, blank=True)
    telegram_id = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
