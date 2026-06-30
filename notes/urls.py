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

]