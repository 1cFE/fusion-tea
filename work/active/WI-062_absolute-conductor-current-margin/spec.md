---
Status: active
Scale: standard
Epic: standalone
Owner: agent
Created: 2026-09-15
Updated: 2026-09-15
---
# WI-062: Absolute conductor-current margin

## Problem and intended use

[NEED] Calculate an absolute tape-to-cable critical-current estimate and allowable operating-current margin using the actual modeled conductor inventory. The entering selected-field-envelope predicate does not establish this quantity. This is a bounded engineering estimate, not conductor qualification. Authority: `work/orchestration/goals/absolute-conductor-current-margin/goal.md`, capturing the owner's 2026-09-15 request.

## Requirements

- R1 [NEED] Trace absolute current normalization, tape dimensions, temperature, orientation, electric-field criterion and field applicability to admissible primary evidence. Distinguish measured behavior, interpolation and extrapolation; no normalization inferred from a desired pass.
- R2 [NEED] Derive parallel tape capacity consistently with physical tape procurement and conductor length. Compare conductor turn current, not coil ampere-turns. State continuous-count, current-sharing, cabling and degradation assumptions.
- R3 [NEED] Expose assembly critical current, Iop/Ic, selected allowable fraction, interpretable margin and native feasibility predicate. Unsupported inputs must be explicit, not silently extrapolated or reported as a normal negative margin.
- R4 [NEED] Establish whether inherited reference density and selected-envelope sizing encode allowance; avoid double counting or a pass constructed from the same sizing target.
- R5 [NEED] Demonstrate pass, exact boundary, fail and unsupported cases; coherent current/actual-field/inventory propagation; numerical agreement between native model, generated execution and independent oracle.
- R6 [NEED] Preserve nominal fit failure and geometry. Preserve procurement/fit consistency with shared inventory. Do not resize or optimize for feasibility.
- R7 [NEED] Decide explicitly whether selected-field-envelope predicate remains independent. Report entering nineteen-predicate feasibility, margin result and combined feasibility separately; attribute changes to the entering package, with older studies historical only.
- R8 [NEED] Support a bounded reference/prior-pass and performance/orientation/degradation sensitivity study plus independent review. Report reference failure without tuning and distinguish consistency, evidence-supported estimate and qualification gaps.
- R9 [INHERITED: modeling_project/REQUIREMENTS.md] Preserve library/design separation, traceable quantitative assumptions and executable constraint binding conventions.

## Scope and evidence

Required reading: `knowledge/holdout/aries-cs/PROTOCOL.md`. Source quarantine remains sealed. Detailed stress/strain degradation, quench, full 3D angle mapping and new manufacturing costs remain out of scope. The source assessment is `work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md` when completed. Inventory/interface derivation is `evidence/interface-assessment.md` in the same goal. Entering checkout: `a45925ec066c2403c72c2702e323a965e2666a3c`; entering native reference and 117 oracle controls are retained there.

## Process and affected consumers

[AGENT] One standard item; compact spec, separate design for scientific/interface review and a short persistent execution checklist. Independent source/math/interface release precedes production edits. Reuse the same fresh reviewer for integrated evidence. Affected surfaces: MFE magnet library definitions/bindings, stellarator parameters/predicate and canonical twin, generated package, oracle, manifest/census, study and model tests. IFE foundation behavior is preserved. Do not repair general integration/research seams within this item.

## Verification plan

[AGENT] Focused analytic identities and boundary/domain tests, native reference and perturbed evaluations, canonical/twin consistency, fresh generation repeatability and sealed metadata, applicable six-level validation with actual failures disclosed, affected consumers and independent audit. The goal coordinator owns integration and study after item evidence; model implementation must supply all necessary public channels and oracle mapping. Full original scalar/reference verdict comparisons use entering controls.
