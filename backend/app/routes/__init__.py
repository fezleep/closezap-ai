"""Routes module"""
from fastapi import APIRouter
from .webhook import router as webhook_router
from .leads import router as leads_router

api_router = APIRouter()
api_router.include_router(webhook_router, prefix="/webhook", tags=["webhook"])
api_router.include_router(leads_router, prefix="/leads", tags=["leads"])

__all__ = ["api_router"]