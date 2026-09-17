from typing import List, Dict, Any
from app.core.logging_config import logger


class NotificationService:
    """Manages notifications across Web, Email, and Push channels"""

    async def send_notification(self, title: str, message: str, channels: List[str] = None):
        channels = channels or ["in-app"]
        for ch in channels:
            logger.info(f"[NOTIF] Dispatched notification over '{ch}': {title} - {message}")
        return True


notification_service = NotificationService()
