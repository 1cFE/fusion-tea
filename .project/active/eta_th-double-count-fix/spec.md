# Spec: eta_th / eta_de Double-Count Fix + Canonical Verification Layer

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-22 08:50 PDT
**Complexity:** MEDIUM
**Branch:** TBD (suggest `fix/eta-th-double-count`)
**GitHub issue:** [#30](https://github.com/1cFE/fusion-tea/issues/30)

---

## Work Item Summary

`canonical_params.py` encodes overall plant efficiencies under thermal-cycle keys for Hybrid and Direct Energy Capture categories, and `standardize_eta_th.py` uses a single regex that overwrites both `eta_th` and `eta_de`/`eta_dec` kwargs with the same canonical value. The result: 8 concepts feed a blended efficiency into `eta_th`, costingfe then adds the DEC channel on top, and LCOE silently under-states by an estimated 15–30%. This work item restructures the canonical table so it returns `(eta_th, eta_de)` pairs matched to costingfe's actual parameter semantics, splits the standardization regex along the same axis, reruns the 8 affected concepts, and adds a `claude -p`-driven verification step that catches the kind of value-vs-narrative drift no regex can see.

## Why This Matters Now

Concept-level LCOE outputs feed the v3 Score Explorer and downstream cross-concept comparisons that landed across PRs #19–#29. Eight of the most commercially interesting non-thermal concepts (Helion, TAE-class mirrors, Realta, ENN p-B11, Marvel, Zephyr, LPPFusion, Blue Laser OEC) are currently understated. The `batch-pipeline-run` work item is queued next; running it before this fix would lock the wrong numbers into another full pipeline pass. The framework-level bug was already identified in May 2026 as F-2 of `.project/research/feedback_eta_th/06-magnetic-mirror.md` and deferred — issue #30 is that deferred fix.

## Key Bets / Constraints

- **Bet:** The `(eta_th, eta_de)` tuple in `canonical_params.py` is the right abstraction. `eta_th` and `eta_de` are the two parameters costingfe physics expects (`physics.py:252,261,264`); the canonical table should match that shape rather than the current single-value-per-category shape.
- **Bet:** Regex stays as the enforcement mechanism. The kwarg-line pattern is stable enough across hand-authored `model_setup.py` files to remain reliable once the two axes are separated. Migrating to libcst is out of scope.
- **Constraint:** Costingfe is not modified. The Energy Capture column in `table.csv` is not modified. The hand-authored narrative form of `model_setup.py` is preserved — sourcing comments stay readable, the script edits only numeric literals.
- **Constraint:** Per-concept `f_dec` values are not touched. They encode physics-fixed (D-T 20% alpha fraction) or design-specific choices and are not category-canonical.
- **Non-goal:** Re-baselining DEC-specific cost-model gaps in costingfe (vacuum, expander, power-conditioning beyond the lumped `dec_base` constant). Out of scope per #30.
- **Non-goal:** Refactoring `model_setup.py` files to import canonical values from a YAML/JSON sidecar. The text-rewriting design is preserved.

---

## Business Goals

### Why This Matters

LCOE is the headline cross-concept comparison output. When 8 of 39 concepts silently under-state LCOE because the cost engine receives the wrong shape of input, every downstream consumer (Score Explorer, taxonomy views, capex sensitivity, synthesis narratives) inherits that error. The bug is structural — it lives in the consistency-enforcement layer that is supposed to be the safety net.

### Success Criteria

- [ ] LCOE for the 8 affected concepts reflects costingfe's intended power-balance semantics (cycle efficiency for thermal heat load, DEC efficiency for end-loss channel, applied additively).
- [ ] The canonical-parameter layer cannot silently introduce the same bug class again: separate canonical functions return values matched to separate costingfe parameters, and the standardization script edits each axis independently.
- [ ] A verification step exists that can catch *semantic* drift — value-vs-narrative-comment contradictions, missing kwargs implied by Energy Capture — without requiring a human to read each `model_setup.py`.
- [ ] Concept 06's physics-grounded derate (`eta_th=0.20`) is preserved as an explicit, sourced `# DEVIATION:`, not lost to the new canonical.

### Priority

P0 — blocks `batch-pipeline-run`. Should land before any pipeline-wide rerun.

---

## Problem Statement

### Current State

1. `canonical_params.py:22-41` defines `_CANONICAL_ETA_TH` as a single-value-per-category map. Thermal categories (e.g. `"thermal (steam)": 0.35`) return cycle efficiency; non-thermal categories return overall plant efficiency:
   - `"hybrid (thermal + direct)": 0.55` — overall blended
   - `"direct (inductive)": 0.85` — Helion EM recovery overall
   - `"direct (charged particle)": 0.70` — TAE/mirror DEC overall
2. `standardize_eta_th.py:54-61` uses one regex `(eta_th|ETA_TH|thermal_efficiency|eta_dec|ETA_DEC)...` that matches both axes and rewrites both to the single canonical value.
3. Costingfe (`/home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py:252,261,264`) treats `eta_th` as thermal-cycle-only (`p_the = eta_th * p_th`) and `eta_de` as DEC-only (`p_dee = f_dec * eta_de * p_transport`), then adds them: `p_et = p_dee + p_the`.
4. Result: for Hybrid/Direct concepts, costingfe receives a blended-overall value where it expects a cycle value, and adds the DEC contribution on top. Affected concepts: **11, 23, 31** (Hybrid); **06, 08, 19, 24, 39** (Direct). #30 estimates +15–30% LCOE on revert.
5. Concept 11 is the live illustration of the bug: `model_setup.py:137` reads `eta_th=0.55  # standardized from 0.36 per scoring_framework.md` while the surrounding 4 lines of sourcing still describe a 0.36 MARS steam Rankine cycle.
6. Concept 06 was hand-patched in `ebcf1c3` (PR #15) — `eta_th=0.20` is physics-grounded (bremsstrahlung partial wall absorption, per `scoring_framework.md` carve-out) — but the underlying canonical table and standardization script were not touched, so the bug remained latent for the other 7 concepts. F-2 of `.project/research/feedback_eta_th/06-magnetic-mirror.md` (May 2026) flagged the framework-level issue but deferred the fix.

### Desired Outcome

- `canonical_params.py` returns `(eta_th, eta_de)` tuples matched to costingfe's actual parameter semantics. Lookups are explicit about *which* efficiency each value represents.
- `standardize_eta_th.py` writes each axis from its own canonical, with independent `# DEVIATION:` opt-out handling.
- All 39 `model_setup.py` files re-standardized; 8 affected concepts re-run through cost models and re-synthesized.
- A new `verify_canonical_params.py` reads each `model_setup.py` via `claude -p` and emits a JSON drift report — flagging value-vs-narrative contradictions, missing kwargs implied by Energy Capture, and any DEVIATION the LLM thinks is unjustified or unsourced. Runs as a separate step after standardization, not a blocker.

---

## Scope

### In Scope

- `exploration/concept_analysis/scripts/lib/canonical_params.py` — restructure to `(eta_th, eta_de)` tuples; collapse unused entries.
- `exploration/concept_analysis/scripts/standardize_eta_th.py` — split regex into two independent patterns; each writes its respective canonical.
- All 39 `model_setup.py` files — re-run standardization; resulting edits to `eta_th` and `eta_de`/`eta_dec` lines.
- 8 affected concepts: cost-model re-run, synthesis regeneration. Per `model_output.txt` and `synthesis.md` outputs.
- Concept 06 reconciliation: convert hand-patched `eta_th=0.20` to explicit `# DEVIATION:` with sourcing preserved from `feedback_eta_th/06-magnetic-mirror.md` F-1.
- New `exploration/concept_analysis/scripts/verify_canonical_params.py` — `claude -p` driven semantic audit. Sonnet model. JSON drift report + human-readable summary. Pipe-to-file invocation pattern to work around CLI stdout-empty-in-non-tty (per auto-memory).
- `scoring_framework.md` — update the canonical-table section to reflect the new tuple structure and the corrected DEC-vs-cycle distinction. Cross-reference issue #30 and this work item.

### Out of Scope

- Re-baselining `f_dec` per-concept.
- DEC-specific cost-model improvements in costingfe.
- Migrating other `standardize_*.py` scripts (availability, mn, lifetime_yr) to libcst.
- Refactoring `model_setup.py` to import canonical values from sidecar.
- Modifying `table.csv` Energy Capture column.
- Changes to v3 scoring axes, Score Explorer UI, or any non-LCOE downstream consumer.

### Edge Cases & Considerations

- **Concept 06 narrative.** The `# DEVIATION:` block must cite `scoring_framework.md §"Justified deviations"` and the bremsstrahlung physics rationale from F-1. Do not silently normalize to `(0.0, 0.70)` — that would erase a sourced physics finding.
- **Kwarg spelling drift.** The current regex matches both `eta_de` and `eta_dec`. Some concepts use one, some the other (concept 11 uses `eta_de`). The new split must catch both spellings in the DEC-side regex.
- **Existing `# standardized from X` annotations.** Re-running standardization will produce new annotations on lines that already carry old ones. Decide whether to append, replace, or preserve the original "standardized from" history. Lean toward replace-with-latest to keep lines readable.
- **Concept 11 stale narrative.** The 4-line sourcing comment around `eta_th=0.55` still describes a 0.36 steam Rankine cycle. Standardization will reset the value (likely to `eta_th=0.35` under new canonical "hybrid (thermal + direct)") but the surrounding narrative comments are *almost* correct again — verify the new value matches the original sourcing, and let the verifier flag any remaining mismatch.
- **`thermal_efficiency` alias.** The current regex matches `thermal_efficiency` as an `eta_th` synonym. Confirm none of the matched call sites mean something else (e.g. a generic plant efficiency intended to span both axes).

---

## Requirement Selection Notes

Requirements below capture what must be true for the bug to be structurally fixed, the 8 concepts to be corrected, and the verifier to provide meaningful drift detection. Decisions deliberately deferred to design: exact prompt wording for the verifier, the JSON schema of its output, whether to run the verifier in CI, and the precise `# DEVIATION:` comment template. The concept 06 reconciliation is settled in this spec because its physics basis is already sourced in `feedback_eta_th/06-magnetic-mirror.md`.

---

## Requirements

### Functional Requirements

> All requirements below are from the user's request via issue #30 unless marked otherwise.

1. **FR-1** — `canonical_params.py` MUST expose `canonical_eta_th(energy_capture: str) -> float` and `canonical_eta_de(energy_capture: str) -> float`, both backed by a single `_CANONICAL_EFFICIENCIES: dict[str, tuple[float, float]]` map.
2. **FR-2** — `_CANONICAL_EFFICIENCIES` MUST contain exactly these keys and values:
   - `"thermal (steam)": (0.35, 0.0)`
   - `"thermal (sco2)": (0.48, 0.0)`
   - `"thermal (unspecified)": (0.35, 0.0)`
   - `"hybrid (thermal + direct)": (0.35, 0.54)`
   - `"direct (inductive)": (0.0, 0.85)`
   - `"direct (charged particle)": (0.0, 0.70)`
   - `"tbd": (0.35, 0.0)`
   - `"unknown": (0.35, 0.0)`
3. **FR-3** — Entries no longer referenced by `table.csv` MUST be removed from the canonical map: `"thermal (steam) saturated"`, `"thermal (steam) superheated"`, `"thermal (steam) supercritical"`, `"thermal (helium brayton)"`, `"thermal (combined cycle)"`, `"pulsed power implosion"`, `"projectile impact"`.
4. **FR-4** — `standardize_eta_th.py` MUST use two independent regex patterns: one matching the `eta_th` / `ETA_TH` / `thermal_efficiency` family, one matching the `eta_de` / `eta_dec` / `ETA_DE` / `ETA_DEC` family. Each pattern MUST write its respective canonical value from the new tuple-based map.
5. **FR-5** — `standardize_eta_th.py` MUST respect `# DEVIATION:` opt-out comments on *either* axis independently. A deviation on `eta_th` MUST NOT block standardization of `eta_de` on the same concept, and vice versa.
6. **FR-6** — `f_dec` MUST NOT be standardized.
7. **FR-7** — After `standardize_eta_th.py --apply` runs against all 39 `model_setup.py` files: no `eta_th` value MUST exceed 0.50, and no `eta_th` value MUST equal 0.55, 0.70, or 0.85, except where an explicit `# DEVIATION:` is present and sourced.
8. **FR-8** — Concept 06's `eta_th=0.20` MUST be preserved as an explicit `# DEVIATION:` with a comment that cites `scoring_framework.md §"Justified deviations"` and the bremsstrahlung partial-wall-absorption physics rationale. The deviation comment SHOULD reference F-1 of `feedback_eta_th/06-magnetic-mirror.md`.
9. **FR-9** — For each of the 8 affected concepts (11, 23, 31, 06, 08, 19, 24, 39), the cost model MUST be re-run and synthesis MUST be regenerated. The LCOE printed in the synthesis MUST match the LCOE in the corresponding `model_output.txt`.
10. **FR-10** — `table.csv` Energy Capture column MUST NOT change. Score Explorer and heatmap surfaces MUST continue to render Energy Capture correctly (regression check; no implementation change expected).
11. **FR-11** — A new `verify_canonical_params.py` MUST exist in `exploration/concept_analysis/scripts/`. For each of the 39 `model_setup.py` files, it MUST invoke `claude -p` (Sonnet) to produce a structured report covering: (a) the `eta_th` value and whether the surrounding comments describe it as thermal-cycle vs overall-plant efficiency; (b) the `eta_de` / `eta_dec` value and what the comments describe it as; (c) any sourcing comment that contradicts the value; (d) any `# DEVIATION:` opt-out present and whether it carries a source citation.
12. **FR-12** — `verify_canonical_params.py` MUST compare the LLM report against `canonical_params.py` and emit two outputs: a machine-readable JSON drift report and a human-readable summary. The script MUST NOT modify any `model_setup.py` file.
13. **FR-13** — `verify_canonical_params.py` invocations of `claude -p` MUST use the pipe-to-file pattern (write stdout to a temp file, then read) to work around the documented CLI stdout-empty-in-non-tty behavior.
14. **FR-14** — `scoring_framework.md` MUST be updated so the canonical-parameters section reflects the new `(eta_th, eta_de)` tuple structure and the corrected DEC-vs-cycle distinction. The update SHOULD cite issue #30 and this work item.

### Non-Functional Requirements

- **NFR-1** — `verify_canonical_params.py` should be runnable end-to-end against 39 concepts in under ~10 minutes wall-clock and cost on the order of single-digit dollars per run (Sonnet pricing). This is a soft target so the script is run-often, not run-rarely.
- **NFR-2** — `standardize_eta_th.py` MUST remain deterministic: the same inputs produce byte-identical edits on every run. (No LLM in the enforcement path.)

---

## Acceptance Criteria

### Core Functionality

- [ ] `canonical_params.py` exports `canonical_eta_th()` and `canonical_eta_de()` backed by a single `_CANONICAL_EFFICIENCIES` map of `(eta_th, eta_de)` tuples (FR-1).
- [ ] Canonical map contents exactly match the table in FR-2; removed keys in FR-3 are gone.
- [ ] `standardize_eta_th.py --apply` runs cleanly across all 39 `model_setup.py` files; both `eta_th` and `eta_de` lines match their respective canonical values where no DEVIATION is present (FR-4, FR-5, FR-7).
- [ ] `f_dec` values are unchanged by the standardization run (FR-6).
- [ ] Concept 06's `eta_th=0.20` is preserved as a sourced `# DEVIATION:` (FR-8).
- [ ] Each of the 8 affected concepts (11, 23, 31, 06, 08, 19, 24, 39) has been re-run; `model_output.txt` is regenerated; `synthesis.md` is regenerated; LCOE values match between the two (FR-9).
- [ ] `verify_canonical_params.py` runs end-to-end against 39 concepts, emits both a JSON drift report and a human-readable summary, and flags at least one known case (e.g. concept 11's pre-fix stale narrative is detected when run against a deliberately un-restandardized snapshot, as a smoke test) (FR-11, FR-12).
- [ ] `scoring_framework.md` is updated; new canonical table reflects tuple structure (FR-14).

### Quality & Integration

- [ ] `table.csv` is unchanged (FR-10).
- [ ] Score Explorer (`docs/`, published at https://score-explorer.1cf.energy/) renders Energy Capture column unchanged when sanity-checked in browser.
- [ ] Existing tests in `exploration/concept_analysis/scripts/` and `exploration/concept_explorer/` continue to pass.
- [ ] No regression in the 7 axes wired by the v3 rewrite (the LCOE re-runs may shift composite scores for affected concepts — that is expected and is the point — but axis logic itself must not change).
- [ ] Standardization is deterministic; running `standardize_eta_th.py --apply` a second time produces a no-op diff (NFR-2).

---

## Next-Stage Handoff

**Settled in this spec:**

- The canonical-table shape is `(eta_th, eta_de)` tuples (not separate maps, not a single overall plant efficiency).
- Regex stays as the enforcement mechanism; libcst is not adopted.
- LLM verification is added as a separate, non-blocking audit step, not folded into `standardize_eta_th.py`.
- Concept 06's `eta_th=0.20` is preserved as a `# DEVIATION:` (not normalized to the new canonical).
- Sonnet is the model for the verifier; pipe-to-file invocation pattern.
- 8 affected concepts will be re-run + re-synthesized in the same work item.

**Design must figure out:**

- The exact split of the regex patterns — whether to keep two regexes in one file, factor into a small `_match_kwarg_line()` helper, or otherwise structure the rewrite logic.
- The `# DEVIATION:` comment template (canonical wording for the 06 case, plus shape for any future deviations).
- The verifier's JSON schema — what fields the LLM is asked to emit, how strict the schema is, how the drift comparator works.
- Whether the verifier surfaces per-concept findings or only flags concepts with drift (signal-to-noise tradeoff).
- Whether to re-extract or replace existing `# standardized from X` annotations during re-standardization.
- The order of operations: regex rewrite → cost-model rerun → synthesis regen → verifier run; or interleave?

**Watch-outs for design:**

- Concept 11's surrounding sourcing comments still describe the original `eta_th=0.36` (close to the new `0.35` canonical). Confirm the new value matches the sourcing before letting the verifier silently approve.
- `thermal_efficiency` regex alias — confirm no call site uses this name to mean "overall plant efficiency" rather than cycle efficiency, otherwise the same bug class reappears under a different name.
- Re-synthesis of 8 concepts will consume LLM budget. Track cost; consider running in batches if cost is a concern.
- `claude -p` non-determinism — same input may produce different JSON across runs. The drift comparator should be robust to phrasing variance in LLM output, not exact-match.
- Score Explorer composite scores for the 8 concepts will change. Communicate this in the PR description; downstream consumers may want a heads-up.

---

## Related Artifacts

- **Issue:** [GitHub #30 — Standardized eta_th bug](https://github.com/1cFE/fusion-tea/issues/30)
- **Prior fix (partial):** commit `ebcf1c3` (part of PR #15) — concept 06 hand-patched, framework-level bug deferred.
- **Prior research:** `.project/research/feedback_eta_th/06-magnetic-mirror.md` — F-1 sources the 06 deviation; F-2 (May 2026) flagged the framework-level bug now being fixed here.
- **Affected files (canonical):**
  - `exploration/concept_analysis/scripts/lib/canonical_params.py`
  - `exploration/concept_analysis/scripts/standardize_eta_th.py`
  - `exploration/concept_analysis/scripts/verify_canonical_params.py` (new)
  - `exploration/concept_analysis/analyses/{06,08,11,19,23,24,31,39}-*/model_setup.py`
  - `exploration/concept_analysis/analyses/{06,08,11,19,23,24,31,39}-*/model_output.txt`
  - `exploration/concept_analysis/analyses/{06,08,11,19,23,24,31,39}-*/synthesis.md`
  - `prompt_templates/config/scoring_framework.md` (table update)
- **Cost engine (reference, not modified):** `/home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py:252,261,264`
- **Design:** `.project/active/eta_th-double-count-fix/design.md` (to be created)
- **Blocks:** `.project/active/batch-pipeline-run/`

---

**Next Steps:** After approval, proceed to `/_my_design`.
