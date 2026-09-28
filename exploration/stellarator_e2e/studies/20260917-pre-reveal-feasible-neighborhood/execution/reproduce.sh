#!/usr/bin/env bash
# Use the retained environment; no dependency synchronization. Follow record.md stages.
set -euo pipefail
export PYTHONPATH=.:/home/reid/1cfe/teax/packages/teax-simkit
export STUDY_REQUIRE_TEAX=1
exec .codex-test/run python "$@"
