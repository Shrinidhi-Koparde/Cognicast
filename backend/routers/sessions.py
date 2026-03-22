"""
Sessions router — list and retrieve generated sessions.
"""

from fastapi import APIRouter, Depends, HTTPException
from services.auth_service import get_current_user
from services import session_service

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])


@router.get("")
async def list_sessions(current_user: dict = Depends(get_current_user)):
    """List all sessions for the authenticated user."""
    sessions = await session_service.list_sessions(current_user["id"])
    return {"sessions": sessions}


@router.get("/{session_id}")
async def get_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Get full session details by ID."""
    session = await session_service.get_session(session_id, current_user["id"])
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
