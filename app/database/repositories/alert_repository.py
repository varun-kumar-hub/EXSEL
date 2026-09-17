from typing import List, Optional
from datetime import datetime
from app.database.client import get_db_client
from app.database.models import AlertModel
from app.mock.alerts import INITIAL_ALERTS
from app.utils.helpers import generate_uuid
from app.core.logging_config import logger


class AlertRepository:
    def __init__(self):
        self._memory_alerts: list[AlertModel] = []
        for a in INITIAL_ALERTS:
            self._memory_alerts.append(
                AlertModel(
                    id=a["id"],
                    alert_type=a["alert_type"],
                    severity=a["severity"],
                    title=a["title"],
                    message=a["message"],
                    is_read=a["is_read"],
                    created_at=a["created_at"],
                )
            )

    async def get_all_alerts(self, limit: int = 50) -> List[AlertModel]:
        client = get_db_client()
        if client:
            try:
                res = client.table("alerts").select("*").order("created_at", desc=True).limit(limit).execute()
                if res.data:
                    return [
                        AlertModel(
                            id=d["id"],
                            alert_type=d["alert_type"],
                            severity=d["severity"],
                            title=d["title"],
                            message=d["message"],
                            is_read=d.get("is_read", False),
                            created_at=datetime.fromisoformat(d["created_at"].replace("Z", "+00:00")),
                        )
                        for d in res.data
                    ]
            except Exception as e:
                logger.warning(f"Supabase error fetching alerts: {e}")
        return sorted(self._memory_alerts, key=lambda x: x.created_at, reverse=True)[:limit]

    async def get_active_alerts(self, limit: int = 4) -> List[AlertModel]:
        all_alerts = await self.get_all_alerts(limit=limit * 2)
        unread = [a for a in all_alerts if not a.is_read]
        return unread[:limit] if unread else all_alerts[:limit]

    async def create_alert(self, alert_type: str, severity: str, title: str, message: str) -> AlertModel:
        alert = AlertModel(
            id=generate_uuid(),
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            is_read=False,
            created_at=datetime.utcnow(),
        )
        self._memory_alerts.insert(0, alert)

        client = get_db_client()
        if client:
            try:
                client.table("alerts").insert({
                    "id": alert.id,
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    "title": alert.title,
                    "message": alert.message,
                    "is_read": False,
                    "created_at": alert.created_at.isoformat(),
                }).execute()
            except Exception as e:
                logger.warning(f"Supabase error creating alert: {e}")

        return alert

    async def mark_as_read(self, alert_id: str) -> bool:
        found = False
        for a in self._memory_alerts:
            if a.id == alert_id:
                a.is_read = True
                found = True
                break

        client = get_db_client()
        if client:
            try:
                client.table("alerts").update({"is_read": True}).eq("id", alert_id).execute()
            except Exception as e:
                logger.warning(f"Supabase error updating alert {alert_id}: {e}")

        return found

    async def delete_alert(self, alert_id: str) -> bool:
        initial_len = len(self._memory_alerts)
        self._memory_alerts = [a for a in self._memory_alerts if a.id != alert_id]

        client = get_db_client()
        if client:
            try:
                client.table("alerts").delete().eq("id", alert_id).execute()
            except Exception as e:
                logger.warning(f"Supabase error deleting alert: {e}")

        return len(self._memory_alerts) < initial_len


alert_repository = AlertRepository()
