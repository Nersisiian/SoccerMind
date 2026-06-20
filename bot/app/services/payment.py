from aiogram import Bot
from aiogram.types import LabeledPrice

PRICES = {
    "monthly": [LabeledPrice(label="⭐️ 1 месяц Premium", amount=500)],
    "yearly": [LabeledPrice(label="👑 Год Premium", amount=4000)],
}

async def send_stars_invoice(bot: Bot, user_id: int, plan: str):
    if plan not in PRICES:
        return
    await bot.send_invoice(
        chat_id=user_id,
        title="Premium SoccerMind AI",
        description="Доступ к AI-прогнозам без ограничений",
        payload=f"sub_{plan}",
        provider_token="",  # Для Telegram Stars оставляем пустым
        currency="XTR",
        prices=PRICES[plan],
        start_parameter="soccermind_premium",
    )