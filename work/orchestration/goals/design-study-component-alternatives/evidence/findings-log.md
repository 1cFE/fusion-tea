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

## F-013 — Reviewed implementation completed within the bounded extension

[AGENT] The fourth design passed independent review. Five substantive bodies include one new iterative finite-water-cooler family; primary loop/network/bypass algorithms remain reused. The isolated package keeps 490 chosen inputs, 876 scalar outputs and 84 executing checks. The independent implementation review accepted numerical/predicate development evidence and the explicit static-diagnostic disposition. Ten stock integration gates passed. Home: WI-096 report and goal `evidence/implementation-integration-review.md`.

## F-014 — Broad native study fails numerical verification

[AGENT] All 498 cases execute; 83 satisfy every native engineering predicate. Six cases exceed unchanged numerical comparison tolerances, including two otherwise-passing efficiency sensitivities. Every independent predicate agrees. Independent review confirms native cooler stopping error near small water temperature rise; no oracle error was demonstrated. Disposition: stop, retain failed evidence, no new model identity or tolerance authority. Home: `evidence/verification-failure-review.md` and native study `results/verification-diagnostics.json`.

## F-015 — Connecting equipment affects conditional comparisons

[AGENT] Unreleased native outputs show that choosing steam exchanger/pump offers instead of retaining all 14 circuits changes the lower-duty cost comparison. Finite catalog results and hypothetical price sensitivities do not establish an unconditional winner. Disposition: retain as diagnostic reading with the verification block, materiality and qualification limits explicit. Home: `evidence/matched-results-draft.md` and complete plot data.

## F-016 — Bounded repair verifies the complete unchanged catalog

[AGENT] Owner authorized the numerical continuation. Independent diagnosis identified four cooler-root defects and two gas cases dominated by heater-root propagation plus smaller local bypass error. Three goal-local numerical variants now resolve the existing bisection brackets to adjacent floating-point endpoints. The oracle, tolerances, equations, physical domain, variable roles and offers are unchanged. Independent repair review passes15 assembled regressions and nine high-precision checks. Fresh integration passes all ten gates; full stock verification passes498 cases ×872 scalars ×84 predicates. All original input maps and engineering verdicts are unchanged. Home: WI-096 numerical-repair report, goal numerical-repair review and repaired study `results/verification_summary.json`/`replay-comparison.json`. Final economic assurance follows separately.
