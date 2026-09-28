#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for project in avod-engine stream-delivery content-recs; do
  echo "==> $project"
  (cd "$ROOT/$project" && python -m unittest discover -s tests -v)
done
