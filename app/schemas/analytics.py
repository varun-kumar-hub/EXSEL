from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    avg_water_level: float
    max_flow_rate: float
    min_flow_rate: float
    system_uptime_pct: float
    total_gate_operations: int
    estimated_water_loss_liters: float


class TimeseriesPoint(BaseModel):
    timestamp: str
    value: float


class GateOperationPerDay(BaseModel):
    date: str
    count: int


class AnalyticsResponse(BaseModel):
    summary: AnalyticsSummary
    water_level_trend: list[TimeseriesPoint]
    flow_rate_trend: list[TimeseriesPoint]
    gate_operations_daily: list[GateOperationPerDay]
