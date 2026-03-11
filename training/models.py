from django.db import models
from accounts.models import TrainerProfile


class SportType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, default="Oslo")
    map_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name="sessions")
    sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE, related_name="sessions")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sessions")

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, blank=True)
    start_datetime = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    price_per_person = models.DecimalField(max_digits=8, decimal_places=2)
    is_group = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")

    def __str__(self):
        return self.title