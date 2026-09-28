#!/bin/bash
set -eu
PRIMARY=/home/reid/1cfe/fusion-tea
RESTORE=/tmp/post-reveal-execution.OIh9Gv
TOOLS="$RESTORE/.project/active/aries-comparison-preparation/post-reveal-preparation/tools"
REGISTER="$PRIMARY/.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1"
cd "$RESTORE"
set +e
"$PRIMARY/.venv/bin/python" "$TOOLS/report.py" --attempt-dir "$REGISTER/attempts/first-forward" --observations "$REGISTER/observations.json" --store "$REGISTER/reports" --name first-forward > "$REGISTER/receipts/report.stdout" 2> "$REGISTER/receipts/report.stderr"
comparison_status=$?
set -e
printf '%s\n' "$comparison_status" > "$REGISTER/receipts/report.exit-status"
exit "$comparison_status"
