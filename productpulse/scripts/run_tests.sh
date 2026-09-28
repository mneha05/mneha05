#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python -m unittest discover -s tests -v
python generator/generate_events.py --users 500 --days 10 --out /tmp/productpulse-events.jsonl
python - <<\'PY\'
import json
from pathlib import Path
from analytics.oracle import funnel, retention, experiment_metrics
rows=[json.loads(x) for x in Path("/tmp/productpulse-events.jsonl").read_text().splitlines()]
print("funnel", funnel(rows))
print("d1_retention", retention(rows,1))
print("experiment", experiment_metrics(rows))
PY
