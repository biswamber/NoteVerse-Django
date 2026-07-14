from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from notes.models import Note
from django.shortcuts import get_object_or_404
from .models import Follow
from .models import Notification
from django.contrib import messages
from .forms import EditProfileForm
from .forms import EditProfileForm, ProfileForm
from django.http import JsonResponse


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
        "is_following": Follow.objects.filter(
    follower=request.user,
    following=profile_user
).exists(),
    }

    return render(
        request,
        "accounts/user_profile.html",
        context
    )

@login_required
def toggle_follow(request, username):

    profile_user = get_object_or_404(User, username=username)

    if profile_user == request.user:
        return JsonResponse({"error": "You cannot follow yourself."}, status=400)

    follow = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    )

    followed = False

    if follow.exists():

        follow.delete()

        Notification.objects.filter(
            sender=request.user,
            receiver=profile_user,
            notification_type="FOLLOW"
        ).delete()

    else:

        Follow.objects.create(
            follower=request.user,
            following=profile_user
        )

        followed = True

        Notification.objects.create(
            sender=request.user,
            receiver=profile_user,
            notification_type="FOLLOW"
        )

    return JsonResponse({

        "followed": followed,

        "followers": profile_user.followers.count()

    })

@login_required
def edit_profile(request):

    if request.method == "POST":

        user_form = EditProfileForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile_form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        user_form = EditProfileForm(
            instance=request.user
        )

        profile_form = ProfileForm(
            instance=request.user.profile
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        }
    )

@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        receiver=request.user
    ).order_by("-created_at")

    notifications.filter(
        is_read=False
    ).update(is_read=True)

    return render(
        request,
        "accounts/notifications.html",
        {
            "notifications": notifications
        }
    )
@login_required
def followers_list(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    followers = Follow.objects.filter(
        following=profile_user
    )

    return render(
        request,
        "accounts/followers.html",
        {
            "profile_user": profile_user,
            "followers": followers,
        }
    )


@login_required
def following_list(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    following = Follow.objects.filter(
        follower=profile_user
    )

    return render(
        request,
        "accounts/following.html",
        {
            "profile_user": profile_user,
            "following": following,
        }
    )