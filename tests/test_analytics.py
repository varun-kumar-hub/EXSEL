import pytest
from app.services.analytics_service import analytics_service


@pytest.mark.asyncio
async def test_analytics_calculations():
    res = await analytics_service.get_analytics("7D")
    summary = res["summary"]

    assert "avg_water_level" in summary
    assert "max_flow_rate" in summary
    assert "total_gate_operations" in summary
    assert "estimated_water_loss_liters" in summary

    assert len(res["water_level_trend"]) > 0
    assert len(res["flow_rate_trend"]) > 0
    assert len(res["gate_operations_daily"]) == 7
