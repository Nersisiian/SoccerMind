from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.schemas.user import ReferralOut
from app.services.auth_service import AuthService

router = APIRouter()

@router.get("/stats", response_model=ReferralOut)
async def referral_stats(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await AuthService(db).get_referral_stats(current_user)