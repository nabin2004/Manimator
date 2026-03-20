"""Text-to-Speech endpoints — provider-agnostic thanks to TTSEngine."""

from __future__ import annotations

import io
import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from manimator.api.dependencies import get_tts_engine
from manimator.api.schemas import (
    TTSProvidersResponse,
    TTSSynthesizeRequest,
    TTSVoicesResponse,
)
from manimator.tts.registry import get_provider, list_providers

router = APIRouter(prefix="/api/tts", tags=["tts"])


def _engine_for_request(provider_override: str | None = None):
    if provider_override:
        try:
            return get_provider(provider_override)
        except KeyError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
    return get_tts_engine()


@router.post("/synthesize")
def synthesize(req: TTSSynthesizeRequest):
    """Synthesize speech and return a WAV audio stream."""
    engine = _engine_for_request(req.provider)

    try:
        audio = engine.generate(req.text, voice=req.voice, speed=req.speed)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {exc}")

    import soundfile as sf

    buf = io.BytesIO()
    sf.write(buf, audio, engine.sample_rate, format="WAV")
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="audio/wav",
        headers={"Content-Disposition": 'attachment; filename="speech.wav"'},
    )


@router.get("/voices", response_model=TTSVoicesResponse)
def voices():
    engine = get_tts_engine()
    active_provider = os.getenv("TTS_PROVIDER", "kitten")
    return TTSVoicesResponse(
        provider=active_provider,
        voices=engine.available_voices(),
    )


@router.get("/providers", response_model=TTSProvidersResponse)
def providers():
    active = os.getenv("TTS_PROVIDER", "kitten")
    return TTSProvidersResponse(providers=list_providers(), active=active)
