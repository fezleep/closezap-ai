"""Tests for webhook endpoints"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.lead import Lead, LeadStatus


class TestWebhook:
    """Tests for POST /api/webhook endpoint"""

    def test_webhook_new_lead(self, client: TestClient, db_session: Session):
        """Test webhook creates new lead"""
        response = client.post(
            "/api/webhook",
            data={
                "From": "whatsapp:+1555000123",
                "Body": "Hello, I'm interested!",
                "MessageSid": "SM123456",
            },
        )
        assert response.status_code == 200

        # Verify TwiML response
        assert "<?xml" in response.text
        assert "<Message>" in response.text

        # Verify lead was created
        lead = db_session.query(Lead).filter(Lead.phone == "+1555000123").first()
        assert lead is not None
        assert lead.status == LeadStatus.ENGAGED

    def test_webhook_existing_lead(self, client: TestClient, sample_lead: Lead):
        """Test webhook updates existing lead"""
        response = client.post(
            "/api/webhook",
            data={
                "From": f"whatsapp:{sample_lead.phone}",
                "Body": "I want to know more",
                "MessageSid": "SM123457",
            },
        )
        assert response.status_code == 200

    def test_webhook_missing_fields(self, client: TestClient):
        """Test webhook with missing required fields"""
        response = client.post(
            "/api/webhook",
            data={
                "From": "",
                "Body": "Hello",
            },
        )
        assert response.status_code == 400

    def test_webhook_health(self, client: TestClient):
        """Test webhook health endpoint"""
        response = client.get("/api/webhook/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestHealthEndpoints:
    """Tests for health check endpoints"""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data

    def test_health_endpoint(self, client: TestClient):
        """Test health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"