#!/usr/bin/env bash
# Preparation does not run this file. Coordinator release and native CANDIDATE are required.
set -euo pipefail
root=$(cd "$(dirname "$0")/../../../../.." && pwd)
cd "$root"
workflow=exploration/stellarator_e2e/studies/20260918-computed-tritium-breeding/execution/workflow.py
.codex-test/run python "$workflow" prepare
.codex-test/run python "$workflow" baseline
.codex-test/run python "$workflow" scan
.codex-test/run python "$workflow" execute
.codex-test/run python "$workflow" verify
.codex-test/run python "$workflow" export
