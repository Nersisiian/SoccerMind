import uuid
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Match(Base):
    __tablename__ = "matches"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    home_team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=False)
    competition_id = Column(UUID(as_uuid=True), ForeignKey("competitions.id"))
    kickoff = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="scheduled")
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    external_id = Column(String, unique=True, index=True)

    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    competition = relationship("Competition")
    odds = relationship("Odds", back_populates="match")
    predictions = relationship("Prediction", back_populates="match")