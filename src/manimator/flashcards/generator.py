"""Flashcard generation agent — uses the project LLM to produce Anki-ready decks."""

from __future__ import annotations
import json

from manimator.flashcards.schema import FlashcardDeck
from manimator.flashcards.prompt import FLASHCARD_SYSTEM_PROMPT, FLASHCARD_USER_TEMPLATE


def generate_flashcards(
    llm,
    topic: str,
    num_cards: int = 10,
    context: str = "",
) -> FlashcardDeck:
    """Ask the LLM for flashcards and parse them into a validated deck.

    Parameters
    ----------
    llm : LLMWithMetrics
        The shared LLM wrapper used across the pipeline.
    topic : str
        Subject to generate cards about.
    num_cards : int
        Desired number of cards (the LLM may return slightly fewer).
    context : str
        Extra material (e.g. lecture notes) to ground the cards.
    """
    user_msg = FLASHCARD_USER_TEMPLATE.format(
        topic=topic, num_cards=num_cards, context=context
    )
    full_prompt = f"{FLASHCARD_SYSTEM_PROMPT}\n\n{user_msg}"

    result = llm.invoke(full_prompt, prompt_version="flashcard_v1", phase="flashcard_gen")
    raw = result.content.strip()

    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"):
            raw = raw[: raw.rfind("```")]

    data = json.loads(raw)
    return FlashcardDeck(**data)
