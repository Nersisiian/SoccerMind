from aiogram import Router, types, F
from aiogram.filters import Command
from app.keyboards.subscription import subscription_keyboard
from app.services.api_client import APIClient

router = Router()

@router.message(Command("subscribe"))
async def cmd_subscribe(message: types.Message):
    await message.answer(
        "💎 <b>Premium подписка SoccerMind AI</b>\n\n"
        "Выберите тариф:",
        reply_markup=subscription_keyboard()
    )

@router.callback_query(F.data.startswith("sub:"))
async def handle_subscription(callback: types.CallbackQuery):
    plan = callback.data.split(":")[1]  # monthly / yearly
    client = APIClient()
    user_id = callback.from_user.id

    # Для Telegram Stars используем внутренний платежный метод
    # В реальной реализации: отправка инвойса
    from app.services.payment import send_stars_invoice
    await send_stars_invoice(callback.bot, callback.from_user.id, plan)
    await callback.answer()
    await callback.message.answer(
        "💳 Выставлен счёт для оплаты через Telegram Stars. Проверьте уведомления бота."
    )