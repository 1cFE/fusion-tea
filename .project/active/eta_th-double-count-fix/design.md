# Design: eta_th / eta_de Double-Count Fix + Canonical Verification Layer

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-22 09:05 PDT
**Branch:** TBD (suggest `fix/eta-th-double-count`)
**Commit at design time:** `dbe9e8a`

---

## Overview

Restructure `canonical_params.py` to return `(eta_th, eta_de)` tuples matched to costingfe's actual parameter semantics, split `standardize_eta_th.py`'s single regex into two independent passes, rerun the 8 affected concepts end-to-end, and add a `claude -p`-driven verifier that catches semantic drift the regex cannot see. Two layers, decoupled: deterministic enforcement on the bottom, LLM-based semantic audit on top.

## Related Artifacts

- **Spec:** `.project/active/eta_th-double-count-fix/spec.md`
- **Issue:** [GitHub #30](https://github.com/1cFE/fusion-tea/issues/30)
- **Prior research:** `.project/research/feedback_eta_th/06-magnetic-mirror.md` (F-1 sources the 06 deviation; F-2 flagged the framework-level bug)
- **Reference (not modified):** `/home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py:252,261,264`

---

## Research Findings

### Existing infrastructure to reuse

- **`exploration/concept_analysis/scripts/lib/claude.py`** — already has `invoke_claude()` and `invoke_claude_validated()` (`lib/claude.py:91, 232`). Handles subprocess invocation, JSON event parsing (`_parse_json_events`), and the pipe-to-file pattern. The verifier should reuse this rather than re-implement, *and* rather than copy the heavier streaming version in `exploration/phase_2a/expand.py:48`.
- **`exploration/concept_analysis/scripts/rerun_all_models.py`** — deterministic helper that re-executes each concept's `model_setup.py` to refresh `model_output.txt`. Supports `--only <ids>` for targeted reruns. This is the natural choice for regenerating cost-model outputs after standardization (`rerun_all_models.py:1-30`).
- **`exploration/concept_analysis/scripts/run_analysis.py`** — has `cmd_synthesize()` (Stage 5) that regenerates `synthesis.md` from model output (`run_analysis.py:749`). The `--force` flag bypasses the freshness check.
- **Sibling standardize scripts** — `standardize_availability.py`, `standardize_mn.py`, `standardize_lifetime.py` use the same regex-rewrite pattern. They are the design template for what the fixed `standardize_eta_th.py` should look like (single canonical, single regex). Our case is the only one where the regex has to span two axes.

### Bug surface, confirmed

- `lib/canonical_params.py:22-41` — `_CANONICAL_ETA_TH` conflates thermal-cycle and overall-plant efficiencies under the same lookup.
- `standardize_eta_th.py:54-61` — single regex with `(eta_th|ETA_TH|thermal_efficiency|eta_dec|ETA_DEC)`. Crucially, the regex does **not** match plain `eta_de` (no `c`). On concept 11 (`model_setup.py:155`), `eta_de=0.54` is written that way and was never touched by the standardizer — so concept 11 escaped the double-write but still got the wrong `eta_th`. Other affected concepts may have written `eta_dec` and gotten both lines stomped. Per-concept audit needed during implementation.
- `prompt_templates/config/scoring_framework.md:305-323` — the canonical η_th table currently published in the framework matches the buggy `canonical_params.py` map (single value per row, 0.55/0.70/0.85 for hybrid/direct). Framework doc and code are the same artifact in two places; both must move together.
- `scoring_framework.md:325-331` — already names concept 06 as a justified-deviation case, so the spec's "convert 06 to explicit `# DEVIATION:`" is just making the existing carve-out machine-readable.

### Affected concept paths (verified)

```
analyses/06-magnetic-mirror/         (Direct CP)  — currently eta_th=0.20 (hand-patched)
analyses/08-helion-frc/              (Direct ind) — currently eta_th=0.85 (bug)
analyses/11-magnetic-mirror/         (Hybrid)     — currently eta_th=0.55 (bug)
analyses/19-zephyr-dipole/           (Direct CP)  — currently eta_th=0.70 (bug)
analyses/23-marvel-laser-icf/        (Hybrid)     — currently eta_th=0.55 (bug)
analyses/24-lppfusion-dpf/           (Direct CP)  — currently eta_th=0.70 (bug)
analyses/31-laser-icf-oec/           (Hybrid)     — currently eta_th=0.55 (bug)
analyses/39-enn-pb11-st/             (Direct CP)  — currently eta_th=0.70 (bug)
```

---

## Core Concept

The fix has two layers, deliberately decoupled.

**Layer 1 — Deterministic enforcement.** `canonical_params.py` becomes the single source of truth for *both* `eta_th` and `eta_de` per Energy Capture category, structured as `(eta_th, eta_de)` tuples that mirror costingfe's parameter semantics one-to-one. `standardize_eta_th.py` does two regex passes per file — one over the `eta_th` family, one over the `eta_de`/`eta_dec` family — each writing its own canonical value. The bug class disappears because the canonical table can no longer conflate two physical quantities, and the regex can no longer overwrite the wrong axis.

**Layer 2 — Semantic verification.** `verify_canonical_params.py` reads each `model_setup.py` through `claude -p` and emits a structured report comparing the numeric values to the surrounding sourcing narrative. It catches the residue the regex cannot see: value-vs-comment contradictions, missing kwargs implied by Energy Capture, unsourced deviations. The verifier never edits files — it produces a JSON drift report plus a human-readable summary.

The key insight: enforcement must be deterministic (so reruns are reproducible and the same input always produces the same edit), but *audit* benefits from semantic understanding (so a stale "MARS steam Rankine ~36%" sourcing comment next to `eta_th=0.55` becomes a signal, not just a curio). Conflating the two — using an LLM to do the rewrite — sacrifices reproducibility for a problem we can solve with two regex passes.

---

## Key Bets & Decisions

- **Tuple-shape canonical, not two parallel maps.** `_CANONICAL_EFFICIENCIES: dict[str, tuple[float, float]]` keeps the two values atomic to the Energy Capture key. Two separate maps would let them drift apart over time.
- **Two regex passes in one script.** Not two scripts. The two axes share the table.csv lookup, the file-walking loop, the DEVIATION handling, and the print/report logic. Splitting only the regex layer keeps the script small.
- **Reuse `lib/claude.py:invoke_claude()`, not phase_2a's streaming pattern.** The verifier needs one-shot JSON per file, not real-time streaming. `lib/claude.py` already handles the CLI stdout-empty-in-non-tty workaround.
- **Verifier never edits.** It only reads and reports. Makes the audit safe to re-run, easy to dry-run, and prevents the LLM from quietly "fixing" things.
- **Concept 06's `eta_th=0.20` becomes a sourced `# DEVIATION:`.** The physics rationale already exists in `feedback_eta_th/06-magnetic-mirror.md` F-1 and `scoring_framework.md:325-331` already carves it out by name. We make it machine-readable, nothing more.
- **No history chain in standardization annotations.** Replace `# standardized from X per scoring_framework.md` with the latest one each run. Otherwise re-running creates a comment-archaeology problem.
- **Verifier is non-blocking.** Runs as a separate step. A failed audit reports drift, doesn't block standardization. The deterministic layer is the source of truth.
- **Out-of-scope-but-tempting that we are NOT doing:** YAML-sidecar for canonical values; libcst-based AST rewriter; touching the other three `standardize_*.py` scripts; modifying costingfe.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: Deterministic enforcement                              │
│                                                                  │
│  table.csv  ─►  canonical_params.py                              │
│                  _CANONICAL_EFFICIENCIES: {key: (eta_th, eta_de)}│
│                  canonical_eta_th(ec)  ─┐                        │
│                  canonical_eta_de(ec)  ─┤                        │
│                                         ▼                        │
│                          standardize_eta_th.py                   │
│                          ├─ pass 1: ETA_TH_PATTERN  → eta_th     │
│                          └─ pass 2: ETA_DE_PATTERN  → eta_de     │
│                                         ▼                        │
│                          39 × model_setup.py (text rewrite)      │
│                                         ▼                        │
│                          rerun_all_models.py  (8 affected)       │
│                                         ▼                        │
│                          model_output.txt                        │
│                                         ▼                        │
│                          run_analysis.py cmd_synthesize          │
│                                         ▼                        │
│                          synthesis.md                            │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: Semantic verification (non-blocking)                   │
│                                                                  │
│  39 × model_setup.py ─►  verify_canonical_params.py              │
│                          ├─ per file: invoke_claude(prompt)      │
│                          ├─ parse JSON report                    │
│                          └─ compare against canonical_params.py  │
│                                         ▼                        │
│                          drift_report.json  +  summary.md        │
└─────────────────────────────────────────────────────────────────┘
```

**Boundaries**:
- Layer 1 is deterministic, fast, idempotent. Re-running produces the same result.
- Layer 2 is LLM-driven, slow (~minutes for 39 calls), and non-deterministic. Its output is advisory.
- Layer 2 reads files Layer 1 may have modified, but never the other way around.
- Costingfe is unchanged. `table.csv` is unchanged. `model_setup.py` is the only authored file Layer 1 mutates.

**Data flow for the 8 affected concepts**:
1. `standardize_eta_th.py --apply` rewrites `eta_th` and `eta_de` lines in all 39 `model_setup.py` files (only the 8 differ from canonical; 06 has DEVIATION; others are no-ops).
2. `rerun_all_models.py --only 06 08 11 19 23 24 31 39` regenerates `model_output.txt` for those 8 via `lib/claude.py:run_model()`.
3. `run_analysis.py synthesize --only ... --force` regenerates `synthesis.md` for those 8.
4. `verify_canonical_params.py` walks all 39 files and emits the drift report.

---

## Required Invariants

1. **Costingfe contract.** `eta_th` passed to `model.forward()` is thermal-cycle-only; `eta_de` is DEC-only. Both are unit-fraction floats in `[0.0, 1.0]`.
2. **Canonical map shape.** Every value in `_CANONICAL_EFFICIENCIES` is a 2-tuple of floats in `[0.0, 1.0]`. Every key is lowercase and matches an entry in the Energy Capture column of `table.csv` (after `.strip().lower()`).
3. **Idempotence.** Running `standardize_eta_th.py --apply` twice in succession produces a no-op diff on the second run.
4. **DEVIATION independence.** A `# DEVIATION:` comment on one axis (e.g. `eta_th`) does not affect standardization of the other axis (e.g. `eta_de`).
5. **Single source of truth.** `_CANONICAL_EFFICIENCIES` is the only place canonical numeric values live. `scoring_framework.md` is documentation generated/maintained to match; the verifier compares files to this map, not to the framework doc.
6. **Verifier read-only.** `verify_canonical_params.py` MUST NOT write to any file under `analyses/`. Output goes only to `verify_output/` (or stdout).
7. **Reproducibility floor.** Layer 1 is deterministic — re-running today and next year on the same inputs produces byte-identical edits.

---

## Component Overview

### Modified: `exploration/concept_analysis/scripts/lib/canonical_params.py`

Replaces `_CANONICAL_ETA_TH` with `_CANONICAL_EFFICIENCIES: dict[str, tuple[float, float]]`. Exposes `canonical_eta_th(energy_capture)` and `canonical_eta_de(energy_capture)`. Each calls a shared `_lookup(energy_capture)` that handles the case/whitespace normalization and parenthetical-stripping fallback the current `canonical_eta_th()` already does. `canonical_availability()`, `canonical_mn()`, `canonical_lifetime_yr()` are untouched.

Interface (illustrative, ~10 lines max):

```python
_CANONICAL_EFFICIENCIES: dict[str, tuple[float, float]] = {
    "thermal (steam)":            (0.35, 0.0),
    "thermal (sco2)":             (0.48, 0.0),
    "thermal (unspecified)":      (0.35, 0.0),
    "hybrid (thermal + direct)":  (0.35, 0.54),
    "direct (inductive)":         (0.0,  0.85),
    "direct (charged particle)":  (0.0,  0.70),
    "tbd":                        (0.35, 0.0),
    "unknown":                    (0.35, 0.0),
}
def canonical_eta_th(energy_capture: str) -> float: ...
def canonical_eta_de(energy_capture: str) -> float: ...
```

### Modified: `exploration/concept_analysis/scripts/standardize_eta_th.py`

Two regex patterns, two passes per file. Each pattern lives next to a small `_apply_pass(pattern, canonical_value, ...)` helper. Shared loop walks all 39 files; for each file, runs pass 1 then pass 2; reports both per axis. DEVIATION opt-out checked per line, independently per axis.

Pattern shapes (illustrative):
- `ETA_TH_PATTERN`: `eta_th|ETA_TH|thermal_efficiency` (+ optional `_SUFFIX`).
- `ETA_DE_PATTERN`: `eta_de|eta_dec|ETA_DE|ETA_DEC` (+ optional `_SUFFIX`). Critically, this catches both `eta_de` (concept 11) and `eta_dec` (other concepts).

Report format extended to show both axes per concept:

```
concept    energy_capture                eta_th(canon/cur)  eta_de(canon/cur)  status
06-...     direct (charged particle)     0.00 / 0.20*       0.70 / 0.70        eta_th DEVIATION
11-...     hybrid (thermal + direct)     0.35 / 0.55        0.54 / 0.54        eta_th needs update
```

### Modified: `exploration/concept_analysis/prompt_templates/config/scoring_framework.md`

Replace the §"Thermal-to-electric conversion efficiency (η_th)" canonical table with a new §"Energy capture efficiencies (η_th, η_de)" table that lists both values per Energy Capture key. Update the §"Helpers" section to show `canonical_eta_de` alongside `canonical_eta_th`. Update the §"Justified deviations" example for 06-magnetic-mirror to reflect the new `(0.0, 0.70)` canonical and the new DEVIATION comment shape.

### New: `exploration/concept_analysis/scripts/verify_canonical_params.py`

CLI script. For each `model_setup.py` under `analyses/`, calls `invoke_claude()` (from `lib/claude.py`) with a templated prompt asking for a structured JSON report. Parses the JSON, compares to `canonical_params.py`, emits drift findings.

Prompt skeleton (illustrative, not full prompt):
```
Read this Python file. For eta_th and eta_de kwargs, report:
  - the numeric value
  - whether surrounding comments describe it as
    "thermal-cycle" or "overall-plant" or "DEC" or other
  - any contradiction between value and sourcing comments
  - any "# DEVIATION:" present and whether it cites a source
Energy Capture for this concept (from table.csv): {ec}
Output JSON conforming to the schema in {schema_path}.
```

Outputs:
- `verify_output/drift_report.json` — machine-readable, one entry per concept with `eta_th`, `eta_de`, `deviations`, `narrative_contradictions`, `missing_kwargs`, `confidence_notes`.
- `verify_output/summary.md` — human-readable; concepts grouped by severity (drift vs clean), each finding linked to file:line.

CLI flags: `--only <ids>` (target subset), `--model {sonnet,haiku}` (default sonnet), `--dry-run` (build prompts, skip LLM call), `--cost-cap USD` (abort if estimated cost exceeds).

### Edited (in-place, by standardization run): 39 × `analyses/*/model_setup.py`

Numeric literals for `eta_th` and `eta_de`/`eta_dec` lines updated to canonical (or preserved if `# DEVIATION:`). The "standardized from X per scoring_framework.md" annotation comment is refreshed on changed lines. Hand-authored sourcing comments above/below the kwarg lines are not touched.

### Edited (by reruns): 8 × `model_output.txt` and 8 × `synthesis.md`

Affected concepts only: 06, 08, 11, 19, 23, 24, 31, 39.

---

## Non-Goals

- Modifying costingfe in any way.
- Changing `table.csv`, the Energy Capture column, or any scoring axis logic.
- Replacing regex with libcst, an AST rewriter, or any other deterministic mechanism.
- Refactoring `model_setup.py` files to import canonical values from a YAML/JSON sidecar.
- Touching `standardize_availability.py`, `standardize_mn.py`, `standardize_lifetime.py`.
- Standardizing `f_dec`.
- Making the verifier blocking, integrating it into `standardize_eta_th.py`, or wiring it into CI in this work item.

---

## Implementation Notes

- **`thermal_efficiency` alias.** Before the standardization runs, audit the 39 files for any line that uses `thermal_efficiency = ...` and verify the author meant cycle efficiency. If any call site uses it to mean overall plant efficiency, flag and refuse to auto-rewrite that file (require human review). Pattern: `grep -rn "thermal_efficiency" exploration/concept_analysis/analyses/`.
- **DEVIATION template.** Settle on a single canonical comment shape during implementation so the verifier can detect it deterministically:
  ```
  # DEVIATION: <one-line rationale>. Source: <file/url>. Canonical: <axis>=<value>.
  ```
- **06-magnetic-mirror DEVIATION text.** Lift the wording from `feedback_eta_th/06-magnetic-mirror.md` F-1's "Recommendation 1" verbatim, with a one-line cite back to that file and to `scoring_framework.md §"Justified deviations"`.
- **Verifier rate-limiting.** 39 sequential `claude -p` calls at Sonnet is ~3–5 min wall-clock. Acceptable for now. If we later want CI integration, parallelize with a small worker pool.
- **Verifier prompt versioning.** The prompt template lives in `scripts/verify_canonical_params.py` as a constant. Treat changes to it as breaking; include a `prompt_version` string in the JSON output so drift-report diffs across runs are interpretable.
- **`pyproject.toml` / `pytest`.** Existing tests under `exploration/concept_analysis/` should continue to pass. If `tests/test_canonical_params.py` exists (TBD — check during implementation), update it to cover the new `canonical_eta_de()` function and the tuple shape.
- **Score Explorer regression check.** No code change is expected; the Energy Capture column is unchanged. Sanity check: open `docs/score-explorer/` in a browser after the runs, confirm Energy Capture renders, confirm the 8 affected concepts show shifted LCOE / composite scores.

---

## Potential Risks

| Risk | Mitigation |
|---|---|
| New canonical for hybrid `(0.35, 0.54)` doesn't match concept-11's sourced `(0.36, 0.54)` exactly — narrative may still drift after rewrite. | Verifier will surface this; close the gap by hand on a per-concept basis if needed, or convert to DEVIATION. |
| `eta_dec` vs `eta_de` spelling differs across affected concepts; one regex catches `eta_dec`, the new split must catch both. | Test the new ETA_DE_PATTERN against every affected file before running `--apply`. Spec FR-4 names both. |
| Re-synthesizing 8 concepts costs LLM budget. | `--only` flag limits scope; not all 39. Cost expected single-digit dollars. |
| Verifier non-determinism produces noisy diffs across runs of `drift_report.json`. | Drift comparator should ignore phrasing variance — match on structured fields, not free text. Schema-first design. |
| Score Explorer composite scores shift for 8 concepts post-rerun; downstream consumers may not expect it. | Call out in PR description. The shift IS the fix. |
| Verifier prompt drift over time produces different reports for unchanged files. | `prompt_version` string in output enables interpretation; pin Sonnet model version in script. |
| `# standardized from` annotation churn pollutes git diffs on no-op reruns. | Idempotence invariant — only emit the annotation when the value actually changed; suppress on no-op. |

---

## Integration Strategy

This fix slots into the existing modeling-consistency layer. The four `standardize_*.py` scripts are siblings; after this work, `standardize_eta_th.py` is the only one with twin-axis rewriting, but its external CLI shape is unchanged: still `--apply`, still walks `table.csv`, still emits a deviation report. Downstream callers (`rerun_all_models.py`, `run_analysis.py synthesize`) need no changes — they just consume the updated `model_setup.py` files.

The verifier is a new tool with no incoming dependencies. It can be run any time, by anyone, without prerequisites. Suggested workflow integration (post-merge):
1. Edit `table.csv` or canonical values → run `standardize_eta_th.py --apply`.
2. Run `rerun_all_models.py --only <affected>` and `run_analysis.py synthesize --only <affected> --force`.
3. Run `verify_canonical_params.py` and review the drift report before opening a PR.

CI integration is explicitly out of scope; a follow-up work item can wire it in if drift catches turn out to be high-value.

This work blocks `batch-pipeline-run/` (queued; would otherwise lock the wrong LCOEs into another full pipeline pass).

---

## Validation Approach

**Layer 1 (deterministic)**:
- Unit tests for `canonical_params.py`: lookup correctness for every key, case/whitespace normalization, unknown-key behavior, tuple shape.
- Unit tests for `standardize_eta_th.py`: regex pattern matches each kwarg-spelling variant; DEVIATION opt-out blocks rewrite per-axis; idempotence (run twice → no diff on second).
- Integration: run `standardize_eta_th.py --apply` on a fixture directory with a representative subset of model files (one per Energy Capture category) and diff against expected output.
- Smoke: after applying on all 39 files, `grep -c "eta_th=" analyses/*/model_setup.py | grep -v ":1"` should be empty (each file has exactly one eta_th line — or be auditable if not).
- Post-rerun: for each of 8 affected concepts, diff `model_output.txt` LCOE; expected +15–30% (matches issue #30 estimate).

**Layer 2 (semantic)**:
- Smoke: deliberately set concept 11's `eta_th=0.55` against a sourcing block describing 0.36 (current state), run verifier, assert the drift report flags this pair as a contradiction.
- Smoke: assert verifier flags a synthetic test case with `eta_de` missing on a Direct concept.
- Verifier output schema validated against a fixed JSON schema (committed to repo) on every run.
- Cost regression: verifier run cost printed at end; warn if >2× prior run.

**Manual**:
- Open Score Explorer in browser; confirm Energy Capture renders unchanged for all 39 concepts; confirm 8 affected concepts show updated LCOE / composite scores.
- Read concept 06's updated `model_setup.py`; confirm DEVIATION block reads cleanly and cites both `feedback_eta_th/06-magnetic-mirror.md` and `scoring_framework.md`.
- Read concept 11's updated `model_setup.py`; confirm `eta_th=0.35` and surrounding MARS-Rankine sourcing narrative now agree.

---

## Next-Stage Handoff

**Settled (plan should treat as fixed):**
- Canonical shape: `(eta_th, eta_de)` tuples in `_CANONICAL_EFFICIENCIES`.
- Two regex passes within a single `standardize_eta_th.py`; not two scripts.
- Verifier reuses `lib/claude.py:invoke_claude()`; it is separate from `standardize_eta_th.py`; never edits files.
- Concept 06's 0.20 stays as `# DEVIATION:`.
- Standardization annotation: replace each run, do not chain history.
- `scoring_framework.md` table replaced to match new tuple shape in same PR.

**Plan must decide / produce:**
- Phase ordering: implementation phases for Layer 1 (canonical_params → standardize → rerun → synthesize) vs Layer 2 (verifier) — likely two parallel tracks, Layer 1 lands first, Layer 2 lands close behind.
- Exact regex strings for ETA_TH_PATTERN and ETA_DE_PATTERN. Test fixtures for both.
- JSON schema for verifier output. Schema test asserting LLM output conforms.
- Final `# DEVIATION:` comment template (one shape, used everywhere).
- Whether to add a `--check` / `--no-write` mode to `standardize_eta_th.py` that exits non-zero on drift (CI hook, even if CI not wired this work item).

**De-risk first:**
- Audit all 39 `model_setup.py` files for `thermal_efficiency` aliases and unexpected kwarg spellings *before* writing the regex split. If anything surprising shows up, the regex design changes.
- Manually run the new canonical against concept 11's expected outputs (hand-calc new `eta_th=0.35` LCOE) to confirm the +15–30% delta claim in #30 — that's our acceptance signal for the entire fix.

---

**Next Step:** After approval → `/_my_plan` (multi-phase work; spec lists 14 FRs across two layers and 8 concept reruns — plan.md with checkboxes will keep phases visible across sessions).
