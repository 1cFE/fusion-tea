# Phase 5 Pilot Report — ARC (concept 01) End-to-End Dry-Run

**Date:** 2026-05-31
**Model:** Opus (pilot quality ceiling; production default is Sonnet per NFR-1)
**Command sequence:** `analyze 01 --force --max-passes 2 --model opus` → `review 01 --force --model opus`
**Pre-pilot snapshot:** `pre_pilot_snapshot/` (old analysis.md / model_setup.py / model_output.txt / review.md)

## Run summary

| Stage | Result |
|---|---|
| cold-start analyze | done (529s, 36 KB analysis.md) |
| model-setup iter-1 | done (221s) → ran, **LCOE 539.0 $/MWh** (1 GWe + overrides) |
| assess iter-1 | 2 findings (FAIL) |
| analyze iter-2 (feedback pass) | done (170s) |
| model-setup iter-2 | done (44s) → ran, **LCOE 543.7 $/MWh** |
| assess iter-2 | 1 finding (did not converge in 2 passes — expected for a bounded pilot) |
| review | done (275s) — **VERDICT: PROCEED** |

LCOE triple (iter-2 model): native **199.0**, 1 GWe library-bare **160.7**, 1 GWe with-overrides **543.7** $/MWh. These differ from the Item-7 oracle (174.5 / 137.2 / 584.5) because Opus selected a slightly different `spec` (R0=3.3, b_max=23, p_input=38.6, …) than the oracle's pinned ARC_SPEC. Same regime, dominated by the $6.9B structural-steel magnet override — not a defect.

## Spec AC walk — Core Functionality

- [x] **Design Point block** — top-of-body `## Design Point` with all five selection fields; `P_native=233 MWe`, name/maturity/grounding match frontmatter exactly. Section 5 quantitative table describes the one named plant at native scale. (FR-1, FR-2, FR-3)
- [x] **Override Candidates YAML** — single fenced block, six fields per entry, **canonical codes only** (C220103, C220101, CAS27, C220108 — no `CAS22.1.3`-style codes). `derived` entries show CPI arithmetic (`5200.0 * 1.33`, `108.1 * 1.33`) in `rationale`. (FR-4, FR-5, FR-7)
- [x] **Per-account walkthrough** — explicit walkthrough prose names which accounts were considered-and-folded vs overridden vs library-owned; a reviewer can name the discipline. (FR-6)
- [x] **Override count band** — 3 enabled overrides, stated as within the High archetype-fit band (0–4); the prompt's flag mechanism fired (none needed). A fourth candidate (C220108 divertor) was carried *disabled* with explicit discipline reasoning (won't depart from the library in the non-conservative direction on an incomplete placeholder). (FR-8)
- [x] **Four-step model_setup.py** — `result, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`; `model`/`result`/`result_1gw` module-level; `validate_model_setup_contract(strict_helper_only=True)` → **valid (helper form)**. (FR-9, FR-10, FR-11, FR-26)
- [x] **No re-passed library defaults** — no `# DEFAULT:` comments; `spec` carries only design-point inputs; `availability`/`lifetime_yr`/`interest_rate`/`inflation_rate` absent from `spec`. (FR-12)
- [x] **`eta_th` discipline holds** — ARC's `model_setup.py` does **not** override `eta_th`; the docstring explicitly explains the 46% Brayton figure is aspirational (demonstrated-material floor ~40% = library default) and leaves it to the library, carrying it as a sensitivity sweep. Exactly the FR-13 distinction. (FR-13)
- [x] **Override `value` expressions** — constant-expression entries (`5200.0 * 1.33`) survive the prompt→file→`validate_override_registry` round-trip (registry valid, 4 entries). (FR-14)
- [x] **Assess / review against new artifacts** — assess emits `VERDICT: FINDINGS` + `### F-N:` with `- **Category:** model`; review emits `VERDICT: PROCEED` + PA-1/PA-2 minor fixes. Both parse cleanly with the rewritten parsers (below). (FR-17, FR-18, FR-19, FR-20)
- [x] **`Reuses:` → `Comparables:`** — zero `Reuses:` in the generated analysis; Section 7 "Family-Delta vs Comparables" works the **fixed** comparables list (`21`/`28`/`29`/`33`) with concrete cost-directional deltas. (FR-24)

## Spec AC walk — Quality & Integration

- [x] **End-to-end loop green** — full analyze→model-setup→assess (×2) + review ran clean; zero references to the removed regex constants remain in the tree. (FR-25–29)
- [x] **Parser return shapes (signal_contract row-for-row)** — on the real pilot artifacts: `parse_verdict_from_feedback → ('FAIL', 1)`; `validate_feedback_verdict → valid`; `has_model_category_findings → True`; `validate_review_verdict → valid`; `parse_proposed_actions → 2 dicts, all nine keys present`. Call sites unchanged. (FR-25)
- [x] **No inline two-knob `forward()`** — helper form is the only `result_1gw` binding; strict contract accepts it. (FR-10, FR-26)
- [x] **`result_1gw` at exactly 1000 MWe** — `result_1gw.params['net_electric_mw'] == 1000.0`. (constraint)
- [x] **Override-toggle test** — all `enabled=False` → 1 GWe LCOE **160.7 $/MWh** (library-bare regime), vs **543.7** with overrides on: the overrides materially move cost (3.4×), and the toggled-off run recovers the library answer. (Phase 5 validation)
- [x] **Explorer reads without fallback** — `extract_explorer_data.py --concept 01` wrote a fresh `01.json`, cleared the stale marker, `net_electric_mw=1000.0` extracted from the helper form via `getattr(module, "result_1gw")` — no fallback path exercised. (comparison-view AC)

## Fixes folded back before merge

1. **`lib/claude.py::_check_interface`** — the costingfe interface heuristic used `^result\s*=`, which does not match the four-step helper's tuple-unpack `result, result_1gw = run_native_and_1gw(...)`, producing a misleading "explorer requires this" stderr warning on every helper-form run. Updated to accept the tuple-unpack / `run_native_and_1gw` form. (The extractor itself was never affected — it reads `getattr(module, "result")` at runtime — but the warning was noise the rework introduced.)

## Observations (non-blocking — tuning candidates, not contract defects)

- **Assessor vs. `eta_th` discipline.** The iter-2 assess finding F-1 (`Category: model`) flags that the native run uses the library-default ~40% η_th rather than ARC's published 46%. The model-setup made the **contract-correct** call (FR-13: an aspirational published efficiency is not grounds to override the archetype default), and the review nonetheless PROCEEDED with only minor documentation fixes (PA-1/PA-2 ask to *note* the η_th/native-LCOE wrinkle, not to change it). Worth considering whether `assessment.md` / `quality_standards.md` should more strongly signal "an aspirational efficiency is not a finding," so the assessor doesn't push toward a departure the contract forbids. Tuning nuance for a later pass; it did not derail the pilot.
- **LCOE vs oracle** — numbers differ from the Item-7 oracle only because Opus chose a slightly different `spec`; same regime. Not actionable.

## Verdict

**All spec acceptance criteria pass.** The atomic swap (FR-29) produces a working loop on a real concept end-to-end: new prompts → helper-form `model_setup.py` → contract validators accept → rewritten parsers read the new format → explorer extracts at 1 GWe. Safe to merge.
