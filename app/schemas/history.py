from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel


class SystemEventResponse(BaseModel):
    id: str
    timestamp: datetime
    event_type: str  # Gate Operation, Sensor Alert, Sequence, Auth, System
    device: str
    action: str
    status: str      # Success, Warning, Failed, Info
    operator: str
    metadata: Optional[dict[str, Any]] = None


class SystemEventFilter(BaseModel):
    search: Optional[str] = None
    event_type: Optional[str] = None
    device: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    page: int = 1
    page_size: int = 15
