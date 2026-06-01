# Spec: Three-Forward Contract — `generic` / `native` / `result_1gw`

**Status:** Implementation Complete (2026-05-31)
**Owner:** Reid W
**Created:** 2026-05-31
**Updated:** 2026-05-31
**Complexity:** MEDIUM
**Branch:** concept-analysis-rework
**Epic:** CONCEPT-REWORK — corrective work item (touches Items 7, 8, 9, 10 and the design/epic contract)

---

## Work Item Summary

Replace the current two-forward `model_setup.py` contract (`result`, `result_1gw`) with a **three-forward** contract — `generic`, `native`, `result_1gw` — so that each adjacent pair differs in exactly **one** dimension. Today `result` (the "native" forward) is `forward(net=P_native, n_mod=1)` with **overrides off** — a library-generic reactor at the design-point size, *not* the concept's actual native cost — and it differs from `result_1gw` in *two* dimensions at once (scale **and** overrides), so the pair brackets no interpretable quantity. The fix: compute and expose three forwards — **`generic`** (design-point size, overrides off), **`native`** (design-point size, overrides on), **`result_1gw`** (1 GWe projection, overrides on, unchanged). `generic → native` isolates the override effect at fixed scale; `native → result_1gw` isolates pure replication scaling at fixed overrides. Relative overrides reference `generic` (the bare library value), not the ambiguous `result`.

## Why This Matters Now

The current naming is actively misleading — `result` reads as "this concept's native cost" but is the library's overrides-off generic, and nothing downstream displays it (the explorer uses it only as a soon-to-be-dropped fallback). The two-dimension gap between `result` and `result_1gw` means there's no clean "what do the overrides do" or "what does replication do" decomposition for a reviewer or the explorer to show. Item 7 (helper + validators) has **shipped** with the two-forward contract, and Items 8 (prompts), 9 (critic), and 10 (explorer) are not yet built — so fixing the contract now, before those land, means they target the correct shape from the start and only Item 7's shipped code needs a (small, contained) change. Deferring it means Items 8/9/10 bake in the misleading contract and the fix gets more expensive.

## Key Bets / Constraints

- **Bet:** three forwards that each move one dimension is the right factorization — it makes the override effect and the replication effect independently legible, and gives the explorer a real per-concept native number (`native`) alongside the cross-concept replication-floor number (`result_1gw`).
- **Constraint (one dimension per step):** `generic` = `forward(net=P_native, n_mod=1)`, **no overrides**. `native` = `forward(net=P_native, n_mod=1, cost_overrides=<enabled>, override_reference_mw=P_native)`, **overrides on, same scale**. `result_1gw` = `forward(net=1000, n_mod=1000/P_native, cost_overrides=<enabled>, override_reference_mw=P_native)`, **overrides on, projected** — unchanged from today.
- **Constraint (relative overrides reference `generic`):** if an override is written relative to the library's own number (e.g. `0.70 * generic.costs.cas21`), it references `generic` — the bare overrides-off value — never `native` or `result_1gw`.
- **Constraint:** the cross-concept comparison number is still `result_1gw` at exactly `net=1000` via the two-knob call. This work changes nothing about that number or its role.
- **Non-goal:** the Phase 3 native-*scale*-up projection (`result_1gw_native`, physics-based single-machine scaling). `native` here is overrides-at-design-point-scale, a different and simpler object; it does not attempt physics scale-up.
- **Non-goal:** changing override semantics, provenance rules, or the two-knob `result_1gw` mechanism.

---

## Business Goals

### Why This Matters

A reviewer (and the explorer) should be able to read a concept's cost story as a clean decomposition: *here is what the library says for a reactor this size (`generic`); here is what it costs once the company's published numbers are applied (`native`); here is what that costs replicated to 1 GWe (`result_1gw`).* The current two-forward contract collapses the middle step and mislabels the first, so neither the "override effect" nor the "replication effect" is visible, and `result` looks like a number it isn't. The three-forward contract makes the accountability story legible by construction.

