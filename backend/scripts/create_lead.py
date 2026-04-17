#!/usr/bin/env python3
"""Script to create test data for development"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.lead import Lead, LeadStatus


def create_test_leads():
    """Create sample leads for testing"""
    db = SessionLocal()

    try:
        # Check if leads already exist
        existing = db.query(Lead).first()
        if existing:
            print("Leads already exist in database. Skipping seed.")
            return

        test_leads = [
            Lead(
                phone="+1234567890",
                name="John Smith",
                interest="Enterprise software solutions",
                status=LeadStatus.NEW,
                created_at=datetime.utcnow() - timedelta(days=1),
            ),
            Lead(
                phone="+1987654321",
                name="Jane Doe",
                interest="Marketing automation tools",
                status=LeadStatus.ENGAGED,
                last_message="Can you tell me more about pricing?",
                created_at=datetime.utcnow() - timedelta(days=3),
                last_contact_at=datetime.utcnow() - timedelta(hours=48),
            ),
            Lead(
                phone="+1555111222",
                name="Bob Wilson",
                interest="CRM integration",
                status=LeadStatus.ENGAGED,
                last_message="I need this for my team of 50 people",
                created_at=datetime.utcnow() - timedelta(days=5),
                last_contact_at=datetime.utcnow() - timedelta(hours=72),
            ),
            Lead(
                phone="+1444333222",
                name="Alice Brown",
                interest="Full platform demo",
                status=LeadStatus.CLOSED,
                last_message="Ready to proceed with the purchase",
                created_at=datetime.utcnow() - timedelta(days=7),
                last_contact_at=datetime.utcnow() - timedelta(days=1),
            ),
            Lead(
                phone="+1666555444",
                name="Charlie Davis",
                interest="API access",
                status=LeadStatus.NEW,
                created_at=datetime.utcnow() - timedelta(hours=2),
            ),
        ]

        for lead in test_leads:
            db.add(lead)

        db.commit()
        print(f"Created {len(test_leads)} test leads successfully!")

        # Display created leads
        for lead in test_leads:
            print(f"  - {lead.name} ({lead.phone}) - {lead.status.value}")

    except Exception as e:
        print(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_leads()