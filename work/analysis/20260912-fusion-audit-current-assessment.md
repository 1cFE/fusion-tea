# Current F01–F20 assessment

**Date:** 2026-09-12. **Production revision assessed:** `ab66658c`. **Original audit:** `.project/reports/20260907-fusion-model-audit.md@e341dc34`, against its older `b244abd8` model. **Native task:** fusion-audit-remediation Round 6, T-028 (`trail.md@bb06e349`). **Authority:** all classifications and recommendations are [AGENT]. Owner-originated requirements and reserved decisions remain in `work/orchestration/goals/fusion-audit-remediation/goal.md`; this report accepts no residual and changes no supported scope.

## Assessment

The goal is not answered. Five original defects have bounded audited correction evidence: F01–F04 and F06. F05, F12–F13 and F15–F18 have partial repair or improved evidence, with unresolved subissues. F07–F11, F14 and F19–F20 remain open. This is a per-finding assessment, not a claim that all repaired model behavior is independently physically validated.

The remaining work includes concrete mathematical and documentation defects that can be corrected without changing scientific assumptions, plus accounting, financial, domain and engineering questions that require additional evidence or owner decisions. A written caution does not make an invalid input impossible or satisfy the goal’s requirement for enforceable limits. No residual has received owner acceptance in this goal.

The final allowed round supplies this evidence assessment. It cannot supply an automatic seventh round or close the goal. Recommendation: re-ground further remediation around these specific residuals; do not certify the existing answer contract complete.

## Scope and evidence method

This is the aspect-focused native analyze-models workflow. It compares every original finding and distinct subissue to current model/code and retained native evidence. It is not a new all-parameter source audit. Two parallel readers examined F01–F07 and F12–F16; the round agent inspected F08–F11/F17–F20 and synthesized the result. A separate fresh round review follows this report.

Evidence notes carry exact current code locations, certificate commits, residual effects and next homes:

- [F01–F07](../orchestration/goals/fusion-audit-remediation/evidence/T-028_assessment/f01-f07.md): source, dependency, power, financial-domain and radius defects.
- [F08–F11 and F17–F20](../orchestration/goals/fusion-audit-remediation/evidence/T-028_assessment/f08-f11-f17-f20.md): accounting, comparisons, reuse, citations and documentation.
- [F12–F16](../orchestration/goals/fusion-audit-remediation/evidence/T-028_assessment/f12-f16.md): lifecycle, thermal closure, engineering breadth and validation.

“Bounded correction” means the identified original defect has specific native repair and independent audit evidence. “Partial” means some subissues moved but the finding is not discharged. “Open” means the finding’s material defect remains. Neither a research route nor an unaccepted use restriction is counted as resolution. Detailed notes distinguish code-enforced guards from documentary limits and proposed restrictions.

## Current finding dispositions

