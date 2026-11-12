#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.."
python_command="${IE212_PYTHON:-python}"
"$python_command" scripts/tasks/validate_contracts.py
"$python_command" -m unittest discover -s tests -t . -v
