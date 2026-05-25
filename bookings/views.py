from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta

from training.models import Session
from .forms import BookingForm, ReviewForm
from .models import Booking, MembershipPlan, Membership, Review


@login_required
def create_booking(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    # Block past sessions
    if session.start_datetime <= timezone.now():
        messages.warning(request, "You cannot book a past session.")
        return redirect("session_detail", session_id=session.id)

    # Block duplicate bookings
    existing_booking = Booking.objects.filter(
        user=request.user,
        session=session
    ).exclude(status="cancelled").first()
    if existing_booking:
        messages.warning(request, "You already have an active booking for this session.")
        return redirect("session_detail", session_id=session.id)

    # Block trainers
    from accounts.models import TrainerProfile
    if TrainerProfile.objects.filter(user=request.user).exists():
        messages.warning(request, "Trainers cannot book sessions.")
        return redirect("session_detail", session_id=session.id)

    # Block overbooking
    confirmed_bookings = Booking.objects.filter(
        session=session
    ).exclude(status="cancelled").count()
    if confirmed_bookings >= session.capacity:
        messages.warning(request, "Sorry, this session is fully booked.")
        return redirect("session_detail", session_id=session.id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.session = session

            active_membership = Membership.objects.filter(
                user=request.user,
                is_active=True
            ).first()

            is_free = session.price_per_person == 0

            # FREE SESSION > no credits, no payment
            if is_free:
                booking.used_credits = False
                booking.save()
                messages.success(request, "Your booking was confirmed. This session is free!")
                return redirect("my_bookings")

            # HAS CREDITS > deduct and confirm
            if active_membership and active_membership.remaining_credits >= booking.seats:
                active_membership.remaining_credits -= booking.seats
                active_membership.save()
                booking.used_credits = True
                booking.save()
                messages.success(request, f"Booking confirmed using {booking.seats} credit(s).")
                return redirect("my_bookings")

            # NO CREDITS OR NO MEMBERSHIP > go to payment
            return redirect("payment", session_id=session.id)

    else:
        form = BookingForm()

    return render(request, "bookings/create_booking.html", {
        "form": form,
        "session": session,
    })


@login_required
def payment(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    active_membership = Membership.objects.filter(
        user=request.user,
        is_active=True
    ).first()

    # Check if can upgrade
    can_upgrade = False
    if active_membership:
        higher_plans = MembershipPlan.objects.filter(
            monthly_price__gt=active_membership.plan.monthly_price
        ).exists()
        can_upgrade = higher_plans

    seats = 1
    total = session.price_per_person * seats

    if request.method == "POST":
        # Simulated payment — always succeeds
        booking = Booking.objects.create(
            user=request.user,
            session=session,
            seats=seats,
            used_credits=False,
            status="confirmed"
        )
        messages.success(request, "Payment successful! Your booking is confirmed.")
        return redirect("my_bookings")

    return render(request, "bookings/payment.html", {
        "session": session,
        "seats": seats,
        "total": total,
        "active_membership": active_membership,
        "can_upgrade": can_upgrade,
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related(
        "session",
        "session__trainer",
        "session__sport_type",
        "session__location"
    ).order_by("-created_at")

    active_membership = Membership.objects.filter(
        user=request.user,
        is_active=True
    ).first()

    total_sessions = bookings.exclude(status="cancelled").count()
    upcoming_count = bookings.filter(
        status="confirmed",
        session__start_datetime__gt=timezone.now()
    ).count()

    is_new_user = total_sessions == 0

    return render(request, "bookings/my_bookings.html", {
        "bookings": bookings,
        "active_membership": active_membership,
        "now": timezone.now(),
        "total_sessions": total_sessions,
        "upcoming_count": upcoming_count,
        "is_new_user": is_new_user,
    })


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        if booking.status == "cancelled":
            messages.warning(request, "This booking is already cancelled.")
            return redirect("my_bookings")

        refund_deadline = booking.session.start_datetime - timedelta(hours=3)

        if timezone.now() <= refund_deadline:
            if booking.used_credits:
                active_membership = Membership.objects.filter(
                    user=request.user,
                    is_active=True
                ).first()
                if active_membership:
                    active_membership.remaining_credits += booking.seats
                    active_membership.save()
                    messages.success(request, "Your booking was cancelled and your credits have been refunded to your membership.")
                else:
                    messages.success(request, "Your booking was cancelled. Please contact us for your credit refund.")
            else:
                messages.success(request, "Your booking was cancelled. A refund will be processed within 3-5 business days.")
        else:
            messages.warning(request, "Your booking was cancelled. No refund is available as cancellation was made less than 3 hours before the session.")

        booking.status = "cancelled"
        booking.save()
        return redirect("my_bookings")

    return render(request, "bookings/cancel_booking.html", {"booking": booking})


def membership_plans(request):
    plans = MembershipPlan.objects.all().order_by("monthly_price")
    return render(request, "bookings/membership_plans.html", {"plans": plans})


@login_required
def subscribe_membership(request, plan_id):
    plan = get_object_or_404(MembershipPlan, id=plan_id)

    existing_membership = Membership.objects.filter(
        user=request.user,
        is_active=True
    ).first()

    if request.method == "POST":
        if existing_membership:
            if existing_membership.plan == plan:
                messages.warning(request, "You already have this active membership.")
                return redirect("membership_plans")

            if plan.monthly_price > existing_membership.plan.monthly_price:
                existing_membership.plan = plan
                existing_membership.start_date = timezone.now().date()
                existing_membership.end_date = timezone.now().date() + timedelta(days=30)
                existing_membership.remaining_credits = plan.monthly_credits
                existing_membership.save()

                messages.success(request, f"Your membership has been upgraded to {plan.name}.")
                return redirect("membership_plans")
            else:
                messages.warning(
                    request,
                    "Downgrading is not allowed until your current plan expires."
                )
                return redirect("membership_plans")

        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)

        Membership.objects.create(
            user=request.user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            remaining_credits=plan.monthly_credits,
            is_active=True,
        )

        messages.success(request, f"You have successfully subscribed to the {plan.name} plan.")
        return redirect("membership_plans")

    return render(request, "bookings/subscribe_membership.html", {"plan": plan})

@login_required
def leave_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Must not be cancelled
    if booking.status == "cancelled":
        messages.warning(request, "You cannot review a cancelled booking.")
        return redirect("my_bookings")

    # Session must have already happened
    if booking.session.start_datetime > timezone.now():
        messages.warning(request, "You can only review a session after it has taken place.")
        return redirect("my_bookings")

    # Check if review already exists
    if hasattr(booking, "review"):
        messages.warning(request, "You have already reviewed this session.")
        return redirect("my_bookings")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.trainer = booking.session.trainer
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted. Thank you!")
            return redirect("my_bookings")
    else:
        form = ReviewForm()

    return render(request, "bookings/leave_review.html", {
        "form": form,
        "booking": booking,
    })