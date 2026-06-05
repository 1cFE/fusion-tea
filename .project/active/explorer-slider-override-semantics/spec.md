# Spec: Explorer Slider Override Semantics

**Status:** Draft (deferred follow-up)
**Owner:** Reid W
**Created:** 2026-06-05
**Complexity:** LOW–MEDIUM (depends on chosen direction)
**Branch:** TBD
**Depends on:** [`explorer-rework-unblock`](../explorer-rework-unblock/spec.md) landing first.

---

## Work Item Summary

When a user drags any slider in the concept explorer, the recomputed LCOE drops the analyst's `cost_overrides` registry, so the displayed number jumps from the analyst-set figure (the JSON's headline) to the library-bare figure — with no input from the user. Under the pre-rework analysis pipeline this was a small effect; under the rework it is a structural one because the override registry is now where analyst judgment lives. This work item decides whether to (a) preserve the current behavior and label the visible discontinuity, (b) re-apply the registry on recompute so sliders perturb the analyst's model rather than the library's, or (c) give the user explicit control. No code changes happen in this spec — its job is to choose a direction.

## Why This Matters Now

Verified on concept 01 with the current `_compute_cached` mechanism: `result_1gw.costs.lcoe = 155.17 $/MWh` (the JSON headline, with the analyst's $1.03B C220103 magnet override applied). The first time a user touches *any* slider, recompute runs `model.forward(**result_1gw.params, **slider_overrides)` *without* the analyst's `cost_overrides`, and LCOE collapses to `127.53 $/MWh` (−27.6 $/MWh, −17.8%). The user did not change anything material — `availability` moved by half a percent — but the headline number jumped because the registry vanished. This makes every slider untrustworthy until the user understands the mechanic, and the mechanic isn't visible anywhere in the UI.

The same mechanism existed pre-rework, but it mattered less: most concepts had small or no override registries, so the slider's effect dominated the registry's disappearance. The rework deliberately moved cost weight into the registry (one analyst-defensible override per CAS departure, six fields each, with provenance and rationale). Concept 01's magnet override alone moves LCOE by ~$28/MWh. Every other concept with non-trivial fit-grade follows the same pattern. The discontinuity is now a first-order UX failure.

## Key Bets / Constraints

- **Bet:** This is a UX correctness issue, not a numerical one. The library and the helper are doing the right thing; the recompute pathway is silently changing the question the slider is asking.
- **Constraint:** Whatever direction we pick has to be consistent with how `model.sensitivity()` computes the tornado baselines. The tornado on the concept page is computed *with* the override registry applied (at extraction time), so option (b) below aligns the slider with the tornado; option (a) admits an explicit divergence the UI must surface.
- **Constraint:** The library exposes `override_reference_mw` so that overrides scale correctly when `n_mod ≠ 1`. Any option that re-applies the registry on recompute must also pass `override_reference_mw=P_native` (i.e. revive the work FR-A4 was meant to do, with a real motivating example this time).
- **Non-goal:** A redesigned slider UI. The data-layer change is independent of any visual treatment; the UI follow-up is downstream and out of scope here.
- **Non-goal:** Touching `model.sensitivity()` or the tornado's baseline computation. The discrepancy is at the slider-recompute path, not the sensitivity path.
- **Non-goal:** Letting the user *edit* the analyst's registry from the UI. The registry is analyst-authored, version-controlled, and source-cited; it is not a runtime knob.

---

## Business Goals

### Why This Matters

The explorer's slider is the primary mechanism by which the user develops intuition for how a concept's LCOE responds to engineering and financial assumptions. If the first slider movement produces a discontinuity unrelated to the slider, the tool teaches the wrong intuition — and silently undermines the analyst's hard-won override work. Resolving this is small surface, large credibility.

### Success Criteria

- [ ] A clearly documented decision: do sliders perturb the library-bare LCOE or the analyst-applied LCOE? (One of these is right for this tool; pick one.)
- [ ] Whichever option is chosen, the recomputed headline is consistent with the JSON's stored headline modulo the *intentional* slider effect — no spurious discontinuity attributable to the override registry.
- [ ] If option (a) is chosen, the UI surfaces the divergence explicitly (e.g. a "library-bare projection" label on the slider's output, distinct from the stored headline) so the user is never misled.
- [ ] If option (b) is chosen, `_forward_with_overrides` re-applies the analyst's `cost_overrides` and passes `override_reference_mw=P_native` so the registry scales correctly under the two-knob mechanism. The LRU cache key is extended to cover the registry hash so cache hits remain correct.

### Priority

P1. Not blocking. Lands after `explorer-rework-unblock` ships and the explorer is observably running again. The discontinuity will be immediately visible the first time someone uses the explorer post-unblock, so this should be scheduled with that visibility in mind.

---

## Problem Statement

### Current State

`server.py:_forward_with_overrides` (the function the slider's `/api/compute` endpoint calls) is documented to *not* re-apply `cost_overrides`:

> "cost_overrides are not re-applied; this is consistent with how `model.sensitivity()` works (it also omits cost_overrides)."

That comment is technically true and was a defensible decision pre-rework. Post-rework it produces three observable inconsistencies:

1. **Headline ↔ first slider value mismatch.** Stored `cost_model.headline.lcoe_per_mwh` is computed with overrides on; the first compute response is computed with overrides off. They disagree by the magnitude of the registry, which on rework-aligned concepts is non-trivial.
2. **Slider ↔ tornado axis mismatch.** The tornado chart's bars are elasticities computed at the with-overrides baseline (via `model.sensitivity(result_1gw.params)`). The slider's response curve is around a *different* baseline (overrides off). The two visualizations on the same concept page answer different questions.
3. **Analyst attribution erased.** The rework's whole point was to make every cost departure from the library a single accountable, sourced, toggleable registry entry. The slider silently throws all of them out.

### Desired Outcome

A direction is chosen. The slider's recomputed LCOE either consistently includes the analyst's overrides (and scales them correctly under the two-knob mechanism) or consistently excludes them with an explicit UI label. The headline ↔ slider ↔ tornado triple agrees about which question is being answered.

---

## Scope

### In Scope

- A decision document recording which of the three options below is adopted and why.
- Once decided, the data-layer changes needed to enforce it: `_forward_with_overrides` behavior, LRU cache key shape, `_FORWARD_NAMED` / `_FORWARD_SKIP` adjustments.
- Tests asserting headline-↔-first-recompute consistency under the chosen behavior.
- A short README addition (or inline doc comment) explaining the chosen semantics so the next reader doesn't have to re-derive them.

### Out of Scope

- UI treatment (labels, badges, slider color states). The UI follow-up is downstream of locking the data-layer semantics.
- Editing the registry from the UI.
- Changes to `model.sensitivity()` or to the helper's `run_native_and_1gw`.
- The 12 old-shape concepts. Their `analysis.md` regen is Item 11 of the rework epic; their slider behavior is whatever this spec lands.

### Options to Decide Between

- **(a) Preserve current behavior; label the divergence in the UI.** Slider recompute remains overrides-off; the UI explicitly badges the slider output as "library-bare projection." Pros: smallest data-layer change; honest about what the slider does compute. Cons: the user has to mentally hold two LCOE numbers per concept; the tornado-↔-slider mismatch remains.
- **(b) Re-apply the registry on recompute; pass `override_reference_mw`.** Slider recompute applies the analyst's `cost_overrides` and `override_reference_mw=P_native` so overrides scale correctly under `n_mod ≠ 1`. Pros: headline ↔ slider ↔ tornado all agree; analyst attribution preserved. Cons: requires the registry to be available to the server (currently it's only in the concept's `model_setup.py`, which is re-imported per concept anyway — so the cost is small but non-zero); LRU cache key needs to extend.
- **(c) Give the user a toggle: "show analyst overrides" on/off.** Both modes available; user chooses. Pros: maximum transparency. Cons: doubles the UI surface; postpones the actual question instead of answering it; adds a state variable to `ExplorerState`.

The author's recommendation is **(b)** — it's what the rework's framing implies the explorer should do — but the decision belongs in this spec's design phase, not here.

### Edge Cases & Considerations

- A concept with an empty override registry: under any option, behavior is unchanged. The discontinuity only matters when the registry is non-trivial.
- Freeform concepts (no `cost_overrides`): unaffected by any option.
- Disabled overrides (`enabled: False`): the helper's `enabled_overrides()` already filters these out; whatever the server reads from the concept module gets the filtered set.
- `cost_overrides` are stored only in the concept's `model_setup.py` (specifically the `overrides` list before `enabled_overrides()` projection). Reading them at compute time means re-evaluating the module-level expressions, which already happens in `_load_model_module`. No new IO.

---

## Requirement Selection Notes

Requirements here capture the *outcome* the explorer must achieve, not the implementation. Whether the chosen path is (a), (b), or (c) is a design-stage decision; the spec only fixes what "consistent" looks like.

---

## Requirements

### Functional Requirements

1. **FR-SO1**: The recomputed `CostModelData` returned by `POST /api/compute` for a concept with `overrides == {}` SHALL produce a headline `lcoe_per_mwh` equal (within floating-point tolerance) to the same concept's stored `cost_model.headline.lcoe_per_mwh`. No spurious discontinuity from the override registry.
2. **FR-SO2**: The slider's response curve (the locus of recomputed LCOE as a single sensitivity parameter sweeps its range) SHALL be consistent with the tornado's elasticity for that parameter (signs agree; small-perturbation slopes agree to leading order).
3. **FR-SO3**: The chosen behavior SHALL be documented in either the spec, the design, or an inline doc comment in `_forward_with_overrides` so the next reader does not re-derive it from runtime behavior.

### Non-Functional Requirements

- No measurable regression in `/api/compute` p95 latency.
- LRU cache hit rate for repeated identical slider positions SHALL remain ≥ pre-change rate (i.e. the cache key extension under option (b) is sound).

---

## Acceptance Criteria

### Core Functionality

- [ ] FR-SO1: for at least three rework-aligned concepts spanning fit-grade tiers (e.g. 01 High, 17a Low, 24 Low-pB11), the no-op slider call (`overrides={}`) returns `lcoe_per_mwh` matching the stored JSON's headline.
- [ ] FR-SO2: a sweep of `availability` from 0.7 to 0.95 in 0.05 steps produces a monotone LCOE curve whose slope sign matches the tornado's `availability` elasticity sign.
- [ ] FR-SO3: the chosen semantics are written down somewhere version-controlled and discoverable.

### Quality & Integration

- [ ] Existing test suite passes.
- [ ] New regression test for FR-SO1 against concept 01.
- [ ] Slider performance not visibly degraded in manual smoke (open concept page, drag a slider, observe no new lag).

---

## Next-Stage Handoff

**Settled in this spec:**
- The discontinuity is real, large, and worth fixing.
- The three options above are the live alternatives; "do nothing" is not.
- UI changes are out of scope here; the data-layer semantics are the deliverable.

**Design must figure out:**
- Which option (a / b / c) is right.
- If (b): where the registry lives at compute time — re-imported from the concept's `model_setup.py` (cheapest; already done via `_load_model_module`'s LRU cache) or stored in the extracted JSON (would mean extending the data-layer schema; bigger surface).
- If (b): the LRU cache key shape. The current key is `(concept_id, frozenset(overrides.items()))`. Under (b) the registry hash is fixed per concept per server lifetime, so the key may not need to change — but verify.
- The exact text of any inline doc comment or README addition explaining the chosen semantics.

**Watch-outs for design:**
- Whatever option is chosen, the slider must remain interactive. A 200 ms p95 ceiling is the right rule of thumb.
- Do not accidentally re-introduce the `result` symbol; the unblock work item removed it deliberately.
- `override_reference_mw` only matters when overrides are non-empty and `n_mod ≠ 1`. Don't accidentally pass it as `None` to a library version that doesn't tolerate it (verify forward signature — current library does accept None as default).

---

## Related Artifacts

- **Predecessor:** [`.project/active/explorer-rework-unblock/spec.md`](../explorer-rework-unblock/spec.md) — the unblock spec where this issue was identified and deferred.
- **Epic:** [`.project/backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md).
- **Three-forward contract:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:1-31`.
- **Override registry shape:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:46-83` (`Override` TypedDict, `enabled_overrides`).
- **Sensitivity baseline computation:** `costingfe.model.CostModel.sensitivity` (called via `build_sensitivity_analysis` in extractor line 178).
- **Concrete evidence of the discontinuity:** concept 01, verified 2026-06-05 — `result_1gw.costs.lcoe = 155.17 $/MWh` vs library-bare re-forward `= 127.53 $/MWh`.

**Next Steps:** After `explorer-rework-unblock` lands and approval here, proceed to `/_my_design` to choose between options (a)/(b)/(c).
