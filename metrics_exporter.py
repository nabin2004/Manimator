from prometheus_client import start_http_server, Counter, Gauge, Histogram
import time
import json
from pathlib import Path

# Metrics
LATENCY = Histogram("llm_latency_seconds", "LLM call latency in seconds", ["phase"])
PROMPT_TOKENS = Counter("llm_prompt_tokens_total", "Prompt tokens used", ["phase"])
COMPLETION_TOKENS = Counter("llm_completion_tokens_total", "Completion tokens used", ["phase"])
CALLS = Counter("llm_calls_total", "Total number of LLM calls", ["phase"])

METRICS_DIR = "metrics_logs"

def load_metrics():
    # Parse JSON files
    for path in Path(METRICS_DIR).rglob("*.json"):
        try:
            with open(path) as f:
                data = json.load(f)
            m = data["metrics"]
            phase = m.get("phase", "default")
            
            LATENCY.labels(phase).observe(m.get("latency_s", 0))
            PROMPT_TOKENS.labels(phase).inc(m.get("prompt_tokens", 0))
            COMPLETION_TOKENS.labels(phase).inc(m.get("completion_tokens", 0))
            CALLS.labels(phase).inc(1)
        except Exception:
            print(f"Failed to load metrics from {path}")
        

if __name__ == "__main__":
    start_http_server(8000)
    print("Prometheus metrics server running on port 8000")

    while True:
        load_metrics()
        time.sleep(10)
