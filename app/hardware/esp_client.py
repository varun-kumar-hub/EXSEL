from typing import Dict, Optional
import httpx
from app.hardware.interface import HardwareInterface
from app.config.settings import settings
from app.core.logging_config import logger


class ESPClient(HardwareInterface):
    """
    Physical Hardware Client for ESP8266 / ESP32 microcontroller
    Communicates via REST JSON endpoints over local network.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or settings.ESP_DEVICE_URL or "http://192.168.1.100").rstrip("/")
        self.timeout = httpx.Timeout(4.0)

    async def read_sensor(self, sensor_id: str) -> Optional[float]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.get(f"{self.base_url}/api/sensor/{sensor_id}")
                if res.status_code == 200:
                    return float(res.json().get("value", 0.0))
        except Exception as e:
            logger.warning(f"ESPClient read_sensor failed: {e}")
        return None

    async def read_all_sensors(self) -> Dict[str, float]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.get(f"{self.base_url}/api/sensors")
                if res.status_code == 200:
                    return res.json().get("readings", {})
        except Exception as e:
            logger.warning(f"ESPClient read_all_sensors failed: {e}")
        return {}

    async def open_gate(self, gate_id: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(f"{self.base_url}/api/gate/{gate_id}/open")
                return res.status_code == 200
        except Exception as e:
            logger.error(f"ESPClient open_gate failed: {e}")
            return False

    async def close_gate(self, gate_id: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(f"{self.base_url}/api/gate/{gate_id}/close")
                return res.status_code == 200
        except Exception as e:
            logger.error(f"ESPClient close_gate failed: {e}")
            return False

    async def get_gate_status(self, gate_id: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.get(f"{self.base_url}/api/gate/{gate_id}/status")
                if res.status_code == 200:
                    return res.json().get("status", "CLOSED")
        except Exception as e:
            logger.warning(f"ESPClient get_gate_status failed: {e}")
        return "ERROR"

    async def get_pump_status(self) -> str:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.get(f"{self.base_url}/api/pump/status")
                if res.status_code == 200:
                    return res.json().get("status", "OFF")
        except Exception as e:
            logger.warning(f"ESPClient get_pump_status failed: {e}")
        return "OFF"

    async def set_pump(self, state: bool) -> bool:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                action = "start" if state else "stop"
                res = await client.post(f"{self.base_url}/api/pump/{action}")
                return res.status_code == 200
        except Exception as e:
            logger.error(f"ESPClient set_pump failed: {e}")
            return False

    async def is_connected(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(2.0)) as client:
                res = await client.get(f"{self.base_url}/api/heartbeat")
                return res.status_code == 200
        except Exception:
            return False
