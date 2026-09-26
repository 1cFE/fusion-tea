---
Status: completed
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-26
Updated: '2026-09-26'
---

# WI-095: Loop return control

## Problem and intended use

The 'Primary Coolant Loop' definition holds the blanket inlet and states that the exchanger must return the helium to the circulator at `T_comp_in`; the assemblies that couple it to the ARIES closure (WI-093 C-1, WI-094 costed) never check that requirement, and no executed case satisfies it (goal design-study-parameters, `evidence/return-condition-check.md`: 48.8 K at the C-1 design point, 0.70–13.6 K at the study's leading passing points). This item makes the requirement explicit in the calculation and the checks by modeling the control that holds it, so that the goal's comparison can be recomputed on cases that satisfy the completed loop model (owner direction of 2026-09-26, `work/orchestration/goals/design-study-parameters/evidence/owner-direction-round3.md`).

## Requirements

- R1 [NEED, direction 1–2] One additive calculation models an explicit primary-side bypass control: the fraction of loop flow routed around the exchanger such that the exchanger, at the loop's delivery temperature and reduced primary flow, transfers exactly the delivered duty, and the mixed return equals the loop's required return `T_comp_in`; the exchanger's performance at reduced flow is the closure's own counterflow effectiveness-NTU form, so the bypass's effect on the exchanger is computed, not assumed.
- R2 [NEED, direction 2] Two checks enforce the relationship: the mixed return equals the required return within a root-solve tolerance (1e-6 K), never a physical allowance; the bypass fraction lies within a chosen maximum (declared 1.0 until the owner sets a design limit). Infeasibility (the exchanger cannot transfer the duty even fully open) reports the physical deficit and fails the check.
- R3 [NEED, MR-7] Flow, ratio, ratings and area stay chosen inputs; the bypass fraction is a calculated control setting from the stated requirement; the maximum bypass and the tolerance are declared inputs with their grades; nothing is sized from a demand; the new parts read only existing outputs so every existing channel of the WI-094 development receipts replays bit-exactly (the pre-change control).
- R4 [NEED, direction 1] The alternative arrangement, consistent operating settings on the cycle side, is representable on the same package as the family of points where the bypass fraction is zero; the goal's study executes that family natively.
- R5 [NEED, MR-3, MR-4] The definitions are concept-agnostic and live in a new library file; every value carries its source and grade; no shared library file, completion body, live package or the WI-094 package's reviewed bodies change (the goal's coordination invariant).
- R6 [INFERRED] The package carries the study tooling on the new identity (interface record, oracle coverage of the new channels, manifest re-pin, seam CANDIDATE) so the goal's round-3 study can run.

## Scope and limits

The bypass's own pressure loss, valve hardware and cost are not modeled (disclosed). The loop's flow and rise stay the definition's (heat-driven, held inlet). No blanket thermal-hydraulic model. The S6 exchanger alternative is a labelled inventory, not a resize.

## References

Goal `design-study-parameters` trail (round 3); `mfe_primary_loop.sysml` doc ("T_comp_in is what the IHX must deliver, not evidence that it can"); the closure body `network_heat_driven_closure_impl.py` (stage arithmetic); MR-7.
