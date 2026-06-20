from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
import uuid

class PredictionOut(BaseModel):
    id: uuid.UUID
    match_id: uuid.UUID
    model_version: Optional[str]
    predicted_home_win: Optional[float]
    predicted_draw: Optional[float]
    predicted_away_win: Optional[float]
    predicted_over_2_5: Optional[float]
    predicted_btts: Optional[float]
    predicted_score: Optional[Dict[str, float]]
    created_at: datetime

    class Config:
        from_attributes = True

class PredictionFilter(BaseModel):
    league: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None