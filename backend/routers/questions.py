"""
Questions router — interactive doubt-clearing feature.
"""

from fastapi import APIRouter, Depends, HTTPException
from models.schemas import AskQuestionRequest, AskQuestionResponse
from services.auth_service import get_current_user
from services import session_service, ai_service

router = APIRouter(prefix="/api", tags=["Questions"])


@router.post("/ask-question", response_model=AskQuestionResponse)
async def ask_question(
    req: AskQuestionRequest,
    current_user: dict = Depends(get_current_user),
):
    """Answer a student's doubt using the session's PDF context."""
    # Get the stored PDF context for this session
    context = await session_service.get_session_context(
        req.session_id, current_user["id"]
    )

    if not context:
        raise HTTPException(status_code=404, detail="Session not found or no context available")

    # Get AI answer
    answer = await ai_service.answer_question(req.question, context)

    return AskQuestionResponse(answer=answer)
