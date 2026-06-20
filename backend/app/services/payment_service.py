import stripe
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.models.user import User
from app.db.models.subscription import Subscription
from app.db.models.payment import Payment
from datetime import datetime, timedelta

stripe.api_key = settings.STRIPE_API_KEY

class PaymentService:
    async def create_stripe_checkout(self, user: User, price_id: str):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{'price': price_id, 'quantity': 1}],
                mode='subscription',
                success_url='https://yourdomain.com/success',
                cancel_url='https://yourdomain.com/cancel',
                client_reference_id=str(user.id),
            )
            return {"url": session.url}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def handle_webhook(self, event, db: AsyncSession):
        event_type = event['type']
        data = event['data']['object']
        if event_type == 'checkout.session.completed':
            user_id = data.get('client_reference_id')
            if user_id:
                user = await db.get(User, user_id)
                if user:
                    subscription_id = data.get('subscription')
                    # Создаем подписку
                    subscription = Subscription(
                        user_id=user.id,
                        plan_id=data.get('display_items', [{}])[0].get('price', {}).get('id'),
                        status='active',
                        current_period_start=datetime.utcnow(),
                        current_period_end=datetime.utcnow() + timedelta(days=30),
                        stripe_subscription_id=subscription_id,
                    )
                    db.add(subscription)
                    await db.commit()
        elif event_type == 'invoice.payment_succeeded':
            # Обновляем статус
            pass
        elif event_type == 'customer.subscription.deleted':
            sub_id = data['id']
            stmt = select(Subscription).where(Subscription.stripe_subscription_id == sub_id)
            result = await db.execute(stmt)
            sub = result.scalar_one_or_none()
            if sub:
                sub.status = 'cancelled'
                await db.commit()