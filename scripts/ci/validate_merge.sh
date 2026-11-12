#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.."
exec "${IE212_PYTHON:-python}" scripts/ci/validate_merge.py "${1:-main}" "${@:2}"
