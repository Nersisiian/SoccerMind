from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.services.prediction_service import PredictionService
from app.core.permissions import RoleChecker

router = APIRouter()

@router.get("/roi")
async def get_roi_statistics(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await PredictionService(db).get_roi(current_user)