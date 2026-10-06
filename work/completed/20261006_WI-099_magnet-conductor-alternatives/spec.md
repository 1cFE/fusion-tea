---
Status: completed
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-29
Updated: '2026-10-06'
---

# WI-099: magnet conductor alternatives at matched duty

## Purpose

Add genuinely different, source-cited REBCO and Nb₃Sn conductor definitions and the winding, cryogenic and cost calculations needed to compare supplied windings of both materials at the same magnetic duty, in an isolated package, without changing any existing model, package or study. Authority: goal `work/orchestration/goals/magnet-material-comparison/` (brief `evidence/owner-brief.md`, owner-ratified 2026-09-29). Governing contract: `work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md` (r3, released). Design: `design.md` in this directory (independently reviewed; review record `…/evidence/contract-review.md`).

## Requirements

| ID | Requirement and provenance | Acceptance evidence |
|---|---|---|
| R1 | [NEED] Two conductor definitions with their own properties, equations, temperatures and validity domains (Nb₃Sn ITER-form strand law; REBCO measured 20 K field shape with exponential temperature law), not changed inputs to one law. Brief § Engineering question. | Library definitions as in design § 2.1–2.2; source-point tests with contract § 5 tolerances. |
| R2 | [NEED] Evaluate supplied windings at a supplied matched duty for current margin, fit, cold load, staged refrigeration and subsystem cost. Brief § Model and study requirements. | Design § 2.3–2.8 executed through the generated package; baseline result. |
| R3 | [INHERITED: MR-7] Turns, element counts, construction areas, temperatures and installed refrigerator capacity are supplied; requirements are calculated and compared; nothing is resized; inventory and cost follow the supplied design; unsupported domains are reported as unsupported. | Design § 4 role record; MR-7 tests: insufficient/sufficient pairs for acceptance, fit, copper, steel and capacity; field varied with hardware fixed; hardware-isolation tests; unsupported case per conductor with no ranking; reference-offer margins ≥ 0. |
| R4 | [INHERITED: MR-3, MR-4] Concept-agnostic library; concept values in the design; every quantitative value cited to a repository source path with Source/Reference/Basis, agent choices and bounded assumptions labelled. | Review of the two SysML files; citations resolve. |
| R5 | [NEED] Preserve existing reference behavior and historical packages and studies. Brief § Model and study requirements. | Only new paths in `git status`; Stellaris and component-alternatives package fingerprints unchanged. |
| R6 | [NEED] Independent numerical check of the implementation. Brief § Model and study requirements (“a calculation reproducing its own formula is not sufficient validation”). | Independent oracle (separate author, contract and design only) agreeing to relative 1e−9 across the study's cases; source-point tests against originals. |

## Scope and stage status

[AGENT] Implemented and independently checked within the declared subsystem scope; formal item closure remains with the owner. Spec and design are combined with the goal's reviewed contract; a separate plan document adds nothing because implementation is one package build with a fixed test list. Design corrections and rechecks, implementation and oracle, sealed 2,310-case numerical study, and independent final interpretation review are recorded in the goal's T-005/T-007/T-008 returns and Round 1 review, with `evidence/final-review.md` and the sealed `20260929-magnet-material-comparison` record. T-010 resolves the earlier missing stock oracle-entry/manifest seam with five acceptance tests. R1–R6 evidence and remaining conditional scientific scope are indexed in the goal's `evidence/pr-readiness/tracking-audit.md`. This item owns model meaning and executable checks; the goal's native study owns exploration and reporting.

## Reference case

`reference-case.json` in this directory supplies the design file's default values (anchor D, 10 T, reference offers). All values are overridable case inputs.
