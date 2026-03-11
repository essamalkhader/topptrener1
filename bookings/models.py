from django.db import models
from django.contrib.auth.models import User
from training.models import Session


class Booking(models.Model):
    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="bookings")

    seats = models.PositiveIntegerField(default=1)
    note_to_trainer = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="confirmed")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "session")

    def __str__(self):
        return f"{self.user.username} - {self.session.title}"