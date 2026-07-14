from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from accounts.models import Notification
from .models import Note, Like, Comment
from .forms import NoteForm, CommentForm
from .models import Bookmark
from django.db.models import Sum
from accounts.models import Follow


def home(request):

    query = request.GET.get("q", "")

    notes = Note.objects.all().order_by("-created_at")
    trending_notes = (
    Note.objects
    .annotate(total_likes=Count("likes"))
    .order_by("-views", "-total_likes")[:5]
)

    if query:

        notes = notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )

    paginator = Paginator(notes, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    liked_notes = []

    saved_notes = []

    if request.user.is_authenticated:

        liked_notes = Like.objects.filter(
            user=request.user
        ).values_list(
            "note_id",
            flat=True
        )

        saved_notes = Bookmark.objects.filter(
            user=request.user
        ).values_list(
            "note_id",
            flat=True
        )

    return render(

        request,

        "notes/home.html",

        {

            "page_obj": page_obj,

            "query": query,

            "liked_notes": liked_notes,

            "saved_notes": saved_notes,
            "trending_notes": trending_notes,

        }

    )


@login_required
def create_note(request):

    if request.method == "POST":

        form = NoteForm(request.POST, request.FILES)

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

        form = NoteForm(request.POST, request.FILES, instance=note)

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

        Notification.objects.filter(
            sender=request.user,
            receiver=note.author,
            note=note,
            notification_type="LIKE"
        ).delete()

    else:

        Like.objects.create(
            user=request.user,
            note=note
        )

        liked = True

        if request.user != note.author:

            Notification.objects.create(
                sender=request.user,
                receiver=note.author,
                note=note,
                notification_type="LIKE"
            )

    return JsonResponse({
        "liked": liked,
        "total_likes": note.likes.count()
    })


@login_required
def add_comment(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":

        content = request.POST.get("content")

        parent_id = request.POST.get("parent_id")

        parent = None

        if parent_id:
            parent = Comment.objects.get(id=parent_id)

        Comment.objects.create(
            user=request.user,
            note=note,
            content=content,
            parent=parent
        )

        if request.user != note.author:

            Notification.objects.create(
                sender=request.user,
                receiver=note.author,
                note=note,
                notification_type="COMMENT"
            )

    return redirect("note_detail", note.id)


def live_search(request):

    query = request.GET.get("q")

    results = []

    if query:

        notes = Note.objects.filter(
            title__icontains=query
        )[:8]

        for note in notes:

            results.append({

                "id": note.id,

                "title": note.title,

            })

    return JsonResponse(results, safe=False)


def note_detail(request, note_id):

    note = get_object_or_404(
        Note,
        id=note_id
    )
    note.views += 1
    note.save(update_fields=["views"])

    comments = note.comments.all().order_by("-created_at")

    context = {
        "note": note,
        "comments": comments,
    }

    return render(
        request,
        "notes/note_detail.html",
        context
    )

@login_required
def toggle_bookmark(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    bookmark = Bookmark.objects.filter(
        user=request.user,
        note=note
    )

    saved = False

    if bookmark.exists():

        bookmark.delete()

    else:

        Bookmark.objects.create(
            user=request.user,
            note=note
        )

        saved = True

    return JsonResponse({

        "saved": saved,

        "count": note.bookmarked_by.count()

    })

@login_required
def saved_notes(request):

    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related("note").order_by("-created_at")

    return render(
        request,
        "notes/saved_notes.html",
        {
            "bookmarks": bookmarks,
        }
    )

@login_required
def dashboard(request):

    notes = Note.objects.filter(
        author=request.user
    )

    recent_notes = notes.order_by("-created_at")[:5]

    total_notes = notes.count()

    total_likes = Like.objects.filter(
        note__author=request.user
    ).count()

    total_views = notes.aggregate(
        total=Sum("views")
    )["total"] or 0

    total_bookmarks = Bookmark.objects.filter(
        user=request.user
    ).count()

    followers = Follow.objects.filter(
        following=request.user
    ).count()

    following = Follow.objects.filter(
        follower=request.user
    ).count()

    context = {

        "total_notes": total_notes,

        "total_views": total_views,

        "total_likes": total_likes,

        "total_bookmarks": total_bookmarks,

        "followers": followers,

        "following": following,

        "recent_notes": recent_notes,

    }

    return render(
        request,
        "notes/dashboard.html",
        context
    )