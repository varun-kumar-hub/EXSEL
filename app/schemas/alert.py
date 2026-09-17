from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: str
    alert_type: str
    severity: str  # critical, warning, info
    title: str
    message: str
    is_read: bool = False
    created_at: datetime


class AlertCreate(BaseModel):
    alert_type: str
    severity: str
    title: str
    message: str
