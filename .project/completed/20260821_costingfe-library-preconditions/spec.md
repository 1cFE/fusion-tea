# Spec: 1costingFE Library Preconditions for Two-Knob Projection

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-05-31 08:16
**Completed:** 2026-05-31
**Complexity:** LOW
**Branch:** concept-analysis-rework (fusion-tea) / fix/scale-overrides-reference-frame (1costingfe, commit a2153ad)
**Epic:** CONCEPT-REWORK — Item 4

---

## Work Item Summary

The concept-analysis rework projects every concept's cost to 1 GWe NOAK with a single uniform call: `forward(net_electric_mw=1000, n_mod=1000/P_native, override_reference_mw=P_native)`. Two preconditions in the 1costingFE library block this call shape from doing what the rework's design assumes. This work item lands both fixes in `~/1cfe/1costingfe/`: (1) accept non-integer `n_mod` so the replication count `1000/P_native` is honored exactly, and (2) fix `_scale_overrides` so the reference-side forward runs at one module at native power, which is the frame the analyst writes the override in. After this item, the two-knob call carries the design's stated semantic: per-module reactor-island overrides pass through unchanged when target per-module power equals reference per-module power; plant-aggregate overrides scale to the target plant total.

## Why This Matters Now

This is the library precondition for every Phase 1 item that touches cost numbers. Item 7 (helpers + validators), Item 8 (prompt rework), and the Item 10 pilot all assume the two-knob mechanism reaches `result_1gw` cleanly. Phase 0 (Item 1) traced the root cause and reproduced both issues empirically — the work to land the fix is small (~5 lines in `_scale_overrides` plus a one-field validator change) but downstream items cannot rely on the projected numbers until it ships. Doing it first also lets every later item pin a single library commit.

## Key Bets / Constraints

- **Bet**: the `_scale_overrides` bug is mechanical — change the reference-side forward from `n_mod=caller_n_mod` to `n_mod=1`, and the design's stated invariant ("per-module overrides pass through unchanged at native per-module power; plant-aggregate overrides scale to target plant total") holds without any other code change. Phase 0's probe (`probe_override_scaling.py`) supports this empirically and the mechanism is fully traced.
- **Constraint**: existing callers of `forward()` that don't use `override_reference_mw` must be unaffected. The fix lives inside the `if override_reference_mw is not None and cost_overrides` branch in `forward()` (`model.py:418`); call sites that don't enter that branch never touch `_scale_overrides`.
- **Constraint**: the `n_mod` validator change must not silently round previously-integer-passing values to a different number. Integer values continue to behave identically; only the type widens.
- **Non-goal**: this item does not change the *semantics* of `override_reference_mw` or document any new public contract beyond what the design already states. It makes the existing contract true.
- **Non-goal**: no API additions, no rename of `_scale_overrides`, no refactor of the `_OVERRIDE_TO_ATTR` map.

---

## Business Goals

### Why This Matters

The whole rework's apples-to-apples cross-concept comparison rests on `result_1gw` being reached identically for every concept via one call shape. If the library silently rescales the analyst's overrides on the way through, the registry's six-field entries (`account / value / enabled / provenance / source / rationale`) are lies — the `value` the analyst sourced is not the value the library applies. Phase 0 surfaced exactly this on concept 01: per-module C220101 and C220106 overrides arrived 47% inflated. Fixing this is the precondition for the override-registry framing to be honest.

### Success Criteria

- [ ] `forward(net_electric_mw=1000, n_mod=1000/P_native, override_reference_mw=P_native, cost_overrides={...})` applies per-module reactor-island overrides at their face value per module (replicated by `n_mod` for the plant total) and scales plant-aggregate overrides to the target plant total.
- [ ] Non-integer `n_mod` (e.g. `4.29` for `P_native=233`) is accepted and used directly — no rounding, no integer-coercion error.
- [ ] Downstream pipeline items (Item 7, Item 8, Item 10) can pin a single library commit and rely on these semantics without monkey-patching.

### Priority

P0 within the epic — blocks Items 7, 8, 10, 11. Parallel with Item 5 (deterministic project tables).

---

## Problem Statement

### Current State

Two issues, both in `~/1cfe/1costingfe/`:

**Issue A — `n_mod` is strict-int with `ge=1`.** `src/costingfe/validation.py:90`:

```python
n_mod: int = Field(default=1, ge=1, strict=True)
```

This forces the caller to pass an integer. The two-knob call computes `n_mod = 1000/P_native` which is non-integer for almost every concept (`P_native=233` → `n_mod=4.29`; `P_native=400` → `n_mod=2.5`). Phase 0 monkey-patched the field at import time to allow float; the production library must accept it directly.

**Issue B — `_scale_overrides` runs its reference forward at the caller's `n_mod`.** `src/costingfe/model.py:865-870`:

