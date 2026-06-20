import uuid
from sqlalchemy import Column, ForeignKey, Float, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), ForeignKey("matches.id"), nullable=False)
    model_version = Column(String)
    predicted_home_win = Column(Float)
    predicted_draw = Column(Float)
    predicted_away_win = Column(Float)
    predicted_over_2_5 = Column(Float)
    predicted_btts = Column(Float)
    predicted_score = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    match = relationship("Match", back_populates="predictions")