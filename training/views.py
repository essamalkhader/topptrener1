from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Session, SportType, Location
from .forms import SessionForm
from accounts.models import TrainerProfile
from django.utils import timezone
import pytz


def home(request):
    return render(request, "home.html")


def session_list(request):
    sessions = Session.objects.filter(
        start_datetime__gt=timezone.now(),
        status="scheduled"
    ).order_by("start_datetime")
    return render(request, "training/session_list.html", {"sessions": sessions})


def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    return render(request, "training/session_detail.html", {"session": session})


@login_required
def trainer_dashboard(request):
    try:
        trainer = TrainerProfile.objects.get(user=request.user)
    except TrainerProfile.DoesNotExist:
        messages.warning(request, "You do not have a trainer profile.")
        return redirect("home")

    sessions = Session.objects.filter(
        trainer=trainer
    ).order_by("start_datetime")

    upcoming = sessions.filter(start_datetime__gt=timezone.now(), status="scheduled")
    past = sessions.filter(start_datetime__lte=timezone.now())

    return render(request, "training/trainer_dashboard.html", {
        "trainer": trainer,
        "upcoming_sessions": upcoming,
        "past_sessions": past,
    })


@login_required
def create_session(request):
    try:
        trainer = TrainerProfile.objects.get(user=request.user)
    except TrainerProfile.DoesNotExist:
        messages.warning(request, "Only trainers can create sessions.")
        return redirect("home")

    if request.method == "POST":
        form = SessionForm(request.POST, request.FILES)
        if form.is_valid():
            session = form.save(commit=False)
            session.trainer = trainer

            # Handle location
            location_name = form.cleaned_data["location_name"]
            location_address = form.cleaned_data.get("location_address", "")
            location_city = form.cleaned_data.get("location_city", "Oslo")
            location, created = Location.objects.get_or_create(
                name=location_name,
                defaults={
                    "address": location_address,
                    "city": location_city,
                }
            )
            session.location = location

            # sport type
            sport_name = form.cleaned_data["sport_name"]
            from django.utils.text import slugify
            sport_type, created = SportType.objects.get_or_create(
                name__iexact=sport_name,
                defaults={
                    "name": sport_name,
                    "slug": slugify(sport_name),
                }
            )
            session.sport_type = sport_type
            
            oslo_tz = pytz.timezone('Europe/Oslo')
            naive_dt = session.start_datetime.replace(tzinfo=None)
            session.start_datetime = oslo_tz.localize(naive_dt)

            session.save()
            messages.success(request, "Session created successfully.")
            return redirect("trainer_dashboard")
    else:
        form = SessionForm()

    return render(request, "training/create_session.html", {"form": form})