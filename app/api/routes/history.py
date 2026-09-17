from typing import Optional
from fastapi import APIRouter, Query, Response
from app.services.history_service import history_service
from app.schemas.common import APIResponse

router = APIRouter(prefix="/history", tags=["History & Audit"])


@router.get("", response_model=APIResponse[dict])
async def get_history(
    search: Optional[str] = None,
    event_type: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
):
    result = await history_service.get_events(
        search=search,
        event_type=event_type,
        status=status,
        page=page,
        page_size=page_size,
    )
    return APIResponse(success=True, data=result)


@router.get("/export")
async def export_history():
    csv_data = await history_service.export_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=smart_water_audit_log.csv"},
    )