| Finding | Assessment | Demonstrated change and remaining obligation | Concrete next home / decision |
|---|---|---|---|
| F01 source transcription | Bounded correction | WI-048 corrects the image-checked Osiris facts and keeps the rounded historical reference distinct from the computed plant. Later assumptions do not become source facts. | WI-048 independent re-audit and operating-point record; retain their applicability limits. |
| F02 IFE dependencies | Bounded correction | One beam/efficiency/rate chain derives bank energy and priced thermal/net power. Original disconnected controls are covered by audit and ordinary study interventions. | WI-048 and the current IFE study consumer; no general engineering envelope follows. |
| F03 net generation | Bounded correction | Strict computed-net assertion and generating indicators guard both price consumers. Driver-only and total parasitic outputs are distinguishable; compatibility alias remains documented. | WI-048 independent negative-net checks and native study exclusions. |
| F04 operating heating | Bounded correction | WI-050 separates operating demand from installed procurement/capacity. Audited direct controls and the demand/reserve study support the change. | WI-050 and operating-heating synthesis; retain invalid negative-demand and unproved full-plant exact-zero limits. |
| F05 financial domains | Partial | IFE zero/near-zero PV factors repaired and audited. MFE equal-rate annuity, DCF, IDC and held-mode replacement singularities remain. Live calendar zero-CRF handling is separate bounded credit. | F01–F07 note’s distinct F05 subissues; scoped MFE limit repair with independent limiting identities, preserving finance meanings. |
| F06 shared radius | Bounded correction | WI-051 and current-consumer audit join the nine plant-R consumers and retire the duplicate public radius; seven R-only cases verify sampled coherence. | WI-051/current-consumer audits and radius synthesis. F07 and F14 retain geometry/source limits. |
| F07 input domains | Open | Negative/zero inboard clearance and broader algebraic/physical domain gaps remain. Local guards do not establish a complete invalid-input contract. | F01–F07 note; targeted native domain repair before unconstrained public-input search. |
| F08 account interface | Open | IFE component capital/CAS metadata and MFE typed/scalar/dialect reconciliation remain incomplete. Arithmetic attribution is not a populated universal account interface. | MR-1/MR-2, AD-005 and F08 note; owner ruling needed if replacing the promised interface. |
| F09 finance normalization | Open | Labels distinguish historical price meanings, but no common currency/year, timing or account-scope comparison record exists. | Owner monetary/finance ruling under goal Reserved gates before normalized comparison implementation. |
| F10 generic MFE reuse | Open | Generic plant still unconditionally uses ISS04 and an ECRH operating chain; separate non-ECRH procurement inputs do not complete mixed heating. | F10 note, MR-3/AD-007; compose appropriate physics or obtain owner scope ruling. |
| F11 modules | Open | Public Real module count scales only part of the plant and differs between price denominators; no coherent multi-module or enforced single-module contract. | Owner supported-module ruling, then accounting/domain implementation under F11. |
| F12 lifecycle availability | Partial | WI-046 joins replacement, downtime, availability and cost on a live calendar. Retained implementation/integration evidence is distinct from an independent item audit. Maintenance assumptions and engineering scope remain. | WI-046 native records and F12 note; review remaining evidence/maintenance bounds before residual acceptance. |
| F13 thermal closure | Partial | WI-045 computes primary-loop and conversion responses; WI-050 feeds coherent operating source heat. Rejected-duty costing, materials/cycle and calibration limitations remain. | WI-045/WI-050 and F13 note; bounded source/engineering follow-up. |
| F14 conductor/geometry | Open | WI-044’s bore-sensitive magnet chain remains credited, but conductor current margin, configuration validity, pack/casing fit and casing-floor limits are unresolved. | Existing WI-038/WI-040 and minor-radius research homes in F14 note; source evidence before broader conductor/geometry claims. |
| F15 breadth | Partial | WI-047 adds bounded exhaust and fuel-inventory/processing checks. Held TBR, shielding/nuclear-heat and configuration-specific exhaust limitations remain. | WI-047 and pending STEP report; source approval/application, engineering work and owner residual ruling remain separate. |
| F16 validation meaning | Partial | New independent source/identity checks and explicitly bounded study evidence improve validation. Oracle/domain coverage and tungsten-fit/convergence questions remain. | F16 note and existing coverage/numerical-research homes; retain separate validation categories. |
| F17 citations | Partial | WI-048/049 local corrections stand. Broken archived paths, shorthand, stale table/source-status claims and missing trace-audit script remain. | Exact paths in F17 note; model citation repair and separately owned coding enforcement work. |
| F18 reuse/metadata | Partial | Derived HIF energy repairs one fixed literal/dependency. Reusable type placement, fixed source-level facts, scalar/metadata mapping and sampling/energy semantics remain. | MR-3, AD-002/006/007 and F18 note; source-faithful parameter/specialization contract. |
| F19 radiation prose | Open | Displayed MW equations still omit 1e-6 while executable handwritten terms include it. Executed power is not shown to be a million times wrong. | Native documentation correction with dimensional examples, under AD-001. |
| F20 precision/guidance | Open | Julian-year shots versus 365-day energy, differing alpha fractions, false universal shape wording and stale catalogs/counts remain. Some runner/IFE guidance improved. | F20 note; alpha research route `20260911-operating-heating#3` stays open. |

## What current evidence permits

The demonstrated IFE chain supports bounded arithmetic and sensitivity results under its stated gain, availability and power/cost assumptions. Its generating-price boundary is enforced by the supported consumers. The current MFE evidence supports the repaired operating/procurement and shared-radius dependency behavior, under the existing stellarator/ECRH configuration. All seven final-radius study points and all fifteen operating-heating study points retain engineering violations. These results do not identify a feasible physical plant or establish a sourced geometric validity interval.

