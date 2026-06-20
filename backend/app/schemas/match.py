from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class TeamShort(BaseModel):
    id: uuid.UUID
    name: str
    country: Optional[str]

class MatchOut(BaseModel):
    id: uuid.UUID
    home_team: TeamShort
    away_team: TeamShort
    kickoff: datetime
    status: str
    home_score: Optional[int]
    away_score: Optional[int]

    class Config:
        from_attributes = True

class MatchDetail(MatchOut):
    odds: Optional[dict]
    predictions: Optional[dict]