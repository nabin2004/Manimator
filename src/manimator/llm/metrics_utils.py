import os
from typing import Dict


def normalize_llm_metadata(metadata: dict) -> dict:
    token_usage = metadata.get("token_usage", {})

    return {
        "model_provider": metadata.get("model_provider"),
        "model_name": metadata.get("model_name"),
        "request_id": metadata.get("id"),
        "finish_reason": metadata.get("finish_reason"),

        "prompt_tokens": token_usage.get("prompt_tokens", 0),
        "completion_tokens": token_usage.get("completion_tokens", 0),
        "total_tokens": token_usage.get("total_tokens", 0),

        "cached_tokens": token_usage
            .get("prompt_tokens_details", {})
            .get("cached_tokens", 0),

        "reasoning_tokens": token_usage
            .get("completion_tokens_details", {})
            .get("reasoning_tokens", 0),

        "cost": token_usage.get("cost", 0),
        "is_byok": token_usage.get("is_byok", False),
    }
