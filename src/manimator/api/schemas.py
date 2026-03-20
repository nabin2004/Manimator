"""Pydantic request / response models for the REST API."""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional


# ── Animation pipeline ────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1, description="Topic to animate")
    output_dir: str = Field("./storage", description="Where to write rendered videos")


class SceneResult(BaseModel):
    scene_id: str
    status: str
    video_path: Optional[str] = None
    error_log: Optional[str] = None


class GenerateResponse(BaseModel):
    topic: str
    scenes: List[SceneResult]


# ── TTS ────────────────────────────────────────────────────────────────

class TTSSynthesizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to speak")
    voice: str = Field("Bella", description="Voice name")
    speed: float = Field(1.0, gt=0.1, le=5.0, description="Playback speed multiplier")
    provider: Optional[str] = Field(None, description="Override default TTS provider")


class TTSVoicesResponse(BaseModel):
    provider: str
    voices: List[str]


class TTSProvidersResponse(BaseModel):
    providers: List[str]
    active: str


# ── Flashcards ─────────────────────────────────────────────────────────

class FlashcardRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    num_cards: int = Field(10, ge=1, le=50)
    context: str = Field("", description="Optional extra context (e.g. lecture notes)")
    format: str = Field("json", description="'json' or 'anki_tsv'")


class FlashcardCard(BaseModel):
    front: str
    back: str
    tags: List[str] = []
    hint: Optional[str] = None


class FlashcardResponse(BaseModel):
    topic: str
    cards: List[FlashcardCard]
    anki_tsv: Optional[str] = None
