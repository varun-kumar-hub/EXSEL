from typing import Optional
from app.hardware.interface import HardwareInterface
from app.hardware.simulator import HardwareSimulator
from app.hardware.esp_client import ESPClient
from app.hardware.mqtt_client import MQTTClient
from app.config.settings import settings
from app.core.logging_config import logger

_hardware_instance: Optional[HardwareInterface] = None


def get_hardware() -> HardwareInterface:
    global _hardware_instance
    if _hardware_instance is None:
        mode = settings.HARDWARE_MODE.lower()
        if mode == "esp":
            logger.info("Initializing ESP8266/ESP32 Hardware Client.")
            _hardware_instance = ESPClient()
        elif mode == "mqtt":
            logger.info("Initializing MQTT Hardware Client.")
            _hardware_instance = MQTTClient(broker=settings.MQTT_BROKER or "localhost", port=settings.MQTT_PORT)
        else:
            logger.info("Initializing Realistic Hydraulic Simulation Engine.")
            _hardware_instance = HardwareSimulator()
    return _hardware_instance


__all__ = [
    "HardwareInterface",
    "HardwareSimulator",
    "ESPClient",
    "MQTTClient",
    "get_hardware",
]
