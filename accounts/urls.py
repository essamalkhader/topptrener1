from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("redirect/", views.login_redirect, name="login_redirect"),
    path("trainer/<int:trainer_id>/", views.trainer_public_profile, name="trainer_profile"),
]