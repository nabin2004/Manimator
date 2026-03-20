"""Flashcard generation endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from manimator.api.dependencies import get_llm
from manimator.api.schemas import FlashcardRequest, FlashcardResponse, FlashcardCard
from manimator.flashcards.generator import generate_flashcards

router = APIRouter(prefix="/api/flashcards", tags=["flashcards"])


@router.post("/generate", response_model=FlashcardResponse)
def create_flashcards(req: FlashcardRequest):
    """Generate a deck of flashcards for the given topic."""
    llm = get_llm()
    try:
        deck = generate_flashcards(
            llm, topic=req.topic, num_cards=req.num_cards, context=req.context
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Flashcard generation failed: {exc}")

    cards = [
        FlashcardCard(front=c.front, back=c.back, tags=c.tags, hint=c.hint)
        for c in deck.cards
    ]

    anki_tsv = deck.to_anki_tsv() if req.format == "anki_tsv" else None

    return FlashcardResponse(topic=deck.topic, cards=cards, anki_tsv=anki_tsv)


@router.post("/generate/anki", response_class=PlainTextResponse)
def create_flashcards_anki(req: FlashcardRequest):
    """Generate flashcards and return Anki-importable TSV directly."""
    llm = get_llm()
    try:
        deck = generate_flashcards(
            llm, topic=req.topic, num_cards=req.num_cards, context=req.context
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Flashcard generation failed: {exc}")

    return PlainTextResponse(
        content=deck.to_anki_tsv(),
        media_type="text/tab-separated-values",
        headers={"Content-Disposition": 'attachment; filename="flashcards.tsv"'},
    )
