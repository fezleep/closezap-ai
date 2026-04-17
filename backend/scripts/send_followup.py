#!/usr/bin/env python3
"""Script to manually trigger follow-up messages"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.lead import Lead, LeadStatus
from app.services.followup_service import followup_service
from app.services.lead_service import LeadService


async def send_followup_to_lead(lead_id: int):
    """Send follow-up to a specific lead"""
    db = SessionLocal()
    try:
        lead_service = LeadService(db)
        lead = lead_service.get_lead(lead_id)

        if not lead:
            print(f"Lead {lead_id} not found")
            return

        print(f"Sending follow-up to lead {lead_id} ({lead.phone})...")
        await followup_service.send_followup(lead, lead_service)
        print("Follow-up sent successfully!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


async def check_inactive():
    """Check for inactive leads"""
    print("Checking for inactive leads...")
    await followup_service.check_inactive_leads()


def list_inactive_leads():
    """List all inactive leads"""
    db = SessionLocal()
    try:
        lead_service = LeadService(db)
        leads = lead_service.get_inactive_leads(hours_inactive=24)

        if not leads:
            print("No inactive leads found")
            return

        print(f"Found {len(leads)} inactive leads:")
        for lead in leads:
            print(f"  - [{lead.id}] {lead.name or 'Unknown'} ({lead.phone})")
            print(f"    Last contact: {lead.last_contact_at}")

    finally:
        db.close()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/send_followup.py <lead_id>  - Send follow-up to specific lead")
        print("  python scripts/send_followup.py --check    - Check all inactive leads")
        print("  python scripts/send_followup.py --list     - List inactive leads")
        return

    if sys.argv[1] == "--check":
        asyncio.run(check_inactive())
    elif sys.argv[1] == "--list":
        list_inactive_leads()
    else:
        try:
            lead_id = int(sys.argv[1])
            asyncio.run(send_followup_to_lead(lead_id))
        except ValueError:
            print("Invalid lead ID")


if __name__ == "__main__":
    main()