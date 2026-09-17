from typing import List, Optional, Dict, Any
from app.database.repositories import sensor_repository, alert_repository, event_repository
from app.database.models import SensorModel
from app.hardware import get_hardware
from app.core.exceptions import SensorNotFoundError
from app.core.logging_config import logger


class SensorService:
    def __init__(self):
        self.hardware = get_hardware()

    async def get_all_sensors(self) -> List[SensorModel]:
        # Sync live values from hardware
        readings = await self.hardware.read_all_sensors()
        sensors = await sensor_repository.get_all_sensors()

        for s in sensors:
            if s.id in readings:
                val = readings[s.id]
                await self._check_thresholds(s, val)
                await sensor_repository.update_reading(s.id, val, status="ONLINE")
                s.last_reading = val

        return sensors

    async def get_sensor(self, sensor_id: str) -> SensorModel:
        sensor = await sensor_repository.get_by_id(sensor_id)
        if not sensor:
            raise SensorNotFoundError(sensor_id)
        val = await self.hardware.read_sensor(sensor_id)
        if val is not None:
            await self._check_thresholds(sensor, val)
            await sensor_repository.update_reading(sensor_id, val)
            sensor.last_reading = val
        return sensor

    async def get_sensor_history(self, sensor_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        sensor = await sensor_repository.get_by_id(sensor_id)
        if not sensor:
            raise SensorNotFoundError(sensor_id)
        return await sensor_repository.get_history(sensor_id, hours=hours)

    async def _check_thresholds(self, sensor: SensorModel, value: float):
        """Evaluate reading against min/max thresholds and generate alerts"""
        if value < sensor.minimum_threshold:
            logger.warning(f"Sensor {sensor.name} breached LOW threshold: {value} < {sensor.minimum_threshold} {sensor.unit}")
            # Generate alert
            await alert_repository.create_alert(
                alert_type=f"low_{sensor.sensor_type}",
                severity="critical" if sensor.sensor_type == "level" else "warning",
                title=f"{sensor.name} Below Threshold",
                message=f"Current reading {value:.1f} {sensor.unit} is below minimum threshold of {sensor.minimum_threshold:.1f} {sensor.unit}.",
            )
            await event_repository.record_event(
                event_type="Sensor Alert",
                device=sensor.name,
                action="THRESHOLD_BREACH_LOW",
                status="Warning",
                operator="Threshold Engine",
                metadata={"reading": value, "threshold": sensor.minimum_threshold},
            )

        elif value > sensor.maximum_threshold:
            logger.warning(f"Sensor {sensor.name} breached HIGH threshold: {value} > {sensor.maximum_threshold} {sensor.unit}")
            await alert_repository.create_alert(
                alert_type=f"high_{sensor.sensor_type}",
                severity="critical" if sensor.sensor_type in ("pressure", "level") else "warning",
                title=f"{sensor.name} Above Threshold",
                message=f"Current reading {value:.1f} {sensor.unit} exceeded safety maximum of {sensor.maximum_threshold:.1f} {sensor.unit}.",
            )
            await event_repository.record_event(
                event_type="Sensor Alert",
                device=sensor.name,
                action="THRESHOLD_BREACH_HIGH",
                status="Warning",
                operator="Threshold Engine",
                metadata={"reading": value, "threshold": sensor.maximum_threshold},
            )


sensor_service = SensorService()
