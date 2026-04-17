"""Lead model and schemas"""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from pydantic import BaseModel, Field
from app.database.base import Base


class LeadStatus(str, Enum):
    """Lead status enumeration"""
    NEW = "new"
    ENGAGED = "engaged"
    CLOSED = "closed"


class LeadIntent(str, Enum):
    """Lead intent classification"""
    HOT = "hot"      # Ready to buy, asking about pricing/timeline
    WARM = "warm"    # Interested, asking questions
    COLD = "cold"    # Just browsing, low engagement


class Lead(Base):
    """Lead database model"""
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), unique=True, nullable=False, index=True)
    interest = Column(Text, nullable=True)
    status = Column(
        SQLEnum(LeadStatus),
        default=LeadStatus.NEW,
        nullable=False,
        index=True
    )
    intent = Column(
        SQLEnum(LeadIntent),
        default=LeadIntent.COLD,
        nullable=False,
        index=True
    )
    last_message = Column(Text, nullable=True)
    conversation_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contact_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Lead(id={self.id}, phone={self.phone}, status={self.status}, intent={self.intent})>"


# Pydantic schemas
class LeadCreate(BaseModel):
    """Schema for creating a lead"""
    name: str | None = None
    phone: str
    interest: str | None = None
    status: LeadStatus = LeadStatus.NEW
    intent: LeadIntent = LeadIntent.COLD


class LeadUpdate(BaseModel):
    """Schema for updating a lead"""
    name: str | None = None
    interest: str | None = None
    status: LeadStatus | None = None
    intent: LeadIntent | None = None
    last_message: str | None = None


class LeadResponse(BaseModel):
    """Schema for lead response"""
    id: int
    name: str | None
    phone: str
    interest: str | None
    status: LeadStatus
    intent: LeadIntent
    last_message: str | None
    conversation_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class LeadIntentAnalysis(BaseModel):
    """Schema for intent analysis response"""
    lead_id: int
    intent: LeadIntent
    suggestions: list[str]
    should_ask_name: bool
    should_push_conversion: bool