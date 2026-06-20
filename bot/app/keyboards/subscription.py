from aiogram.utils.keyboard import InlineKeyboardBuilder

def subscription_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="⭐️ 1 месяц – 500 Stars", callback_data="sub:monthly")
    builder.button(text="👑 Год – 4000 Stars", callback_data="sub:yearly")
    builder.adjust(1)
    return builder.as_markup()