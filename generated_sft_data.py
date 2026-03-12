"""
generate_sft_data.py
====================
Teacher-model distillation data generator for Manimator SFT training.

Architecture:
  - Gemini / any large teacher model via OpenRouter
  - Resume-safe incremental JSON persistence
  - Per-scene retry with exponential backoff
  - Pydantic schema validation on every saved entry
  - Rich console logging (falls back to stdlib if rich not installed)
  - Async-ready design with sync entrypoint

Usage:
  python generate_sft_data.py [--topics topics.txt] [--output ./storage/sft_data.json]
  python generate_sft_data.py --dry-run           # validate env only
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# ── Optional rich logging ───────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
        TimeElapsedColumn,
    )
    from rich.table import Table

    _console = Console(stderr=True)

    def log_info(msg: str) -> None:
        _console.log(f"[cyan]ℹ[/cyan]  {msg}")

    def log_success(msg: str) -> None:
        _console.log(f"[green]✓[/green]  {msg}")

    def log_warn(msg: str) -> None:
        _console.log(f"[yellow]⚠[/yellow]  {msg}")

    def log_error(msg: str) -> None:
        _console.log(f"[red]✗[/red]  {msg}")

    def log_panel(title: str, body: str, style: str = "blue") -> None:
        _console.print(Panel(body, title=title, border_style=style))

    HAS_RICH = True

except ImportError:  # pragma: no cover
    import logging

    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
    _logger = logging.getLogger("sft_gen")

    def log_info(msg: str) -> None:
        _logger.info(msg)

    def log_success(msg: str) -> None:
        _logger.info("✓  " + msg)

    def log_warn(msg: str) -> None:
        _logger.warning(msg)

    def log_error(msg: str) -> None:
        _logger.error(msg)

    def log_panel(title: str, body: str, style: str = "blue") -> None:
        _logger.info(f"[{title}] {body}")

    HAS_RICH = False


# ── Pydantic schema (optional but strongly recommended) ─────────────────────
try:
    from pydantic import BaseModel, Field, field_validator

    class SceneEntry(BaseModel):
        scene_name: str
        explanation: str = ""
        code: str = ""
        examples: list[dict[str, Any]] = Field(default_factory=list)
        metadata: dict[str, Any] = Field(default_factory=dict)

        @field_validator("scene_name")
        @classmethod
        def name_not_empty(cls, v: str) -> str:
            if not v.strip():
                raise ValueError("scene_name must not be empty")
            return v

    def validate_entry(entry: dict[str, Any]) -> dict[str, Any]:
        return SceneEntry(**entry).model_dump()

    HAS_PYDANTIC = True

except ImportError:  # pragma: no cover
    log_warn("pydantic not installed – skipping schema validation")
    HAS_PYDANTIC = False

    def validate_entry(entry: dict[str, Any]) -> dict[str, Any]:  # type: ignore[misc]
        return entry


# ── Manimator imports ───────────────────────────────────────────────────────
try:
    from langchain_openai import ChatOpenAI

    from manimator.intent.resolve import resolve_intent
    from manimator.llm.llm import LLMWithMetrics
    from manimator.metrics.run_metrics import RunMetrics
    from manimator.orchestration.langgraph_pipeline import run_pipeline
    from manimator.planner.resolve import plan_topic
except ImportError as exc:  # pragma: no cover
    log_error(f"Manimator / LangChain import failed: {exc}")
    log_error("Run:  pip install manimator langchain-openai python-dotenv")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

DEFAULT_OUTPUT = Path("./storage/sft_training_data.json")
TEACHER_MODEL = "google/gemini-2.5-flash-preview"
PIPELINE_VERSION = "manimator_v0.20.1"

# Retry config
MAX_RETRIES = 3
BACKOFF_BASE = 2.0  # seconds; doubles each attempt

# Default topics if none are provided via CLI
DEFAULT_TOPICS: list[str] = [
    """
    I want to understand two concepts:
    1. What is a Multi-Layer Perceptron (MLP) in machine learning?
    2. What is recursion in computer science?
    Explain both concepts clearly with simple examples.
    """,
    """
    Explain the following:
    1. Gradient Descent and how it minimises a loss function.
    2. The Attention mechanism in Transformer models.
    Use visual intuitions and concrete math where helpful.
    """,
    """
    Explain:
    1. Big-O notation for algorithm complexity.
    2. Binary Search Trees and their traversal methods.
    """,
]


# ──────────────────────────────────────────────────────────────────────────────
# Persistence helpers
# ──────────────────────────────────────────────────────────────────────────────


def load_existing_data(output_file: Path = DEFAULT_OUTPUT) -> dict[str, dict]:
    """Return {scene_name: entry} for all previously saved scenes."""
    if output_file.exists():
        try:
            with output_file.open("r", encoding="utf-8") as f:
                raw: list[dict] = json.load(f)
            return {e["scene_name"]: e for e in raw if "scene_name" in e}
        except (json.JSONDecodeError, KeyError) as exc:
            log_warn(f"Could not parse existing data ({exc}); starting fresh.")
    return {}


def save_scene_incremental(
    scene_name: str,
    scene_data: dict[str, Any],
    output_file: Path = DEFAULT_OUTPUT,
    *,
    model_source: str = TEACHER_MODEL,
    pipeline_version: str = PIPELINE_VERSION,
) -> None:
    """Atomically upsert a single scene into the JSON dataset."""
    existing = load_existing_data(output_file)

    entry: dict[str, Any] = {
        "scene_name": scene_name,
        "explanation": scene_data.get("explanation", ""),
        "code": scene_data.get("code", ""),
        "examples": scene_data.get("examples", []),
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_source": model_source,
            "pipeline_version": pipeline_version,
            "token_usage": scene_data.get("token_usage", {}),
            "latency_ms": scene_data.get("latency_ms"),
        },
    }

    # Validate schema
    entry = validate_entry(entry)

    existing[scene_name] = entry
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write to a temp file first, then rename (atomic on POSIX)
    tmp_file = output_file.with_suffix(".tmp")
    with tmp_file.open("w", encoding="utf-8") as f:
        json.dump(list(existing.values()), f, indent=2, ensure_ascii=False)
    tmp_file.replace(output_file)

    log_success(f"Saved scene '{scene_name}' → {output_file}")


# ──────────────────────────────────────────────────────────────────────────────
# Pipeline runner with retry
# ──────────────────────────────────────────────────────────────────────────────


def run_topic_with_retry(
    topic: str,
    llm: LLMWithMetrics,
    output_dir: Path,
    completed_scenes: set[str],
    output_file: Path,
    *,
    topic_index: int = 0,
) -> tuple[int, int]:
    """
    Run the full pipeline for one topic string.
    Returns (scenes_saved, scenes_skipped).
    """
    scenes_saved = 0
    scenes_skipped = 0

    # ── Intent resolution ──────────────────────────────────────────────────
    log_info(f"[Topic {topic_index + 1}] Resolving intent …")
    intent = resolve_intent(topic.strip(), llm=llm)

    # ── Scene planning ─────────────────────────────────────────────────────
    log_info(f"[Topic {topic_index + 1}] Planning scenes …")
    plan = plan_topic(intent, llm=llm)

    # ── Pipeline execution ────────────────────────────────────────────────
    log_info(f"[Topic {topic_index + 1}] Executing pipeline …")
    pipeline_state: dict[str, Any] = run_pipeline(
        llm=llm, plan=plan, output_dir=str(output_dir)
    )

    # ── Per-scene save with retry ─────────────────────────────────────────
    for scene_name, scene_data in pipeline_state.items():
        if scene_name in completed_scenes:
            log_warn(f"  Skipping already-completed scene '{scene_name}'")
            scenes_skipped += 1
            continue

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                save_scene_incremental(
                    scene_name,
                    scene_data,
                    output_file=output_file,
                )
                completed_scenes.add(scene_name)
                scenes_saved += 1
                break
            except Exception as exc:
                wait = BACKOFF_BASE ** attempt
                log_warn(
                    f"  Save attempt {attempt}/{MAX_RETRIES} for '{scene_name}' "
                    f"failed: {exc}. Retrying in {wait:.1f}s …"
                )
                if attempt == MAX_RETRIES:
                    log_error(f"  Giving up on scene '{scene_name}' after {MAX_RETRIES} attempts.")
                    traceback.print_exc()
                else:
                    time.sleep(wait)

    return scenes_saved, scenes_skipped


# ──────────────────────────────────────────────────────────────────────────────
# Summary table (rich only)
# ──────────────────────────────────────────────────────────────────────────────


def print_summary(
    total_saved: int,
    total_skipped: int,
    total_failed: int,
    output_file: Path,
    elapsed: float,
) -> None:
    if HAS_RICH:
        table = Table(title="Distillation Run Summary", show_lines=True)
        table.add_column("Metric", style="bold")
        table.add_column("Value", justify="right")
        table.add_row("Scenes saved", f"[green]{total_saved}[/green]")
        table.add_row("Scenes skipped (already done)", str(total_skipped))
        table.add_row("Scenes failed", f"[red]{total_failed}[/red]" if total_failed else "0")
        table.add_row("Output file", str(output_file))
        table.add_row("Elapsed", f"{elapsed:.1f}s")
        _console.print(table)
    else:
        log_info(
            f"Summary — saved={total_saved} skipped={total_skipped} "
            f"failed={total_failed} elapsed={elapsed:.1f}s → {output_file}"
        )


# ──────────────────────────────────────────────────────────────────────────────
# Environment bootstrap
# ──────────────────────────────────────────────────────────────────────────────


def bootstrap_env() -> None:
    """Validate and inject required environment variables."""
    load_dotenv()

    router_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    missing = []
    if not router_key:
        missing.append("OPENROUTER_API_KEY")
    if not base_url:
        missing.append("OPENAI_BASE_URL")
    if missing:
        log_error(f"Missing required environment variables: {', '.join(missing)}")
        log_error("Create a .env file or export them before running.")
        sys.exit(1)

    os.environ["OPENAI_API_KEY"] = router_key  # type: ignore[arg-type]
    os.environ["OPENAI_BASE_URL"] = base_url  # type: ignore[arg-type]


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate SFT distillation data from a teacher model via Manimator."
    )
    parser.add_argument(
        "--topics",
        type=Path,
        default=None,
        help="Path to a plain-text file of topics, one topic per line (or blank-line-separated paragraphs).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output JSON file (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--model",
        default=TEACHER_MODEL,
        help=f"OpenRouter model string (default: {TEACHER_MODEL})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate environment and print config, then exit.",
    )
    return parser.parse_args()


def load_topics_from_file(path: Path) -> list[str]:
    """Split a text file into individual topic strings (blank-line delimited)."""
    raw = path.read_text(encoding="utf-8")
    # Split on double newlines to support multi-line topic descriptions
    chunks = [c.strip() for c in raw.split("\n\n") if c.strip()]
    return chunks or [raw.strip()]


# ──────────────────────────────────────────────────────────────────────────────
# Main entry point
# ──────────────────────────────────────────────────────────────────────────────


def run(
    topics: list[str],
    output_file: Path,
    model: str = TEACHER_MODEL,
) -> None:
    bootstrap_env()

    log_panel(
        "Manimator SFT Distillation Generator",
        f"Teacher model : {model}\n"
        f"Topics        : {len(topics)}\n"
        f"Output        : {output_file}",
        style="bright_blue",
    )

    # Build LLM
    llm_base = ChatOpenAI(model=model, temperature=0.0)
    llm = LLMWithMetrics(llm_base)
    _run_metrics = RunMetrics()  # available for later aggregation

    output_dir = output_file.parent
    completed_scenes: set[str] = set(load_existing_data(output_file).keys())

    if completed_scenes:
        log_info(f"Resuming – {len(completed_scenes)} scene(s) already done.")

    total_saved = total_skipped = total_failed = 0
    t0 = time.monotonic()

    progress_ctx: Any
    if HAS_RICH:
        progress_ctx = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        )
    else:
        from contextlib import nullcontext
        progress_ctx = nullcontext()

    with progress_ctx as progress:
        task = (
            progress.add_task("Processing topics …", total=len(topics))
            if HAS_RICH
            else None
        )

        for idx, topic in enumerate(topics):
            topic_label = topic.strip()[:60].replace("\n", " ")
            if HAS_RICH:
                progress.update(task, description=f"Topic {idx + 1}: {topic_label} …")

            try:
                saved, skipped = run_topic_with_retry(
                    topic=topic,
                    llm=llm,
                    output_dir=output_dir,
                    completed_scenes=completed_scenes,
                    output_file=output_file,
                    topic_index=idx,
                )
                total_saved += saved
                total_skipped += skipped
            except Exception as exc:
                log_error(f"Topic {idx + 1} failed entirely: {exc}")
                traceback.print_exc()
                total_failed += 1

            if HAS_RICH:
                progress.advance(task)

    elapsed = time.monotonic() - t0
    print_summary(total_saved, total_skipped, total_failed, output_file, elapsed)


def main() -> None:
    args = parse_args()

    if args.dry_run:
        bootstrap_env()
        log_success("Environment OK – dry run complete.")
        return

    topics = (
        load_topics_from_file(args.topics)
        if args.topics
        else DEFAULT_TOPICS
    )

    run(topics=topics, output_file=args.output, model=args.model)


if __name__ == "__main__":
    main()