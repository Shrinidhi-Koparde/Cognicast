"""
Application configuration — loads settings from .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # MongoDB
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "castpod")

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # ElevenLabs
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_STUDENT_VOICE_ID: str = os.getenv(
        "ELEVENLABS_STUDENT_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"
    )
    ELEVENLABS_MENTOR_VOICE_ID: str = os.getenv(
        "ELEVENLABS_MENTOR_VOICE_ID", "ErXwobaYiN019PkySvjV"
    )

    # Audio / TTS mode: "gtts" (free, default), "elevenlabs" (premium), "mock" (silent)
    MOCK_AUDIO: bool = os.getenv("MOCK_AUDIO", "false").lower() == "true"
    TTS_MODE: str = os.getenv("TTS_MODE", "gtts")

    # Paths
    UPLOAD_DIR: str = os.path.join(os.path.dirname(__file__), "uploads")
    AUDIO_DIR: str = os.path.join(os.path.dirname(__file__), "uploads", "audio")


settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.AUDIO_DIR, exist_ok=True)
