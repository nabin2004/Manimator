import json
from pathlib import Path
from datetime import datetime


def write_run_metrics(run_id, metrics_snapshot, base_dir="metrics_logs"):
    now = datetime.utcnow()

    # Folder structure: metrics_logs/YYYY-MM-DD/HH-MM-SS-ffffff
    date_dir = now.strftime("%Y-%m-%d")
    time_dir = now.strftime("%H-%M-%S-%f")

    base_path = Path(base_dir) / date_dir / time_dir
    base_path.mkdir(parents=True, exist_ok=True)

    path = base_path / f"{run_id}.json"

    payload = {
        "run_id": run_id,
        "timestamp": now.isoformat(),
        "metrics": metrics_snapshot,
    }

    # overwrite is fine here since run_id is unique
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
