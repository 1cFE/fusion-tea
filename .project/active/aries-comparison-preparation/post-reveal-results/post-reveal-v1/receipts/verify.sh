#!/bin/bash
set -eu
PRIMARY=/home/reid/1cfe/fusion-tea
RESTORE=/tmp/post-reveal-execution.OIh9Gv
PREP=.project/active/aries-comparison-preparation/post-reveal-preparation
TOOLS="$RESTORE/$PREP/tools"
REGISTER="$PRIMARY/.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1"
set -a
source /home/reid/1cfe/agentic-mbse/.env
source "$PRIMARY/.venv/integration.env"
set +a
cd "$RESTORE"
"$PRIMARY/.venv/bin/python" "$TOOLS/adapter.py" --verify > "$REGISTER/receipts/identity-verification.json"
"$PRIMARY/.venv/bin/python" -m pytest "$TOOLS/test_tools.py" -q -p no:cacheprovider > "$REGISTER/receipts/tests.txt" 2>&1
printf '%s\n' '{"schema_version":"adapter-request/v1","purpose":"synthetic_preparation","values":{}}' > "$RESTORE/synthetic.json"
"$PRIMARY/.venv/bin/python" "$TOOLS/adapter.py" --request "$RESTORE/synthetic.json" --store "$RESTORE/synthetic-attempts" --attempt baseline > "$REGISTER/receipts/synthetic.stdout" 2> "$REGISTER/receipts/synthetic.stderr"
