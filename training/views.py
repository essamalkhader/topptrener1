from django.shortcuts import render, get_object_or_404
from .models import Session


def home(request):
    return render(request, "home.html")


def session_list(request):
    sessions = Session.objects.all().order_by("start_datetime")
    return render(request, "training/session_list.html", {"sessions": sessions})


def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    return render(request, "training/session_detail.html", {"session": session})

