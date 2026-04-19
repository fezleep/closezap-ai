"""Seed script to populate database with sample leads"""
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.lead import Lead, LeadStatus, LeadIntent


def get_sample_leads():
    """Generate sample lead data"""
    now = datetime.utcnow()

    return [
        {
            "name": "John Smith",
            "phone": "+1234567890",
            "interest": "Looking for AI automation for his real estate business",
            "status": LeadStatus.NEW,
            "intent": LeadIntent.WARM,
            "last_message": "Hi! I saw your ad about AI sales assistants. Tell me more?",
            "conversation_count": 2,
            "last_contact_at": now - timedelta(hours=1),
        },
        {
            "name": "Sarah Johnson",
            "phone": "+1234567891",
            "interest": "E-commerce store owner interested in automated follow-ups",
            "status": LeadStatus.ENGAGED,
            "intent": LeadIntent.HOT,
            "last_message": "What's the pricing like? I need this for my Black Friday campaign.",
            "conversation_count": 8,
            "last_contact_at": now - timedelta(hours=3),
        },
        {
            "name": "Mike Chen",
            "phone": "+1234567892",
            "interest": "Insurance agency exploring lead nurturing solutions",
            "status": LeadStatus.ENGAGED,
            "intent": LeadIntent.WARM,
            "last_message": "Can your AI handle multiple languages? We have Spanish-speaking clients.",
            "conversation_count": 5,
            "last_contact_at": now - timedelta(hours=12),
        },
        {
            "name": "Emily Davis",
            "phone": "+1234567893",
            "interest": "Fitness studio owner wanting automated membership sales",
            "status": LeadStatus.CLOSED,
            "intent": LeadIntent.HOT,
            "last_message": "Perfect! Let's get started. When can we onboard?",
            "conversation_count": 12,
            "last_contact_at": now - timedelta(days=1),
        },
        {
            "name": "Robert Wilson",
            "phone": "+1234567894",
            "interest": "Car dealership interested in AI lead qualification",
            "status": LeadStatus.NEW,
            "intent": LeadIntent.COLD,
            "last_message": "Just browsing for now. What do you offer?",
            "conversation_count": 1,
            "last_contact_at": now - timedelta(hours=24),
        },
        {
            "name": "Lisa Anderson",
            "phone": "+1234567895",
            "interest": "Online course creator looking for sales automation",
            "status": LeadStatus.ENGAGED,
            "intent": LeadIntent.HOT,
            "last_message": "This sounds great! Do you offer payment plans?",
            "conversation_count": 6,
            "last_contact_at": now - timedelta(hours=2),
        },
        {
            "name": "David Brown",
            "phone": "+1234567896",
            "interest": "SaaS startup founder needing demo booking automation",
            "status": LeadStatus.NEW,
            "intent": LeadIntent.WARM,
            "last_message": "Can the AI integrate with Calendly for booking demos?",
            "conversation_count": 3,
            "last_contact_at": now - timedelta(hours=6),
        },
        {
            "name": "Jennifer Martinez",
            "phone": "+1234567897",
            "interest": "Home services company wanting appointment setting",
            "status": LeadStatus.ENGAGED,
            "intent": LeadIntent.WARM,
            "last_message": "How does it handle rescheduling? We get a lot of that.",
            "conversation_count": 4,
            "last_contact_at": now - timedelta(hours=8),
        },
        {
            "name": "Tom Garcia",
            "phone": "+1234567898",
            "interest": "Legal firm exploring client intake automation",
            "status": LeadStatus.NEW,
            "intent": LeadIntent.COLD,
            "last_message": "Send me some info and I'll review it.",
            "conversation_count": 1,
            "last_contact_at": now - timedelta(days=2),
        },
        {
            "name": "Amanda Taylor",
            "phone": "+1234567899",
            "interest": "Travel agency interested in vacation package promotions",
            "status": LeadStatus.CLOSED,
            "intent": LeadIntent.HOT,
            "last_message": "Signed the contract! Excited to get this rolling.",
            "conversation_count": 15,
            "last_contact_at": now - timedelta(days=3),
        },
    ]


def seed_database():
    """Seed the database with sample leads"""
    print("Connecting to database...")

    db = next(get_db())

    try:
        # Check if data already exists
        existing_count = db.query(Lead).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} leads. Skipping seed.")
            return

        # Add sample leads
        sample_leads = get_sample_leads()

        for lead_data in sample_leads:
            lead = Lead(**lead_data)
            db.add(lead)
            print(f"  Added: {lead_data['name']} ({lead_data['phone']})")

        db.commit()
        print(f"\nSuccessfully seeded {len(sample_leads)} sample leads!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("CloseZap AI - Database Seeder")
    print("=" * 50)
    seed_database()
