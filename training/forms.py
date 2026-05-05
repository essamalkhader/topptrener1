from django import forms
from .models import Session


class SessionForm(forms.ModelForm):
    # Location fields 
    location_name = forms.CharField(
        max_length=200,
        label="Location Name",
        help_text="e.g. Frogner Park"
    )
    location_address = forms.CharField(
        max_length=255,
        label="Address",
        required=False,
        help_text="e.g. Middelthunsgate 28"
    )
    location_city = forms.CharField(
        max_length=100,
        label="City",
        initial="Oslo"
    )

    # Sport type 
    sport_name = forms.CharField(
        max_length=100,
        label="Sport Type",
        help_text="e.g. Football, Yoga,"
    )

    class Meta:
        model = Session
        fields = [
            "title",
            "description",
            "level",
            "start_datetime",
            "duration_minutes",
            "capacity",
            "price_per_person",
            "is_group",
            "photo",
        ]
        widgets = {
            "start_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.start_datetime:
            self.initial["start_datetime"] = self.instance.start_datetime.strftime(
                "%Y-%m-%dT%H:%M"
            )