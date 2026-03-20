"""KittenTTS provider — lightweight ONNX-based TTS that runs on CPU."""

from __future__ import annotations
from typing import List

import numpy as np

from manimator.tts.engine import TTSEngine
from manimator.tts.registry import register_provider


_MODEL_VARIANTS = {
    "mini": "KittenML/kitten-tts-mini-0.8",
    "micro": "KittenML/kitten-tts-micro-0.8",
    "nano": "KittenML/kitten-tts-nano-0.8",
    "nano-int8": "KittenML/kitten-tts-nano-0.8-int8",
}

DEFAULT_VARIANT = "mini"


class KittenTTSProvider(TTSEngine):
    """Wraps the ``kittentts`` library behind the common TTSEngine interface.

    Parameters
    ----------
    model_variant : str
        One of ``mini``, ``micro``, ``nano``, ``nano-int8``,
        **or** a full Hugging Face repo id.
    cache_dir : str | None
        Where to cache downloaded ONNX files.
    """

    def __init__(self, model_variant: str = DEFAULT_VARIANT, cache_dir: str | None = None):
        from kittentts import KittenTTS

        repo = _MODEL_VARIANTS.get(model_variant, model_variant)
        self._model = KittenTTS(repo, cache_dir=cache_dir)
        self._variant = model_variant

    def generate(self, text: str, voice: str = "Bella", speed: float = 1.0) -> np.ndarray:
        return self._model.generate(text, voice=voice, speed=speed, clean_text=True)

    def available_voices(self) -> List[str]:
        return self._model.available_voices

    @property
    def sample_rate(self) -> int:
        return 24_000


register_provider("kitten", KittenTTSProvider)
