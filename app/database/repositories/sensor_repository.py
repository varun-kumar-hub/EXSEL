from typing import Optional, List
from datetime import datetime, timedelta
from app.database.client import get_db_client
from app.database.models import SensorModel
from app.mock.sensors import INITIAL_SENSORS
from app.mock.dashboard import generate_timeseries
from app.core.logging_config import logger


class SensorRepository:
    def __init__(self):
        self._memory_sensors: dict[str, SensorModel] = {}
        self._history_readings: dict[str, list[dict]] = {}

        for s in INITIAL_SENSORS:
            sensor = SensorModel(
                id=s["id"],
                name=s["name"],
                sensor_type=s["sensor_type"],
                unit=s["unit"],
                minimum_threshold=s["minimum_threshold"],
                maximum_threshold=s["maximum_threshold"],
                status=s["status"],
                last_reading=s["last_reading"],
                last_updated_at=s["last_updated_at"],
            )
            self._memory_sensors[sensor.id] = sensor

            # Pre-generate some historical points
            base = s["last_reading"] if s["last_reading"] is not None else 50.0
            self._history_readings[sensor.id] = generate_timeseries(
                hours=24, base_val=base, variance=base * 0.08, points_count=24
            )

    async def get_all_sensors(self) -> List[SensorModel]:
        client = get_db_client()
        if client:
            try:
                res = client.table("sensors").select("*").order("id").execute()
                if res.data:
                    return [
                        SensorModel(
                            id=d["id"],
                            name=d["name"],
                            sensor_type=d["sensor_type"],
                            unit=d["unit"],
                            minimum_threshold=float(d["minimum_threshold"]),
                            maximum_threshold=float(d["maximum_threshold"]),
                            status=d.get("status", "ONLINE"),
                            last_reading=float(d["last_reading"]) if d.get("last_reading") is not None else None,
                            last_updated_at=datetime.fromisoformat(d["last_updated_at"].replace("Z", "+00:00")) if d.get("last_updated_at") else datetime.utcnow(),
                        )
                        for d in res.data
                    ]
            except Exception as e:
                logger.warning(f"Supabase error fetching sensors: {e}")
        return list(self._memory_sensors.values())

    async def get_by_id(self, sensor_id: str) -> Optional[SensorModel]:
        client = get_db_client()
        if client:
            try:
                res = client.table("sensors").select("*").eq("id", sensor_id).execute()
                if res.data:
                    d = res.data[0]
                    return SensorModel(
                        id=d["id"],
                        name=d["name"],
                        sensor_type=d["sensor_type"],
                        unit=d["unit"],
                        minimum_threshold=float(d["minimum_threshold"]),
                        maximum_threshold=float(d["maximum_threshold"]),
                        status=d.get("status", "ONLINE"),
                        last_reading=float(d["last_reading"]) if d.get("last_reading") is not None else None,
                        last_updated_at=datetime.fromisoformat(d["last_updated_at"].replace("Z", "+00:00")) if d.get("last_updated_at") else datetime.utcnow(),
                    )
            except Exception as e:
                logger.warning(f"Supabase error fetching sensor {sensor_id}: {e}")
        return self._memory_sensors.get(sensor_id)

    async def update_reading(self, sensor_id: str, value: float, status: str = "ONLINE") -> Optional[SensorModel]:
        sensor = self._memory_sensors.get(sensor_id)
        if sensor:
            sensor.last_reading = value
            sensor.status = status
            sensor.last_updated_at = datetime.utcnow()

            # Record in-memory reading point
            pts = self._history_readings.setdefault(sensor_id, [])
            pts.append({
                "timestamp": datetime.utcnow().strftime("%H:%M"),
                "value": round(value, 1),
            })
            if len(pts) > 100:
                pts.pop(0)

        client = get_db_client()
        if client:
            try:
                client.table("sensors").update({
                    "last_reading": value,
                    "status": status,
                    "last_updated_at": datetime.utcnow().isoformat(),
                }).eq("id", sensor_id).execute()

                client.table("sensor_readings").insert({
                    "sensor_id": sensor_id,
                    "value": value,
                    "recorded_at": datetime.utcnow().isoformat(),
                }).execute()
            except Exception as e:
                logger.warning(f"Supabase error recording sensor reading: {e}")

        return sensor

    async def get_history(self, sensor_id: str, hours: int = 24) -> list[dict]:
        return self._history_readings.get(sensor_id, [])


sensor_repository = SensorRepository()
