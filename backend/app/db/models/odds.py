import uuid
from sqlalchemy import Column, ForeignKey, Float, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func

class Odds(Base):
    __tablename__ = "odds"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), ForeignKey("matches.id"), nullable=False)
    bookmaker = Column(String)
    market = Column(String)
    home_win = Column(Float)
    draw = Column(Float)
    away_win = Column(Float)
    over = Column(Float)
    under = Column(Float)
    btts_yes = Column(Float)
    btts_no = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    match = relationship("Match", back_populates="odds")