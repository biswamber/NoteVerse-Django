from .models import Notification


def notification_data(request):

    if request.user.is_authenticated:

        notifications = Notification.objects.filter(
            receiver=request.user
        ).order_by("-created_at")[:5]

        unread = Notification.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()

        return {
            "notification_count": unread,
            "latest_notifications": notifications,
        }

    return {
        "notification_count": 0,
        "latest_notifications": [],
    }