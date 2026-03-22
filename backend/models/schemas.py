"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ─── Auth ───────────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: str


# ─── Session / Content ─────────────────────────────────────────
class ConversationTurn(BaseModel):
    speaker: str  # "student" or "mentor"
    text: str


class Flashcard(BaseModel):
    front: str
    back: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct_index: int
    explanation: str = ""


class SessionResponse(BaseModel):
    id: str
    title: str
    mode: str
    status: str
    created_at: str
    conversation: list[ConversationTurn] = []
    summary: str = ""
    cheat_sheet: str = ""
    flashcards: list[Flashcard] = []
    quiz: list[QuizQuestion] = []
    diagrams: list[str] = []
    audio_url: str = ""


class SessionListItem(BaseModel):
    id: str
    title: str
    mode: str
    status: str
    created_at: str


class AskQuestionRequest(BaseModel):
    session_id: str
    question: str


class AskQuestionResponse(BaseModel):
    answer: str
