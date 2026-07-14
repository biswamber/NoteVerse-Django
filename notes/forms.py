from django import forms
from .models import Note, Comment


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note

        fields = [
            "title",
            "content",
            "image",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter note title"
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Write your note here..."
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = ["content"]

        widgets = {

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Write a comment..."
                }
            ),

        }