from django.contrib import admin
from .models import Note, Comment, Like, Bookmark

admin.site.register(Note)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Bookmark)