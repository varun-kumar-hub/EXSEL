from fastapi import APIRouter, Query
from app.services.analytics_service import analytics_service
from app.schemas.common import APIResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("", response_model=APIResponse[dict])
async def get_analytics(range: str = Query("7D", description="'Today', '7D', '30D'")):
    data = await analytics_service.get_analytics(date_filter=range)
    return APIResponse(success=True, data=data)
