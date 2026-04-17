#!/usr/bin/env python3
"""Script to check database connection and status"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models.lead import Lead, LeadStatus
from sqlalchemy import inspect


def check_database():
    """Check database connection and display status"""
    print("=" * 50)
    print("CloseZap AI - Database Check")
    print("=" * 50)

    # Check connection
    try:
        with engine.connect() as conn:
            print("\n✓ Database connection: OK")
    except Exception as e:
        print(f"\n✗ Database connection: FAILED - {e}")
        return

    # Check tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\n✓ Tables found: {len(tables)}")
    for table in tables:
        print(f"  - {table}")

    # Check leads count
    db = SessionLocal()
    try:
        total_leads = db.query(Lead).count()
        print(f"\n✓ Total leads: {total_leads}")

        # Count by status
        for status in LeadStatus:
            count = db.query(Lead).filter(Lead.status == status).count()
            print(f"  - {status.value}: {count}")

        # Show recent leads
        recent = db.query(Lead).order_by(Lead.created_at.desc()).limit(5).all()
        if recent:
            print("\n✓ Recent leads:")
            for lead in recent:
                print(f"  - [{lead.id}] {lead.name or 'Unknown'} ({lead.phone}) - {lead.status.value}")

    except Exception as e:
        print(f"\n✗ Error querying leads: {e}")
    finally:
        db.close()

    print("\n" + "=" * 50)


if __name__ == "__main__":
    check_database()