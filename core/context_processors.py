from core.models import Notification


def notifications_context(request):
    if not request.user.is_authenticated:
        return {
            "unread_notifications_count": 0,
            "latest_notifications": [],
        }

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")[:10]

    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return {
        "unread_notifications_count": unread_count,
        "latest_notifications": notifications,
    }