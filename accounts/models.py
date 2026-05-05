from django.db import models
from django.contrib.auth.models import User


class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="trainer_profile")
    bio = models.TextField(blank=True)
    specialties = models.TextField(blank=True)
    photo = models.ImageField(upload_to="trainers/", blank=True, null=True)

    def __str__(self):
        return self.user.username

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            return round(total / reviews.count(), 1)
        return None

    def review_count(self):
        return self.reviews.count()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username