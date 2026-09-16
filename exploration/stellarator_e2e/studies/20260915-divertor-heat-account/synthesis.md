# Executor synthesis: divertor heat-account study

**Author:** Codex executor `/root/divertor_research`; this is an executor reading, not an independent review. **Date:** 2026-09-16 UTC. **Evidence commit:** `ac1b529baeadf06172cfc141ae2666dbc81191b7`. **Snapshot SHA256:** `92d2a24565645de602384a530ee6c32776e66b4787af8245b81d3d099df3fbbd`. Only committed artifacts inside this study directory were read for this synthesis; frozen evidence is unchanged.

## What the study set out to do

The owner asked for a bounded revisit of reference and joint-sizing rejection cases, separating geometry changes from deposition assumptions and preserving failed cases. The 27-point diagnostic sample compares five named controls, paired source profiles, total-radiation sensitivities, six radius changes and one explicit negative-burn control. All acceptance limits remain fixed. The [record, §§2–8](record.md) preserves the owner’s words and scope.

## What it found

**Thirteen points pass the non-radiated divertor predicate with valid active accounts; none passes all 20 predicates.** Two points have invalid heat accounts and remain failed numerical controls. The accounting extension preserves all 218 entering mapped outputs and all 20 predicates at every matched point; its eight added outputs expose heat destinations and reference-profile area equivalents. Entering attribution uses a captured independent oracle, not an old-native rerun. [Analysis](results/analysis.json), [entering comparison](results/comparison-entering.json).

| Named base control | High profile, F=.90 | Low profile, F=.90 | High profile, F=.92 | Other failures at the base |
|---|---:|---:|---:|---|
| Legacy reference | 10.517842 | 5.535706 | 8.414273 | Conductor current, pack fit |
| Current-sized reference | 10.517842 | 5.535706 | 8.414273 | Pack fit |
| Allocated current-sized reference | 10.517842 | 5.535706 | 8.414273 | Peak field |
| R12.7, a1.35, I16.2 MA | 9.603709 | 5.054583 | 7.682967 | Peak field |
| R13.1, a1.45, I15.4 MA | 11.156873 | 5.872039 | 8.925499 | Loop capacity |

Values are peak heat flux in MW/m² against the held 10 MW/m² limit. The low profile is a different source transport assumption on the proposed target arrangement. F=.92 is an engineering radiation sensitivity. Neither is a demonstrated design improvement. Full coordinates and failures are in [case-summary.csv](results/case-summary.csv).

The legacy reference has 553.571 MW absorbed heating and 55.357 MW non-radiated transport. The high profile deposits 54.803 MW on targets and leaves 0.554 MW uncaptured. Its equivalent area is 5.210526 m². This is captured power divided by peak flux, not measured wetted area. The reference would need a 4.923% target-power reduction, a 5.178% equivalent-area increase, or total radiation of 90.492% at held heating and source profile to reach the limit. Those are necessary arithmetic conditions. The record supplies no engineered route to achieve them. [Analysis, reference account and conditional requirements](results/analysis.json).

## Framing verdict

[Executor interpretation] The recorded sensitivity framing remains appropriate for all 21 groups. Source-profile and radiation contrasts isolate their stated assumptions; radius samples show a local response. Other changing groups belong to coordinated context controls, while held groups have no measured independent response. No boundary, optimized design or causal effect from co-varying context is established. Indicators report possible constraint paths for every group; they do not establish monotonicity or physical identity. [Record, §§5–8](record.md), [indicators](indicators.json).

At held plasma coordinates, the low profile lowers the target peak while increasing uncaptured non-radiated heat. Increasing radiation reduces the non-radiated target load. Both leave plant heat, primary-loop demand, target capital and LCOE unchanged in the model. That absence of cost or accommodation response limits what these sensitivities can support. Larger radius increases the fixed-target peak in all three sampled pairs; the radius-scaled shadow remains a conditional peak, never an average or demonstrated geometry benefit. [Paired consequences](results/analysis.json).

## Constraint structure and verification

The field-only base already meets the target limit but fails peak field. The field-passing base fails divertor heat and loop capacity; changing source profile or radiation clears only its divertor failure. Its R12.9 variant has negative auxiliary demand and an invalid account, as does the explicit signed-negative control. Both are excluded from physical heat-load-gain interpretation. The legacy reference’s LCOE is $144.747/MWh, but it fails three predicates; no feasible cost minimum emerges. [Record, §§3–4](record.md), [window decision](reviews/window-selection.md).

All 6,102 mapped scalar comparisons and 540 exact predicate comparisons pass. Generic verification independently samples all 13 observed verdict combinations, checking 27 channels and re-deriving 20 predicates. The native stores retain 27 study cases plus the required baseline, with complete content-addressed evidence. These checks establish arithmetic and custody, not reactor qualification. [All-point verification](results/oracle-all-points.json), [stratified verification](results/verification_summary.json), [custody check](reviews/artifact-check.json).

## Findings carried forward

The following are the recorded dispositions, not new approvals or goal decisions. [Record, §15](record.md).

| Existing finding ID | Disposition carried forward |
|---|---|
| `20260915-divertor-heat-account#1` | Keep the low source profile conditional; wall interception and geometry-specific engineering/cost consequences remain unrepresented. |
| `20260915-divertor-heat-account#2` | Keep geometry transfer unresolved; equivalent-area and peaking gains are conditional requirements. |
| `20260915-divertor-heat-account#3` | Keep radiation-control capability, total radiative target deposition and wall accommodation unqualified. |
| `20260915-divertor-heat-account#4` | Retain both invalid accounts and exclude them from physical heat-load-gain interpretation. |
| `20260915-divertor-heat-account#5` | Preserve the joint study’s bounded negative; these selected sensitivities do not regrade it or establish global infeasibility. |

## What the record does not support

No independent physical wetted area, peaking factor, per-target sharing map or qualified size-transfer law is established. Total radiative surface deposition, neutral exhaust, breeding impacts, target cooling/support/manufacturing and target/control costs remain absent. Sixteen retained native channels lack independent oracle comparison. The record does not contain a final independent study/goal review or later coordinator dispositions. Those facts cannot be recovered from this frozen record and are not inferred here. [Record, §§13–17](record.md).
