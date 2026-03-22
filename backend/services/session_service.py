"""
Session orchestration service — runs the full content generation pipeline.
"""

import os
import uuid
from datetime import datetime, timezone
from bson import ObjectId
from services.database import get_db
from services import pdf_service, ai_service, audio_service


async def create_session(user_id: str, pdf_path: str, filename: str, mode: str) -> dict:
    """
    Full pipeline: PDF → Extract → AI Generate → Audio → Save to MongoDB.

    Returns the complete session document.
    """
    db = get_db()

    # Create initial session record
    session = {
        "user_id": user_id,
        "title": _generate_title(filename),
        "mode": mode,
        "status": "processing",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "conversation": [],
        "summary": "",
        "cheat_sheet": "",
        "flashcards": [],
        "quiz": [],
        "diagrams": [],
        "audio_url": "",
        "pdf_text": "",
    }

    result = await db.sessions.insert_one(session)
    session_id = str(result.inserted_id)

    try:
        # Step 1: Extract PDF content
        await _update_status(db, session_id, "extracting")
        pdf_content = pdf_service.extract_content(pdf_path)
        chunks = pdf_content["chunks"]
        images = pdf_content["images"]

        # Store extracted text for doubt-answering context
        pdf_text = pdf_content["text"][:10000]  # Cap stored text

        # Step 2: Generate AI content (parallel-ish — sequential for API rate limits)
        await _update_status(db, session_id, "generating")

        conversation = await ai_service.generate_conversation(chunks, mode)
        summary = await ai_service.generate_summary(chunks)
        cheat_sheet = await ai_service.generate_cheat_sheet(chunks)
        flashcards = await ai_service.generate_flashcards(chunks)
        quiz = await ai_service.generate_quiz(chunks)

        # Step 3: Generate audio
        await _update_status(db, session_id, "audio")
        audio_url = await audio_service.generate_podcast(conversation)

        # Step 4: Save everything to MongoDB
        update_data = {
            "status": "completed",
            "conversation": conversation,
            "summary": summary,
            "cheat_sheet": cheat_sheet,
            "flashcards": flashcards,
            "quiz": quiz,
            "diagrams": images[:20],  # Limit stored images
            "audio_url": audio_url,
            "pdf_text": pdf_text,
        }

        await db.sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": update_data},
        )

        session.update(update_data)
        session["id"] = session_id
        return session

    except Exception as e:
        # Mark session as failed
        await db.sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"status": "failed", "error": str(e)}},
        )
        raise e
    finally:
        # Clean up uploaded PDF
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


async def get_session(session_id: str, user_id: str) -> dict | None:
    """Get a single session by ID, ensuring it belongs to the user."""
    db = get_db()
    session = await db.sessions.find_one({
        "_id": ObjectId(session_id),
        "user_id": user_id,
    })
    if session:
        session["id"] = str(session.pop("_id"))
        session.pop("pdf_text", None)  # Don't send raw text to frontend
    return session


async def list_sessions(user_id: str) -> list[dict]:
    """List all sessions for a user (summary view)."""
    db = get_db()
    cursor = db.sessions.find(
        {"user_id": user_id},
        {
            "_id": 1,
            "title": 1,
            "mode": 1,
            "status": 1,
            "created_at": 1,
        },
    ).sort("created_at", -1)

    sessions = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        sessions.append(doc)
    return sessions


async def get_session_context(session_id: str, user_id: str) -> str:
    """Get stored PDF text for doubt-answering context."""
    db = get_db()
    session = await db.sessions.find_one(
        {"_id": ObjectId(session_id), "user_id": user_id},
        {"pdf_text": 1},
    )
    return session.get("pdf_text", "") if session else ""


async def _update_status(db, session_id: str, status: str):
    await db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"status": status}},
    )


def _generate_title(filename: str) -> str:
    """Generate a clean title from the PDF filename."""
    name = os.path.splitext(filename)[0]
    # Replace underscores/hyphens with spaces, title case
    name = name.replace("_", " ").replace("-", " ")
    return name.title()[:100]
