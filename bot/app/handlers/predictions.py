from aiogram import Router, types
from aiogram.filters import Command
from app.keyboards.main_menu import main_menu_keyboard
from app.services.api_client import APIClient

router = Router()

@router.message(Command("predictions"))
async def cmd_predictions(message: types.Message):
    client = APIClient()
    user_id = message.from_user.id
    data = await client.get_daily_predictions(user_id)
    if not data:
        await message.answer("На сегодня прогнозов пока нет. Загляни позже!", reply_markup=main_menu_keyboard())
        return
    text = "<b>⚽️ Ежедневные прогнозы SoccerMind AI</b>\n\n"
    for p in data:
        text += (
            f"🏟 {p['match']['home_team']['name']} vs {p['match']['away_team']['name']}\n"
            f"⏰ {p['match']['kickoff']}\n"
            f"📊 Исход: {p['home_win']:.0%} | {p['draw']:.0%} | {p['away_win']:.0%}\n"
            f"🥅 Обе забьют: {p['btts']:.0%}\n"
            f"📈 Тотал >2.5: {p['over2_5']:.0%}\n\n"
        )
    await message.answer(text, reply_markup=main_menu_keyboard())

@router.message(Command("history"))
async def cmd_history(message: types.Message):
    client = APIClient()
    user_id = message.from_user.id
    data = await client.get_prediction_history(user_id)
    if not data:
        await message.answer("История прогнозов пуста.")
        return
    text = "<b>📅 История прогнозов</b>\n\n"
    for p in data[:10]:
        text += (
            f"🏟 {p['match']['home_team']['name']} vs {p['match']['away_team']['name']}\n"
            f"📅 {p['created_at']}\n"
            f"✅ Результат: {p['actual_result'] if 'actual_result' in p else 'ожидается'}\n\n"
        )
    await message.answer(text, reply_markup=main_menu_keyboard())

@router.message(Command("roi"))
async def cmd_roi(message: types.Message):
    client = APIClient()
    user_id = message.from_user.id
    roi_data = await client.get_roi(user_id)
    text = (
        "<b>📈 Ваша ROI статистика</b>\n\n"
        f"💰 Процент возврата: {roi_data['roi_percent']}%\n"
        f"📊 Всего ставок: {roi_data['total_bets']}\n"
        f"🏆 Выигрышей: {roi_data['wins']}"
    )
    await message.answer(text, reply_markup=main_menu_keyboard())