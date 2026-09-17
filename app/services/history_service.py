from typing import Optional, Dict, Any, List
import csv
import io
from app.database.repositories import event_repository
from app.database.models import EventModel


class HistoryService:
    async def get_events(
        self,
        search: Optional[str] = None,
        event_type: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 15,
    ) -> Dict[str, Any]:
        events, total = await event_repository.query_events(
            search=search,
            event_type=event_type,
            status=status,
            page=page,
            page_size=page_size,
        )
        total_pages = max(1, (total + page_size - 1) // page_size)

        return {
            "items": [
                {
                    "id": e.id,
                    "timestamp": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_type": e.event_type,
                    "device": e.device,
                    "action": e.action,
                    "status": e.status,
                    "operator": e.operator,
                    "metadata": e.metadata,
                }
                for e in events
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    async def export_csv(self) -> str:
        """Export full event log as CSV string"""
        events = await event_repository.get_all_events()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Timestamp", "Event Type", "Device", "Action", "Status", "Operator"])

        for e in events:
            writer.writerow([
                e.id,
                e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                e.event_type,
                e.device,
                e.action,
                e.status,
                e.operator,
            ])

        return output.getvalue()


history_service = HistoryService()
