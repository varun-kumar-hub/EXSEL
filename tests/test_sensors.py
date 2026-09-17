import pytest
from app.services.sensor_service import sensor_service


@pytest.mark.asyncio
async def test_get_sensors():
    sensors = await sensor_service.get_all_sensors()
    assert len(sensors) >= 5
    sensor_types = [s.sensor_type for s in sensors]
    assert "level" in sensor_types
    assert "flow" in sensor_types
    assert "pressure" in sensor_types


@pytest.mark.asyncio
async def test_sensor_telemetry_reading():
    sensor = await sensor_service.get_sensor("SENS_LVL_01")
    assert sensor.id == "SENS_LVL_01"
    assert sensor.last_reading is not None
    assert 20.0 <= sensor.last_reading <= 100.0


@pytest.mark.asyncio
async def test_sensor_history():
    history = await sensor_service.get_sensor_history("SENS_LVL_01", hours=24)
    assert len(history) > 0
    assert "timestamp" in history[0]
    assert "value" in history[0]
