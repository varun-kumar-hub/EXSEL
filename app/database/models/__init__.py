from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any


@dataclass
class UserModel:
    id: str
    email: str
    password_hash: str
    full_name: Optional[str] = None
    role: str = "viewer"
    avatar_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class GateModel:
    id: str
    name: str
    location: str
    status: str = "CLOSED"  # OPEN, CLOSED, OPENING, CLOSING, ERROR
    mode: str = "AUTO"      # AUTO, MANUAL
    is_connected: bool = True
    last_changed_at: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SensorModel:
    id: str
    name: str
    sensor_type: str
    unit: str
    minimum_threshold: float
    maximum_threshold: float
    status: str = "ONLINE"
    last_reading: Optional[float] = None
    last_updated_at: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AlertModel:
    id: str
    alert_type: str
    severity: str
    title: str
    message: str
    is_read: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EventModel:
    id: str
    timestamp: datetime
    event_type: str
    device: str
    action: str
    status: str
    operator: str = "System"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DistributionStepModel:
    id: str
    step_order: int
    step_name: str
    status: str = "WAITING"
    gate_target: Optional[str] = None
    target_flow: Optional[float] = None
    notes: Optional[str] = None


@dataclass
class DistributionSequenceModel:
    id: str
    name: str
    status: str = "WAITING"
    current_step_index: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    steps: list[DistributionStepModel] = field(default_factory=list)
