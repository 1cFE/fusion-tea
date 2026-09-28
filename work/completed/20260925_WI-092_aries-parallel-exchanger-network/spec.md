---
Status: completed
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-25
Updated: '2026-09-25'
---

# ARIES parallel exchanger network alternative

## Problem and intended use

The integrated ARIES assembly closes its thermal cycle with `Heat Driven Closure`, which passes the whole cycle helium flow in series through the blanket-helium, divertor-helium and PbLi exchangers. The published network (Raffray Fig. 12, retained image `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p736.png`) is a series blanket-helium stage followed by parallel PbLi and divertor-helium stages that rejoin before the turbine. Round 1 of goal `aries-reference-heat-electricity-reconciliation` established that the source-conditioned case's unremoved heat is entirely a PbLi-stage limit produced by the series order and the PbLi capacity rate (`work/orchestration/goals/aries-reference-heat-electricity-reconciliation/learnings.md` L-001). This item adds the published arrangement as an explicit alternative so the goal can evaluate a revised source-conditioned reference case. Consumer: that goal's round 2 and its answer. Scientific qualification of exchangers, hydraulics and materials remains outside scope.

## Requirements

| ID | Requirement and provenance | Observable acceptance |
|---|---|---|
| R1 | [NEED] Represent the published series-then-parallel network as an explicit alternative closure selectable per case. Source: owner brief § Work to pursue item 2 ("Compare the implemented sequential exchangers with the published network … An architecture correction is permitted and must be reviewed before implementation"), `evidence/owner-brief.md`. | In network mode 1 the generated graph publishes per-stage transferred/unmet heat, stream outlet temperatures for the PbLi and divertor streams, the mixed outlet, and the same turbine, recuperator and ledger channels as before; the helium stage sees the whole flow, the PbLi and divertor stages see the split flows from the helium-stage outlet. |
| R2 | [NEED] Retain the original failing case verbatim and evaluable. Source: owner brief ("Retain the original failing case"; goal invariants). | With network mode 0 (the default) every one of the four canonical cases and the 27 points sealed at `581e3c1a` reproduces all 546 numeric outputs at relative 1e-12 or better and all 14 verdicts exactly; the only public-input change is two added keys with defaults. |
| R3 | [INHERITED] MR-7: the split fraction is a supplied operating choice; no other quantity changes role; hardware stays chosen and demand calculated. Source: `modeling_project/REQUIREMENTS.md` MR-7; goal invariants. | The design's role table lists every affected quantity; at fixed hardware the split is a direction test: a smaller split leaves more PbLi heat unremoved, a split near one leaves divertor heat unremoved, and no split resizes anything (the PbLi heat is not fully transferred at the C3 inputs in any mode because the PbLi primary capacity rate and the helium-stage bound limit it); no UA, flow, rating or bound is derived from demand; the selected hardware is unchanged between the pair. |
| R4 | [NEED] Preserve Stellaris, shared definitions, frozen records and the predecessor sealed packages. Source: owner brief § Preservation; goal invariants. | Goal preservation manifest (18,725 files) unchanged; isolated Stellaris replay exact; no edit to any file owned by the MFE/IFE families; frozen study directories untouched. |
| R5 | [NEED] Every advertised output comes from the generated native graph; the package is regenerated on the stock route with a fixed point, the live study manifest re-pinned, and the integration seam returns one CANDIDATE. Source: owner brief § Studies and engineering discipline; MR-4/MR-7. | Build receipts show fixed-point regeneration; a machine-readable migration report lists the two new keys; `scripts/integrate.py` returns `CANDIDATE` with the new fingerprints. |
| R6 | [INFERRED] The bounded closure remains a strictly monotone root problem in network mode 1, with bracket, residual and iteration count exposed and runtime refusals retained. Basis: R1 and the WI-089 closure contract. | The completion asserts the bracket signs, converges within the existing caps, exposes residual and iterations, and refuses a split outside (0, 1). |

## Scope and limits

Additive: one new calc definition and completion in `models/library/analyses/integrated_heat_electricity.sysml` (an ARIES-only file), the assembly's `heat_exchangers` part rebound to it with two new supplied attributes, regenerated package, re-pinned manifest. The reviewed `Heat Driven Closure` definition stays in the library for the frozen packages and traceability; its equations are copied into mode 0 of the new definition and disclosed as a copy. No change to `dual_circuit_heat_accounting`, `ideal_gas_brayton_components`, the electrical balance, the ledger, equipment or cost definitions. No pressure-loss model for the parallel branches, no mixing loss beyond adiabatic enthalpy mixing, no control law for the split, no resizing. The resized-compressor alternative is a study input, not a model change.

## References

Goal `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/` (goal.md, trail.md round 2, evidence/reference-case-contract.md § 4, evidence/parallel-network-scratch.py); `work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md` § Heat-driven recuperated cycle; `exploration/aries_integrated/native_completions/heat_driven_closure_impl.py`.
