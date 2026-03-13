from django.shortcuts import render
from .models import Session


def home(request):
    return render(request, "home.html")


def session_list(request):
    sessions = Session.objects.all().order_by("start_datetime")
    return render(request, "training/session_list.html", {"sessions": sessions})