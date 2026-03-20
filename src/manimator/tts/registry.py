"""Provider registry — single place to look up, list, or add TTS backends."""

from __future__ import annotations
from typing import Dict, Type
from manimator.tts.engine import TTSEngine

_PROVIDERS: Dict[str, Type[TTSEngine]] = {}


def register_provider(name: str, cls: Type[TTSEngine]) -> None:
    _PROVIDERS[name.lower()] = cls


def get_provider(name: str, **kwargs) -> TTSEngine:
    """Instantiate a registered provider by name (case-insensitive)."""
    key = name.lower()
    if key not in _PROVIDERS:
        raise KeyError(
            f"Unknown TTS provider '{name}'. "
            f"Available: {', '.join(_PROVIDERS)}"
        )
    return _PROVIDERS[key](**kwargs)


def list_providers() -> list[str]:
    return list(_PROVIDERS.keys())


def _auto_register() -> None:
    """Import built-in providers so they self-register on import."""
    from manimator.tts.providers import kitten  # noqa: F401


_auto_register()
