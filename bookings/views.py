from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from training.models import Session
from .forms import BookingForm
from .models import Booking


@login_required
def create_booking(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    existing_booking = Booking.objects.filter(user=request.user, session=session).first()
    if existing_booking:
        messages.warning(request, "You have already booked this session.")
        return redirect("session_detail", session_id=session.id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.session = session
            booking.save()
            messages.success(request, "Your booking was created successfully.")
            return redirect("session_detail", session_id=session.id)
    else:
        form = BookingForm()

    return render(request, "bookings/create_booking.html", {
        "form": form,
        "session": session,
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related("session", "session__trainer", "session__sport_type", "session__location").order_by("-created_at")
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})