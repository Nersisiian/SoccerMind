from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from app.keyboards.main_menu import main_menu_keyboard
from app.services.api_client import APIClient

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    # Попытка зарегистрировать пользователя в API
    client = APIClient()
    resp = await client.register_user(user_id, message.from_user.username)
    if resp.get("created"):
        await message.answer(
            f"👋 Привет, {message.from_user.full_name}!\nДобро пожаловать в SoccerMind AI — твоего персонального футбольного аналитика.\n\n"
            "Я буду присылать тебе ежедневные AI-прогнозы, ROI-статистику и помогать побеждать букмекеров.",
            reply_markup=main_menu_keyboard()
        )
    else:
        await message.answer(
            f"С возвращением, {message.from_user.full_name}!\nЧем могу помочь?",
            reply_markup=main_menu_keyboard()
        )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "⚽️ <b>SoccerMind AI Bot</b>\n\n"
        "Команды:\n"
        "/start — Главное меню\n"
        "/predictions — Прогнозы на сегодня\n"
        "/history — История прогнозов\n"
        "/roi — Моя ROI статистика\n"
        "/subscribe — Premium подписка\n"
        "/referral — Моя реферальная ссылка\n"
        "/help — Помощь"
    )