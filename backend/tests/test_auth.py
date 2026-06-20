import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # Регистрация
    resp = await client.post("/api/v1/auth/register", json={"email": "test@example.com", "password": "secret1234"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "test@example.com"

    # Логин
    resp = await client.post("/api/v1/auth/login", data={"username": "test@example.com", "password": "secret1234"})
    assert resp.status_code == 200
    tokens = resp.json()
    assert "access_token" in tokens