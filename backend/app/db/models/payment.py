import uuid
from sqlalchemy import Column, ForeignKey, Float, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func

class Payment(Base):
    __tablename__ = "payments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Float)
    currency = Column(String)
    payment_method = Column(String)
    status = Column(String)
    stripe_payment_intent_id = Column(String, unique=True)
    telegram_payload = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="payments")