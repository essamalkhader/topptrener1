from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from training.views import home, session_list, session_detail, trainer_dashboard, create_session, edit_session, cancel_session

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("sessions/", session_list, name="session_list"),
    path("sessions/<int:session_id>/", session_detail, name="session_detail"),
    path("trainer/dashboard/", trainer_dashboard, name="trainer_dashboard"),
    path("trainer/create-session/", create_session, name="create_session"),
    path("trainer/session/<int:session_id>/edit/", edit_session, name="edit_session"),
    path("trainer/session/<int:session_id>/cancel/", cancel_session, name="cancel_session"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    path("", include("bookings.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)