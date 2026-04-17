"""Lead Service for managing leads"""
import logging
import re
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.lead import Lead, LeadStatus, LeadIntent, LeadCreate, LeadUpdate

logger = logging.getLogger(__name__)


class LeadService:
    """Service for managing leads"""

    # Regex patterns to extract name from messages
    NAME_PATTERNS = [
        r"(?:my name is|i'm|i am|call me|this is)\s+([A-Z][a-z]+)",
        r"^([A-Z][a-z]+)(?:\s+here|\s+speaking)?$",
        r"^(?:hi|hello|hey)[,\s]+(?:i'?m\s+)?([A-Z][a-z]+)",
    ]

    def __init__(self, db: Session):
        self.db = db

    def get_lead(self, lead_id: int) -> Optional[Lead]:
        """Get a lead by ID"""
        return self.db.query(Lead).filter(Lead.id == lead_id).first()

    def get_lead_by_phone(self, phone: str) -> Optional[Lead]:
        """Get a lead by phone number"""
        return self.db.query(Lead).filter(Lead.phone == phone).first()

    def get_leads(
        self,
        status: Optional[LeadStatus] = None,
        intent: Optional[LeadIntent] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Lead]:
        """Get leads with optional filtering"""
        query = self.db.query(Lead)

        if status:
            query = query.filter(Lead.status == status)

        if intent:
            query = query.filter(Lead.intent == intent)

        return query.order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()

    def create_lead(self, lead_data: LeadCreate) -> Lead:
        """Create a new lead"""
        lead = Lead(
            name=lead_data.name,
            phone=lead_data.phone,
            interest=lead_data.interest,
            status=lead_data.status,
            intent=lead_data.intent,
            last_contact_at=datetime.utcnow(),
        )
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        logger.info(f"Created new lead: {lead.id} - {lead.phone}")
        return lead

    def get_or_create(self, phone: str, initial_message: str = "") -> Lead:
        """Get existing lead or create new one"""
        lead = self.get_lead_by_phone(phone)

        if lead:
            # Update last contact time
            lead.last_contact_at = datetime.utcnow()
            lead.conversation_count = (lead.conversation_count or 0) + 1
            self.db.commit()
            self.db.refresh(lead)
            logger.info(f"Found existing lead: {lead.id}")
            return lead

        # Create new lead
        new_lead = Lead(
            phone=phone,
            status=LeadStatus.NEW,
            intent=LeadIntent.COLD,
            last_message=initial_message[:500] if initial_message else None,
            last_contact_at=datetime.utcnow(),
            conversation_count=1,
        )
        self.db.add(new_lead)
        self.db.commit()
        self.db.refresh(new_lead)
        logger.info(f"Created new lead: {new_lead.id} - {new_lead.phone}")
        return new_lead

    def update_lead(self, lead_id: int, lead_update: LeadUpdate) -> Optional[Lead]:
        """Update a lead"""
        lead = self.get_lead(lead_id)

        if not lead:
            return None

        update_data = lead_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(lead, field, value)

        lead.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(lead)
        logger.info(f"Updated lead: {lead_id}")
        return lead

    def update_lead_message(
        self,
        lead_id: int,
        user_message: str,
        ai_response: str,
        detected_intent: LeadIntent = None
    ):
        """Update lead with latest conversation and optionally update intent"""
        lead = self.get_lead(lead_id)

        if lead:
            # Store conversation
            lead.last_message = f"User: {user_message[:200]}\nAI: {ai_response[:200]}"
            lead.last_contact_at = datetime.utcnow()
            lead.conversation_count = (lead.conversation_count or 0) + 1

            # Extract name from message if not known
            if not lead.name:
                extracted_name = self._extract_name_from_message(user_message)
                if extracted_name:
                    lead.name = extracted_name
                    logger.info(f"Extracted name '{extracted_name}' for lead {lead_id}")

            # Update status to engaged if it's a new lead
            if lead.status == LeadStatus.NEW:
                lead.status = LeadStatus.ENGAGED

            # Update intent if provided and better than current
            if detected_intent:
                # Upgrade intent if new one is higher priority
                intent_priority = {"cold": 0, "warm": 1, "hot": 2}
                current_priority = intent_priority.get(lead.intent.value, 0)
                new_priority = intent_priority.get(detected_intent.value, 0)
                if new_priority > current_priority:
                    lead.intent = detected_intent
                    logger.info(f"Upgraded lead {lead_id} intent to {detected_intent.value}")

            self.db.commit()
            logger.info(f"Updated lead {lead_id} conversation")

    def _extract_name_from_message(self, message: str) -> Optional[str]:
        """Extract a person's name from their message"""
        for pattern in self.NAME_PATTERNS:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                name = match.group(1).capitalize()
                # Filter out common false positives
                if name.lower() not in ["interested", "looking", "calling", "here", "there", "hello", "hi", "hey"]:
                    return name
        return None

    def update_intent(self, lead_id: int, intent: LeadIntent) -> Optional[Lead]:
        """Update lead intent classification"""
        lead = self.get_lead(lead_id)

        if lead:
            lead.intent = intent
            lead.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(lead)
            logger.info(f"Updated lead {lead_id} intent to {intent}")
            return lead
        return None

    def update_status(self, lead_id: int, status: LeadStatus) -> Optional[Lead]:
        """Update lead status"""
        lead = self.get_lead(lead_id)

        if lead:
            lead.status = status
            lead.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(lead)
            logger.info(f"Updated lead {lead_id} status to {status}")
            return lead
        return None

    def mark_closed(self, lead_id: int) -> Optional[Lead]:
        """Mark a lead as closed (converted)"""
        return self.update_status(lead_id, LeadStatus.CLOSED)

    def delete_lead(self, lead_id: int) -> bool:
        """Delete a lead"""
        lead = self.get_lead(lead_id)

        if lead:
            self.db.delete(lead)
            self.db.commit()
            logger.info(f"Deleted lead: {lead_id}")
            return True
        return False

    def get_inactive_leads(
        self,
        hours_inactive: int = 24,
        limit: int = 100
    ) -> List[Lead]:
        """
        Get leads that have been inactive for a specified number of hours.
        Only returns leads with status 'engaged' that haven't been contacted recently.
        """
        cutoff_time = datetime.utcnow()

        leads = self.db.query(Lead).filter(
            and_(
                Lead.status == LeadStatus.ENGAGED,
                Lead.last_contact_at < cutoff_time,
            )
        ).limit(limit).all()

        # Filter by actual inactivity in Python (for SQLite compatibility)
        threshold = datetime.utcnow() - timedelta(hours=hours_inactive)
        inactive_leads = [
            lead for lead in leads
            if lead.last_contact_at and lead.last_contact_at < threshold
        ]

        return inactive_leads

    def get_hot_leads(self, limit: int = 100) -> List[Lead]:
        """Get all leads classified as HOT (ready to buy)"""
        return self.db.query(Lead).filter(
            Lead.intent == LeadIntent.HOT
        ).order_by(Lead.updated_at.desc()).limit(limit).all()

    def get_leads_for_followup(self, limit: int = 100) -> List[Lead]:
        """Get leads that need follow-up based on their status and intent"""
        threshold = datetime.utcnow() - timedelta(hours=24)
        return self.db.query(Lead).filter(
            and_(
                Lead.status == LeadStatus.ENGAGED,
                Lead.last_contact_at < threshold,
            )
        ).order_by(Lead.intent.desc()).limit(limit).all()  # HOT leads first