from aiogram import Router, types
from aiogram.filters import Command
from app.services.api_client import APIClient

router = Router()

@router.message(Command("referral"))
async def cmd_referral(message: types.Message):
    client = APIClient()
    user_id = message.from_user.id
    stats = await client.get_referral_stats(user_id)
    link = f"https://t.me/your_bot_username?start=ref_{stats.get('referral_code', user_id)}"
    await message.answer(
        f"🎁 <b>Реферальная программа</b>\n\n"
        f"👥 Приглашено друзей: {stats['referrals_count']}\n"
        f"💎 Заработано бонусов: {stats['earned_credits']}\n\n"
        f"Ваша ссылка:\n<code>{link}</code>\n\n"
        "За каждого друга вы получите +7 дней Premium!"
    )