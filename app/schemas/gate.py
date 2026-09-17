from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class GateResponse(BaseModel):
    id: str
    name: str
    location: str
    status: str  # OPEN, CLOSED, OPENING, CLOSING, ERROR
    mode: str    # AUTO, MANUAL
    is_connected: bool = True
    last_changed_at: Optional[datetime] = None


class GateOperationRequest(BaseModel):
    operation: str = Field(..., description="'OPEN' or 'CLOSE'")
    reason: Optional[str] = "Manual operator action"


class GateModeRequest(BaseModel):
    mode: str = Field(..., description="'AUTO' or 'MANUAL'")