### Success Criteria

- [ ] Every regenerated `model_setup.py` exposes `model`, `generic`, `native`, `result_1gw` at module level; `result` (the ambiguous name) is gone.
- [ ] `generic` is overrides-off at design-point scale; `native` is overrides-on at design-point scale; `result_1gw` is overrides-on at 1 GWe — verified by per-account spot check (with overrides off, `generic == native`; with `P_native == 1000`, `native == result_1gw`).
- [ ] Relative overrides reference `generic`; the validator rejects references to `native`/`result_1gw`.
- [ ] The shipped Item 7 helper + validators, the design doc, the epic, and the Item 8/9/10 specs all describe the three-forward contract consistently (no lingering two-forward `result`).

### Priority

P0 — corrective; should land before Item 8's prompt rework and Item 10's explorer adapter productionize the contract, to avoid baking in the two-forward shape.

---

## Problem Statement

### Current State

- `lib/model_setup_helpers.py:run_native_and_1gw` returns `(result, result_1gw)`. `result` = `forward(net=P_native, n_mod=1)` with **no `cost_overrides`** (docstring: "the library's bare per-account reference… no overrides"). `result_1gw` = the overridden two-knob projection.
- So `result` and `result_1gw` differ in **two** dimensions (scale: P_native→1000; overrides: off→on). The pair is not a before/after of any single quantity; the meaningful override-effect comparison (Phase 0's toggle probe) holds scale fixed and compares overrides-off vs overrides-on at the *same* scale.
- `result` is named/exposed as if it were the concept's native cost, but it excludes the company overrides (which *are* the concept-specific cost). It is "a library-generic reactor at the design-point size."
- The module contract `model`, `result`, `result_1gw` is enforced by `validate_model_setup_contract` (validators.py:542); the explorer requires `result` (extract_explorer_data.py:254) but only as the `result_1gw`-absent fallback (dropped in Item 10). FR-14 relative overrides reference `result` (design doc).

### Desired Outcome

Three module-level forwards — `generic`, `native`, `result_1gw` — each one dimension apart, with relative overrides referencing `generic`, the validators enforcing the three names and the new frame rule, and the design/epic/downstream specs aligned.

---

## Scope

### In Scope

- **`lib/model_setup_helpers.py`** — produce all three forwards; the exact call signature is a design detail. Print/CAS-breakdown block updated to show all three.
- **`lib/validators.py`** — `validate_model_setup_contract`: require module-level `model`, `generic`, `native`, `result_1gw`; recognize the new helper-form binding(s). `validate_override_registry`: the relative-override frame check requires references to `generic` and rejects `native`/`result_1gw`.
- **Tests** — `test_model_setup_helpers.py`, `test_validators.py` updated for the three-forward contract and the new frame rule.
- **Design doc** (`concept-analysis-rework-design.md`) — the four-step `model_setup.py` example becomes five-step (add the `native` forward); the Override Entry FR-14 example references `generic`; Required Invariants and How-It-Works updated.
- **Epic** (`epic_concept_analysis_rework.md`) — Critical Success Factor, Future State four-step bullet, and the success criteria that name `result`/`result_1gw` updated to the three-forward contract.
- **Downstream specs** (consumers; update to target the new contract): Item 8 (`model_setup` prompt FR-10/FR-11 four-step→five-step; FR-14 relative form references `generic`), Item 9 (critic reads three forwards), Item 10 (explorer reads `generic`/`native`/`result_1gw`; drops the `result` requirement and the fallback).

### Out of Scope

- Phase 3 native-scale-up projection (`result_1gw_native`).
- Any change to the `result_1gw` number, the two-knob mechanism, override provenance, or the upstream tables.
- Re-running / regenerating concepts (Items 10/11) — this item fixes the contract and the shipped tooling; regeneration consumes it.

### Edge Cases & Considerations

- **Overrides off (empty registry):** `generic == native` (no overrides to apply). Not an error; the validator and any spot-check must treat equality as expected.
- **`P_native == 1000`:** `n_mod == 1` and `native == result_1gw`. No special-casing.
- **`override_reference_mw` on the `native` forward:** at `net=P_native, n_mod=1` the per-module power equals the reference, so the scaling ratio is 1.0 and overrides pass through at face value whether or not `override_reference_mw=P_native` is passed. Design must confirm the library yields identical `native` either way and pick the explicit form for uniformity.

---

## Decisions Locked Here

### The three forwards

| name | call | scale | overrides | role |
|---|---|---|---|---|
| `generic` | `forward(net=P_native, n_mod=1, **spec)` | design point | **off** | library default story at the design-point size; the reference relative overrides are written against |
| `native` | `forward(net=P_native, n_mod=1, cost_overrides=<enabled>, override_reference_mw=P_native, **spec)` | design point | **on** | the concept's actual cost at its own scale |
| `result_1gw` | `forward(net=1000, n_mod=1000/P_native, cost_overrides=<enabled>, override_reference_mw=P_native, **spec)` | 1 GWe | **on** | the standardized cross-concept comparison number (unchanged) |

`generic → native` = override effect at fixed scale. `native → result_1gw` = replication effect at fixed overrides. No pair moves two dimensions.

### Module-level contract

`model`, `generic`, `native`, `result_1gw` are importable at module level. `result` is removed. The explorer's primary number remains `result_1gw`; `native` and `generic` become available for a per-concept decomposition view.

### Relative-override reference frame

The FR-14 relative form references `generic` (e.g. `0.70 * generic.costs.cas21`) — the bare library value. References to `native` or `result_1gw` are invalid (circular / wrong scale) and rejected by `validate_override_registry`.

---

## Requirement Selection Notes

The requirements lock the three forwards, their exact call shapes, the module-level names, and the relative-override reference frame — the things that must be true for the contract to be coherent and for downstream items to target it. Deferred to design: the helper call signature; whether `native` passes `override_reference_mw` explicitly; the exact identifier spelling (`generic`/`native`/`result_1gw` per the user's intent vs. a parallel `result_generic`/`result_native`/`result_1gw`); and the explorer's decomposition view (Item 10).

## Requirements

### Functional Requirements

1. **FR-1**: `model_setup.py` MUST expose `model`, `generic`, `native`, `result_1gw` at module level. `result` MUST NOT be used as a contract name.
2. **FR-2**: `generic` MUST be `forward(net=P_native, n_mod=1, **spec)` with **no** `cost_overrides`.
3. **FR-3**: `native` MUST be the overrides-on forward at design-point scale (`net=P_native, n_mod=1, cost_overrides=<enabled>`, `override_reference_mw=P_native`), differing from `generic` only by the applied overrides.
4. **FR-4**: `result_1gw` MUST be unchanged: the two-knob call at `net=1000, n_mod=1000/P_native, override_reference_mw=P_native, cost_overrides=<enabled>`.
5. **FR-5**: Relative override `value` expressions MUST reference `generic`; `validate_override_registry` MUST reject references to `native` and `result_1gw` (extending the current `result_1gw` frame-error check).
6. **FR-6**: `validate_model_setup_contract` MUST require `model`, `generic`, `native`, `result_1gw` at module level and recognize the helper-form binding(s) that produce them.
7. **FR-7**: The shared helper(s) MUST produce all three forwards with no per-concept duplication of the call shapes.
8. **FR-8** [INFERRED]: The design doc, epic, and Item 8/9/10 specs MUST be updated to the three-forward contract; no document may continue to describe the two-forward `result`/`result_1gw` shape.

### Non-Functional Requirements

- The extra forward (`native`) is one additional `forward()` call per concept — negligible cost; no NFR concern.

---

## Acceptance Tests

- [ ] A hand-written five-step `model_setup.py` for concept 01 binds `model`, `generic`, `native`, `result_1gw`; passes `validate_model_setup_contract`.
- [ ] With the 4 ARC overrides on: `generic` LCOE ≈ the library-bare native number, `native` LCOE reflects the overrides at 233 MWe scale, `result_1gw` ≈ 668 $/MWh (per Phase 0). With all overrides disabled: `generic == native` per-account.
- [ ] `validate_override_registry` accepts `value: 0.70 * generic.costs.cas21`; rejects `0.70 * native.costs.cas21` and `0.70 * result_1gw.costs.cas21` with a frame-error message naming `generic` as the required reference.
- [ ] `validate_model_setup_contract` fails a module missing `native`; fails one still binding only `result`/`result_1gw`.
- [ ] `test_model_setup_helpers.py` and `test_validators.py` pass with the three-forward fixtures; no lingering `result`-only fixtures.
- [ ] `grep` shows no remaining two-forward `result` contract references in the design doc, epic, helper, validators, or the Item 8/9/10 specs.

---

## Open Questions

- **Helper signature.** Whether one call returns all three forwards, or `generic` is a standalone line and the helper returns `native`/`result_1gw`. Either works; design picks. `validate_model_setup_contract`'s helper-form recognition updates from `result, result_1gw = ...` to the chosen shape.
- **Identifier spelling.** User intent is `generic` / `native` / `result_1gw`. A parallel set (`result_generic` / `result_native` / `result_1gw`) is more greppable and consistent but more churn. Pick one in design; default to the user's words.
- **`native` and `override_reference_mw`.** Confirm the library yields identical `native` with and without `override_reference_mw=P_native` at `net=P_native, n_mod=1`, and pass it explicitly for uniformity.
- **Explorer decomposition view (Item 10).** Whether/how the explorer surfaces `generic`/`native` alongside `result_1gw` (e.g. a per-concept override-effect bar). Out of scope here; flagged for Item 10.

---

## Dependencies

- **Item 7 (shipped):** this changes Item 7's `run_native_and_1gw` return shape, the print block, `validate_model_setup_contract`, and `validate_override_registry`. Small, contained edits to landed code + tests.
- **Items 8 / 9 / 10 (not yet built):** consume the new contract; their specs get updated by this item (FR-8) so they target three forwards from the start.
- **Item 4 (landed):** `_scale_overrides` `n_mod=1` reference fix is what makes `native` (overrides at the design-point single-module frame) scale correctly. No further library change.
- **Design doc / epic:** updated by this item to describe the three-forward contract.

---

## Next-Stage Handoff

**Settled in this spec:**
- The three forwards, their exact call shapes, and the one-dimension-per-step factorization.
- Module-level contract `model` / `generic` / `native` / `result_1gw`; `result` removed.
- Relative overrides reference `generic`; validator rejects `native`/`result_1gw`.
- `result_1gw` and the two-knob mechanism are unchanged.

**Design must figure out:**
- The helper call signature.
- Identifier spelling; whether `native` passes `override_reference_mw` explicitly.
- The exact AST changes to the two validators and the test-fixture updates.

**Watch-outs for design:**
- Don't reintroduce a two-dimension gap: `native` and `result_1gw` MUST share the same enabled-override set; the only difference is scale.
- The empty-registry case makes `generic == native` — fixtures and any "did the overrides do anything" check must expect equality, not flag it.
- Keep `result_1gw` byte-for-byte the same call — this item must not perturb the cross-concept number.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_concept_analysis_rework.md`
- **Design doc:** `.project/concepts/concept-analysis-rework-design.md` (four-step shape → five-step; Override Entry FR-14 form)
- **Item 7 (helper + validators, shipped):** `.project/active/concept-rework-helpers-validators/`, `lib/model_setup_helpers.py`, `lib/validators.py`
- **Item 8 / 9 / 10 specs:** consumers updated by FR-8
- **Prototype:** `.project/active/concept-rework-prototype/artifacts/model_setup.py` (two-forward reference; the override numbers remain the oracle)

**Next Steps:** After approval, proceed to `/_my_design`.
