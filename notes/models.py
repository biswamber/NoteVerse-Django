from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    content = models.TextField()

    image = models.ImageField(
    upload_to="notes/",
    blank=True,
    null=True
)
    views = models.PositiveIntegerField(
    default=0
)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Like(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    class Meta:
        unique_together = ("user", "note")

    def __str__(self):
        return f"{self.user.username} likes {self.note.title}"
    
class Bookmark(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name="bookmarked_by"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "user",
            "note",
        )

    def __str__(self):

        return f"{self.user.username} bookmarked {self.note.title}"


class Comment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    content = models.TextField()

    parent = models.ForeignKey(
    "self",
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name="replies"
)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.note.title}"