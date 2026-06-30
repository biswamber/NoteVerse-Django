from django.contrib import admin
from .models import Note, Like, Comment

admin.site.register(Note)
admin.site.register(Like)
admin.site.register(Comment)