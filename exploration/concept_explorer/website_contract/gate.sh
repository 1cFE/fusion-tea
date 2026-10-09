#!/usr/bin/env bash
# The website contract gate: does this checkout still serve what the website's pinned
# explorer frontend needs? Design: .project/active/explorer-api-contract-gate/design.md.
#
#   gate.sh                                  check this checkout (CI runs this on every push)
#   gate.sh record <sha> [--js-reverified]   re-record contract.txt from the website's pin,
#                                            then check this checkout against it
#
# Each step prints "step <name> <seconds>s". The exit status is non-zero if anything failed.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
export LC_NUMERIC=C  # step timings use a decimal point

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
CONTRACT_PY="$HERE/contract.py"
# Check-mode test tools, resolved once against the serving set (plan decision 2).
CHECK_TOOLS=(pytest==9.1.1 httpx==0.28.1)
SELF_TESTS=(
  exploration/concept_explorer/tests/test_cors.py
  exploration/concept_explorer/tests/test_website_contract.py
)
WORK="$(mktemp -d "${RUNNER_TEMP:-/tmp}/website-contract.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PY="$WORK/venv/bin/python"

usage() {
  echo "usage: gate.sh | gate.sh record <full-sha> [--js-reverified]" >&2
  exit 2
}

# step <name> <command...>: run the command and print how long it took.
step() {
  local name="$1" start="$EPOCHREALTIME" status=0
  shift
  "$@" || status=$?
  printf 'step %s %.1fs\n' "$name" "$(awk -v s="$start" -v e="$EPOCHREALTIME" 'BEGIN { print e - s }')"
  return "$status"
}

# retry <command...>: up to three attempts, for package downloads that fail transiently.
retry() {
  local attempt
  for attempt in 1 2 3; do
    "$@" && return 0
    echo "attempt $attempt of 3 failed: $*" >&2
    if [ "$attempt" -lt 3 ]; then sleep 5; fi
  done
  return 1
}

check_mode() {
  local failed=0 start="$EPOCHREALTIME"
  cd "$REPO"
  if [ "$(git config --bool core.sparseCheckout || true)" = true ]; then
    local paths
    mapfile -t paths < <(grep -v -e '^#' -e '^$' "$HERE/runtime_paths.txt")
    step sparse-checkout git sparse-checkout add "${paths[@]}"
  fi
  step venv uv venv -q --python 3.12 "$WORK/venv"
  step install retry uv pip install -q --python "$PY" -r requirements-serve.txt "${CHECK_TOOLS[@]}"
  # The contract check and the self-tests always both run.
  step contract "$PY" -I -B "$CONTRACT_PY" check || failed=1
  step self-tests "$PY" -B -m pytest -p no:cacheprovider -q "${SELF_TESTS[@]}" || failed=1
  printf 'step total %.1fs\n' "$(awk -v s="$start" -v e="$EPOCHREALTIME" 'BEGIN { print e - s }')"
  return "$failed"
}

record_mode() {
  local sha="$1"
  shift
  [[ "$sha" =~ ^[0-9a-f]{40}$ ]] || usage
  cd "$REPO"
  local cutoff
  cutoff="$(git show -s --format=%cI "$sha")"
  step venv uv venv -q --python 3.12 "$WORK/venv"
  step extract "$PY" -I -B "$CONTRACT_PY" extract "$sha" "$WORK/tree"
  # The pin's own serving set, fully pinned, so it installs without a cutoff. The test
  # tools resolve as of the pin's commit time, so recording depends only on the pin (N2).
  step install retry uv pip install -q --python "$PY" -r "$WORK/tree/requirements-serve.txt"
  step install-tools retry uv pip install -q --python "$PY" --exclude-newer "$cutoff" pytest httpx
  step record "$PY" -I -B "$CONTRACT_PY" record --tree "$WORK/tree" --pin "$sha" "$@"
  # Check this checkout against the new contract, which also reports stale waivers.
  "$HERE/gate.sh"
}

case "${1:-}" in
  "") [ $# -eq 0 ] || usage; check_mode ;;
  record) [ $# -ge 2 ] || usage; shift; record_mode "$@" ;;
  *) usage ;;
esac
