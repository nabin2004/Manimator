import os
import time
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from manimator.metrics.run_metrics import RunMetrics
from manimator.metrics.sink import write_run_metrics
from pathlib import Path

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# Create metrics container
run_metrics = RunMetrics()
run_id = "run_2026_01_24_001"

# Original LLM
llm_base = ChatOpenAI(model="xiaomi/mimo-v2-flash:free", temperature=0.0)

# Wrapper class
class LLMWithMetrics:
    def __init__(self, llm, run_metrics, run_id, default_phase="default"):
        self.llm = llm
        self.run_metrics = run_metrics
        self.run_id = run_id
        self.default_phase = default_phase
        os.makedirs("metrics_logs", exist_ok=True)

    def invoke(self, prompt, phase=None):
        phase = phase or self.default_phase

        start = time.time()
        result = self.llm.invoke(prompt)
        latency = time.time() - start

        usage = result.response_metadata['token_usage']
        self.run_metrics.record_call(
            phase=phase,
            prompt_tokens=usage['prompt_tokens'],
            completion_tokens=usage['completion_tokens'],
            latency_s=latency
        )

        write_run_metrics(self.run_id, metrics_snapshot=result.response_metadata)
        with open(f"metrics_logs/{self.run_id}_{phase}.json", "w") as f:
            json.dump(result.response_metadata, f, indent=2)

        return result

if __name__ == "__main__":
    llm = LLMWithMetrics(llm_base, run_metrics, run_id)
    result = llm.invoke("How are you today?", phase="greeting")
    print(result.content)

    write_run_metrics(run_id, run_metrics.snapshot())
