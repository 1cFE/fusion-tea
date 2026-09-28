---
Status: completed
Scale: standard
Owner: reid
Created: 2026-09-22
Updated: '2026-09-22'
---

# WI-089: Integrated ARIES heat and electricity

## Authority and outcome

[INHERITED: work/orchestration/goals/aries-integrated-heat-electricity/evidence/owner-brief.md] Deliver one executable native assembly connecting an explicitly selected fusion-power producer to fuel, deposited heat, three coolant/exchanger paths, a recuperated helium cycle and net electricity. Preserve the original Stellaris and transfer artifacts. This is post-reveal development with qualified assumptions, not independent prediction of the published plant. Formal closure remains owner-held.

## Requirements

- **R1 [INHERITED]:** Expose an explicit source-conditioned/calculated-plasma producer selection. Both feed the same fuel and heat consumers. Calculated mode uses the accepted WI-083 profile integration unchanged and never fits profile normalization to published fusion power.
- **R2 [INHERITED]:** Keep one named Lyon-oriented nominal assumed configuration, a literal Lyon source-input configuration and a separately named Raffray source-accounting configuration. Never represent source-derived branch accounting as predicted transport. Compare Lyon 2436 MW fusion, 1253 MW gross electricity and the table's 1-GW-electric plant basis with matching boundary qualifications.
- **R3 [INHERITED]:** Preserve independently supplied flow, primary-loop flow, exchanger conductance, compressor ratios and ratings. Calculate supported temperatures and transferred/unremoved heat. No demand-derived equipment assignment or prescribed turbine temperature inconsistent with available heat.
- **R4 [INHERITED]:** Model neutron/charged energy, nuclear multiplication, deposited heating, blanket/divertor/other sinks, inter-coolant transfer and recovered pumping heat exactly once. Calculate turbine/compressor work, generator conversion, named pump/heating/cryo/fuel/control/other demands and signed net electricity in the graph.
- **R5 [INHERITED]:** Every advertised ledger, capacity margin, support flag and comparison residual is generated graph-owned. Magnet and breeding qualification remain unsupported. A missing demand law remains a named supplied assumption; support is separate from scalar capacity adequacy.
- **R6 [INHERITED]:** Execute baseline, fixed-hardware upstream perturbation, sufficient/insufficient chosen equipment and conversion/interface sensitivity. Retain failed and unsupported points. Independent review must trace one executed upstream change to net electricity and verify no resizing or source substitution.
- **R7 [INFERRED]:** Use finite/domain-checked typed completions, bounded heat-exchanger closure and explicit residual tolerances. Run the supported package generation/native route, check frozen-source preservation, and provide a tracked staging root, snapshot, census, sealed package and integration/study evidence.

## Accepted use and limits

[AGENT] This is a constant-property steady-state thermal/electrical approximation. Selected fusion power must be strictly positive because the unchanged fuel balance divides by its burn rate. Heat that cannot enter the cycle is a reported unmet-removal requirement, not quietly rejected through an invented cooler. A nonzero unmet-removal result makes the selected operating point thermally inadequate even when candidate cycle output is finite. Source hot temperatures act as assumed permissible bulk bounds; material, hydraulic and machine-map qualification remain unverified. No inventory/cost claim is added by this item.

## Design gate and acceptance

The new source interpretations, exchanger/cycle closure, parameter roles and electrical boundary need independent review before implementation. The design and single assumption register are in `design.md`. The executable checklist is in `plan.md`. Tests must establish energy balance to `max(1e-6 MW, 1e-9 * total input MW)`, preserve all chosen hardware, distinguish capacity failure from unsupported qualification, and prove changed native dependency outputs under a supported input perturbation. The nominal assumed scenario must have finite connected results with thermal/electrical ledger closure; equipment shortages may remain explicitly failed. Exact claims of a thermally closed operating point additionally require zero unmet heat within tolerance.

## Implementation evidence

The additive native assembly and sealed package execute. See report.md and evidence/verification.json for 40 checked scenarios, exact boundaries, failed source cases and validation limitations. Design acceptance is recorded in `work/orchestration/goals/aries-integrated-heat-electricity/evidence/design-review.md`; consequential completion review and native goal study remain separate acceptance evidence. Formal closure is unchanged.
