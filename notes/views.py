from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Note, Like, Comment
from .forms import NoteForm, CommentForm


def home(request):

    query = request.GET.get("q", "")

    notes = Note.objects.all().order_by("-created_at")

    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )

    paginator = Paginator(notes, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "notes/home.html",
        {
            "page_obj": page_obj,
            "query": query,
        }
    )


@login_required
def create_note(request):

    if request.method == "POST":

        form = NoteForm(request.POST)

        if form.is_valid():

            note = form.save(commit=False)

            note.author = request.user

            note.save()

            return redirect("home")

    else:

        form = NoteForm()

    return render(
        request,
        "notes/create_note.html",
        {
            "form": form
        }
    )


@login_required
def edit_note(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    if note.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":

        form = NoteForm(request.POST, instance=note)

        if form.is_valid():

            form.save()

            return redirect("home")

    else:

        form = NoteForm(instance=note)

    return render(
        request,
        "notes/edit_note.html",
        {
            "form": form
        }
    )


@login_required
def delete_note(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    if note.author != request.user:
        return HttpResponseForbidden()

    note.delete()

    return redirect("home")


@login_required
def toggle_like(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    like = Like.objects.filter(
        user=request.user,
        note=note
    )

    liked = False

    if like.exists():
        like.delete()
    else:
        Like.objects.create(
            user=request.user,
            note=note
        )
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": note.likes.count()
    })


@login_required
def add_comment(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.user = request.user

            comment.note = note

            comment.save()

    return redirect("home")