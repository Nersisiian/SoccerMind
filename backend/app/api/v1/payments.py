from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.services.payment_service import PaymentService
from app.core.config import settings
import stripe

router = APIRouter()

@router.post("/create-checkout-session")
async def create_checkout_session(price_id: str, current_user=Depends(get_current_user)):
    return await PaymentService().create_stripe_checkout(current_user, price_id)

@router.post("/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    await PaymentService().handle_webhook(event, db)
    return {"success": True}