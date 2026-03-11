from django.contrib import admin
from .models import Booking, Review, MembershipPlan, Membership


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "session", "seats", "status", "created_at")
    list_filter = ("status", "session")
    search_fields = ("user__username", "session__title")
    ordering = ("-created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "trainer", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("user__username", "trainer__user__username")


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "monthly_price", "monthly_credits")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "remaining_credits", "is_active")
    list_filter = ("is_active",)