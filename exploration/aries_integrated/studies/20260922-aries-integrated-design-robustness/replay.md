# Robustness replay

Restore the unchanged sealed lifecycle package and final retained support/executor sources into an isolated checkout at native execution commit `d976da4779bfc1575330bfc8d683e7968ef4e8e9`. Use a fresh record path; never execute into this immutable record. The record-local manifest includes the explicitly reviewed two-input HX price uncertainty tie. Retain the complete configuration, proposals and matched-design labels. Use the licensed .codex-test/run environment and pinned runtime from integration_return_used.json.

The original commands were:

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m exploration.aries_integrated.studies.design_support execute --record exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness --integration-return work/orchestration/goals/aries-integrated-lcoe/evidence/integration-attempt1/integration_return.json'
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m scripts.study.verify --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness/manifest.json --identity exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness/results/package_identity.json --store exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness/results/native/20260922-aries-integrated-design-robustness.db --sample-size 174 --out exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness/results/verification_summary.json'
.codex-test/run python -m exploration.aries_integrated.studies.design_reporting --record exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness --out exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness/results/accounting.json
MPLCONFIGDIR=/tmp/aries-design-matplotlib .codex-test/run python exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness/analyze_results.py
```

Before verification copy the exact preparation/package_identity.json into results/package_identity.json. Original baseline replay is reused under explicit provenance because executable, semantics, pinned headline and licensed runtime remain unchanged. Fresh indicators and all six preflight gates use the record-local manifest/groups. Both no-constraint-response groups received quoted owner authorization and missing-response findings before coordinator GO and launch.

All 174 native maps completed once; no retry or export recovery occurred. Reporting reads stored native outputs only. For reporting replay copy results and use a new output path for accounting.json because design_reporting refuses overwrite. analyze_results.py checks the immutable read-only store, emits matched comparisons and CSV, and creates readable summary plots and report; it does not load an evaluator. It compares identical uncertainty and fuel scenarios, marks either-side failures unrankable, and retains numerical differences.

Do not alter or remove WAL files or open the frozen SQLite store mutably. Replaying native evaluation requires a fresh store. snapshot/archive/freeze are coordinator-owned.
