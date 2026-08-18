from core.models import ActivityLog

def log_activity(user, action, **meta):
    ActivityLog.objects.create(
        user=user,
        action=action,
        meta=meta or {}
    )
def require_steps_1_4(user):
    return user and (user.role in ["ADMIN", "MASTER_ADMIN"] or user.can_steps_1_4)

def require_steps_5_7(user):
    return user and (user.role in ["ADMIN", "MASTER_ADMIN"] or user.can_steps_5_7)

from core.models import Notification


def create_notification(user, title, message="", url=""):
    if user is None:
        return

    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        url=url,
    )

from core.models import ActivityLog


def create_activity(user, action):

    ActivityLog.objects.create(
        user=user,
        action=action
    )