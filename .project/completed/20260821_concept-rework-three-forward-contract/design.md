# Design: Three-Forward Contract — `generic` / `native` / `result_1gw`

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-31
**Updated:** 2026-05-31
**Branch:** concept-analysis-rework
**Commit:** b94ca91
**Complexity:** MEDIUM

---

## Overview

Replace the two-forward `model_setup.py` contract (`result`, `result_1gw`) with a three-forward contract — `generic`, `native`, `result_1gw` — where each adjacent pair moves exactly one dimension. The local working tree has already done the load-bearing half of this: it factored the overrides-off forward into a `generic_reference()` helper. This design promotes that helper's output to the mandatory module-level name `generic`, adds the missing `native` (overrides-on at design-point scale) forward, and aligns the two validators, the print block, the design doc, the epic, and the Item 8/9/10 specs.

## Related Artifacts

- **Spec:** `.project/active/concept-rework-three-forward-contract/spec.md`
- **Epic:** `.project/backlog/epic_concept_analysis_rework.md` (Item 8/9/10 are children)
- **Design doc (updated by this item):** `.project/concepts/concept-analysis-rework-design.md`
- **Shipped Item 7 code:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py`, `.../lib/validators.py`
- **Prototype oracle:** `.project/active/concept-rework-prototype/artifacts/model_setup.py`

## Research Findings

The working tree already carries an interim step toward this contract. Reconciling with it is the central design constraint, so it is documented first.

**Local changes (uncommitted) — already done:**
- `model_setup_helpers.py:68` adds `generic_reference(model, spec, p_native, *, noak=True)` — a plain overrides-off forward at `net=p_native, n_mod=1`. `run_native_and_1gw` now calls it for its `result` (`:123`), so `result == generic_reference(...)`.
- The prompt templates (`model_setup_costingfe.md`, `config/account_walkthrough.md`, `output_template.md`) were rewritten so a *relative* override references `ref = generic_reference(...)` instead of the (not-yet-defined-at-overrides-time) `result`. `ref` is **optional** — imported/called only when a relative override needs it.
- The rename the user flagged (`native_reference` → `generic_reference`) is **complete**: no `native_reference` identifier remains anywhere (`grep` clean).

**Key realization:** `generic` (the spec's overrides-off, design-point forward) is *exactly* what `generic_reference()` computes. The interim `ref` line and the contract's `generic` binding are the same object under two names. So the contract does not need new machinery — it needs to (a) promote `ref` to the mandatory module-level name `generic`, (b) add the `native` forward the two-forward shape was missing, and (c) repoint the relative-override frame from "the native `result`" to `generic`.

**Forward semantics (confirmed, `1costingfe/src/costingfe/model.py:forward`):** `cost_overrides` + `override_reference_mw` scale each override by the ratio of its account at `(net_electric_mw, n_mod)` vs. at the reference power. For the `native` forward — `net=p_native, n_mod=1, override_reference_mw=p_native` — target power equals reference power, so every ratio is 1.0 and overrides pass through at face value. `native` is therefore **identical** with or without `override_reference_mw=p_native`; we pass it explicitly for uniformity with `result_1gw` (resolves spec Open Question 3). Empty `cost_overrides` is falsy, so `_scale_overrides` is skipped entirely and `native == generic` when the registry is empty.

**Validators (`validators.py`):**
- `validate_model_setup_contract` (`:507`) requires `model`, `result`, `result_1gw`; classifies the `result_1gw` binding as **helper form** (`result, result_1gw = run_native_and_1gw(...)`, `:559`) or **inline form** (`:564`). Helper-form recognition keys on the tuple containing `result`.
- `validate_override_registry` (`:654`) frame check (`:742`) rejects a `value` referencing `result_1gw`; accepts any other runtime `Name` (including `result`) as a relative override.

**Explorer / tests downstream:** `extract_explorer_data.py:302` and `server.py:553` read `result` as a hard requirement (with a `result_1gw → result` fallback). These are **Item 10's** code; this item updates only Item 10's *spec*, not its code (regeneration is out of scope, so shipped concept files still bind `result`).

## Core Concept

A concept's cost story should read as a clean three-point decomposition, each step isolating one variable:

```
generic ──(apply company overrides, same scale)──▶ native ──(replicate to 1 GWe, same overrides)──▶ result_1gw
```

- **`generic`** — `forward(net=P_native, n_mod=1)`, **overrides off**. The library's bare answer for a reactor this size. It is the reference a relative override is written against, and the left anchor of the override-effect comparison.
- **`native`** — same call **plus** the enabled overrides (`cost_overrides=<enabled>, override_reference_mw=P_native`). The concept's actual cost at its own scale. `generic → native` is the pure override effect at fixed scale.
- **`result_1gw`** — the enabled overrides replicated to 1 GWe via the two-knob call (`net=1000, n_mod=1000/P_native`). **Byte-for-byte unchanged.** `native → result_1gw` is the pure replication effect at fixed overrides.

The insight that makes this cheap: the contract's `generic` and the local `generic_reference()` output are the same forward. The relative-override ordering constraint — `generic` must exist *before* the `overrides` list is built — already forces `generic` to be a standalone line ahead of the registry. That same line satisfies FR-1's "module-level `generic`" requirement. One line does both jobs; the helper just stops recomputing the overrides-off forward and instead computes the overrides-**on** `native`.

## Key Bets & Decisions

### Decision 1 — `generic` is a mandatory standalone line; the helper returns `(native, result_1gw)`

**This resolves spec Open Question 1** ("one call returns all three vs. `generic` standalone + helper returns the other two").

The module-level shape (helper form, the real prompt):
```python
model   = CostModel(concept=..., fuel=...)
generic = generic_reference(model, spec, P_native)          # forward 1: overrides OFF
overrides = [ {"value": 0.70 * generic.costs.cas21, ...} ]  # relative refs `generic`
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)  # forwards 2 & 3: overrides ON
print_cas_breakdown(generic, native, result_1gw, overrides)
```

**Why standalone `generic`, not all-three-in-helper:** a relative override references `generic`, and `overrides` is an *argument* to the helper — so `generic` must be bound before the helper runs. The alternative (`generic, native, result_1gw = run_native_and_1gw(...)`) cannot supply `generic` to the override list without a second call or a callback. The local `generic_reference()` change already commits to the standalone form; this decision keeps it and makes it mandatory rather than relative-override-only.

**Change from the interim local state:** `generic` is **always present** (FR-1), not the optional `ref` the local prompt edits made it. Every `model_setup.py` binds it, even with an empty registry — which also gives the explorer the `generic`-vs-`native` override-effect decomposition for free.

**Rejected:** helper returns all three. Breaks relative-override ordering; discards the `generic_reference` abstraction; more machinery, not less.

### Decision 2 — Identifier spelling: `generic` / `native` / `result_1gw`

Per spec default (the user's words), not the parallel `result_generic` / `result_native`. `result_1gw` is unchanged, so two of three names already match; only the new `native` and the renamed `generic` are introduced.

### Decision 3 — Helper keeps the name `run_native_and_1gw`, returns `(native, result_1gw)`

Its old `result` return (overrides-off) is dropped; the new first return is `native` (overrides-**on** at design point). The name now describes its output *more* accurately than before — `native` is genuinely the concept's native cost. Renaming the helper would churn the validator's name-match, three prompt files, and the tests for no semantic gain. Internally the helper stops calling `generic_reference` (no recomputation); it issues the `native` forward directly.

### Decision 4 — `validate_override_registry` frame rule: require `generic`, reject `native` and `result_1gw`

Extend the existing single-name `result_1gw` frame check to a forbidden set `{native, result_1gw}`, with the error message naming `generic` as the required reference (FR-5, acceptance test 3). A reference to the now-removed `result` is also caught (it would `NameError` at runtime) and gets the same frame message, so a file carried over from the two-forward shape fails loudly. Constant and numeric `value` forms are unaffected.

## Architecture

Five edit surfaces, in dependency order. The first two are the contract; the rest conform to it.

1. **`model_setup_helpers.py`** — the contract's source of truth.
   - `generic_reference()`: structurally unchanged (already the right call); **docstring** rewritten — it now produces the module-level `generic`, no longer "the same forward `run_native_and_1gw` issues for `result`."
   - `run_native_and_1gw()`: replace the `result = generic_reference(...)` line with a `native = model.forward(net=p_native, n_mod=1, cost_overrides=enabled_overrides(overrides), override_reference_mw=p_native, ...)` call; return `(native, result_1gw)`. `result_1gw` call **untouched**.
   - `print_cas_breakdown()`: signature → `(generic, native, result_1gw, overrides)`; three CAS columns; headline `result_1gw` LCOE line **unchanged** (the `run_model` grep at `loop.py:676` depends on it being first).
   - Module docstring: "four-step" → the three-forward shape.

2. **`validators.py`** — enforce the new contract shape (AST, no LLM).
   - `validate_model_setup_contract`: required names `{model, generic, native, result_1gw}`; helper-form recognition updates from the `result, result_1gw = run_native_and_1gw(...)` tuple to the `native, result_1gw = run_native_and_1gw(...)` tuple, **plus** a `generic = generic_reference(...)` binding check. Messages updated.
   - `validate_override_registry`: forbidden-frame set `{native, result_1gw}` (and `result`); message names `generic`.

3. **Tests** — `test_model_setup_helpers.py`, `test_validators.py` retargeted to the three-forward contract and the new frame rule (see Appendix B).

4. **Design doc** (`concept-analysis-rework-design.md`) — the four-step inline example becomes the three-forward inline example (add the `native` forward); the Override Entry FR-14 prose references `generic`; the module-level contract line, Required Invariants, and the How-It-Works / edge-case passages drop `result`.

5. **Epic + Item 8/9/10 specs** — FR-8 documentation alignment (see Appendix C for the inventory). Prompt templates (Item 8's domain, but already partly edited locally) flip `ref`→`generic`, make it mandatory, and update Hard Rule 5 and the contract names.

**Data flow unchanged downstream:** `result_1gw` remains the explorer's primary number, reached by the identical two-knob call. `generic`/`native` are *additional* module-level attributes; nothing that reads `result_1gw` is perturbed.

## Required Invariants

- **One dimension per step.** `generic` and `native` share `(net=P_native, n_mod=1)`; differ only by overrides. `native` and `result_1gw` share the enabled-override set; differ only by scale. No pair moves two dimensions.
- **`result_1gw` is byte-for-byte unchanged** — same call, same number, same `verify_two_knob` contract.
- **`native` and `result_1gw` use the identical enabled-override set** (`enabled_overrides(overrides)`), applied at the same `override_reference_mw=P_native`.
- **Empty registry ⇒ `generic == native`** per account. Expected, never flagged.
- **`P_native == 1000` ⇒ `n_mod == 1` ⇒ `native == result_1gw`.** No special-casing.
- **Relative overrides reference `generic` only.** `native` / `result_1gw` / `result` references are frame errors.

## Component Overview

- **`generic_reference(model, spec, p_native, *, noak=True)`** — `model_setup_helpers.py`. Produces the `generic` forward (overrides off, design point). Already exists; docstring updated.
- **`run_native_and_1gw(model, spec, overrides, p_native, *, noak=True) → (native, result_1gw)`** — same module. Owns the two overrides-on forward shapes; no per-concept duplication (FR-7).
- **`print_cas_breakdown(generic, native, result_1gw, overrides)`** — same module. Three-column human inspection block; grepable `result_1gw` headline.
- **`validate_model_setup_contract`** — `validators.py`. AST gate for the four module-level names and the two helper-form bindings.
- **`validate_override_registry`** — same module. AST gate; the `generic`-frame rule lives in its value check.

## Non-Goals

- The Phase 3 native-*scale-up* projection (`result_1gw_native`). `native` here is overrides-at-design-point-scale, not physics scale-up.
- Any change to the `result_1gw` number, the two-knob mechanism, override provenance/semantics, or the upstream tables.
- Regenerating concepts (Items 10/11) or editing explorer **code** — only Item 10's *spec* is updated here. Shipped concept files keep `result` until regenerated.

## Implementation Notes

- The `native` forward must source `availability`/`lifetime_yr` from the library exactly as `generic_reference` and the `result_1gw` call do — never a literal in the helper. The helper already computes both locals.
- `enabled_overrides(overrides)` is called twice (for `native` and `result_1gw`). Cheap and pure; fine to call twice or bind once — implementation detail.
- `print_cas_breakdown`'s positional call in the prompt grows by one argument (`generic`); keep `result_1gw` the grep target and keep its line first.
- Helper-form AST recognition for `generic = generic_reference(...)`: match a module-level `ast.Assign` whose single target name is `generic` and whose value `_is_call_to_name(value, "generic_reference")`. Mirror the existing `_is_call_to_name(value, "run_native_and_1gw")` check.

## Potential Risks

- **Grep-headline regression.** Reordering the print block could move the `LCOE:` line off first position and break `run_model`'s headline grep. Mitigation: invariant above; the existing test `test_emits_grepable_lcoe_line` guards it — keep it green.
- **Two-forward residue.** A doc or spec left describing `result` re-introduces the misleading contract. Mitigation: acceptance test 6 (`grep` shows no two-forward `result` contract references) is the gate; Appendix C enumerates the surface.
- **Validator over-tightening.** Forbidding all non-`generic` names in relative overrides could reject a legitimate local helper variable. Mitigation: forbid only the known frame names `{native, result_1gw, result}`; leave other runtime names runtime-checked, matching today's permissiveness.
- **`native` numeric drift.** `native` is a newly pinned oracle number; if `override_reference_mw` were omitted it would still be correct (ratio 1.0) but the explicit form must be the tested one. Mitigation: spy test asserts both kwargs on the `native` call.

## Integration Strategy

This item is corrective and lands **before** Item 8 (prompts) and Item 10 (explorer) productionize the contract, so they target three forwards from the start. It modifies shipped Item 7 code (helper return shape, print block, both validators) with small contained edits, updates the design doc/epic, and pre-edits the Item 8/9/10 specs (FR-8). It changes nothing about `result_1gw` or any number the explorer currently reads; the explorer keeps working against still-`result`-bearing shipped files until Item 10 regenerates.

## Validation Approach

- **Unit (helper):** oracle `generic` LCOE ≈ 174.5 (233 MWe, overrides off); `native` newly pinned (overrides on, 233 MWe); `result_1gw` ≈ 584.5 (all-on) — all via the spy/real-model fixtures. Empty registry ⇒ `native == generic`. `P_native==1000` ⇒ `native == result_1gw`.
- **Unit (validators):** contract validator requires `native`; rejects a module still binding only `result`/`result_1gw`. Registry validator accepts `0.70 * generic.costs.cas21`; rejects `native`/`result_1gw`/`result` with a `generic`-naming frame message.
- **Integration:** a hand-written three-forward `model_setup.py` for concept 01 binds all four names and passes `validate_model_setup_contract`.
- **Hygiene:** `grep` finds no two-forward `result` contract language in helper, validators, design doc, epic, or Item 8/9/10 specs (acceptance test 6).

## Next-Stage Handoff

**Fixed (do not revisit in plan):** the three forwards and their call shapes; `generic` mandatory standalone via `generic_reference`; helper returns `(native, result_1gw)` and keeps its name; identifier spelling; `native` passes `override_reference_mw=P_native`; `result_1gw` untouched.

**Open for plan:** exact AST node-match edits in the two validators (Appendix A); the precise test-fixture rewrites (Appendix B); the exact doc/spec line edits (Appendix C). All mechanical.

**De-risk first:** pin the `native` oracle number by running the real model once, then write the helper test against it — everything else keys off that value.

**Next Step:** After approval → `/_my_plan` (or `/_my_implement` for direct execution; this is a contained, mostly-mechanical change).

---

## Appendix A — Validator AST edits (for the plan)

**`validate_model_setup_contract`:**
- `:542` required-name tuple `("model", "result", "result_1gw")` → `("model", "generic", "native", "result_1gw")`; update the `missing` message (drop "explorer reads `result`").
- `:555–567` form classification: the helper tuple to match becomes `native, result_1gw = run_native_and_1gw(...)` (check `"native" in names and "result_1gw" in names` with `_is_call_to_name(value, "run_native_and_1gw")`). Add a separate scan for a `generic = generic_reference(...)` binding; if absent, fail (the contract needs `generic` bound by the helper, not a hand-rolled forward — mirror the strict-helper rationale). Inline form (`:564`) may stay as the non-strict escape hatch or be dropped; recommend keeping it for parity but it now also needs `generic`/`native`. Plan picks.
- `:518–519`, `:574–577` docstrings/messages updated to the three-forward shape.

**`validate_override_registry`:**
- `:742` `if "result_1gw" in referenced:` → `if referenced & {"native", "result_1gw", "result"}:`; message names `generic` as the required reference (acceptance test 3).
- `:662`, `:735–736`, `:746–748`, `:761–762` doc/comment/message text: "native `result`" → "`generic`".

## Appendix B — Test fixture changes (for the plan)

`test_model_setup_helpers.py`:
- Unpack `native, result_1gw = run_native_and_1gw(...)` throughout; rename local `result`→`native`.
- `TestOracle`: add a `generic` assertion (= `generic_reference(...)`, ≈174.5); pin `native` (overrides-on at 233 MWe) — **new oracle number to capture from a real run**; keep `result_1gw` ≈ 584.5.
- `test_empty_overrides_is_library_bare`: assert `native == generic` (both ≈174.5) with `[]`.
- `test_native_call_omits_override_kwargs` (`:152`): **inverts** — the `native` call now *passes* `cost_overrides` and `override_reference_mw=P_native`. Re-author as `test_native_call_passes_overrides`.
- `test_native_equals_projection` (`:201`): unchanged logic (`P_native=1000`), renamed locals.
- `TestPrintCasBreakdown`: call `print_cas_breakdown(generic, native, result_1gw, overrides)`; keep `test_emits_grepable_lcoe_line` green.

`test_validators.py`: contract fixtures bind `model`/`generic`/`native`/`result_1gw`; add a failing fixture that binds only `result`/`result_1gw`. Registry fixtures: accept `generic.costs.cas21`; add rejecting fixtures for `native.*`, `result_1gw.*`, `result.*`.

## Appendix C — FR-8 documentation surface (for the plan)

- **Design doc** `concept-analysis-rework-design.md`: `:104` "four-step"→three-forward framing; `:115–145` inline example gains the `native` forward and renames `result`→`generic`; `:120–124`,`:162` Override Entry references `generic`; `:145`,`:172`,`:188–189`,`:214`,`:221`,`:246–250` module-contract / invariant / edge-case lines drop `result`, add `generic`/`native`.
- **Epic** `epic_concept_analysis_rework.md`: `:34` four-step bullet → three-forward; `:38`,`:48` success criteria naming `result`/`result_1gw` → the three names; `:19` Critical Success Factor (mentions only `result_1gw`, likely fine — verify).
- **Item 8** `concept-rework-prompt-templates/spec.md` + the three prompt template files: `ref`→`generic`, mandatory not optional, Hard Rule 1/5 names, the four-step→three-forward step count.
- **Item 9** `concept-rework-model-critic/spec.md`: critic reads three forwards (`generic`/`native`/`result_1gw`) instead of two.
- **Item 10** `concept-rework-explorer-pilot/spec.md` (+ `design.md`): explorer reads `generic`/`native`/`result_1gw`; drop the `result` requirement and the `result_1gw → result` fallback. **Code** untouched here.
