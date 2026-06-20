import httpx
import os

API_BASE_URL = os.getenv("NEXT_PUBLIC_API_URL", "http://backend:8000/api/v1")

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL

    async def register_user(self, user_id: int, username: str = None):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/auth/register",
                json={"email": f"tg_{user_id}@soccermind.ai", "password": "tg_default", "telegram_id": user_id, "username": username}
            )
            return resp.json()

    async def get_daily_predictions(self, user_id: int):
        async with httpx.AsyncClient() as client:
            # Получаем токен для пользователя (упрощенно: используем фиксированный или получаем)
            # В реальном боте нужно хранить токен, здесь заглушка
            resp = await client.get(
                f"{self.base_url}/predictions/daily",
                headers={"Authorization": f"Bearer {self._get_token(user_id)}"}
            )
            return resp.json() if resp.status_code == 200 else []

    async def get_prediction_history(self, user_id: int):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/predictions/history",
                headers={"Authorization": f"Bearer {self._get_token(user_id)}"}
            )
            return resp.json() if resp.status_code == 200 else []

    async def get_roi(self, user_id: int):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/analytics/roi",
                headers={"Authorization": f"Bearer {self._get_token(user_id)}"}
            )
            return resp.json() if resp.status_code == 200 else {"roi_percent": 0, "total_bets": 0, "wins": 0}

    async def confirm_telegram_payment(self, user_id: int, telegram_payment_charge_id: str, total_amount: int, currency: str):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/payments/telegram",
                json={
                    "user_id": user_id,
                    "telegram_payment_charge_id": telegram_payment_charge_id,
                    "total_amount": total_amount,
                    "currency": currency,
                },
                headers={"Authorization": f"Bearer {self._get_token(user_id)}"}
            )
            return resp.json()

    async def get_referral_stats(self, user_id: int):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/referrals/stats",
                headers={"Authorization": f"Bearer {self._get_token(user_id)}"}
            )
            return resp.json() if resp.status_code == 200 else {"referrals_count": 0, "earned_credits": 0, "referral_code": ""}

    def _get_token(self, user_id: int) -> str:
        # В реальном проекте токен получается при авторизации и сохраняется в кеш
        # Для простоты используем статический токен, полученный от API при регистрации
        # Либо бот сам авторизуется и хранит маппинг user_id -> token
        # Здесь используем встроенный сервисный токен (неправильно, но для демо)
        # В production нужно реализовать обмен tg_id на токен через специальный эндпоинт.
        return "service_token_placeholder"