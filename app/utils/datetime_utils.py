from datetime import datetime, timedelta
from typing import Union


def format_timestamp(dt: Union[datetime, str, None]) -> str:
    """Format datetime as HH:MM:SS AM/PM"""
    if not dt:
        return "--"
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except Exception:
            return dt
    return dt.strftime("%I:%M:%S %p")


def format_short_time(dt: Union[datetime, str, None]) -> str:
    """Format datetime as HH:MM AM/PM"""
    if not dt:
        return "--"
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except Exception:
            return dt
    return dt.strftime("%I:%M %p")


def format_relative_time(dt: Union[datetime, str, None]) -> str:
    """Format relative time (e.g. 'Updated 10 sec ago', '2 min ago')"""
    if not dt:
        return "Updated just now"
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except Exception:
            return "Updated recently"

    now = datetime.utcnow()
    # Ensure naive comparison
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)

    diff = (now - dt).total_seconds()
    if diff < 5:
        return "Updated just now"
    if diff < 60:
        return f"Updated {int(diff)} sec ago"
    if diff < 3600:
        mins = int(diff // 60)
        return f"Updated {mins} min{'s' if mins > 1 else ''} ago"
    hours = int(diff // 3600)
    return f"Updated {hours} hour{'s' if hours > 1 else ''} ago"
