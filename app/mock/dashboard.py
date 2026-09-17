"""
Mock Dashboard Telemetry and Timeseries Generator
"""
from datetime import datetime, timedelta
import random


def generate_timeseries(hours: int = 24, base_val: float = 72.0, variance: float = 3.0, points_count: int = 30) -> list[dict]:
    """Generate realistic smooth continuous timeseries data"""
    now = datetime.utcnow()
    step_minutes = (hours * 60) // points_count
    points = []
    current_val = base_val

    for i in range(points_count, 0, -1):
        ts = now - timedelta(minutes=i * step_minutes)
        # Random walk for realism
        current_val += random.uniform(-0.6, 0.6)
        current_val = max(base_val - variance, min(base_val + variance, current_val))
        points.append({
            "timestamp": ts.strftime("%H:%M" if hours <= 24 else "%b %d %H:%M"),
            "value": round(current_val, 1),
        })

    return points
