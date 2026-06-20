from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.schemas.prediction import PredictionOut, PredictionFilter
from app.services.prediction_service import PredictionService
from app.core.permissions import RoleChecker

router = APIRouter()
allow_premium = RoleChecker(["user", "admin"])

@router.get("/daily", response_model=list[PredictionOut])
async def daily_predictions(filters: PredictionFilter = Depends(), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await PredictionService(db).get_daily_predictions(current_user, filters)

@router.get("/history", response_model=list[PredictionOut])
async def prediction_history(filters: PredictionFilter = Depends(), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await PredictionService(db).get_prediction_history(current_user, filters)