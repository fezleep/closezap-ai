"""Tests for lead endpoints"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.lead import Lead, LeadStatus


class TestGetLeads:
    """Tests for GET /api/leads endpoint"""

    def test_get_leads_empty(self, client: TestClient):
        """Test getting leads when none exist"""
        response = client.get("/api/leads")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_leads_with_data(self, client: TestClient, sample_lead: Lead):
        """Test getting leads with data"""
        response = client.get("/api/leads")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["phone"] == sample_lead.phone

    def test_get_leads_filter_by_status(
        self, client: TestClient, sample_lead: Lead, engaged_lead: Lead
    ):
        """Test filtering leads by status"""
        response = client.get("/api/leads?status=engaged")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "engaged"

    def test_get_leads_pagination(self, client: TestClient, db_session: Session):
        """Test pagination of leads"""
        # Create multiple leads
        for i in range(15):
            lead = Lead(phone=f"+12345678{i:02d}", status=LeadStatus.NEW)
            db_session.add(lead)
        db_session.commit()

        # Get first page
        response = client.get("/api/leads?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

        # Get second page
        response = client.get("/api/leads?skip=10&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5


class TestGetLead:
    """Tests for GET /api/leads/{id} endpoint"""

    def test_get_lead_by_id(self, client: TestClient, sample_lead: Lead):
        """Test getting a specific lead by ID"""
        response = client.get(f"/api/leads/{sample_lead.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_lead.id
        assert data["phone"] == sample_lead.phone

    def test_get_lead_not_found(self, client: TestClient):
        """Test getting a non-existent lead"""
        response = client.get("/api/leads/99999")
        assert response.status_code == 404


class TestUpdateLead:
    """Tests for PATCH /api/leads/{id} endpoint"""

    def test_update_lead_name(self, client: TestClient, sample_lead: Lead):
        """Test updating lead name"""
        response = client.patch(
            f"/api/leads/{sample_lead.id}",
            json={"name": "Updated Name"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_update_lead_status(self, client: TestClient, sample_lead: Lead):
        """Test updating lead status"""
        response = client.patch(
            f"/api/leads/{sample_lead.id}",
            json={"status": "closed"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "closed"

    def test_update_lead_partial(self, client: TestClient, sample_lead: Lead):
        """Test partial update of lead"""
        original_name = sample_lead.name
        response = client.patch(
            f"/api/leads/{sample_lead.id}",
            json={"interest": "New interest"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == original_name  # Name unchanged
        assert data["interest"] == "New interest"

    def test_update_lead_not_found(self, client: TestClient):
        """Test updating non-existent lead"""
        response = client.patch(
            "/api/leads/99999",
            json={"name": "Test"},
        )
        assert response.status_code == 404


class TestDeleteLead:
    """Tests for DELETE /api/leads/{id} endpoint"""

    def test_delete_lead(self, client: TestClient, sample_lead: Lead):
        """Test deleting a lead"""
        response = client.delete(f"/api/leads/{sample_lead.id}")
        assert response.status_code == 200

        # Verify deleted
        response = client.get(f"/api/leads/{sample_lead.id}")
        assert response.status_code == 404

    def test_delete_lead_not_found(self, client: TestClient):
        """Test deleting non-existent lead"""
        response = client.delete("/api/leads/99999")
        assert response.status_code == 404