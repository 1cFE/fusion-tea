# Preparation replay

These commands were run on the accepted unchanged package. Metadata and oracle-scan deliberately refuse to overwrite existing receipts; replay in a separate checkout with a new empty preparation record. The declared study has not executed. The only new native evaluation is the pinned preparation baseline.

```bash
.codex-test/run python -m exploration.aries_integrated.studies.prepare_cost_study metadata
.codex-test/run python -m exploration.aries_integrated.studies.prepare_cost_study oracle-scan
.codex-test/run python -m scripts.study.indicators --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/manifest.json --groups exploration/aries_integrated/studies/axes.json --out exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/indicators.json
.codex-test/run python -m scripts.study.preflight gates --help
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python - <<'"'"'PY'"'"'
from pathlib import Path
from exploration.aries_integrated.studies.study_route import execute_baseline
print(execute_baseline(Path("exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/preparation")))
PY'
.codex-test/run python -m scripts.study.preflight gates --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/manifest.json --groups exploration/aries_integrated/studies/axes.json --identity exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/preparation/package_identity.json --baseline-result exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/preparation/baseline_result.json --out exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/preparation/preflight_results.json
```

The first standalone narrative-writing invocation failed before writing because `/tmp` was outside the repository import path. Adding `PYTHONPATH="$PWD"` allowed the documentation-only script to run. No native route failed or retried. No generated model, existing oracle body or frozen study was written.

Execution is a separate released action. Use the unchanged `execute_study` route with this record and the retained original integration return; verify with `--sample-size 113`. Before freeze, copy this study's actual new preflight into `results/integration/preflight_results.json`, identify other integration files as reused, and retain exact execution commit and commands. The coordinator owns snapshot/archive and commit.
