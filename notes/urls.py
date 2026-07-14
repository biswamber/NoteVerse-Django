from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path(
        "create/",
        views.create_note,
        name="create_note"
    ),

    path(
        "edit/<int:note_id>/",
        views.edit_note,
        name="edit_note"
    ),

    path(
        "delete/<int:note_id>/",
        views.delete_note,
        name="delete_note"
    ),

    path(

"like/<int:note_id>/",

views.toggle_like,

name="toggle_like"

),
    path(
    "comment/<int:note_id>/",
    views.add_comment,
    name="add_comment"
),

path(
    "live-search/",
    views.live_search,
    name="live_search",
),

path(
    "note/<int:note_id>/",
    views.note_detail,
    name="note_detail",
),

path(
    "bookmark/<int:note_id>/",
    views.toggle_bookmark,
    name="toggle_bookmark",
),
path(
    "saved-notes/",
    views.saved_notes,
    name="saved_notes",
),

path(
    "dashboard/",
    views.dashboard,
    name="dashboard",
),

]