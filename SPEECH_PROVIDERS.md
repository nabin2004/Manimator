# Speech Providers — Swappable TTS Guide

Manimator's text-to-speech layer is **provider-agnostic**.  Every backend
implements the same `TTSEngine` interface, and you can switch between them
at startup via an environment variable — or at request time via the API.

---

## Architecture at a glance

```
                     ┌────────────────────┐
  API / Pipeline ──▶ │   TTSEngine (ABC)  │ ◀── uniform contract
                     └────────┬───────────┘
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
         ┌──────────┐  ┌──────────┐  ┌──────────────┐
         │ KittenTTS│  │ Your own │  │ Cloud (e.g.  │
         │ Provider │  │ Provider │  │ ElevenLabs)  │
         └──────────┘  └──────────┘  └──────────────┘
```

Every provider lives in `src/manimator/tts/providers/` and self-registers
by calling `register_provider("name", ProviderClass)` at module level.

---

## Built-in providers

### KittenTTS (`kitten`)

Lightweight, ONNX-based, CPU-only.  Ships models from 15 M to 80 M params.

| Variant     | Params | Disk   | HF repo                             |
|-------------|--------|--------|--------------------------------------|
| `mini`      | 80 M   | 80 MB  | `KittenML/kitten-tts-mini-0.8`      |
| `micro`     | 40 M   | 41 MB  | `KittenML/kitten-tts-micro-0.8`     |
| `nano`      | 15 M   | 56 MB  | `KittenML/kitten-tts-nano-0.8`      |
| `nano-int8` | 15 M   | 25 MB  | `KittenML/kitten-tts-nano-0.8-int8` |

**Install:**

```bash
pip install "kittentts>=0.8.1"
# or, if using uv with the project:
uv pip install "manimator[tts-kitten]"
```

**Configure** (`.env`):

```dotenv
TTS_PROVIDER=kitten
TTS_MODEL_VARIANT=mini   # mini | micro | nano | nano-int8
```

**Voices:** Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo

---

## Switching providers

### At startup (env var)

Set `TTS_PROVIDER` to any registered name:

```dotenv
TTS_PROVIDER=kitten          # default
TTS_PROVIDER=my_custom       # your own backend
```

### At request time (API)

Pass the optional `provider` field in the synthesis request:

```bash
curl -X POST http://localhost:8000/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "Bella", "provider": "kitten"}' \
  --output speech.wav
```

### Listing registered providers

```bash
curl http://localhost:8000/api/tts/providers
# {"providers": ["kitten"], "active": "kitten"}
```

---

## Writing your own provider

1. **Create a file** in `src/manimator/tts/providers/`, e.g. `my_backend.py`.

2. **Subclass `TTSEngine`** and implement three things:

```python
from manimator.tts.engine import TTSEngine
from manimator.tts.registry import register_provider
import numpy as np

class MyBackendProvider(TTSEngine):

    def __init__(self, **kwargs):
        # Accept any kwargs you need (api_key, model_path, …).
        # The registry passes **kwargs from get_provider().
        ...

    def generate(self, text: str, voice: str = "default",
                 speed: float = 1.0) -> np.ndarray:
        # Must return a 1-D float32 numpy array of PCM samples.
        ...

    def available_voices(self) -> list[str]:
        return ["default"]

    @property
    def sample_rate(self) -> int:
        return 24_000          # or 22050, 16000, etc.

register_provider("my_backend", MyBackendProvider)
```

3. **Register the import** in `src/manimator/tts/registry.py`:

```python
def _auto_register() -> None:
    from manimator.tts.providers import kitten       # noqa
    from manimator.tts.providers import my_backend   # noqa
```

4. **Set the env var** and you're done:

```dotenv
TTS_PROVIDER=my_backend
```

### Provider constructor kwargs

The registry calls `ProviderClass(**kwargs)`.  For the built-in Kitten
provider this includes `model_variant` and `cache_dir`.  For your own
provider, define whatever `__init__` kwargs make sense — they'll be
forwarded when the dependency layer constructs the engine.

---

## API reference (TTS endpoints)

| Method | Path                   | Description                              |
|--------|------------------------|------------------------------------------|
| POST   | `/api/tts/synthesize`  | Synthesize text → WAV audio stream       |
| GET    | `/api/tts/voices`      | List voices for the active provider      |
| GET    | `/api/tts/providers`   | List all registered providers            |

### POST `/api/tts/synthesize`

**Request body:**

```json
{
  "text": "Hello, world!",
  "voice": "Bella",
  "speed": 1.0,
  "provider": null
}
```

**Response:** `audio/wav` binary stream.

### GET `/api/tts/voices`

```json
{
  "provider": "kitten",
  "voices": ["Bella", "Jasper", "Luna", "Bruno", "Rosie", "Hugo", "Kiki", "Leo"]
}
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Unknown TTS provider 'foo'` | Make sure the provider module is imported in `_auto_register()` |
| `ModuleNotFoundError: kittentts` | `pip install kittentts>=0.8.1` |
| Slow first request | Model weights are downloaded on first use — subsequent calls use cache |
| `nano-int8` gives poor output | Known upstream issue — switch to `nano` or `micro` |
