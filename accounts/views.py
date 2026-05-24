from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import SignUpForm, UserProfileForm, TrainerProfileForm
from .models import UserProfile, TrainerProfile


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_trainer = form.cleaned_data.get("is_trainer")
            if is_trainer:
                TrainerProfile.objects.create(user=user)
            else:
                UserProfile.objects.create(user=user)
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if TrainerProfile.objects.filter(user=request.user).exists():
        return redirect("trainer_dashboard")
    return redirect("my_bookings")


@login_required
def profile(request):
    is_trainer = TrainerProfile.objects.filter(user=request.user).exists()

    if is_trainer:
        trainer_profile = TrainerProfile.objects.get(user=request.user)
        if request.method == "POST":
            form = TrainerProfileForm(request.POST, request.FILES, instance=trainer_profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Your trainer profile has been updated.")
                return redirect("profile")
        else:
            form = TrainerProfileForm(instance=trainer_profile)
        return render(request, "accounts/profile.html", {
            "form": form,
            "is_trainer": True,
            "profile": trainer_profile,
        })
    else:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile has been updated.")
                return redirect("profile")
        else:
            form = UserProfileForm(instance=user_profile)
        return render(request, "accounts/profile.html", {
            "form": form,
            "is_trainer": False,
            "profile": user_profile,
        })
        
def trainer_public_profile(request, trainer_id):
    trainer = get_object_or_404(TrainerProfile, id=trainer_id)
    from training.models import Session
    from django.utils import timezone

    upcoming_sessions = Session.objects.filter(
        trainer=trainer,
        start_datetime__gt=timezone.now(),
        status="scheduled"
    ).order_by("start_datetime")

    from bookings.models import Review
    reviews = Review.objects.filter(
        trainer=trainer
    ).select_related("user").order_by("-created_at")

    return render(request, "accounts/trainer_profile.html", {
        "trainer": trainer,
        "upcoming_sessions": upcoming_sessions,
        "reviews": reviews,
        "avg_rating": trainer.average_rating(),
        "review_count": trainer.review_count(),
    })