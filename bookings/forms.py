from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["seats", "note_to_trainer"]
        widgets = {
            "seats": forms.NumberInput(attrs={
                "min": 1,
                "class": "w-20 text-center text-lg font-bold border border-slate-200 rounded-lg p-2 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none"
            }),
            "note_to_trainer": forms.Textarea(attrs={
                "rows": 3,
                "class": "w-full bg-white border border-slate-200 rounded-lg p-4 text-slate-900 placeholder:text-slate-400 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all resize-none text-sm"
            }),
        }