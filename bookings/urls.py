from django.urls import path
from .views import (
    create_booking, my_bookings, cancel_booking,
    membership_plans, subscribe_membership,
    leave_review, payment)

urlpatterns = [
    path("sessions/<int:session_id>/book/", create_booking, name="create_booking"),
    path("sessions/<int:session_id>/payment/", payment, name="payment"),
    path("my-bookings/", my_bookings, name="my_bookings"),
    path("booking/<int:booking_id>/cancel/", cancel_booking, name="cancel_booking"),
    path("booking/<int:booking_id>/review/", leave_review, name="leave_review"),
    path("membership-plans/", membership_plans, name="membership_plans"),
    path("membership-plans/<int:plan_id>/subscribe/", subscribe_membership, name="subscribe_membership"),
]