from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional


class Flashcard(BaseModel):
    front: str
    back: str
    tags: List[str] = []
    hint: Optional[str] = None


class FlashcardDeck(BaseModel):
    topic: str
    cards: List[Flashcard]

    def to_anki_tsv(self) -> str:
        """Export in Anki-importable tab-separated format.

        Each line: front<TAB>back<TAB>tags
        Tags are space-separated, prefixed with the topic slug.
        """
        lines: list[str] = []
        topic_tag = self.topic.lower().replace(" ", "_")
        for card in self.cards:
            tags = " ".join([topic_tag, *card.tags]) if card.tags else topic_tag
            front = card.front.replace("\t", " ").replace("\n", "<br>")
            back = card.back.replace("\t", " ").replace("\n", "<br>")
            if card.hint:
                back = f"{back}<br><br><i>Hint: {card.hint}</i>"
            lines.append(f"{front}\t{back}\t{tags}")
        return "\n".join(lines)

    def to_anki_csv(self) -> str:
        """Alias kept for discoverability; same tab-separated format Anki expects."""
        return self.to_anki_tsv()
