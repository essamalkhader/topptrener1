from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["seats", "note_to_trainer"]
        widgets = {
            "seats": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "note_to_trainer": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }