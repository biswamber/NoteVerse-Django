from django import forms
from django.contrib.auth.models import User
from .models import Profile


class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "image",
            "bio",
        ]

        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write something about yourself..."
                }
            )
        }