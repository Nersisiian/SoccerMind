from aiogram import Router, types, F
from aiogram.types import PreCheckoutQuery, Message
from app.services.api_client import APIClient

router = Router()

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    # Всегда подтверждаем предварительную оплату
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    payment = message.successful_payment
    client = APIClient()
    # Сообщаем API о платеже
    await client.confirm_telegram_payment(
        user_id=message.from_user.id,
        telegram_payment_charge_id=payment.telegram_payment_charge_id,
        total_amount=payment.total_amount,
        currency=payment.currency,
    )
    await message.answer(
        "✅ Оплата прошла успешно! Премиум-подписка активирована.\n"
        "Теперь вам доступны все прогнозы без задержек."
    )