from django.contrib import admin
from django.urls import path,include
from training.views import home, session_list, session_detail



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("sessions/", session_list, name="session_list"),
    path("sessions/<int:session_id>/", session_detail, name="session_detail"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),

]