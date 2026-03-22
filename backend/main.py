"""
CAstPod Backend — FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from services.database import connect_db, close_db
from routers import auth, upload, sessions, questions
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="CAstPod API",
    description="AI-Powered Learning Platform — Transform PDFs into interactive podcasts",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated audio files
app.mount("/api/audio", StaticFiles(directory=settings.AUDIO_DIR), name="audio")

# Include routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(sessions.router)
app.include_router(questions.router)


@app.get("/")
async def root():
    return {
        "name": "CAstPod API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
