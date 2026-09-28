# Goal: Physically consistent divertor peak heat load

## Status

`grounded` — 2026-09-15. [OWNER] The initiating request supplies the question, evidence, success criteria and autonomous execution authority. [AGENT] Slug selected as a routine workflow decision under that authority.

## Question

[OWNER] Can the represented stellarator divertor peak heat load be traced consistently from plasma exhaust through deposition, geometry and spatial concentration, and what does that establish at the joint magnet-sizing rejection cases?

## Consumer

[OWNER] The model owner needs physically justified divertor design dependencies and explicit conditional requirements before interpreting joint plant feasibility.

## Answered when

- [OWNER] Existing peak and area-based calculations have reconciled definitions or clearly explained differences; an average must not replace a peak merely because it passes.
- [OWNER] Power accounting distinguishes confined-plasma exhaust, radiation and other losses, deposited power per target or group, effective wetted area, average flux and peak concentration, consistently with plant energy balance.
- [OWNER] Supported model changes expose deposited power, effective area, average flux, peak flux and margin, with traceable assumptions. Native model, generated package and independent oracle agree; tests cover conservation, physical responses, boundaries and invalid inputs.
- [OWNER] A bounded study revisits the reference and selected joint-sizing rejection cases, attributing changes against the entering package and separating geometry from deposition/peaking assumptions. Changed reference results are explained without tuning.
- [OWNER] Independent review checks the source/math basis and integrated answer. The answer identifies required heat-load reductions, physically demonstrated options, conditional changes and separate divertor/all-predicate feasibility.
- [OWNER] A reviewed explanation and quantified evidence gap are valid if the current peak basis is justified and no transferable geometry relation is supported. Unsupported capabilities must remain unavailable rather than supplied by invented assumptions.

## Invariants

- [INHERITED: entering checkout] Package/model entering checkpoint: `f76ec031951d7918fbfec2de23d298830941c121`; joint study checkpoint `02af7123`, cited by its native record. Matched entering evaluations anchor attribution.
- [OWNER] Keep 10 MW/m² unchanged unless original evidence proves a genuine interpretation or implementation error; such a finding needs explicit independent review.
- [OWNER] Preserve magnet current sizing, current margin, field limits, fit and primary-loop constraints. A divertor pass is separate from combined feasibility; loop sizing belongs to follow-up.
- [OWNER] Preserve failed cases and the joint study's bounded negative conclusion unless a documented correction or physical change alters it. Do not force feasibility or tune reference coefficients to pass.
- [OWNER] Explicit physical improvements must carry accommodation, energy-balance and modeled cost consequences; missing consequences make them conditional requirements or sensitivities.
- [OWNER] Exclude detailed edge simulation, erosion/lifetime qualification, full target mechanics and new cooling-system design. Preserve source quarantine; no merge or push.

## Grounding evidence

All following tracked paths are cited at entering commit `f76ec031951d7918fbfec2de23d298830941c121`.

- `work/orchestration/goals/joint-magnet-sizing-feasibility/answer.md` and `evidence/coupled-dependencies.md`: bounded negative and named cases, including 11.156873 MW/m² with loop-capacity failure.
- `exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/record.md`: frozen native study and predicate evidence.
- `models/library/analyses/mfe_divertor_heat.sysml`, `models/library/cost_structure/mfe_power_core.sysml`, `models/designs/stellarator_09/stellarator_plant.sysml`: existing ledger, carrier and bindings.
- `work/active/WI-047_fuel-divertor-vacuum-flows/`: prior divertor implementation basis.
- `work/orchestration/goals/plant-closure/` and `work/orchestration/goals/wall-and-heating/`: power/account and wall-load history.
- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md`, section 2.6; `work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p15_divertor.png`: admissible original divertor basis.
- `knowledge/holdout/aries-cs/PROTOCOL.md`: mandatory clean-room rule; only the protocol is admissible within this holdout directory.

## Limits

[AGENT] Execution limits, chosen under owner-authorized routine engineering judgment:

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | One pin and one committed study per round; research and study bounds declared in their native requests |

## Reserved gates

[OWNER] No merge or push; preserve quarantine. No routine parameter or workflow decisions require a pause. [INHERITED: GOAL_RUNBOOK.md] Unresolved scientific interpretation that changes comparison meaning remains owner-held. [AGENT] Any proposed acceptance-limit change is parked for explicit independent evidence review before a decision; no change is assumed necessary.

## Close rule

[OWNER] Continue autonomously through justified implementation, study, independent review and answer. [INHERITED: GOAL_RUNBOOK.md] Formal goal close and native work-item archive remain owner-held; technical completion can be reported with closure recommended.

## Amendments

None.
