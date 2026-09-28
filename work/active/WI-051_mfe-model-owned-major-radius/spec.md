---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-09-11
Updated: 2026-09-11
---

# WI-051: MFE model-owned major radius

## Outcome and authority

Repair F06 so an ordinary change to the supported plant's major radius drives both plasma and magnet calculations. Retire the duplicate public radius input while preserving the baseline, reusable magnet interfaces and fixed reference anchors.

[INHERITED] Immutable alignment: [mfe-model-owned-major-radius.md](../../orchestration/mfe-model-owned-major-radius.md) at `b847558b`. Scope is T-022 in [the goal trail](../../orchestration/goals/fusion-audit-remediation/trail.md#t-022-scope). Existing goal authorization supplies alignment; routine stage approvals belong to the parent. This spec does not grant source approval, finance or supported-scope changes, residual acceptance, archive, integration, study, or goal closure.

[INFERRED] All item-specific requirements below derive from the agent-originated alignment and [T-021 assessment](../../analysis/20260911-230953_radius-ownership.md) at `2f8856b7`. They are not owner-originated settled decisions. Ratification does not change that grade. Existing project requirements retain their inherited authority.

## Context and evidence

[INHERITED] The [MFE epic](../../backlog/epic-mfe-cost-modeling.md) supplies reusable CAS cost structure and executable sensitivity goals. This item serves RQ-1, RQ-2, RQ-3 and RQ-5 in `modeling_project/OVERVIEW.md:26–42`; that document uses RQ identifiers, so no G/AQ identifiers are invented. DI-002 records CAS22 divergence; DI-010/011 explain why magnet geometry and field affect more than procurement. No new insight or project requirement is proposed for promotion.

[INHERITED] Current split: `models/library/cost_structure/mfe_power_core.sysml:89` declares reusable `R0`; `models/designs/generic_mfe/mfe_plant.sysml:133` declares plant `R`; `models/designs/stellarator_09/stellarator_plant.sysml:139,528` independently set both to 12.7 m. Generic plant bindings at `:143,168,250,283,293,304,331,618,1101` divide nine consumers between them. `tests/model_families.py:58` defines the 23-file MFE family and its twin.

[INHERITED, REFERENT] The evidence directory [20260911-230953_radius-ownership-evidence](../../analysis/20260911-230953_radius-ownership-evidence/) at `2f8856b7` is the frozen pre-repair reference: `inventory.json` contains exact edges, input groups and hashes; `results.json` contains complete inputs, native outputs/responses/reports, component probes and geometry; `checks.py` and `checks.json` contain independent identities and the isolated oracle-operand experiment; `probe.py` documents execution. `source-meaning.md` records the parent's image inspection and source hashes. This stage inherits that source assessment; it does not claim a new independent source review. Existing source intent supports one plasma/axis scale, not equality of every real modular-coil surface or an operating envelope.

## Requirements and verification

All requirements are P0. Sources abbreviated below: A = immutable alignment `b847558b`; E = assessment and evidence `2f8856b7`. Structural, input-key, verdict and baseline equality checks are exact. Off-baseline numeric checks use relative and absolute tolerance 1e-9 in each channel's documented units. Freeze comparator inputs and output coverage before production changes; do not use newly generated expectations as their own oracle.

| ID / grade / type | Requirement | Rationale and source | Verification |
|---|---|---|---|
| MR-051-01 [INFERRED] Functional | The supported plant SHALL expose one authoritative major-radius producer, `stellarator_09__stellaris__R` in `stellarator_plant_params`, reaching all nine exact direct consumer/formal pairs below through native generated bindings. | Eliminate split geometry; A, E inventory; RQ-5. | SV-083: exact source-entry to formal edges in generated contract/pipeline, including native execution; module reachability or name suffixes alone are insufficient. |
| MR-051-02 [INFERRED] Constraint | The model SHALL retain supported standalone reusable magnet `R0` inputs and the independent fixed anchors `magnet.R_ref`, `magnet.a_coil_ref`, `wall_peak_R_ref`, `R_ref_divertor`; coil-bore and coil-centre minor radii SHALL retain their separate meanings. | Preserve reuse and source-case normalization; A, E source-meaning; project MR-3. | SV-084: standalone input acceptance and radius response; exact anchor values/bindings unchanged under plant R mutation; inspect distinct minor-radius surfaces. |
| MR-051-03 [INFERRED] Functional | Generated public contracts SHALL retire `stellarator_09__stellaris__magnet__R0` from `stellarator_plant_params`. Supported direct model callers SHALL explicitly refuse that obsolete key, including when supplied alone, alongside equal R, or alongside conflicting R, identifying the obsolete key rather than silently dropping it. | Prevent an ignored override from appearing successful; A, E caller inventory. | SV-083/085: re-derived complete public census and exact contract delta; refusal tests through each supported direct input path. 247→246 is a prediction, not proof. |
| MR-051-04 [INFERRED] Quality | At unchanged baseline controls, the generated model and supported direct runners SHALL preserve all pre-repair numeric outputs and named verdicts, including every downstream cost/finance channel, with no retuning or unexplained lost channels. | Binding adds no equation; A, E `cases.baseline.native`; RQ-1/2. | SV-086: exact complete channel-set/value and verdict comparison against retained baseline; preserve any additional direct-runner outputs using a frozen pre-change capture. Metadata identities may change and must be accounted for separately. |
| MR-051-05 [INFERRED] Functional | With only public plant R set to 14 m and every other control held at the retained baseline, supported direct execution SHALL match pre-repair `cases.tied_R14.native` and the independent ratios below, without a study tie. | Reproduce coherent geometry through ordinary input; A, E results/checks; RQ-5. | SV-087: complete outputs and named verdicts through both direct runners and supported generated input path; independent geometric and cost checks, not headline-only or oracle-only parity. |
| MR-051-06 [INFERRED] Constraint | The repair SHALL retain explicit invalid-case failures and evidence of the original F07 negative-peak component defect. It SHALL not turn invalid inputs into accepted operation by clipping or fallback equations. Any binding-induced defect requiring changed handling SHALL be surfaced to the parent before dependent work. | Existing arithmetic failures are not general domain enforcement; A, E domain probes. | SV-088: cases and adverse component behavior below; preserve original evidence and disclose remaining F07. Broad guard redesign requires a surfaced necessity, not inference from this spec. |
| MR-051-07 [INFERRED] Quality | Native regeneration SHALL preserve canonical/twin equality, family isolation, genuine handwritten implementations and live/snapshot executable agreement; model tests and current census/snapshot SHALL reflect the actual generated contract. | Source binding must govern execution; A, E inventory; project MR-6 and AD-004. | SV-089: family generation/snapshot checks, focused and model regression tests, semantic/executable identity records and implementation provenance; distinguish genuine handwritten bodies from stale autogenerated bodies. |
| MR-051-08 [INHERITED] Traceability | Changed bindings SHALL retain source/basis citations and native traceability under project MR-4. Verification SHALL preserve Round 4 operating/procurement separation and cost classifications, fixed finance and alpha bases, historical studies/pins/source evidence, and L-001–L-007. | A; project MR-1/2/3/4, AD-003; WI-050 audit at `55456198`. | SV-089: review source and traceability delta, protected-surface diff and all six native validation levels; report inherited findings separately from introduced findings. No new project-rule promotion. |
| MR-051-09 [INFERRED] Traceability | The item SHALL publish an exact retired-key, generated-contract and oracle-expectation handoff for the separately certified coding migration, explicitly stating that current-study compatibility remains incomplete. | A and T-022 narrow the assessment's broader caller recommendation. | SV-089: handoff coverage below and fresh independent audit of this model scope; no passing credit for excluded study surfaces. |

All nine module names below have prefix `stellarator_09__stellaris__`. The required edges originate at the exact `(stellarator_plant_params, stellarator_09__stellaris__R)` entry, not a second independent public input.

| Module suffix | Formal |
|---|---|
| rb | R_in |
| geom | R_in |
| sustain | R_in |
| divheat | R_in |
| coil_length | R0 |
| field_calc | R0 |
| peak_field_calc | R_in |
| magnet_cost | R0 |
| stored_energy | R0 |

[INFERRED, REFERENT] For R=14 versus R=12.7, with minor geometry/current fixed: `geom__V` and `coil_length__c_coil` ratios are `14/12.7`; `field_calc__B_axis` and `stored_energy__W_mag` ratios are `12.7/14`; `peak_field_calc__B_peak` ratio is `(12.7-c)/(14-c)` with `c=results.derived_baseline_geometry.coil_centre` (3.1500000000000004 m). `magnet_cost__capital_cost` conductor procurement remains invariant because B×R cancels at fixed current. Decomposed magnet capital follows the retained coordinated control through winding/casing consequences; it is not the same channel as conductor procurement. Compare complete downstream costs and both LCOE channels against E, without inventing a universal cost ratio. These are required diagnostic controls, not feasible-plant examples.

[INFERRED, REFERENT] Under unified input, R=4, exact baseline coil-centre radius, 3, 0 and −1 must fail explicitly. Preserve the original `plant_zero` and `magnet_zero` records; the now-obsolete magnet-zero proposal must fail contract validation, not be dropped. Preserve component `original_negative` (R=12.7, coil centre=13: negative peak satisfies the upper comparison), `equality`, `reference_equal` and `reference_inverted` results. Unchanged component arithmetic must reproduce these adverse results; a necessity to alter that behavior is a parent gate. Baseline violates divertor heat; coordinated14 also violates wall load, sustainment and loop capacity. Neither is a fully valid plant, and the aggregate headline is not a nineteenth authored assertion.

## Scope and completion boundary

[INHERITED] In scope: canonical generic/stellarator plant sources named above and their matching `exploration/stellarator_e2e/models/` twins; the MFE generated package under `exploration/stellarator_e2e/generated/`; affected direct callers `run_stellaris.py` and `run_stellaris_single.py`; `tests/models/`, `tests/model_families.py`, current `tests/models/data/mfe_census.json` and `exploration/stellarator_e2e/stellarator.snapshot.json`; native validation/traceability records. Reusable magnet definitions are preservation/verification surfaces. Binding placement and regeneration mechanics belong to design, which must confirm supported caller assumptions.

[INHERITED] Excluded for later separately certified coding migration: `exploration/stellarator_e2e/verify_stellaris.py`, current `studies/oracle_entry.py`, `manifest.json`, `study_route.py`, `ANNEX.md`, and `tests/study/` fixtures/tests. Historical studies, package pins, snapshots and source evidence remain unchanged. This stage writes registration/spec and pending verification only; production modeling and design are subsequent stages.

[INFERRED] The final handoff must enumerate the old/new `(group,key)` contract diff and complete census, the nine edges, baseline and R14 outputs/verdicts with tolerances, source/package identities, direct-caller refusal behavior, and fixed anchors. It must identify the oracle's incorrect sustainment radius operand and require plant R consistently for magnet operation and sustainment; list the adapter mapping, tie metadata/route, annex and fixture expectations to migrate; preserve generic tie tests and historical records. It must give reproducible controls and evidence paths without requiring mutation of excluded surfaces to verify this model item.

[INHERITED] Completion requires a fresh positive independent native audit of the written scope and handoff. SV-083–SV-089 in `modeling_project/VALIDATION_MATRIX.md` start pending. Native validation must report all levels; entering WI-050 evidence has L2 ten inherited findings and L6 229 findings, with 364 model tests passed and 13 inherited skips. Do not report these levels as passing or treat counts alone as justification: classify diagnostic deltas and surface new binding-induced blockers. Finite diagnostic tests do not certify complete domain validity.

## Assumptions and gates

1. [INHERITED, high confidence] E found no second supported canonical caller requiring independent major-radius surfaces. A contrary supported caller or physical-reference finding is a blocker to dependent design, not permission to expand scope.
2. [INFERRED, unproven] Native generation can express the producer binding while preserving standalone formals. The design prototype must establish this; this spec makes no capability certification.
3. [INHERITED, certain] Current-study compatibility remains incomplete until the later coding task is certified. Old oracle parity must not substitute for the retained independent controls.
4. [INHERITED] Source approval, finance/supported-scope changes and residual acceptance remain reserved. Parent holds routine approvals and orchestration; this author stops before design.

Related artifacts: immutable alignment and assessment above; [WI-050 spec](../WI-050_mfe-coherent-operating-heating/spec.md) and its audit at `55456198`; `design.md` and `plan.md` are not yet created.
