# Replay from retained evidence

Restore `../../post-reveal-preparation/package/post-reveal-v1.tar.gz` into an empty directory after verifying its adopted SHA256 `d65d6ea44517dba3d9012d06706e74fe3006247e2809f6b4bdd64edd85ab5a7a`. Follow the adopted `package/reproduce.md` for the licensed Python 3.12 sealed environment. Credentials are external prerequisites and are not retained here.

Run the restored adapter's `--verify` before using it. Reporting replay consumes the original retained attempt and observations; do not invoke `adapter.py --request` for replay. Original attempt/report receipts must be checked against retained bytes first. Export can be reproduced through the archived adapter's pure `export` function using the retained result, historical manifest and current model contract. Report replay uses restored `report.py`, original attempt, reviewed observations and a new verification store.

The original extraction root was `/tmp/post-reveal-execution.OIh9Gv`; its files are reproducible from the adopted archive. The durable evidence root is `/home/reid/1cfe/fusion-tea/.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1`. Detailed replay commands and independent results will be recorded after execution. Report comparisons must include all scientific rows, ratios, statuses, accounting, predicates and evidence identities. Absolute restoration/store paths and pointer identities may differ and must be disclosed.

## Repeat reporting without a physical run

The following commands restore source and replay only the original report into a fresh durable verification directory. The registered observations must retain SHA256 `e4305c2dafef62f5e0d0151dd11eb3c82b3d530ba50fe108632b5c9fd30a958e`. The original receipt check precedes replay; do not inspect the original SQLite database with a writable connection. If database inspection is needed, copy it and its sidecars first.

```bash
PRIMARY=/home/reid/1cfe/fusion-tea
PREP="$PRIMARY/.project/active/aries-comparison-preparation/post-reveal-preparation"
REGISTER="$PRIMARY/.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1"
RESTORE=$(mktemp -d /tmp/post-reveal-report-replay.XXXXXX)
printf '%s  %s\n' d65d6ea44517dba3d9012d06706e74fe3006247e2809f6b4bdd64edd85ab5a7a "$PREP/package/post-reveal-v1.tar.gz" | sha256sum -c -
tar -xzf "$PREP/package/post-reveal-v1.tar.gz" -C "$RESTORE"
TOOLS="$RESTORE/.project/active/aries-comparison-preparation/post-reveal-preparation/tools"
VERIFY=$(mktemp -d "$REGISTER/replay-verification/repeat.XXXXXX")
cd "$RESTORE"
"$PRIMARY/.venv/bin/python" "$TOOLS/adapter.py" --verify > "$VERIFY/identity.json"
"$PRIMARY/.venv/bin/python" - "$REGISTER" <<'PY'
import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1])
for subdir in ('attempts/first-forward','reports/first-forward'):
    folder=root/subdir
    receipt=json.loads((folder/'receipt.json').read_bytes())
    for name,digest in receipt['artifacts'].items():
        assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest, name
assert hashlib.sha256((root/'observations.json').read_bytes()).hexdigest()=='e4305c2dafef62f5e0d0151dd11eb3c82b3d530ba50fe108632b5c9fd30a958e'
print('Original attempt, report and observation identities verified')
PY
"$PRIMARY/.venv/bin/python" "$TOOLS/report.py" --attempt-dir "$REGISTER/attempts/first-forward" --observations "$REGISTER/observations.json" --store "$VERIFY/reports" --name replay
"$PRIMARY/.venv/bin/python" - "$REGISTER/reports/first-forward/report.json" "$VERIFY/reports/replay/report.json" <<'PY'
import json,sys
original,replayed=[json.load(open(path)) for path in sys.argv[1:]]
differences={key for key in original.keys()|replayed.keys() if original.get(key)!=replayed.get(key)}
assert differences <= {'first_report_attempt','attempt_path'}, differences
for key in ('numerical_comparison','current_predicates','observations_sha256','attempt_artifacts','selection','first_execution_attempt'):
    assert original[key]==replayed[key], key
print('Scientific content and evidence identities match; differing fields:', sorted(differences))
PY
```

The reporting-only commands use the documented sealed interpreter and archived pure reporting code. They do not require a new model evaluation or license checkout. Physical evaluation/restoration baseline testing additionally requires the original licensed runtime and documented environment setup. The independent review records tested environment versions; the archive is not a complete environment installer.

The independent [replay receipt](review/replay-receipt.json) and [review](review/replay-review.md) retain the actual verification and its differences. Their scripts under `review/replay-tools/` record the exact independent invocation and fixed replay name; use the fresh-directory procedure above for later repetitions. Original report bytes remain under `reports/first-forward/`, and the independent replay is separate under `replay-verification/reports/independent-replay/`.
