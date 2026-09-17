from typing import Sequence
import numpy as np


def compute_average(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return float(np.mean(values))


def compute_max(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return float(np.max(values))


def compute_min(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return float(np.min(values))


def estimate_water_loss(total_inflow_liters: float, total_outflow_liters: float) -> float:
    """Calculate estimated water loss in distribution system"""
    loss = max(0.0, total_inflow_liters - total_outflow_liters)
    return round(loss, 1)
