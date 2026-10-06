# Magnet plant-map reproducibility checks — 2026-10-05

[AGENT] Reporting rebuild and bounded current-runtime replay pass. This report checks evidence integrity and numerical reproducibility; the sealed study's engineering conclusions remain conditional on its stated assumptions. No models, generated packages, supplied case policy, original stores, snapshot or native results were changed.

## Evidence integrity and reporting

[AGENT] Snapshot SHA-256 remains `d494d0e92768ff6ed2498c32f9d24fc1cee9e8562cf863e269f92a01eed46de7`. [check_reproducibility.py](check_reproducibility.py) resolves package-relative, record-relative and repository-relative hash entries. All 132 distinct file/aggregate checks pass: 117 tracked paths and 15 local files or directory aggregates. This includes all eight original SQLite stores and aggregate hashes over both per-case artifact directories. Exact hashes, paths and tracking status are in [seal-render-receipt.json](seal-render-receipt.json).

[AGENT] The renderer ran into an empty temporary directory. All three SVGs, three PNGs, three CSVs and `provenance.json` reproduce byte for byte. Before, rebuilt and after hashes are recorded in the seal/render receipt. Its assertions pass for 2,921 unique retained cases, selected-case/LCOE parity and account closure below 1e-9 USD/MWh. Reporting arithmetic does not repeat plant calculation or policy selection.

[AGENT] The reference, REBCO and Nb₃Sn live package names and indicator-input fingerprints match their sealed manifests. Their semantic and executable fingerprints match the retained integration identities. Full identities are in the seal/render receipt. The current TEAx revision is `8d877460ac4f6f264561d916e40c1708adb13397`. [runtime-receipt.json](runtime-receipt.json) records module locations and verification hashes. All current-runtime commands used `uv run --no-sync`, retained the owner's editable agentic-mbse, and sourced the license/integration environment without printing credentials.

## Full verification and bounded replay

[INHERITED: sealed results/verification_summary.json] The retained full verification covers 2,115 REBCO cases (2,111 completed and four domain refusals) and 806 completed Nb₃Sn cases. It compares 1,423 and 1,422 nonconstant scalar channels respectively: 3,003,953 + 1,146,132 = 4,150,085 comparisons. All 73 predicate verdicts per completed case are rederived from oracle operands, and statuses and refusals are compared. No scalar, verdict, status or refusal disagreement is retained. Four REBCO constant channels and five Nb₃Sn constant channels (including `eps_min`) are excluded. Two static-load channels per arm have no oracle leg: `nuclear_density_eff` and `q_structure_nuclear`; their identity checks are distinct from independent oracle comparison. Agreement uses the reviewed maximum of 1e-9 relative and 1e-9 absolute per channel unit, with exact nonfinite matching.

[AGENT] The existing four-case smoke verification matches its retained receipt hash. A new replay of the first two declared cases per material passes 5,690 covered scalar comparisons and all predicates under the same verifier. [fresh-smoke-verification.json](fresh-smoke-verification.json) retains that result. It reads the original local supplied case list and oracle scan. It is a four-case smoke check, not a fresh replay of all 2,921 cases. Numeric 0/1 values under boolean annotations produce the existing Pydantic serialization warnings; no inputs or outputs were altered.

[AGENT] [portable-smoke-fixture.json](portable-smoke-fixture.json) captures the same four sealed supplied case records, labels, per-case hashes and original oracle-scan rows, plus one non-executed base record needed to resolve operating-point classification. [portable_smoke.py](portable_smoke.py) checks the fixture, snapshot and sealed tool/oracle source hashes, uses the unchanged executor's integration CANDIDATE, package-cleanliness and live fingerprint gates, then uses the unchanged full-channel verifier. Its explicit fixture provider and empty temporary case/scan paths avoid reading the ignored original case list, oracle scan or stores. This provides a bounded checkout regression example. It does not reconstruct the original policy or establish full fresh replay.

[AGENT] The portable run passes all 5,690 covered scalar comparisons and all 73 predicates per case with zero scalar, verdict, refusal or status disagreements. [portable-smoke-receipt.json](portable-smoke-receipt.json) captures this session's result, fixture hash, sealed source checks and temporary output location. The runner itself writes receipts only into its fresh temporary directory. The first fixture attempt exposed an absent Nb₃Sn base record needed for status classification; the fixture now retains that exact source record as non-executed supporting context, without changing any executed input.

## Focused tests

