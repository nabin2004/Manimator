import os
import time
import json
import uuid
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from manimator.metrics.run_metrics import RunMetrics
from manimator.metrics.sink import write_run_metrics
from manimator.llm.metrics_utils import normalize_llm_metadata

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")


class LLMWithMetrics:
    def __init__(
        self,
        llm: ChatOpenAI,
        metrics_dir: str = "metrics_logs",
        default_phase: str = "default",
    ):
        self.llm = llm
        self.default_phase = default_phase
        self.run_metrics = RunMetrics()

        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

    def _generate_run_id(self) -> str:
        # time + uuid keeps ordering and uniqueness
        return f"run_{int(time.time())}_{uuid.uuid4().hex[:8]}"

    def invoke(self, prompt: str, phase: str | None = None, run_id: str | None = None):
        phase = phase or self.default_phase
        run_id = run_id or self._generate_run_id()

        start = time.time()
        result = self.llm.invoke(prompt)
        latency = time.time() - start

        raw_metadata = result.response_metadata
        metrics = normalize_llm_metadata(raw_metadata)

        self.run_metrics.record_call(
            phase=phase,
            prompt_tokens=metrics["prompt_tokens"],
            completion_tokens=metrics["completion_tokens"],
            latency_s=latency,
        )

        snapshot = {
            "run_id": run_id,
            "phase": phase,
            "latency_s": latency,
            **metrics,
            "raw_metadata": raw_metadata,
            "result": result.content,
        }

        # Persist aggregated metrics (non-overwriting)
        write_run_metrics(run_id, snapshot)

        # # Persist per-call snapshot (never overwritten)
        # log_path = self.metrics_dir / f"{run_id}_{phase}.json"
        # with open(log_path, "x") as f:
        #     json.dump(snapshot, f, indent=2)

        return result

    def snapshot(self):
        return self.run_metrics.snapshot()
