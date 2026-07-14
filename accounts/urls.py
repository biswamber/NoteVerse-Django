from django.urls import path
from . import views

urlpatterns = [

    path("register/", views.register, name="register"),

    path("login/", views.user_login, name="login"),

    path("logout/", views.user_logout, name="logout"),

    path("profile/", views.profile, name="profile"),

    path(
        "user/<str:username>/",
        views.user_profile,
        name="user_profile"
    ),

    path(
        "follow/<str:username>/",
        views.toggle_follow,
        name="toggle_follow"
    ),
    
    path(
    "edit-profile/",
    views.edit_profile,
    name="edit_profile",
),

path(
    "notifications/",
    views.notifications,
    name="notifications",
),

path(
    "followers/<str:username>/",
    views.followers_list,
    name="followers_list",
),

path(
    "following/<str:username>/",
    views.following_list,
    name="following_list",
),
]