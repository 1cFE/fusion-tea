# Independent implementation and study-release review

Reviewer: continuing non-author `/root/feasibility_review`. This is the substantive integration check required by the fourth design verdict. Do not repeat source/design checks whose exact premises remain valid. Review the implemented bindings, evidence and study framing against that verdict.

## Authority and stop rule

The owner authorized exactly one additional design submission; it passed. No fifth design submission, policy waiver, silent equipment sizing or major new physical model is authorized. MR-7 still applies. Source heat, compressor ratios and installed equipment remain chosen inputs. Bypass fraction and cooler water flow are calculated operating controls under the reviewed rationale; recuperator effectiveness follows supplied UA and flow.

If an implementation defect can be corrected faithfully within the reviewed design, identify the exact defect. If the implemented model needs another scientific premise, physical solve, major extension or policy exception, identify the unresolved requirement and stop dependent execution. Formal goal/item closure remains owner-held.

## Entry evidence

- `work/active/WI-096_matched-conversion-subsystems/spec.md`, `design.md`, `plan.md` and `report.md`.
- Your `evidence/design-review-fourth-submission.md`; exact reviewed design hash `ec7d08e01ec0702e33ac6589dfaaa1a4eec5edad565c5be7bf9dc22c92c03f91` and spec hash `b7e021efe1c9bca12431879c5eddc541966469ef0a824283ee3629a65c78068c`.
- `models/designs/component_alternatives/plant.sysml`, the two new analysis definitions, `exploration/component_alternatives/build.py`, its five addition/variant bodies and its reuse evidence.
- Development receipts under WI-096 `evidence/`, including the retained first execution with omitted Boolean guards, corrected guard census and explicit undersized/type-failure controls. Do not accept a passing baseline as complete constraint coverage.
- The generated model/package contracts, pipeline, snapshot and census; package-owned `verify.py`, `oracle_*.py`, retained property data and oracle provenance.
- `exploration/component_alternatives/studies/{ANNEX.md,declare_axes.py,proposals.py,prepare_interface.py,oracle_entry.py,study_route.py,execute_study.py}` and draft `20260926-design-study-component-alternatives/study-plan.md`.

## Questions

1. Does the actual model preserve each reviewed choice and implement all required coupled calculations internally? Inspect both source joins, actual failed-duty propagation, the salt shaft-heat treatment, gas recuperator and cooler bindings, controller capacities and source-return requirements.
2. Do the emitted and executing constraints cover the intended source, machine, pump, property, controller and accounting checks? Check their operands and at least the omitted-guard regression, insufficient source, insufficient controller and cooler no-root cases.
3. Are the energy and financial ledgers complete within the declared boundary, with no duplicate recovered work, omitted load or overlapping replacement base? Confirm chosen quote/rating independence, currency conversion and treatment of unknown scope corrections.
4. Does independent verification actually cover the physical outputs and all predicate operands at the policy's tolerance? Identify shared property/source assumptions and any value identical by construction. Reuse your earlier independent NTU/profile checks where unchanged, and inspect new native evidence.
5. Does the complete implementation remain within the reviewed five-body/one-new-iterative-calculation scope? Distinguish helper packaging, generated checks and translated existing equations from substantive physical additions.
6. Is the proposed direct catalog and sensitivity study faithful to the owner? Both selected steam connecting hardware and Brayton offers must get their declared opportunity; failed cases stay visible. No source/ratio search, purchased-equipment sizing, claim of equally optimized technologies or whole-plant LCOE may enter through study preparation.

The native integration seam remains an executable gate after your substantive review. It establishes package lineage and native readiness; it does not substitute for the questions above. The exact interface/manifest and corrected development report will be named at dispatch so you can distinguish finished evidence from files still being written.

## Ownership and return

You are not alone in this workspace. Read model/package/study files; do not change the author's implementation or coordinator's records. Own only `evidence/implementation-integration-review.md` in this goal directory. Preserve other agents' work.

This review spans coupled source, steam, Brayton and accounting behavior, so the normal short review budget is expanded as needed to inspect original evidence and run focused independent checks. Avoid another broad source audit. Return PASS or FINDINGS with exact blocking requirements, evidence paths and remaining claim limits. Keep the chat return concise; the artifact carries the audit. The same reviewer rechecks corrective implementation diffs.
