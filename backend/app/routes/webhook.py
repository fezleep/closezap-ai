"""Webhook routes for receiving WhatsApp messages"""
import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lead import LeadIntent
from app.services.lead_service import LeadService
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_class=PlainTextResponse)
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Receive WhatsApp webhook from Twilio.

    Handles incoming messages and generates AI responses.
    """
    try:
        # Parse form data from Twilio
        form_data = await request.form()

        # Extract message details
        from_number = form_data.get("From", "")
        message_body = form_data.get("Body", "")
        message_sid = form_data.get("MessageSid", "")

        # Clean phone number (remove whatsapp: prefix if present)
        phone = from_number.replace("whatsapp:", "").strip()

        logger.info(f"Received webhook from {phone}: {message_body[:50]}...")

        if not phone or not message_body:
            logger.warning("Missing phone or message body in webhook")
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Initialize services
        lead_service = LeadService(db)
        ai_service = AIService()

        # Get or create lead
        lead = lead_service.get_or_create(phone, message_body)

        # Detect intent from message
        detected_intent = ai_service._detect_intent(message_body)
        logger.info(f"Detected intent '{detected_intent}' for lead {lead.id}")

        # Generate AI response
        ai_response = await ai_service.generate_response(
            lead=lead,
            user_message=message_body
        )

        # Update lead with conversation and intent
        lead_service.update_lead_message(
            lead.id,
            message_body,
            ai_response,
            detected_intent=LeadIntent(detected_intent)
        )

        # Log if HOT lead detected
        if detected_intent == "hot":
            logger.info(f"🔥 HOT LEAD detected! Lead {lead.id} - {phone}")

        # Send response via Twilio (return TwiML)
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{ai_response}</Message>
</Response>"""

        logger.info(f"Sent AI response to {phone} (intent: {detected_intent})")
        return PlainTextResponse(content=twiml_response, media_type="application/xml")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def webhook_health():
    """Health check endpoint for webhook"""
    return {"status": "healthy", "service": "webhook"}


@router.post("/analyze/{lead_id}")
async def analyze_lead_intent(
    lead_id: int,
    message: str,
    db: Session = Depends(get_db)
):
    """
    Analyze the intent of a message for a specific lead.

    Returns intent classification and suggestions.
    """
    try:
        lead_service = LeadService(db)
        ai_service = AIService()

        lead = lead_service.get_lead(lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Analyze intent
        analysis = await ai_service.analyze_lead_intent(lead, message)

        return {
            "lead_id": lead_id,
            "phone": lead.phone,
            "name": lead.name,
            "current_status": lead.status.value,
            "current_intent": lead.intent.value,
            "analysis": analysis
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing intent: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")