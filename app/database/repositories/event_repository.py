from typing import List, Optional, Tuple
from datetime import datetime, timedelta
from app.database.client import get_db_client
from app.database.models import EventModel
from app.utils.helpers import generate_uuid
from app.core.logging_config import logger


class EventRepository:
    def __init__(self):
        now = datetime.utcnow()
        self._memory_events: list[EventModel] = [
            EventModel(
                id="evt-1",
                timestamp=now - timedelta(minutes=3),
                event_type="Gate Operation",
                device="Gate 01",
                action="OPEN",
                status="Success",
                operator="Operator Alex",
                metadata={"source": "Auto-Sequence"},
            ),
            EventModel(
                id="evt-2",
                timestamp=now - timedelta(minutes=14),
                event_type="Sensor Alert",
                device="Secondary Flow",
                action="ALERT",
                status="Warning",
                operator="System",
                metadata={"reading": 14.2, "unit": "L/min"},
            ),
            EventModel(
                id="evt-3",
                timestamp=now - timedelta(minutes=35),
                event_type="Sequence",
                device="Sector B",
                action="START",
                status="Success",
                operator="Chief Admin",
                metadata={"sequence": "Sector B Distribution"},
            ),
            EventModel(
                id="evt-4",
                timestamp=now - timedelta(hours=2),
                event_type="Gate Operation",
                device="Gate 03",
                action="OPEN",
                status="Success",
                operator="Chief Admin",
                metadata={"source": "Manual Override"},
            ),
            EventModel(
                id="evt-5",
                timestamp=now - timedelta(hours=4),
                event_type="Auth",
                device="Session Auth",
                action="LOGIN",
                status="Success",
                operator="Operator Alex",
                metadata={"client": "Web Desktop"},
            ),
            EventModel(
                id="evt-6",
                timestamp=now - timedelta(hours=5),
                event_type="System",
                device="Telemetry Node",
                action="HEARTBEAT",
                status="Info",
                operator="System",
                metadata={"nodes_checked": 5},
            ),
            EventModel(
                id="evt-7",
                timestamp=now - timedelta(hours=8),
                event_type="Gate Operation",
                device="Gate 04",
                action="CLOSE",
                status="Success",
                operator="Operator Alex",
                metadata={"reason": "Night spillway isolation"},
            ),
        ]

    async def record_event(
        self,
        event_type: str,
        device: str,
        action: str,
        status: str = "Success",
        operator: str = "System",
        metadata: dict = None,
    ) -> EventModel:
        event = EventModel(
            id=generate_uuid(),
            timestamp=datetime.utcnow(),
            event_type=event_type,
            device=device,
            action=action,
            status=status,
            operator=operator,
            metadata=metadata or {},
        )
        self._memory_events.insert(0, event)

        client = get_db_client()
        if client:
            try:
                client.table("system_events").insert({
                    "id": event.id,
                    "timestamp": event.timestamp.isoformat(),
                    "event_type": event.event_type,
                    "device": event.device,
                    "action": event.action,
                    "status": event.status,
                    "operator": event.operator,
                    "metadata": event.metadata,
                }).execute()
            except Exception as e:
                logger.warning(f"Supabase error logging event: {e}")

        return event

    async def query_events(
        self,
        search: Optional[str] = None,
        event_type: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 15,
    ) -> Tuple[List[EventModel], int]:
        filtered = self._memory_events[:]

        if search:
            s = search.lower()
            filtered = [
                e for e in filtered
                if s in e.device.lower()
                or s in e.action.lower()
                or s in e.event_type.lower()
                or s in e.operator.lower()
            ]

        if event_type and event_type != "All":
            filtered = [e for e in filtered if e.event_type == event_type]

        if status and status != "All":
            filtered = [e for e in filtered if e.status.lower() == status.lower()]

        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end], total

    async def get_all_events(self) -> List[EventModel]:
        return sorted(self._memory_events, key=lambda x: x.timestamp, reverse=True)


event_repository = EventRepository()
