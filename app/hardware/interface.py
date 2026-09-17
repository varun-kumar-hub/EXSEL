from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class HardwareInterface(ABC):
    """
    Abstract Hardware Interface
    Decouples business logic and UI from physical electronics (ESP8266/ESP32/relays/sensors).
    """

    @abstractmethod
    async def read_sensor(self, sensor_id: str) -> Optional[float]:
        """Read instantaneous value from specific sensor"""
        pass

    @abstractmethod
    async def read_all_sensors(self) -> Dict[str, float]:
        """Read all live sensor values in one batch"""
        pass

    @abstractmethod
    async def open_gate(self, gate_id: str) -> bool:
        """Command physical actuator to open gate"""
        pass

    @abstractmethod
    async def close_gate(self, gate_id: str) -> bool:
        """Command physical actuator to close gate"""
        pass

    @abstractmethod
    async def get_gate_status(self, gate_id: str) -> str:
        """Get current physical limit switch status of gate (OPEN, CLOSED, OPENING, CLOSING)"""
        pass

    @abstractmethod
    async def get_pump_status(self) -> str:
        """Get pump operation state (ON, OFF)"""
        pass

    @abstractmethod
    async def set_pump(self, state: bool) -> bool:
        """Turn main distribution pump ON or OFF"""
        pass

    @abstractmethod
    async def is_connected(self) -> bool:
        """Verify device connectivity heartbeat"""
        pass
