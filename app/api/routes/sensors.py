from fastapi import APIRouter
from app.services.sensor_service import sensor_service
from app.schemas.common import APIResponse

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.get("", response_model=APIResponse[list])
async def list_sensors():
    sensors = await sensor_service.get_all_sensors()
    return APIResponse(
        success=True,
        data=[
            {
                "id": s.id,
                "name": s.name,
                "sensor_type": s.sensor_type,
                "unit": s.unit,
                "minimum_threshold": s.minimum_threshold,
                "maximum_threshold": s.maximum_threshold,
                "status": s.status,
                "last_reading": s.last_reading,
                "last_updated_at": s.last_updated_at,
            }
            for s in sensors
        ],
    )


@router.get("/{sensor_id}", response_model=APIResponse[dict])
async def get_sensor(sensor_id: str):
    sensor = await sensor_service.get_sensor(sensor_id)
    return APIResponse(
        success=True,
        data={
            "id": sensor.id,
            "name": sensor.name,
            "sensor_type": sensor.sensor_type,
            "unit": sensor.unit,
            "minimum_threshold": sensor.minimum_threshold,
            "maximum_threshold": sensor.maximum_threshold,
            "status": sensor.status,
            "last_reading": sensor.last_reading,
            "last_updated_at": sensor.last_updated_at,
        },
    )


@router.get("/{sensor_id}/history", response_model=APIResponse[list])
async def get_sensor_history(sensor_id: str):
    history = await sensor_service.get_sensor_history(sensor_id)
    return APIResponse(success=True, data=history)
