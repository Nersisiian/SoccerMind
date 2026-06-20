import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Регистрация
        resp = await ac.post("/api/v1/auth/register", json={"email": "test@example.com", "password": "secret1234"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "test@example.com"

        # Логин
        resp = await ac.post("/api/v1/auth/login", data={"username": "test@example.com", "password": "secret1234"})
        assert resp.status_code == 200
        tokens = resp.json()
        assert "access_token" in tokens
