from django.contrib import admin
from .models import SportType, Location, Session


@admin.register(SportType)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "address")
    search_fields = ("name", "city", "address")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "trainer",
        "sport_type",
        "location",
        "start_datetime",
        "capacity",
        "price_per_person",
        "is_group",
        "status",
    )
    list_filter = ("sport_type", "location", "is_group", "status", "level")
    search_fields = ("title", "description", "trainer__user__username")
    ordering = ("start_datetime",)