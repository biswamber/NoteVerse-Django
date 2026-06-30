from django import forms
from .models import Note, Comment


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ["title", "content"]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]