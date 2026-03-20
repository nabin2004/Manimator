"""Manimator FastAPI application.

Run with:
    uvicorn manimator.api.app:app --reload --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from manimator.api.routes import animation, tts, flashcards

app = FastAPI(
    title="Manimator API",
    description=(
        "REST API for the Manimator pipeline — generate math animations, "
        "synthesize speech (swappable TTS), and create Anki-ready flashcards."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(animation.router)
app.include_router(tts.router)
app.include_router(flashcards.router)


@app.get("/", tags=["root"])
def root():
    return {
        "service": "manimator",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": {
            "animation": "/api/animation",
            "tts": "/api/tts",
            "flashcards": "/api/flashcards",
        },
    }


@app.get("/health", tags=["root"])
def health():
    return {"status": "ok"}
