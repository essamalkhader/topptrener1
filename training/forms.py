from django import forms
from .models import Session


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = [
            "title",
            "description",
            "sport_type",
            "location",
            "level",
            "start_datetime",
            "duration_minutes",
            "capacity",
            "price_per_person",
            "is_group",
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