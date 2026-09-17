from fastapi import APIRouter, Query
from app.services.dashboard_service import dashboard_service
from app.schemas.common import APIResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=APIResponse[dict])
async def get_dashboard_data():
    data = await dashboard_service.get_overview()
    return APIResponse(success=True, data=data)


@router.get("/water-level", response_model=APIResponse[list])
async def get_water_level_chart(range: str = Query("24H", description="1H, 6H, 24H, 7D")):
    data = await dashboard_service.get_chart_data("water_level", time_range=range)
    return APIResponse(success=True, data=data)


@router.get("/flow", response_model=APIResponse[list])
async def get_flow_chart(range: str = Query("24H", description="1H, 6H, 24H, 7D")):
    data = await dashboard_service.get_chart_data("flow_rate", time_range=range)
    return APIResponse(success=True, data=data)
