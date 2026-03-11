from django.db import models
from django.contrib.auth.models import User


class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    specialties = models.TextField(blank=True)

    def __str__(self):
        return self.user.username