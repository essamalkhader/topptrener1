from django.urls import path
from .views import create_booking, my_bookings, cancel_booking


urlpatterns = [
    path("sessions/<int:session_id>/book/", create_booking, name="create_booking"),
    path("my-bookings/", my_bookings, name="my_bookings"),
    path("booking/<int:booking_id>/cancel/", cancel_booking, name="cancel_booking"),
]