---
Verdict: fail
Disposition: FINDINGS
Created: 2026-09-27
Related Artifacts:
  Brief: ./final-results-review-brief.md
  Implementation Review: ./implementation-integration-review.md
---

# Final study review: round 1

**FINDINGS. No economic result is released from this study.** [AGENT] Independent review by boundary_review, 2026-09-27. All 2496 proposed native evaluations completed, but the official all-case numerical verifier failed. The preparation and reporting checks below do not override that gate. Preserve this record as failed evidence; any revised proposal requires the declared follow-up process and a new record.

Reviewed record: `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion`. Package executable remains `6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f`; semantic fingerprint remains `bb284160ba12996bc129ba91c1838aed3281d54dc0e729fe03ca02a9d413d6e3`. Existing physical, source, accounting and MR-7 integration coverage remains applicable to that unchanged identity.

## F1 — official numerical verification failed

The stock verifier reports this mismatch for candidate `20260927-design-study-whole-plant-conversion:c2438`, channel `whole_plant_conversion__plant__cryogenic_demand__evaluate__cold_margin_W`:

| Quantity | Value |
|---|---:|
| Native margin W | 0.003072599989536684 |
| Independent margin W | 0.0030725999968126416 |
| Absolute difference W | 7.276e-12 |
| Relative deviation | 2.368e-9 |
| Declared relative tolerance | 1e-9 |
| Declared absolute tolerance | 0 |

The verifier exits 1. Its failure path writes no successful verification summary. The retained [verification log](../../../../../exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/verification.log) supplies the actual tool diagnostic; [execution context](../../../../../exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/execution-context.json) retains the exact command requesting all 2496 cases. A coordinator-authored failure receipt must remain labelled as such.

The mismatch occurs at the deliberately close cryogenic-capacity bracket. Its small absolute size is consistent with cancellation near zero, but it exceeds the declared test and cannot be waived. The first-error verifier output does not establish that this is the only discrepancy; complete discrepancy inspection remains necessary before choosing corrective work. No change to the oracle, tolerances, package or stored result is approved by this review.

Required disposition: retain the failed study, investigate all-case discrepancies, and review the exact next proposal before execution. A wider predeclared capacity bracket could retain the engineering question while avoiding unnecessary proximity to zero. That is a proposal for separate review, not retroactive repair of this record.

## Completed coverage retained for reuse

- **Preparation identity and completeness:** checked frozen hashes, all 2496 unique complete 637-input points, all 2651 aliases and all 3900 oracle scan records. The finite nominal catalog includes 125 gas and 24 steam offers per source at 2500/2800/3000 MW. Both opposing performance scenarios repeat the complete affected catalogs at 2500/2800 MW.
- **Admission and pairing:** checked the partition of 23 shared, 43 gas and 59 steam predicates against conservative input dependencies. No shared predicate depends on an input classified as exclusive to a branch, and no branch predicate requires the opposite branch's exclusive inputs. All 121 ranking scenario/source groups share one common input map before selection.
- **Pruning:** checked all 11735 unchanged-failure proofs and 189 explicit reevaluations in the common-scenario audit, plus 467 proofs and 67 reevaluations in the interaction audit. Separately checked 2168 omitted price/service combinations and 7748 omitted 3000 MW scenario combinations. Where conservative module dependencies included price inputs, inspected the retained equations: quote/service changes do not repair nonpositive export or steam physical-capacity failures. No newly passing offer was identified among those exclusions.
- **Native retention and extraction:** checked all 2496 completed native cases against their frozen complete inputs and executable identity. Every one of the 2651 aliases resolves. Independently reconstructed all 264 reported ranking groups from applicable native predicates and model-owned whole-plant LCOE. Checked 4992 branch power/capital/PV decompositions and the inclusive ±5 USD2025/MWh and ±5 MW reporting classifications. These checks establish extraction consistency, not successful numerical verification.
- **Threshold design:** algebraic-zero and reporting-band scenarios rerank every admitted offer from the gas-favourable performance catalog. Their positive quote path is explicit. Cryogenic brackets retain the selected hardware and zero extra cold watts. No bracket is an empirical uncertainty interval. The failed close bracket remains part of this record.
- **Presentation:** inspected the paired assembly diagram, power budget, cost contributions and preference-gap PNGs, their renderer logic and native channel mapping. Cost figures normalize published PV components by published energy PV and retain the native LCOE headline. Reports use the explicit account mapping rather than incorrect generated CAS tags. Unsupported cases have no winner value. Uncaught catalog edges and unequal steam/Brayton operating freedoms remain disclosed. The inspected renderings remain unreleased products of the failed study.

[Preparation checks](final-results-review/preparation-checks.json) and [native/report checks](final-results-review/native-result-checks.json) retain machine-readable coverage. Their passing statuses have the bounded scopes stated here.

## Evidence identities and stopping point

| Evidence | SHA256 |
|---|---|
| Candidate freeze | `f27a42b08f6f12c2477f04afa952bbcb97de4edaded8ba9004b1018fb1203cbd` |
| Native cases | `d8c376386777e17cca8aa74fcc1b63a4e5fc082b11400d1fc9a41b6698d49292` |
| Inspected native ranking | `5eb8fae96dbb1aca97645ec595d019399ef5496c94fce313f0385ffec0d5d515` |

The integration CANDIDATE and six study preflight gates pass under the declared manifest pin `89acea93750da8794f74883315fb0ff658d6213d0d4b2ffcaf2b1edb320deeae`. Official final verification fails as described above. Final answer/article claims and successful study lifecycle completion are therefore not approved. The unchanged implementation review remains valid; the goal's requested engineering answer remains pending.
