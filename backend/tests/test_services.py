"""Tests for service classes"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.orm import Session

from app.models.lead import Lead, LeadStatus
from app.services.lead_service import LeadService
from app.services.ai_service import AIService


class TestLeadService:
    """Tests for LeadService"""

    def test_get_lead_by_id(self, db_session: Session, sample_lead: Lead):
        """Test getting lead by ID"""
        service = LeadService(db_session)
        lead = service.get_lead(sample_lead.id)
        assert lead is not None
        assert lead.id == sample_lead.id

    def test_get_lead_not_found(self, db_session: Session):
        """Test getting non-existent lead"""
        service = LeadService(db_session)
        lead = service.get_lead(99999)
        assert lead is None

    def test_get_lead_by_phone(self, db_session: Session, sample_lead: Lead):
        """Test getting lead by phone"""
        service = LeadService(db_session)
        lead = service.get_lead_by_phone(sample_lead.phone)
        assert lead is not None
        assert lead.phone == sample_lead.phone

    def test_create_lead(self, db_session: Session):
        """Test creating a lead"""
        from app.models.lead import LeadCreate

        service = LeadService(db_session)
        lead_data = LeadCreate(
            phone="+1999999999",
            name="New Lead",
            interest="Test interest",
        )
        lead = service.create_lead(lead_data)
        assert lead.id is not None
        assert lead.phone == "+1999999999"
        assert lead.name == "New Lead"

    def test_get_or_create_existing(self, db_session: Session, sample_lead: Lead):
        """Test get_or_create with existing lead"""
        service = LeadService(db_session)
        lead = service.get_or_create(sample_lead.phone, "Test message")
        assert lead.id == sample_lead.id

    def test_get_or_create_new(self, db_session: Session):
        """Test get_or_create with new lead"""
        service = LeadService(db_session)
        lead = service.get_or_create("+1888888888", "New message")
        assert lead.id is not None
        assert lead.phone == "+1888888888"
        assert lead.status == LeadStatus.NEW

    def test_update_lead_status(self, db_session: Session, sample_lead: Lead):
        """Test updating lead status"""
        from app.models.lead import LeadUpdate

        service = LeadService(db_session)
        update_data = LeadUpdate(status=LeadStatus.CLOSED)
        updated_lead = service.update_lead(sample_lead.id, update_data)
        assert updated_lead.status == LeadStatus.CLOSED

    def test_delete_lead(self, db_session: Session, sample_lead: Lead):
        """Test deleting lead"""
        service = LeadService(db_session)
        result = service.delete_lead(sample_lead.id)
        assert result is True

        # Verify deleted
        lead = service.get_lead(sample_lead.id)
        assert lead is None


class TestAIService:
    """Tests for AIService"""

    def test_init_without_api_key(self):
        """Test AIService initialization without API key"""
        with patch("app.services.ai_service.settings") as mock_settings:
            mock_settings.openai_api_key = None
            service = AIService()
            assert service.client is None

    @pytest.mark.asyncio
    async def test_fallback_response(self, sample_lead: Lead):
        """Test fallback response when AI not available"""
        with patch("app.services.ai_service.settings") as mock_settings:
            mock_settings.openai_api_key = None
            mock_settings.ai_system_prompt = "Test prompt"
            service = AIService()
            response = await service.generate_response(sample_lead, "Hello")
            assert isinstance(response, str)
            assert len(response) > 0

    @pytest.mark.asyncio
    async def test_followup_fallback(self, sample_lead: Lead):
        """Test followup fallback when AI not available"""
        with patch("app.services.ai_service.settings") as mock_settings:
            mock_settings.openai_api_key = None
            mock_settings.ai_system_prompt = "Test prompt"
            service = AIService()
            response = await service.generate_followup_message(sample_lead)
            assert isinstance(response, str)
            assert len(response) > 0