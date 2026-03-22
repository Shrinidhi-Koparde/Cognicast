"""
Upload router — handles PDF upload and triggers the content generation pipeline.
"""

import os
import uuid
import traceback
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from services.auth_service import get_current_user
from services import session_service
from config import settings

router = APIRouter(prefix="/api", tags=["Upload"])


@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    mode: str = Form(default="student"),
    current_user: dict = Depends(get_current_user),
):
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    # Validate mode
    if mode not in ("kids", "student", "exam"):
        raise HTTPException(status_code=400, detail="Mode must be: kids, student, or exam")

    # Save file temporarily
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.pdf"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)

    try:
        contents = await file.read()
        with open(filepath, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Run the full generation pipeline
    try:
        session = await session_service.create_session(
            user_id=current_user["id"],
            pdf_path=filepath,
            filename=file.filename,
            mode=mode,
        )
        return {
            "message": "Session created successfully",
            "session_id": session["id"],
            "status": session["status"],
        }
    except Exception as e:
        # Log the full traceback for debugging
        traceback.print_exc()
        # Clean up file on failure
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
