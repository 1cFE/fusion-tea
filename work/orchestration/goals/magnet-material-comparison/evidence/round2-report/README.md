# Round 2 reporting artifacts

[AGENT] Coordinator reading of the committed `20260930-magnet-material-plant-map@a9683fa1d` record. Draft interpretation; independent integration and interpretation review is pending. Snapshot SHA-256: `d494d0e92768ff6ed2498c32f9d24fc1cee9e8562cf863e269f92a01eed46de7`.

The renderer reads only the sealed `results/summary.json` and `results/cases.csv`. It runs no plant calculation or selection policy. `provenance.json` records source and exported-artifact hashes. Every map, interaction and decomposition row names its source case ids. The case table contains all retained outcomes; plotting only ranking-eligible designs does not delete failed cases.

## Figures and data

- `assumption-map.svg` / `.png`, `map.csv`: cell preference at 80, 30 and 10 USD2021/m, and the maximum tape price at which any tested ranking-eligible REBCO design equals the cell's best tested Nb₃Sn design. No Nb₃Sn design qualifies in anchored × 1.0, so that cell has no comparison.
- `field-size-interactions.svg` / `.png`, `interactions.csv`: best crossing at each tested target peak field or major radius, against the same cell's best Nb₃Sn design. Field panels use only own-sized REBCO designs; equal-duty REBCO cases carry the Nb₃Sn target label and can have a different actual peak, so those labels cannot be read as REBCO field. Size panels retain all ranking-eligible offers. The CSV carries actual REBCO peak field and equal-duty status for every row. Each point maximizes the crossing over other tested design choices; this is a conditional envelope, not a one-variable sensitivity with hardware fixed. Radius groups include different minor radii. Negative crossings mean even zero-priced tape would not make that tested REBCO design beat the comparator under its unchanged non-conductor costs. Lines guide the eye between discrete tested points.
- `lcoe-decomposition.svg` / `.png`, `decomposition.csv`: exact account differences between the best tested designs at the reference prices. Capital and annual terms are evaluated at the REBCO design's annual energy; the final denominator term accounts for the different Nb₃Sn energy. Refrigeration electricity and heating draw affect net energy; their capital costs remain in their account groups. The three plotted groups sum to the cell gap.

## Evidence labels

[INHERITED: ../plant-contract.md §§ 3.1–3.2] S means supported at the source configuration, A means an analogue from another configuration, D means derived from source data, and U means an unsupported transfer or supplied assumption. These label physical evidence, separately from numerical screening status.

[AGENT] Every best design in this map carries U for confinement application and U for coil-geometry application. The confinement sources provide values at named configurations, not a validity band for these selected designs. The anchored geometry is source-supported only at the reference pack; all selected REBCO packs differ and every Nb₃Sn pack differs. HELIAS cells use an analogue ratio inside a hybrid Stellaris geometry. The pack-size arm transfers a Helias-5-derived slope to another coil geometry. Beta-limit evidence is A; policy choices are U. Hence all cell comparisons have U as their weakest label. Source-supported or derived ingredients do not qualify the assembled design. These labels require the pending independent interpretation review.

## Rebuild the reporting artifacts

From the repository root:

```bash
MPLCONFIGDIR=/tmp/fusion-tea-mpl UV_CACHE_DIR=/tmp/fusion-tea-codex-uv-cache uv run --no-sync python work/orchestration/goals/magnet-material-comparison/evidence/round2-report/render.py
```

The renderer checks the snapshot hash, 2,921 unique retained cases, selected-case/LCOE parity and account closure within 1e-9 USD/MWh. This validates reporting arithmetic only. It does not repeat the native model verification.

## Numerical replay

The native stores and full per-case exports are machine-local and hashed in the snapshot. They remain present in this checkout. Fresh evaluation writes to `/tmp`; never run a write-once producer against sealed `results/`. Before a replay, check the manifest/package fingerprints, current TEAx revision and source hashes against the snapshot and integration receipts. Preserve mismatches as failures rather than repairing the pin silently. The declared case-list hash must remain `f07133acdd561610287ff9dea01f641bf48b1562ec417254c85484ea8645e583`.

```bash
set -a
source /home/reid/1cfe/agentic-mbse/.env
source .venv/integration.env
set +a
export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"
export UV_CACHE_DIR=/tmp/fusion-tea-codex-uv-cache
study_path=exploration/stellarator_materials/studies/20260930-magnet-material-plant-map
replay_path=$(mktemp -d /tmp/magnet-plant-replay.XXXXXX)
for material in rebco nb3sn; do
  uv run --no-sync python "$study_path/execute_study.py" --unit "$material" --integration-return "work/orchestration/goals/magnet-material-comparison/evidence/integration-r3-$material/integration_return.json" --out-root "$replay_path"
done
uv run --no-sync python "$study_path/verify_all.py" --root "$replay_path" --workers 4
```

These are replay instructions, not a claim that a full fresh replay was performed on 2026-10-04. The verifier reads the original oracle scan and declared case list. A fresh checkout lacking machine-local artifacts must restore those files by snapshot hashes or independently reconstruct them in a separate record copy; the current scripts' write-once checks must not be bypassed. Re-running the offer policy is a separate reconstruction step, not part of evaluating already supplied designs. The scripts retain every failed/refused case and compare every covered output and predicate.

The renderer and replay commands retain the owner's local editable agentic-mbse installation by using only `uv run --no-sync`.
