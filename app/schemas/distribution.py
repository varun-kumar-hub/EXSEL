from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DistributionStepResponse(BaseModel):
    id: str
    step_order: int
    step_name: str
    gate_target: Optional[str] = None
    target_flow: Optional[float] = None
    status: str  # COMPLETED, ACTIVE, WAITING, FAILED
    notes: Optional[str] = None


class DistributionStatusResponse(BaseModel):
    id: str
    name: str
    status: str  # COMPLETED, ACTIVE, WAITING, FAILED
    current_step_index: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    steps: list[DistributionStepResponse]