```python
ref_result = self.forward(
    net_electric_mw=reference_mw, cost_overrides=None, **forward_kwargs
)
target_result = self.forward(
    net_electric_mw=target_mw, cost_overrides=None, **forward_kwargs
)
```

`**forward_kwargs` (assembled at `model.py:423-430`) includes the caller's `n_mod`. So when the caller invokes the two-knob call with `n_mod = 1000/P_native`, the reference run executes at `(net=P_native, n_mod=1000/P_native)` — meaning per-module power in the *reference* run is `P_native² / 1000`, not `P_native`. For any account whose per-module cost has a per-module thermal-power dependence (C220101 structure, C220106 vacuum vessel, blanket, etc.), the override scaling ratio `tgt_val / ref_val` is computed against the wrong reference frame, silently inflating per-module overrides.

Phase 0's probe (`.project/active/concept-rework-prototype/artifacts/probe_override_scaling.py`) quantified this on ARC at `P_native=400`, `n_mod=2.5`:

| account | what design wants | ratio currently | ratio if ref were `n_mod=1` |
|---|---|---|---|
| C220103 (coils — no power term) | 1.0000 (passthrough) | 1.0000 ✓ | 1.0000 ✓ |
| C220101 (structure) | 1.0000 (passthrough) | 1.4671 ✗ | 1.0000 ✓ |
| C220106 (vacuum vessel) | 1.0000 (passthrough) | 1.4671 ✗ | 1.0000 ✓ |
| CAS27 (per-module — uses `pt.p_net` which is per-module) | 1.0000 (passthrough) | 2.5000 ✗ | 1.0000 ✓ |
| CAS22 (plant-aggregate — already summed over `n_mod` in default) | ≈ n_mod | n/a (no per-mod power dep) | ≈ n_mod ✓ |

Phase 0's probe table mislabeled CAS27 as plant-aggregate; spot-checking during implementation showed it is in fact per-module (`cas27_special_materials(cc, pt.p_net, …)` reads `pt.p_net` which is per-module net power). With the fix it passes through unchanged like the other per-module accounts. CAS22 is the actual plant-aggregate account (its default `c22_detail["C220000"] = per_module_equipment * n_mod + labor + plant_wide` is already summed over modules), and the target-side call's `n_mod` keeps that scaling correct. The fix is to change the *reference* call to `n_mod=1`; the target call is untouched.

### Desired Outcome

The two-knob call has the semantics the design already documents: the analyst writes per-module overrides at native per-module power, and the library applies them at that face value per module without surreptitious rescaling. Non-integer `n_mod` is supported directly.

---

## Scope

### In Scope

- `~/1cfe/1costingfe/src/costingfe/validation.py:90` — relax `n_mod` to accept any positive real value.
- `~/1cfe/1costingfe/src/costingfe/model.py:865-870` — change the reference-side forward inside `_scale_overrides` to `n_mod=1`.
- New library tests in `~/1cfe/1costingfe/tests/` covering both changes (test file location and naming per existing library conventions — `test_model.py` is the closest fit).
- Library version bump, pinned in the fusion-tea consumer.

### Out of Scope

- Any change to `_OVERRIDE_TO_ATTR`, the public `forward()` signature, or the `override_reference_mw` contract docstring beyond what's needed to reflect the fix.
- Any change to fusion-tea pipeline code (Items 5–11 own that).
- Re-running or regenerating any concept's artifacts (Item 11's job).
- Removing the existing fusion-tea-side monkey-patch in `probe_override_scaling.py` (prototype artifact, kept for the record).

### Edge Cases & Considerations

- **`n_mod < 1`**: design intent is "more than one module to reach 1 GWe", so `gt=0` is technically permissive but values like `0.5` (a sub-module fraction) are physically odd. The validator should still accept `gt=0` to keep the field uniform; the rework never generates `n_mod < 1` in practice because `P_native < 1000 MWe` is the regime of interest.
- **Existing integer call sites**: any caller passing `n_mod=1` (the default) or any other integer continues to work; the only change is that float values stop raising validation errors.
- **`CAS28` digital-twin zero-cost case**: the `ref_val > 0` guard at `model.py:888` already handles this; changing ref-side `n_mod` to 1 does not affect that branch.
- **Per-module accounts with no power term (C220103 coils)**: ratio is 1.0 under both the buggy and fixed reference frames, so these accounts are silent on the fix's correctness; the test must hit a power-dependent per-module account.
- **Library callers that pass `override_reference_mw` *without* using the two-knob call** (e.g. the prior `costingfe-scaled-overrides` integration): the fix changes the numerical result for these callers when the caller's `n_mod != 1`. Spot-check before bump: confirm prior fusion-tea integrations either use `n_mod=1` or are tolerant of the corrected ratios.

---

## Requirement Selection Notes

