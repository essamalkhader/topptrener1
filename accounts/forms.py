from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TrainerProfile, UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_trainer = forms.BooleanField(
        required=False,
        label="I want to register as a trainer",
        help_text="Check this if you are a coach or trainer offering sessions."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_trainer")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["photo", "bio"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }


class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ["photo", "bio", "specialties"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
            "specialties": forms.Textarea(attrs={"rows": 3}),
        }