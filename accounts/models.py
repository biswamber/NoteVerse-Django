from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE
    )

    following = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="profile_pictures/",
        default="profile_pictures/default.png"
    )

    bio = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username
    
class Notification(models.Model):

    NOTIFICATION_TYPES = (

        ("LIKE", "Like"),

        ("COMMENT", "Comment"),

        ("FOLLOW", "Follow"),

    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_notifications"
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    note = models.ForeignKey(
        "notes.Note",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.sender} -> {self.receiver} ({self.notification_type})"