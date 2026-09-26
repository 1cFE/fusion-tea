# Findings log

[AGENT] Goal-owned audit/design findings. These are not native study discovery IDs; none is invented for a study that has not run.

| ID | Finding | Disposition and evidence |
|---|---|---|
| F-01 | Equal MW does not establish equal thermal interfaces; steam reads a fixed salt supply while Brayton uses finite primary-stream stages. | Select isolated supplied-source boundary; compatibility map and three audit files. |
| F-02 | Original C-1 needs about 31% bypass, while the retained matched point has a numerical bypass near 1e-6; bypass hardware/losses are omitted. | Retain controls, require matched active exchanger duty/return in WI-096; readiness B0/B1. |
| F-03 | Steam lower-temperature operation changes offered-condition verdicts; changing salt temperature alone breaks the heat join. | Keep inherited rated states for duty/circuit comparison; readiness S1/S2/S3. |
| F-04 | Fixed fully active steam IHX area with four fixed terminal temperatures implies one duty; arbitrary duty variation needs control. | Replace 80/90/100% proposal with independent 10/11/12 circuit offers whose matched duties are consequences; WI-096 design. |
| F-05 | Brayton outlet conditioning and water balance alone do not prove finite cooler heat transfer. | Proposed actual-terminal, finite-UA water-flow closure and independently selected capacity tests; fresh feasibility review and WI-096 design. |
| F-06 | Early audit reading suggested SG/reheater omission; later WI-079 record explicitly includes represented children in the aggregate. | Corrected steam/cost audit; preserve inclusive offer and avoid duplicate purchases. |
| F-07 | Captured steam dollar year was unspecified in WI-079; original coefficient code now supplies a USD2025 label. | Monetary-basis.md records exact match, source-declared year and unverified historical escalation; existing CPI rawHTML supports purchasing-power mapping of USD2004 offers. |
| F-08 | Equipment/account prices and recurring costs remain assumptions with incomplete empirical support. | Explicit disjoint hypothetical offers, sensitivity and correction frontier; no unconditional procurement recommendation. |
| F-09 | A source balance and passing implemented checks do not establish detailed generator cooling, site or machine-map qualification. | Separate conditional model performance from scientific qualification in all results. |
| F-10 | Source duties below nominal do not establish original-loop consistency; return temperature changes with heat. | Diagnostic unchanged-loop/independent-NTU checks support three source matches; actual topology hydraulics remain an imposed-resistance assumption. |
| F-11 | The proposed external source-heat and ratio solves enforce physical closure outside the model, contrary to STUDY_POLICY §§3 and 5.3. | Final review FINDINGS; two-revision cap reached; implementation and main study stopped for owner decision. Earlier policy reading missed this conflict. |
| F-12 | Internalizing source, ratio and finite-water closures as separate new handwritten solves would trigger STUDY_POLICY §4's third-rung limit. | Record exact design-scope dependency; any permitted continuation must resolve it before implementation. This is not a demonstrated major-physics blocker. |

## Failed attempts and process corrections

- An initial file replacement patch was rejected by the editing tool before applying any changes; the template copies were then filled directly. No native model attempt occurred.
- Initial Git staging failed because the sandbox makes `.git` read-only. The host approved explicit-path Git operations; commits 19c60ae6 and 55eb24b8 contain only this goal's work and its WI-096 registration.
- Native registration preceded the T-002 start entry; the trail records the ordering deviation. No implementation preceded design review.
- Readiness S1 and S3 are expected physical/interface refusals. They were retained and not retried; no mechanical retry allowance was consumed.
