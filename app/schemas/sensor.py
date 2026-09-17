from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SensorResponse(BaseModel):
    id: str
    name: str
    sensor_type: str
    unit: str
    minimum_threshold: float
    maximum_threshold: float
    status: str
    last_reading: Optional[float] = None
    last_updated_at: Optional[datetime] = None


class SensorReadingPoint(BaseModel):
    timestamp: datetime
    value: float


class SensorHistoryResponse(BaseModel):
    sensor_id: str
    name: str
    unit: str
    readings: list[SensorReadingPoint]
