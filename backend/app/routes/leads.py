"""Lead management routes"""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lead import Lead, LeadStatus, LeadIntent, LeadResponse, LeadUpdate, LeadIntentAnalysis
from app.services.lead_service import LeadService
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=List[LeadResponse])
async def get_leads(
    status: Optional[LeadStatus] = Query(None, description="Filter by lead status"),
    intent: Optional[LeadIntent] = Query(None, description="Filter by lead intent"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: Session = Depends(get_db)
):
    """
    Get all leads with optional filtering.

    - **status**: Filter leads by status (new, engaged, closed)
    - **intent**: Filter leads by intent (hot, warm, cold)
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        lead_service = LeadService(db)
        leads = lead_service.get_leads(status=status, intent=intent, skip=skip, limit=limit)
        logger.info(f"Retrieved {len(leads)} leads")
        return leads
    except Exception as e:
        logger.error(f"Error fetching leads: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching leads")


@router.get("/hot", response_model=List[LeadResponse])
async def get_hot_leads(
    limit: int = Query(50, ge=1, le=200, description="Maximum number of records"),
    db: Session = Depends(get_db)
):
    """
    Get all HOT leads (ready to buy).

    These are leads that have shown strong buying signals.
    """
    try:
        lead_service = LeadService(db)
        leads = lead_service.get_hot_leads(limit=limit)
        logger.info(f"Retrieved {len(leads)} hot leads")
        return leads
    except Exception as e:
        logger.error(f"Error fetching hot leads: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching hot leads")


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific lead by ID.

    - **lead_id**: The ID of the lead to retrieve
    """
    try:
        lead_service = LeadService(db)
        lead = lead_service.get_lead(lead_id)

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        return lead
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching lead {lead_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching lead")


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a lead's information.

    - **lead_id**: The ID of the lead to update
    - **lead_update**: Fields to update (name, interest, status, intent, last_message)
    """
    try:
        lead_service = LeadService(db)

        # Check if lead exists
        existing_lead = lead_service.get_lead(lead_id)
        if not existing_lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Update lead
        updated_lead = lead_service.update_lead(lead_id, lead_update)
        logger.info(f"Updated lead {lead_id}")

        return updated_lead
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating lead {lead_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error updating lead")


@router.patch("/{lead_id}/status", response_model=LeadResponse)
async def update_lead_status(
    lead_id: int,
    status: LeadStatus,
    db: Session = Depends(get_db)
):
    """
    Update a lead's status.

    - **lead_id**: The ID of the lead to update
    - **status**: New status (new, engaged, closed)
    """
    try:
        lead_service = LeadService(db)

        # Check if lead exists
        existing_lead = lead_service.get_lead(lead_id)
        if not existing_lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Update status
        updated_lead = lead_service.update_status(lead_id, status)
        logger.info(f"Updated lead {lead_id} status to {status}")

        return updated_lead
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating lead status {lead_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error updating lead status")


@router.patch("/{lead_id}/intent", response_model=LeadResponse)
async def update_lead_intent(
    lead_id: int,
    intent: LeadIntent,
    db: Session = Depends(get_db)
):
    """
    Update a lead's intent classification.

    - **lead_id**: The ID of the lead to update
    - **intent**: New intent (hot, warm, cold)
    """
    try:
        lead_service = LeadService(db)

        # Check if lead exists
        existing_lead = lead_service.get_lead(lead_id)
        if not existing_lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Update intent
        updated_lead = lead_service.update_intent(lead_id, intent)
        logger.info(f"Updated lead {lead_id} intent to {intent}")

        return updated_lead
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating lead intent {lead_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error updating lead intent")


@router.post("/{lead_id}/close", response_model=LeadResponse)
async def close_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark a lead as closed (converted to customer).

    - **lead_id**: The ID of the lead to close
    """
    try:
        lead_service = LeadService(db)

        # Check if lead exists
        existing_lead = lead_service.get_lead(lead_id)
        if not existing_lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Mark as closed
        closed_lead = lead_service.mark_closed(lead_id)
        logger.info(f"Lead {lead_id} marked as closed")

        return closed_lead
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error closing lead {lead_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error closing lead")


@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a lead.

    - **lead_id**: The ID of the lead to delete
    """
    try:
        lead_service = LeadService(db)

        # Check if lead exists
        existing_lead = lead_service.get_lead(lead_id)
        if not existing_lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Delete lead
        lead_service.delete_lead(lead_id)
        logger.info(f"Deleted lead {lead_id}")

        return {"message": "Lead deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting lead {lead_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error deleting lead")