[AGENT] After inspecting test coverage, the material implementation, plant material variants, policy reproduction/MR-7 isolation and oracle-entry tests passed in the current runtime. The combined run reported 114 passing tests and one stale repository-pin assertion in dependency provenance. The parent corrected that assertion to the intentional current agentic-mbse commit `c37ff53b5b6f10e8dc8733d7f4c85d22877429af`; current pin/shape checks then passed twice. The provenance suite also passed all three tests using the sealed historical wheel target. That second context proves the recorded wheel hashes and public APIs; it does not assert that the current editable installation is those historical wheels. Receipts: [focused-tests.txt](focused-tests.txt), [current-pin-tests.txt](current-pin-tests.txt), [provenance-tests.txt](provenance-tests.txt).

## Checkout requirements and branch scope

[AGENT] After the helper style fixes, targeted Ruff checks pass for both new scripts and the dependency-provenance test, and both scripts pass format checks. The final seal/render rerun again passes all 132 hashes and all ten exact reporting outputs. The final portable rerun again passes all four cases and 5,690 scalar comparisons. Compact receipts: [final-focused-lint.txt](final-focused-lint.txt), [final-seal-render.txt](final-seal-render.txt), [final-portable-smoke.txt](final-portable-smoke.txt).

[AGENT] The reporting rebuild is usable from tracked study summary, case CSV, snapshot and renderer, given the plotting dependencies. Full numerical replay is not immediately usable from Git alone. The declared `exploration/stellarator_materials/studies/cases.json`, original `results/oracle_scan.json`, full per-case exports, detailed oracle verification, eight SQLite stores and native artifact directories are machine-local. Their exact hashes are retained by the snapshot and checked here. Restore those exact artifacts before following the full replay instructions, or reconstruct the policy and scan in a separate study record; the sealed producers' write-once protections remain applicable. A bare checkout also needs the separately installed licensed SysIDE/codegen dependencies, configured integration environment and exact TEAx checkout. The portable fixture requires those runtime dependencies but no original native stores or ignored study inputs.

[AGENT] The actual remote main object is `f96ad312c63e8c66695971b12feab971f3ba6eb3`, read by the parent; its merge base with this branch is `499bdd7741f36221e6298c79456715ef395c9cf6`. The upcoming three-dot diff contains 1,855 files, including 1,697 under `exploration/stellarator_materials`. These are mostly the reviewed generated package and study evidence. Published editorial changes are already before the merge base. Local `main`/`origin/main` at `16acbb768` were stale and produce a broader diff that is not the upcoming PR scope. [branch-scope.json](branch-scope.json) records counts. No `.db`, `.sqlite`, `.pyc`, `__pycache__`, `.venv` or `_work` garbage appears in the actual-base diff. The pre-existing untracked status report was preserved.

[AGENT] Actual-base `git diff --check` returns 3,464 diagnostics in 382 files. Of those, 2,922 are the sealed `results/cases.csv` CRLF endings; the rest are preserved/generated package bytes and three build-diff diagnostics. [branch-diff-check.txt](branch-diff-check.txt) records per-file counts. Changing those bytes would invalidate the sealed package/evidence identity, so they remain recorded exceptions. Newly authored reporting/docs changes are checked separately by the parent. No full fresh study rerun was warranted by these checks.

## Commands

Run from the repository root with the existing configured environment. Every Python command disables synchronization.

```bash
set -a
source /home/reid/1cfe/agentic-mbse/.env
source .venv/integration.env
set +a
export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"
export UV_CACHE_DIR=/tmp/fusion-tea-codex-uv-cache
export MPLCONFIGDIR=/tmp/fusion-tea-mpl
uv run --no-sync python -m scripts.archived_work -- uv run --no-sync python work/orchestration/goals/magnet-material-comparison/evidence/pr-readiness/portable_smoke.py
uv run --no-sync python -m scripts.archived_work -- uv run --no-sync python work/orchestration/goals/magnet-material-comparison/evidence/pr-readiness/check_reproducibility.py
```

[AGENT] The portable command uses the tracked fixture and writes evaluation outputs and its receipt only into a fresh `/tmp` directory, whose path it prints. The complete seal checker additionally requires the original machine-local artifacts to be restored; it rebuilds figures under `/tmp` and captures its seal/render receipt under this directory.

[AGENT] October 6 closure update: commands now use the explicit temporary archive-path adapter because sealed oracle readers retain their historical active paths. [Closure handoff](../closure/README.md) maps current native locations and records preservation; this command update does not change original verification or study hashes.
