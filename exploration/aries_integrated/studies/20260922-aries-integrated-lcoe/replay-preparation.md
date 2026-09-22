# Preparation replay

[AGENT] Package checkpoint `e44a0ded` is the committed coherent input to preparation. Current executable `d13f4153accc48a3d6533a2d29a8e8b6b7cecd86644c322bb64f59fa402e419b`, semantic `419e6e3d7ba46320a1f88b5f478d36abb5ead85d2ecb6fcdb7aff5fcb2c1e131`. Use an isolated checkout with the retained package and final study interface/oracle sources. Never overwrite this record. Preparation executes one native baseline; the oracle scan is independent arithmetic only.

## Commands executed

```bash
.codex-test/run python -m exploration.aries_integrated.studies.prepare_lifecycle_study metadata --author-receipt work/active/WI-091_aries-integrated-lifecycle-cost/evidence/development-cases.json
.codex-test/run python -m exploration.aries_integrated.studies.prepare_lifecycle_study oracle-scan
.codex-test/run python -m exploration.aries_integrated.studies.prepare_lifecycle_study check-canonical
.codex-test/run python -m scripts.study.indicators --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/manifest.json --groups exploration/aries_integrated/studies/axes.json --out exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/indicators.json
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python - <<'"'"'PY'"'"'
from pathlib import Path
from exploration.aries_integrated.studies.study_route import execute_baseline
print(execute_baseline(Path("exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/preparation")))
PY'
.codex-test/run python -m scripts.study.preflight gates --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/manifest.json --groups exploration/aries_integrated/studies/axes.json --identity exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/preparation/package_identity.json --baseline-result exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/preparation/baseline_result.json --out exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/preparation/preflight_results.json
```

The final manifest includes the exact channel-specific IDC tolerance in `tiny-rate-tolerance.json`; retain its units and basis fields when preparing a fresh manifest. Earlier receipts are preserved: the first canonical check caught the oracle binding's salvage-magnitude sign, corrected without model changes; the first preflight refused incomplete tolerance schema fields, then passed after units/basis were supplied. One native baseline ran; no declared study points ran. The first indicator write rejected an unknown tolerance field before output. These metadata corrections do not relax shared gates.

## Released work still pending

The coordinator must obtain native integration and release declared execution. Its command will use this record's `execute_study.py`, with `--record` and `--integration-return` arguments, under the same native environment above. The exact integration return path will be recorded when it exists. The record-local executor fixes full-map numeric matching before execution; it retains native StudyRunner, complete evidence, and before/after persistent evidence hashes. `export-matching-check.json` tests representation parity, changed-key rejection and uniqueness of all 64 proposals without evaluating the package.

Use the actual new preparation preflight/identity/baseline when collecting integration evidence for freeze. Native all-point verification will use sample size 64 and the final manifest; all 364 comparison channels and 14 predicates are declared. Diagnostic controls remain outside those 64 finite-LCOE points. Their actual native and isolated diagnostic receipts are copied in `diagnostic-refusals.json`, `author-development-receipt.json` and `diagnostics/`; the latter contains the diagnostic runtime source copy and provenance. The independent oracle does not manufacture diagnostic outputs.
