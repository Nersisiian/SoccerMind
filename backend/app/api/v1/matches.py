from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.match import MatchOut, MatchDetail
from app.services.prediction_service import PredictionService

router = APIRouter()

@router.get("/", response_model=list[MatchOut])
async def get_matches(league: str = None, db: AsyncSession = Depends(get_db)):
    return await PredictionService(db).get_matches(league=league)

@router.get("/{match_id}", response_model=MatchDetail)
async def get_match(match_id: str, db: AsyncSession = Depends(get_db)):
    return await PredictionService(db).get_match_detail(match_id)