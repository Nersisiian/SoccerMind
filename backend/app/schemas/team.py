from pydantic import BaseModel
from typing import Optional
import uuid

class TeamCreate(BaseModel):
    name: str
    country: Optional[str]
    external_id: Optional[str]

class TeamOut(BaseModel):
    id: uuid.UUID
    name: str
    country: Optional[str]
    external_id: Optional[str]

    class Config:
        from_attributes = True