from typing import Dict, Optional
from app.hardware.interface import HardwareInterface
from app.core.logging_config import logger


class MQTTClient(HardwareInterface):
    """MQTT Hardware Interface implementation stub"""

    def __init__(self, broker: str = "localhost", port: int = 1883):
        self.broker = broker
        self.port = port
        self._connected = False

    async def read_sensor(self, sensor_id: str) -> Optional[float]:
        return None

    async def read_all_sensors(self) -> Dict[str, float]:
        return {}

    async def open_gate(self, gate_id: str) -> bool:
        logger.info(f"[MQTT] Publish command: water/gate/{gate_id}/cmd OPEN")
        return True

    async def close_gate(self, gate_id: str) -> bool:
        logger.info(f"[MQTT] Publish command: water/gate/{gate_id}/cmd CLOSE")
        return True

    async def get_gate_status(self, gate_id: str) -> str:
        return "CLOSED"

    async def get_pump_status(self) -> str:
        return "OFF"

    async def set_pump(self, state: bool) -> bool:
        logger.info(f"[MQTT] Publish command: water/pump/cmd {'ON' if state else 'OFF'}")
        return True

    async def is_connected(self) -> bool:
        return self._connected


class SerialClient(HardwareInterface):
    """USB Serial Hardware Interface implementation stub"""

    def __init__(self, port: str = "COM3", baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self._connected = False

    async def read_sensor(self, sensor_id: str) -> Optional[float]:
        return None

    async def read_all_sensors(self) -> Dict[str, float]:
        return {}

    async def open_gate(self, gate_id: str) -> bool:
        logger.info(f"[SERIAL] Send command: AT+GATE={gate_id},OPEN")
        return True

    async def close_gate(self, gate_id: str) -> bool:
        logger.info(f"[SERIAL] Send command: AT+GATE={gate_id},CLOSE")
        return True

    async def get_gate_status(self, gate_id: str) -> str:
        return "CLOSED"

    async def get_pump_status(self) -> str:
        return "OFF"

    async def set_pump(self, state: bool) -> bool:
        logger.info(f"[SERIAL] Send command: AT+PUMP={'1' if state else '0'}")
        return True

    async def is_connected(self) -> bool:
        return self._connected
