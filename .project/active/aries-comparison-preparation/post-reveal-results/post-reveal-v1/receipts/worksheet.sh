#!/bin/bash
set -eu
PRIMARY=/home/reid/1cfe/fusion-tea
RESTORE=/tmp/post-reveal-execution.OIh9Gv
TOOLS="$RESTORE/.project/active/aries-comparison-preparation/post-reveal-preparation/tools"
REGISTER="$PRIMARY/.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1"
cd "$RESTORE"
"$PRIMARY/.venv/bin/python" "$TOOLS/observations.py" --attempt-dir "$REGISTER/attempts/first-forward" --output "$REGISTER/observations-template.json"