Two normative requirements only: (1) the `n_mod` type widening, (2) the `_scale_overrides` reference-frame fix. Everything else is design detail or test mechanics, left to design/implementation. The phrase "test must hit a power-dependent per-module account" is a test-design constraint (FR-3) because without it the test is silent on the bug — Phase 0 showed that picking the wrong account hides the regression.

---

## Requirements

### Functional Requirements

1. **FR-1**: The library MUST accept any positive real value for `n_mod` in `CostingInput`. Integer values MUST continue to behave identically.
2. **FR-2**: When `forward()` is called with `override_reference_mw` set and non-`None` `cost_overrides`, `_scale_overrides` MUST run its reference forward at `n_mod=1` (regardless of the caller's `n_mod`). The target-side forward MUST continue to use the caller's `n_mod`.
3. **FR-3**: The library test suite MUST include at least one regression test exercising the two-knob call shape `forward(net=1000, n_mod=1000/P_native, override_reference_mw=P_native, cost_overrides={...})` and MUST assert: (a) a per-module reactor-island override on a *power-dependent* account (e.g. C220101 or C220106) passes through unchanged per module (scaling ratio = 1.0); (b) a plant-aggregate override on CAS22 scales by the library's own measured CAS22 ratio between the reference and target frames (close to but not exactly `n_mod` due to the multi-unit labor factor). The plant-aggregate assertion guards against an over-eager fix that also forces target-side `n_mod=1`.
4. **FR-4**: The library MUST be released at a new version pinnable by the fusion-tea consumer.

### Non-Functional Requirements

- No behavior change for `forward()` calls that do not pass `override_reference_mw`.

---

## Acceptance Criteria

### Core Functionality

- [x] `CostingInput(n_mod=4.29)` validates without error and the value is used as-is by `forward()`.
- [x] The regression tests from FR-3 pass (4 tests in `tests/test_model.py`, covering both per-module and plant-aggregate scaling).
- [x] Two-knob call probe reproduces the "ratio_intended" column from Phase 0: C220101, C220103, C220106, CAS27 all arrive at ratio 1.0000 (per-module passthrough). Verified against the live library post-fix.

### Quality & Integration

- [x] Existing 1costingFE tests continue to pass (359 total, including 4 new regression tests).
- [x] Fusion-tea consumes costingfe via editable local install (`pyproject.toml:33`); no version bump needed — fix is live. The monkey-patch in `probe_override_scaling.py` is left in place (prototype artifact); no other fusion-tea code uses it.

---

## Next-Stage Handoff

**Settled in this spec:**
- The root cause and exact fix for both issues are traced and small. Reference-side `n_mod=1`; target-side unchanged.
- `n_mod` validator widens to positive float with no other field changes.
- Test must include a power-dependent per-module account (per FR-3) — picking only C220103 would silently hide the regression.

**Design must figure out:**
- Test placement and structure inside `tests/` (which existing test file, which fixtures, parametrize or separate tests).
- Whether to add an internal docstring to `_scale_overrides` capturing the reference-frame semantic, or leave it implicit.
- Library version bump strategy (patch vs minor — depends on the library's existing versioning convention; spot-check whether any current external caller relies on the buggy ratios).
- Migration note (if any) for callers of `override_reference_mw` who passed `n_mod != 1` previously.

**Watch-outs for design:**
- The fix is `n_mod=1` on the *reference* call only; an over-eager refactor that also forces target-side `n_mod=1` breaks plant-aggregate scaling.
- The `**forward_kwargs` plumbing at `model.py:865-870` passes a lot of kwargs through; mutating the dict in place to override `n_mod` is one path, an explicit `dict(forward_kwargs, n_mod=1)` is cleaner — design's call.
- Fractional `n_mod` may surface latent integer assumptions elsewhere in the model (e.g. anywhere `n_mod` indexes a list, or appears in a JAX shape). A grep for `n_mod` usages in `model.py` before signing off catches that.

---

## Related Artifacts

- **Epic**: `.project/backlog/epic_concept_analysis_rework.md` — Item 4.
- **Phase 0 findings**: `.project/active/concept-rework-prototype/findings.md` (Bet #1).
- **Phase 0 probe**: `.project/active/concept-rework-prototype/artifacts/probe_override_scaling.py` + `.txt` (reproducer).
- **Library source**: `~/1cfe/1costingfe/src/costingfe/model.py:849-896` (`_scale_overrides`), `src/costingfe/validation.py:90` (`n_mod` field), `src/costingfe/model.py:394-431` (`forward()` call site).
- **Design**: `.project/concepts/concept-analysis-rework-design.md`.
- **Touchpoints research**: `.project/research/20260530-concept-rework-code-touchpoints.md`.
- **Enum map** (for account-code reference): `.project/research/20260509-1costingfe-enum-map.md`.

---

**Next Steps:** After approval, proceed to `/_my_design`.
