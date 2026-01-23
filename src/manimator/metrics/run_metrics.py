from collections import defaultdict
from dataclasses import dataclass

@dataclass
class PhaseMetrics:
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_s: float = 0.0
    retries: int = 0


class RunMetrics:
    def __init__(self):
        self.by_phase = defaultdict(PhaseMetrics)

    def record_call(self, phase, *, prompt_tokens, completion_tokens, latency_s):
        m = self.by_phase[phase]
        m.calls += 1
        m.prompt_tokens += prompt_tokens
        m.completion_tokens += completion_tokens
        m.latency_s += latency_s

    def record_retry(self, phase):
        self.by_phase[phase].retries += 1

    def snapshot(self):
        return {
            phase: vars(metrics)
            for phase, metrics in self.by_phase.items()
        }
