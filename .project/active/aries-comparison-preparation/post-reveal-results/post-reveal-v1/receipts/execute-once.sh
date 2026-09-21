#!/bin/bash
set -eu
PRIMARY=/home/reid/1cfe/fusion-tea
RESTORE=/tmp/post-reveal-execution.OIh9Gv
TOOLS="$RESTORE/.project/active/aries-comparison-preparation/post-reveal-preparation/tools"
REGISTER="$PRIMARY/.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1"
# This script records the single authorized invocation. Re-execution requires owner instruction.
test ! -e "$REGISTER/attempts/first-attempt.json"
set -a
source /home/reid/1cfe/agentic-mbse/.env
source "$PRIMARY/.venv/integration.env"
set +a
cd "$RESTORE"
set +e
"$PRIMARY/.venv/bin/python" "$TOOLS/adapter.py" --request "$REGISTER/request.json" --store "$REGISTER/attempts" --attempt first-forward > "$REGISTER/receipts/execution.stdout" 2> "$REGISTER/receipts/execution.stderr"
comparison_status=$?
set -e
printf '%s\n' "$comparison_status" > "$REGISTER/receipts/execution.exit-status"
exit "$comparison_status"
