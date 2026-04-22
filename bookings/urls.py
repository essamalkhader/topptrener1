from django.urls import path
from .views import create_booking, my_bookings, cancel_booking, membership_plans, subscribe_membership


urlpatterns = [
    path("sessions/<int:session_id>/book/", create_booking, name="create_booking"),
    path("my-bookings/", my_bookings, name="my_bookings"),
    path("booking/<int:booking_id>/cancel/", cancel_booking, name="cancel_booking"),
    path("membership-plans/", membership_plans, name="membership_plans"),
    path("membership-plans/<int:plan_id>/subscribe/", subscribe_membership, name="subscribe_membership"),
]
