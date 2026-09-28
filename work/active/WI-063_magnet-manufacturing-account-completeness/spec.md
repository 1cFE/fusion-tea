---
Status: active
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-15
Updated: 2026-09-15
---
# WI-063: Magnet manufacturing account completeness

## Problem and intended use

[NEED] Improve magnet manufacturing-cost completeness and eliminate ambiguous account overlap. The initiating owner request under `work/orchestration/goals/magnet-manufacturing-cost-completeness/goal.md` is the authority. The component estimate must be economically coherent, with source-linked quantities and boundaries; a factory quotation or lower cost is not required.

## Requirements

- R1 [NEED] Map every affected charge by quantity, unit rate, operations included/excluded, price year and evidence. Distinguish complete tape, external cable materials, insulation/impregnation/assembly, winding, electromagnetic supports and nonmagnet infrastructure.
- R2 [NEED] Remove demonstrated overlap without deleting required scope. Uncertain overlap remains explicitly uncertain. Do not add fabrication to an all-in rate or assume stock prices cover manufacturing.
- R3 [NEED] Quantified insulation/cable additions follow current physical construction and geometry. Do not count tape constituents twice or turn geometric clearance into purchased material.
- R4 [NEED] Investigate supported winding effort drivers. Use the simplest defensible relation; preserve unsupported effort as unresolved or clearly labeled sensitivity rather than inventing a cross-section multiplier.
- R5 [NEED] Separate quantity from price uncertainty. Normalize years only with defensible evidence and disclose unresolved bases. Material, fabrication and total subtotals reconcile, with all-in charges distinguished where the source does not support a split.
- R6 [INHERITED] Preserve existing physical inventory, current and fit definitions for cost-only changes. Held design inputs retain the nominal adverse predicates; this item does not qualify buildability.
- R7 [INHERITED] Preserve the nonmagnet budget as an explicit allowance. Preserve source quarantine, native generation, canonical/twin consistency and immutable prior studies.
- R8 [INFERRED] Expose unquantified quantities/operations in the final account record; absent rates must not silently acquire zero-cost meaning. A conditional source-backed material estimate may coexist with unresolved process expense.

## Entry evidence

- `../../orchestration/goals/magnet-manufacturing-cost-completeness/evidence/account-map.md`: current model ownership and uncertainty.
- `../../orchestration/goals/magnet-manufacturing-cost-completeness/evidence/entering-reconciliation.json`: arithmetic identities over the frozen current-margin native baseline.
- `../../orchestration/goals/magnet-manufacturing-cost-completeness/goal.md`: owner constraints and pinned preceding evidence.
- Required reading: `knowledge/holdout/aries-cs/PROTOCOL.md`, `modeling_project/MODELING_PROCESS.md`, applicable modeling patterns and requirements.

## Scope and review selection

[AGENT] One cohesive account improvement. Candidate surfaces are `mfe_winding_pack_cost.sysml`, `mfe_magnet_cost.sysml`, physical part definitions, generic cost assembly, Stellaris configuration, synchronized exploration twins, generated package and affected independent oracle/tests. Actual changes will be selected from T-002 evidence and documented before implementation. New insulation geometry, source/rate interpretations and public interfaces require independent source/math/design review. Shared definitions require consumer enumeration and preserved-input comparisons; integrated accounting changes require a focused independent final assessment. Existing physical source limitations remain explicit.

## Acceptance evidence

- [x] Account map and source/rate decisions resolve every touched term to quantified, assumed or unresolved status.
- [x] Independent source/math/interface review releases the chosen implementation.
- [x] Production model, generated package and independent account identities agree at reference and off-reference points.
- [x] Quantity/rate separability, no duplicate tape constituents, no purchased clearance and unchanged unrelated physical predicates are tested.
- [x] Subtotals reconcile; year and manufacturing-coverage limitations survive into the final answer.
- [x] Applicable native validation and affected consumers checked; independent integrated coverage recorded.

## Preparation notes

2026-09-15 [AGENT]: Native PM registered WI-063. As in prior items, the active spec carries the implementation stage while native PM has no separate activation operation. Research is in flight; source-dependent design and implementation are pending. No model edits authorized by a fabricated evidence assumption.

2026-09-15 [AGENT]: Acceptance evidence is complete for the conditional component account. See audit.md and the independent integrated assessment; unsupported manufacturing and common-year price limits remain explicit. Native status remains active until owner-held closure.
