---
Status: active
Created: 2026-09-13
Updated: 2026-09-13
Related Artifacts: spec.md, design.md, basis.md
---

# WI-040 implementation plan

- [x] Verify corrected source composition, research parameter/accounting basis, and retain entering baseline and regression evidence (659 passed/13 inherited skips; `baseline-before.json`, `evidence/baseline-model-tests.xml`).
- [x] Implement the two normative calculation contracts and typed completions, canonical physical bindings and initial parameter values; expose geometric winding volume and legacy comparison. Source locators verified; corrected generated tuple ordering and exposed literal price/escalation inputs. All 137 new component/public tests pass.
- [x] Synchronize family twins, generate coherently with all normative seeds, update current oracle and public mappings, recapture snapshot/census/manifest and refresh derived indicator fixtures. Exact fresh equality with 13 preserved and two new seeds; 263 inputs, 174 outputs. Historical artifacts preserved through a current boundary adapter; final metadata recapture follows the source-citation correction.
- [ ] Verify local domain/identity tests and public perturbations, reconcile baseline and off-reference changes, run affected model/study regressions and all applicable validation levels. Record inherited diagnostics by identity.
- [ ] Obtain positive independent native audit and address its findings; leave item close/archive owner-held. Integrate through a separately scoped goal task.

## Verification mapping

| Outcome | Check and expected observation | Basis | Evidence |
|---|---|---|---|
| MR-WI040-1/3 | Image/vendor/NIST/code values; independently calculated masses and prices with declared rounding | research reports and design parameter table | 137 kept component/public tests pass; audit checking original sources |
| MR-WI040-2/4 | Additive procurement/fabrication identities; volume and individual-price perturbations; tape price leaves fabrication unchanged | PROCESS additive form and mass identity | test_winding_pack_cost.py public perturbations pass |
| MR-WI040-5 | Extra cold volume changes cryo output without changing pack material inventory | physical component boundary | test_winding_pack_cost.py extra-volume test passes |
| MR-WI040-6 | Existing physics/verdicts equal at unchanged inputs; cost changes follow the new account through downstream totals | entering baseline and dependency graph | baseline-reconciliation.json: 142 exact unchanged, 16 explained economic changes, 18 unchanged verdicts; R14 native/direct checks pass |
| MR-WI040-7/9 | Exact family twins, named ownership, generated-interface coherence and current oracle parity | AD-008 and native integration contract | exact fresh generation; 158 baseline oracle comparisons; model suite 809/13; independent audit and final consumer checks in progress |
| MR-WI040-8 | Invalid fractions, density, price, state and winding inputs refuse deliberately; finite valid extremes retain identities | design domains | kept component/public domain tests pass |

## Ownership

Coordinator owns goal trail, shared registries, package generation, metadata and final integration. Canonical model and manual-completion authoring may be delegated with the design's exact ABI. Oracle/tests consumer work may be delegated independently after that ABI is fixed. Workers preserve each other's changes; package generation remains sequential.
