from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta

from training.models import Session
from .forms import BookingForm
from .models import Booking, MembershipPlan, Membership


@login_required
def create_booking(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    if session.start_datetime <= timezone.now():
        messages.warning(request, "You cannot book a past session.")
        return redirect("session_detail", session_id=session.id)

    existing_booking = Booking.objects.filter(
        user=request.user,
        session=session
    ).exclude(status="cancelled").first()

    if existing_booking:
        messages.warning(request, "You already have an active booking for this session.")
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

            if active_membership:
                if active_membership.remaining_credits < booking.seats:
                    messages.warning(request, "You do not have enough credits for this booking.")
                    return redirect("session_detail", session_id=session.id)

                active_membership.remaining_credits -= booking.seats
                active_membership.save()

                booking.used_credits = True
                messages.success(request, "Your booking was created successfully using membership credits.")
            else:
                booking.used_credits = False
                messages.success(request, "Your booking was created successfully.")

            booking.save()
            return redirect("session_detail", session_id=session.id)
    else:
        form = BookingForm()

    return render(request, "bookings/create_booking.html", {
        "form": form,
        "session": session,
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

    return render(request, "bookings/my_bookings.html", {
        "bookings": bookings,
        "active_membership": active_membership,
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