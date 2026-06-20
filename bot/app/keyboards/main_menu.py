from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="⚽️ Прогнозы")
    builder.button(text="📅 История")
    builder.button(text="📈 ROI")
    builder.button(text="💎 Premium")
    builder.button(text="🎁 Рефералы")
    builder.button(text="ℹ️ Помощь")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)