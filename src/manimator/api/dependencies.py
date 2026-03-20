"""Shared singleton resources for the API layer.

Lazily initialised so importing this module is always cheap — the heavy
objects (LLM client, TTS engine) are created on first access.
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from manimator.llm.llm import LLMWithMetrics
from manimator.tts.engine import TTSEngine
from manimator.tts.registry import get_provider

load_dotenv()


@lru_cache(maxsize=1)
def get_llm() -> LLMWithMetrics:
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "")
    os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL", "")
    base = ChatOpenAI(model="google/gemini-3-flash-preview", temperature=0.0)
    return LLMWithMetrics(base)


@lru_cache(maxsize=1)
def get_tts_engine() -> TTSEngine:
    provider_name = os.getenv("TTS_PROVIDER", "kitten")
    model_variant = os.getenv("TTS_MODEL_VARIANT", "mini")
    return get_provider(provider_name, model_variant=model_variant)
