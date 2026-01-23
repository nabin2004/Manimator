import json
from pathlib import Path
from datetime import datetime

def write_run_metrics(run_id, metrics_snapshot, base_dir="metrics_logs"):
    Path(base_dir).mkdir(parents=True, exist_ok=True)

    path = Path(base_dir) / f"{run_id}.json"
    payload = {
        "run_id": run_id,
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": metrics_snapshot,
    }

    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
