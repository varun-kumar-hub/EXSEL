import asyncio
import random
from typing import Dict, Optional
from app.hardware.interface import HardwareInterface
from app.core.logging_config import logger


class HardwareSimulator(HardwareInterface):
    """
    Simulated Hardware Layer
    Simulates realistic hydraulic physics with smooth gradual drift
    and realistic gate transit transitions (OPENING/CLOSING).
    """

    def __init__(self):
        # Initial hydraulic baseline values
        self._water_level: float = 72.4
        self._flow_rate: float = 18.4
        self._pressure: float = 2.7
        self._secondary_flow: float = 8.9
        self._ph: float = 7.1
        self._turbidity: float = 2.4
        self._pump_on: bool = True

        # Gate states
        self._gates: Dict[str, str] = {
            "GATE_01": "OPEN",
            "GATE_02": "OPEN",
            "GATE_03": "OPEN",
            "GATE_04": "CLOSED",
        }

        self._connected: bool = True
        self._transit_tasks: Dict[str, asyncio.Task] = {}

    def step_simulation(self):
        """Gradually adjust values to simulate natural hydraulic dynamics"""
        # Water level gradual drift (-0.15% to +0.15%)
        drift = random.uniform(-0.15, 0.15)
        # Gentle mean reversion towards 72.0%
        mean_pull = (72.0 - self._water_level) * 0.05
        self._water_level = round(max(25.0, min(95.0, self._water_level + drift + mean_pull)), 1)

        # Flow rate affected by pump and gate states
        open_count = sum(1 for s in self._gates.values() if s == "OPEN")
        if self._pump_on and open_count > 0:
            target_flow = 14.0 + (open_count * 1.5)
            flow_drift = random.uniform(-0.2, 0.2)
            self._flow_rate = round(max(0.0, self._flow_rate + (target_flow - self._flow_rate) * 0.1 + flow_drift), 1)
        else:
            self._flow_rate = max(0.0, round(self._flow_rate * 0.8, 1))

        # Pressure dynamics
        target_p = 2.7 if self._pump_on else 0.5
        self._pressure = round(max(0.2, min(5.0, self._pressure + (target_p - self._pressure) * 0.1 + random.uniform(-0.05, 0.05))), 2)

        # Secondary sector flow
        self._secondary_flow = round(max(1.0, min(16.0, self._secondary_flow + random.uniform(-0.1, 0.1))), 1)

        # Water quality pH (6.9 - 7.3) and Turbidity (2.0 - 2.8)
        self._ph = round(max(6.5, min(8.0, self._ph + random.uniform(-0.02, 0.02))), 2)
        self._turbidity = round(max(1.5, min(3.5, self._turbidity + random.uniform(-0.03, 0.03))), 2)

    async def read_sensor(self, sensor_id: str) -> Optional[float]:
        self.step_simulation()
        mapping = {
            "SENS_LVL_01": self._water_level,
            "SENS_FLW_01": self._flow_rate,
            "SENS_PRS_01": self._pressure,
            "SENS_FLW_02": self._secondary_flow,
            "SENS_WQL_01": self._ph,
            "SENS_WQL_02": self._turbidity,
        }
        return mapping.get(sensor_id)

    async def read_all_sensors(self) -> Dict[str, float]:
        self.step_simulation()
        return {
            "SENS_LVL_01": self._water_level,
            "SENS_FLW_01": self._flow_rate,
            "SENS_PRS_01": self._pressure,
            "SENS_FLW_02": self._secondary_flow,
            "SENS_WQL_01": self._ph,
            "SENS_WQL_02": self._turbidity,
        }

    async def _transit_gate(self, gate_id: str, target_state: str, transit_seconds: float = 2.0):
        transit_state = "OPENING" if target_state == "OPEN" else "CLOSING"
        self._gates[gate_id] = transit_state
        logger.info(f"[SIMULATOR] Gate {gate_id} motor engaged -> {transit_state}")
        await asyncio.sleep(transit_seconds)
        self._gates[gate_id] = target_state
        logger.info(f"[SIMULATOR] Gate {gate_id} limit switch hit -> {target_state}")

    async def open_gate(self, gate_id: str) -> bool:
        if gate_id not in self._gates:
            return False
        if self._gates[gate_id] == "OPEN":
            return True

        # Cancel any active transit task
        if gate_id in self._transit_tasks and not self._transit_tasks[gate_id].done():
            self._transit_tasks[gate_id].cancel()

        self._transit_tasks[gate_id] = asyncio.create_task(
            self._transit_gate(gate_id, "OPEN")
        )
        return True

    async def close_gate(self, gate_id: str) -> bool:
        if gate_id not in self._gates:
            return False
        if self._gates[gate_id] == "CLOSED":
            return True

        if gate_id in self._transit_tasks and not self._transit_tasks[gate_id].done():
            self._transit_tasks[gate_id].cancel()

        self._transit_tasks[gate_id] = asyncio.create_task(
            self._transit_gate(gate_id, "CLOSED")
        )
        return True

    async def get_gate_status(self, gate_id: str) -> str:
        return self._gates.get(gate_id, "CLOSED")

    async def get_pump_status(self) -> str:
        return "ON" if self._pump_on else "OFF"

    async def set_pump(self, state: bool) -> bool:
        self._pump_on = state
        logger.info(f"[SIMULATOR] Pump state changed to {'ON' if state else 'OFF'}")
        return True

    async def is_connected(self) -> bool:
        return self._connected
