import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_daily_predictions_unauthorized(client: AsyncClient):
    resp = await client.get("/api/v1/predictions/daily")
    assert resp.status_code == 401