from django.contrib import admin
from django.urls import path
from training.views import home, session_list


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("sessions/", session_list, name="session_list"),
]