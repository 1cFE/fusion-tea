---
Status: active
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-30
Updated: 2026-09-30
---

# WI-100: plant-level conductor material variants on the Stellaris plant

## Purpose

Let the Stellaris plant model evaluate a supplied Nb₃Sn winding at 4.5 K and a supplied REBCO winding at 20 K (Round 1's conductor definitions, WI-099) as selectable magnet-system variants, with temperature-staged refrigeration, a supplied element count, a pack-area check, and a slot for the pack-size peak-field term, inside an isolated derived package that leaves `exploration/stellarator_e2e` and the Stellaris design file byte-identical and reproduces the current pin bit-for-bit under the reference selection. Authority: goal `work/orchestration/goals/magnet-material-comparison/` Round 2 (owner brief `evidence/owner-brief-round2.md`; goal.md Amendments 1–2). Governing contract: `evidence/plant-contract.md` (r2, under recheck). Evidence: `evidence/plant-chain-audit.md` § 2, § 4, § 6. Design: `design.md` in this directory (fresh modeler; fresh review).

## Requirements

| ID | Requirement and provenance | Acceptance evidence |
|---|---|---|
| R1 | [NEED] Two magnet-system variants (`'Nb3Sn Magnet System'`, `'Round1 REBCO Magnet System'`) selectable by retyping in an isolated design file, each using the WI-099 conductor law, turn-area screen, inventory-and-cost and cold-load calcs at its own supply temperature, with the supplied element count and a new `pack_area_ok` check. Brief § Scope and approach; contract §§ 4, 9. | Design § 2–3; variant instances execute through the generated package; retyping is the only selection mechanism. |
| R2 | [NEED] A staged cryoplant variant carrying Round 1's cold-load and refrigeration laws for both materials, feeding the plant's recirculating power where the plant's cryo electricity enters today. Contract § 6. | Design binding table; power-balance channel identity under the reference selection. |
| R3 | [NEED] A pack-size slot on the peak-field calc (`a1_ratio`, `A_wp`, `A_wp_ref`) that is exactly 1.0 at its default, plus entry points for `peak_ratio`, `f_ren`, `beta_limit`, `B_max`, and every contract § 5 supplied quantity (turns, turn current, pack side, allocation, casing interior, structure mass, installed heating, cryo ratings, package ratings and purchase costs, power classes, conductor prices). Contract §§ 3, 5. | Design § 6 interface table with entry keys; route acceptance of every key. |
| R4 | [INHERITED: MR-7] Every quantity the contract's policy proposes is supplied; requirements are calculated and checked; nothing is resized; unsupported conductor status is reported, never pass/fail; `B_max` is an envelope flag, not a limit. | Design § 4 role table; tests: insufficient/sufficient supplied designs for acceptance, pack area, fit, capacity; unsupported case per conductor with status only. |
| R5 | [NEED] Preservation: the reference-selection instance reproduces the current `stellarator_e2e` pin's 1,352 outputs and 67 verdicts bit-for-bit; `exploration/stellarator_e2e/**` and `models/designs/stellarator_09/stellarator_plant.sysml` are byte-identical; shared-library edits are value-neutral (WI-080 `enabled`/`evaluation_defined` pattern; `default` promotions per WI-057 D5). Brief § Scope; goal invariant "Package". | Regression comparison in the build receipts; `git diff --stat` on the protected paths empty. |
| R6 | [INHERITED: MR-3, MR-4] Concept-agnostic library additions outside the canonical `mfe_*` tree; every new quantity cited with Source/Reference/Basis; agent choices and bounded assumptions labelled. | Review of the SysML files; citations resolve. |
| R7 | [NEED] Independent verification: the existing plant oracles for unchanged channels, WI-099's oracle for the magnet channels, and a new independent oracle (separate author) for the variant bindings, `pack_area_ok`, staged cryo insertion, the pack-arm slot and the structure-mass rule; policy acceptance tests. Contract § 9. | Oracle agreement at 1e−9 across the study's cases; source-point tests. |

## Scope and stage status

[AGENT] Spec and design are combined with the goal's plant contract; implementation, oracle and policy are delegated under goal tasks with briefs in the goal's `evidence/briefs/`. This item owns model meaning and executable checks; the goal's native study owns exploration and reporting. Formal item closure remains with the owner.
