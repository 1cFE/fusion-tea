# Round 1 assurance and independent R2c.P grade

2026-09-18. Grader: independent non-author `/root/method_review`. **PASS for the accurately bounded research round; goal unmet; OWNER_GATE remains.** This review does not select the physical target or authorize goal closure.

## Current grade

| Field | Assessment |
|---|---|
| cell_id | R2c.P |
| rubric_version | `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d` |
| model_version | `e78099cb93ab36b57debf70045cc9c4e7bcfcdd8`; no working-tree diff in `models/` or the generated package |
| score | **1** |
| anchor_satisfied | “Thickness, lifetime, or TBR held as cited values” — the TBR branch |
| model_evidence | `models/designs/stellarator_09/stellarator_plant.sysml:597` holds 1.074; `:1753` holds floor 1.05; `:1782` binds held breeding into the predicate; `models/library/structure/mfe_plant_systems.sysml:283` passes it to fuel accounting |
| runtime_evidence | Static generated evidence: `exploration/stellarator_e2e/generated/schemas/stellarator_plant_params.py:26` exposes breeding as input; `modules/constraints/predicates.py:129` compares operands. No new plant execution or package-identity claim is made |
| study_evidence | None added; source-domain research probe is not a plant study |
| why_not_next | Achieved breeding is not computed from the retained blanket configuration |

**P2 not met:** exact anchor is “2c: TBR computed from blanket configuration.” The independently recovered network computes another assembly's response outside the plant package; current blanket thickness/material choices still do not derive achieved TBR.

**P3 not met:** exact anchor is “2c: computed TBR vs floor pushes back on blanket/build choices.” The existing comparison uses held production. Conditional required-breeding arithmetic neither computes production nor makes production respond to build choices. There is no grade advancement from this round.

## Round assurance

I read Round 1's trail result, native report `knowledge/research/pending/20260918-130310_computed-tritium-breeding-methods.md`, both native request returns, pinned rubric Row 2 and grading protocol, and the current model/generated consumers above. Original-page inspections and executable checks are explicitly reused from `method-review.md`; this is continuing independent coverage, not a second independent reviewer.

T-001's no-model-edit scope was respected. Native requests registered three sources. The first reached its capture bound and retained a failed URL receipt; successful local-PDF registration recovered that acquisition. The second request investigated a specific newly found thesis. This is acquisition recovery and bounded follow-up, not a semantic retry that overrides an adverse scientific finding. The trail discloses unpinned research evidence and promotes no model pin or study result.

The probe accurately executes the published example. Independent original-C++ comparison is now reproducible through `evidence/verify_hcll_original_cpp.py`, with retained results in `evidence/hcll-original-cpp-verification.json`. All arrays match the original and five outputs agree within 2.3e-16. The final-module reference discrepancy remains disclosed. The final network's error statistics are not established for the example network; its corrected result is an arithmetic diagnostic, not qualified uncertainty. Source-domain code agreement and the thesis's tokamak transport comparison do not validate stellarator transfer.

## Accepted learning and remaining work

Accept both proposed learnings: an executable, material-sensitive HCLL surrogate exists but excludes current geometry; a held-floor pass does not establish fuel self-sufficiency under unresolved recovery semantics. These are bounded evidence statements, not owner-approved design decisions or promoted domain insights.

Remaining work is explicit assembly definition, an applicable calculation and independent checks, physical recovery/extraction assumptions, plant bindings and executable verification, then evidence that computed breeding constrains design. The pending physical-target decision legitimately stops dependent integration. No evidence supports declaring the goal achieved or claiming that a suitable method is impossible.