The report recommends against treating the current outputs as normalized cross-concept rankings, general MFE/mixed-heating predictions, coherent multi-module costs, conductor-qualified designs, or a complete source-faithful Monte Carlo model. Those recommendations are not new owner-approved scope restrictions and are not uniformly enforced by the executable model. Closing the corresponding findings requires implemented contracts or owner-accepted residual dispositions with their effects made explicit and enforceable.

## Validation and process limits

This assessment uses current static inspection and retained execution certificates. It does not rerun models, source audits, integration or studies. Each certificate remains separate:

- IFE repair and zero-discount audits establish their named source facts, counterexamples, numerical identities, ordinary cases and explicit exclusions.
- WI-050/WI-051 independent audits and current-consumer audits establish bounded source-to-execution dependency changes. The retained model certificate’s 428 passes and 13 inherited skips do not erase the L2/L6 findings. The current consumer’s 233 targeted passes and broader 580 passes/97 matched historical failures/four write-safety deselections are separate batteries.
- WI-045/046/047 implementation and integration evidence supports later engineering increments, but this assessment does not manufacture missing independent per-item audit certificates.
- Integration CANDIDATE checks, mirrored numerical parity, analytic identities, source-image verification and engineering coverage answer different questions. The current MFE adapter accepts 99 of 246 native inputs; 147 overrides remain unsupported. Its independent oracle computes 141 of 158 native scalars; 17 omitted channels have frozen controls, not independent computation.
- Round 5 remains FINDINGS. The original helper’s seven quarantine-file hashes were unauthorized reads. The corrected helper and independent guard establish corrected behavior only. Existing digest metadata and reviewed diffs do not prove every historical action or reasoning step. The T-027 fresh-child account is retained, but its serialized dispatcher log lacks a raw spawn event. Neither limit is erased or converted into an unsupported claim of scientific data use.

No source under `knowledge/holdout/` was read or hashed by T-028. No model/consumer, historical pin/store, source registry, requirement, validation registry or work-item status was changed. Pending STEP research remains pending; its P_sep/R proxy does not establish a generic MW/m² conversion or authorize the current target threshold to change.

## Answer-contract assessment and owner decisions

| Goal condition | Result at this round |
|---|---|
| Current assessment and evidence-linked disposition for every finding/subissue | Supplied by this report and its three detailed notes, subject to fresh review. Open findings remain open. |
| Reproducible defects corrected through audited native work | Not met: F05/F07 and multiple accounting/documentation/reuse defects remain; some earlier engineering items lack distinct independent item audit certificates. |
| Implemented accounting/reuse/comparison contracts | Not met: F08–F11/F18 remain, with owner comparison/scope gates. |
| Concrete limitations, use effects and owner-accepted residuals | Partly documented, not satisfied: evidence limitations and proposed use effects are explicit, but enforcement and owner acceptance remain absent for open residuals. |
| Fresh final review with separated evidence categories | Pending at authoring; the fresh Round 6 review is recorded in the goal trail and review evidence directory. |

The immediate owner decision is whether to re-ground further remediation after the six-round limit, or redirect/close without certifying the original goal answered. Recommended next scope if re-grounded: finish reproducible MFE financial/domain defects and live documentation issues, then resolve accounting/comparison and engineering evidence contracts against this assessment. This is prioritization advice, not an opened round or future task list.

Finance normalization, supported concept/module changes, project requirements, source/research adoption and residual acceptance require their existing separate rulings. The historical plant-closure preservation ruling is already resolved. The historical process incident remains recorded; no new incident-approval ceremony is imposed by this report.

## Discovery updates and document checks

T-028 appended assessment references under seven existing IFE IDs and twenty-six existing MFE IDs. Prior dispositions are retained except the two lifetime/availability sightings (`20260821-power-cycle-ab#1` and `20260904-wall-and-heating#5`), which now credit WI-046’s live-calendar dependency while retaining broader maintenance/reliability and audit-evidence limits. The update does not rewrite historical study results or accept residuals. Current native sources and the precise next decision/evidence home are supplied in the detailed notes and this report. The retained helper `evidence/T-028_assessment/append-dispositions.py` is a one-time mutator with a duplicate-append guard, not a read-only validation command.

The existing stellarator record-join checks passed: 14 passed, 26 unrelated tests deselected (`evidence/T-028_assessment/record-joins.log`). A direct read-only check verified exact F01–F20 summary coverage and both IFE record/log joins. `git diff --check` passed. These validate record structure only; no numerical, model, source or engineering coverage is added by them. The previously known unrelated wall-and-heating narrative-reference failure was not rerun.
