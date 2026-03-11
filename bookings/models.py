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
        
class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="review")
    trainer = models.ForeignKey("accounts.TrainerProfile", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="reviews")

    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username}"
    

class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2)
    monthly_credits = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Membership(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="memberships")
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    remaining_credits = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"