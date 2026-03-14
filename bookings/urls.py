from django.urls import path
from .views import create_booking


urlpatterns = [
    path("sessions/<int:session_id>/book/", create_booking, name="create_booking"),
]