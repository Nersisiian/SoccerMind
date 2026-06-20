import uuid
from sqlalchemy import Column, ForeignKey, String, Date
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class Injury(Base):
    __tablename__ = "injuries"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"))
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))
    match_id = Column(UUID(as_uuid=True), ForeignKey("matches.id"))
    description = Column(String)
    status = Column(String)
    expected_return = Column(Date)