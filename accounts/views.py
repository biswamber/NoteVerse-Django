from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from notes.models import Note
from django.shortcuts import get_object_or_404
from .models import Follow


def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")

    else:

        form = UserCreationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect("home")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form},
    )


def user_logout(request):

    logout(request)

    return redirect("home")

@login_required
def profile(request):

    notes = Note.objects.filter(author=request.user)

    total_notes = notes.count()

    total_likes = 0

    for note in notes:
        total_likes += note.likes.count()

    context = {
        "total_notes": total_notes,
        "total_likes": total_likes,
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )

def user_profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    notes = Note.objects.filter(
        author=profile_user
    ).order_by("-created_at")

    total_likes = 0

    for note in notes:
        total_likes += note.likes.count()

    context = {
        "profile_user": profile_user,
        "notes": notes,
        "total_notes": notes.count(),
        "total_likes": total_likes,
    }

    return render(
        request,
        "accounts/user_profile.html",
        context
    )

@login_required
def toggle_follow(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    if profile_user == request.user:
        return redirect("user_profile", username=username)

    follow = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    )

    if follow.exists():
        follow.delete()
    else:
        Follow.objects.create(
            follower=request.user,
            following=profile_user
        )

    return redirect(
        "user_profile",
        username=username
    )