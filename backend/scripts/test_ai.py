#!/usr/bin/env python3
"""Script to test AI responses without sending messages"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.lead import Lead, LeadStatus
from app.services.ai_service import AIService


async def test_ai_response(phone: str, message: str):
    """Test AI response generation"""
    db = SessionLocal()
    try:
        # Get or create lead
        lead = db.query(Lead).filter(Lead.phone == phone).first()
        if not lead:
            lead = Lead(
                phone=phone,
                name="Test User",
                status=LeadStatus.NEW,
            )
            db.add(lead)
            db.commit()
            db.refresh(lead)

        print(f"\n{'='*60}")
        print(f"Lead: {lead.name} ({lead.phone})")
        print(f"Status: {lead.status.value}")
        print(f"{'='*60}")
        print(f"\nUser message: {message}")
        print("-" * 60)

        # Generate response
        ai_service = AIService()
        response = await ai_service.generate_response(lead, message)

        print(f"\nAI Response:")
        print(response)
        print("=" * 60)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


async def test_followup(phone: str):
    """Test follow-up message generation"""
    db = SessionLocal()
    try:
        lead = db.query(Lead).filter(Lead.phone == phone).first()
        if not lead:
            print(f"Lead with phone {phone} not found")
            return

        print(f"\n{'='*60}")
        print(f"Generating follow-up for: {lead.name} ({lead.phone})")
        print(f"{'='*60}")

        ai_service = AIService()
        response = await ai_service.generate_followup_message(lead)

        print(f"\nFollow-up message:")
        print(response)
        print("=" * 60)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/test_ai.py <message>           - Test with default phone")
        print("  python scripts/test_ai.py --followup <phone>  - Test follow-up message")
        print("  python scripts/test_ai.py <phone> <message>   - Test with specific phone")
        return

    if sys.argv[1] == "--followup":
        if len(sys.argv) < 3:
            print("Phone number required for follow-up test")
            return
        asyncio.run(test_followup(sys.argv[2]))
    elif len(sys.argv) == 2:
        # Single argument is the message
        asyncio.run(test_ai_response("+1555000000", sys.argv[1]))
    else:
        # Two arguments: phone and message
        asyncio.run(test_ai_response(sys.argv[1], sys.argv[2]))


if __name__ == "__main__":
    main()