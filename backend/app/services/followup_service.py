"""Follow-up Service for automated lead follow-ups"""
import logging
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import SessionLocal
from app.models.lead import Lead, LeadStatus
from app.services.lead_service import LeadService
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)


class FollowUpService:
    """Service for managing automated follow-ups"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.ai_service = AIService()
        self.is_running = False

    def start(self):
        """Start the follow-up scheduler"""
        if not settings.followup_enabled:
            logger.info("Follow-up service is disabled")
            return

        if self.is_running:
            logger.warning("Follow-up scheduler is already running")
            return

        # Schedule the follow-up check job
        self.scheduler.add_job(
            self.check_inactive_leads,
            IntervalTrigger(minutes=settings.followup_check_interval_minutes),
            id="followup_check",
            replace_existing=True,
        )

        self.scheduler.start()
        self.is_running = True
        logger.info(
            f"Follow-up scheduler started. "
            f"Checking every {settings.followup_check_interval_minutes} minutes."
        )

    def stop(self):
        """Stop the follow-up scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Follow-up scheduler stopped")

    async def check_inactive_leads(self):
        """
        Check for inactive leads and send follow-up messages.
        This is called automatically by the scheduler.
        """
        logger.info("Checking for inactive leads...")

        db = SessionLocal()
        try:
            lead_service = LeadService(db)

            # Get inactive leads
            inactive_leads = lead_service.get_inactive_leads(
                hours_inactive=settings.followup_inactivity_hours
            )

            if not inactive_leads:
                logger.info("No inactive leads found")
                return

            logger.info(f"Found {len(inactive_leads)} inactive leads")

            # Process each lead
            for lead in inactive_leads:
                try:
                    await self.send_followup(lead, lead_service)
                    # Small delay between messages
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.error(f"Error sending follow-up to lead {lead.id}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error checking inactive leads: {e}", exc_info=True)
        finally:
            db.close()

    async def send_followup(self, lead: Lead, lead_service: LeadService):
        """
        Send a follow-up message to a lead.

        Args:
            lead: The lead to follow up with
            lead_service: Lead service instance for updates
        """
        logger.info(f"Sending follow-up to lead {lead.id}")

        # Generate follow-up message using AI
        followup_message = await self.ai_service.generate_followup_message(lead)

        # Send via Twilio (if configured)
        if settings.twilio_account_sid and settings.twilio_auth_token:
            success = await self._send_via_twilio(lead.phone, followup_message)

            if success:
                # Update lead's last contact time
                lead_service.update_lead_message(
                    lead.id,
                    "[Follow-up]",
                    followup_message
                )
                logger.info(f"Follow-up sent to lead {lead.id}")
            else:
                logger.warning(f"Failed to send follow-up to lead {lead.id}")
        else:
            logger.info(
                f"Twilio not configured. Would send to {lead.phone}: "
                f"{followup_message[:50]}..."
            )
            # Still update the lead
            lead_service.update_lead_message(
                lead.id,
                "[Follow-up - not sent]",
                followup_message
            )

    async def _send_via_twilio(self, to_phone: str, message: str) -> bool:
        """
        Send a message via Twilio.

        Args:
            to_phone: Phone number to send to
            message: Message content

        Returns:
            True if successful, False otherwise
        """
        try:
            from twilio.rest import Client

            client = Client(
                settings.twilio_account_sid,
                settings.twilio_auth_token
            )

            # Format phone number for WhatsApp
            to_whatsapp = f"whatsapp:{to_phone}"
            from_whatsapp = f"whatsapp:{settings.twilio_phone_number}"

            # Send message
            sent_message = client.messages.create(
                body=message,
                from_=from_whatsapp,
                to=to_whatsapp
            )

            logger.info(f"Twilio message sent: {sent_message.sid}")
            return True

        except Exception as e:
            logger.error(f"Error sending via Twilio: {e}", exc_info=True)
            return False

    async def send_followup_now(self, lead_id: int) -> dict:
        """
        Manually trigger a follow-up for a specific lead.

        Args:
            lead_id: The ID of the lead to follow up with

        Returns:
            Dictionary with result information
        """
        db = SessionLocal()
        try:
            lead_service = LeadService(db)
            lead = lead_service.get_lead(lead_id)

            if not lead:
                return {"success": False, "error": "Lead not found"}

            await self.send_followup(lead, lead_service)
            return {"success": True, "lead_id": lead_id}

        except Exception as e:
            logger.error(f"Error sending manual follow-up: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
        finally:
            db.close()


# Global follow-up service instance
followup_service = FollowUpService()