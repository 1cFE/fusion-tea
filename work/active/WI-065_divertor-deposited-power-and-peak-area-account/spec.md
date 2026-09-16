---
Status: active
Scale: standard
Epic: standalone
Owner: agent
Created: 2026-09-15
Updated: 2026-09-15
---
# WI-065: Divertor deposited-power and peak-area account

## Contract

[NEED] Make divertor power destinations and the basis of the peak heat-load constraint explicit, preserve the 10 MW/m² acceptance limit and existing magnet/loop constraints, and validate source/geometry assumptions without forcing feasibility. Owner request: `work/orchestration/goals/divertor-peak-heat-load/goal.md`.

[INHERITED] Required reading: `knowledge/holdout/aries-cs/PROTOCOL.md`; `modeling_project/REQUIREMENTS.md`; `modeling_project/MODELING_PROCESS.md`. Original source and independent release: `work/orchestration/goals/divertor-peak-heat-load/evidence/entering-account.md`, `external-research.md`, `source-review.md`. The source is a resonant island divertor. Existing peak normalization includes capture and spatial concentration; no new physical-area transfer law is supported.

## Bounded design

[AGENT] Extend the existing Divertor Heat Ledger with source-case capture metadata and explicit conserved destinations. Follow the reviewed candidate boundary/interface contract in `entering-account.md`. Keep every existing peak, shadow, heat-margin and physical plant calculation unchanged at entering valid inputs. No new acceptance predicate. The native SysML calculation becomes an explicitly documented typed manual completion to enforce domains and represent undefined ratios without division by zero. Keep all26 existing manual bodies unchanged; add only this formerly auto-generated ledger to the reviewed manual seed inventory.

[AGENT] New Divertor-owned attribute `target_capture_fraction` defaults1 generically and explicitly0.99 in Stellaris; formal `target_capture_fraction_in`. The alternate source case ties capture0.97 to q_target_ref5 at unchanged p_nonrad_ref50. This parameter annotates a reference profile; changing it alone changes deposited-power diagnostics and implied area together, not q_peak. It is not a stand-alone physical gain.

[AGENT] Preserve all9 existing output names. Add exactly8 outputs: `p_rad_total`, `p_rad_edge`, `p_target_deposited`, `p_nonrad_uncaptured`, `peak_equivalent_area`, `peak_equivalent_area_defined`, `f_rad_edge_defined`, `power_account_valid`. All are Real; flags exactly0/1. Add pure EXPOSEs on Divertor for these8 outputs. Definitions: H=p_alpha_heat+p_coupled; C=p_rad_core; total radiation=F H; E=F H-C; N=H-F H; D=cN; U=N-D; Aeq=c Nref/qref when qref>0, otherwise carrier0/defined0. E>=0 yields account_valid1 after enforced input domains. q_peak=qref*N/Nref retains exact old arithmetic. Peak-equivalent area is A_wet/k_peak, not a numerical identification of either physical wetted area or concentration separately. q_peak=D/Aeq is an independent check when the source pair is active, not a second production formula. Neither an average nor per-target shares are invented.

[AGENT] Domain behavior is the reviewed contract in entering-account.md: finite inputs; nonnegative physical powers/limits/reference peak; signed finite auxiliary requirement; fractions in[0,1]; strictly positive Nref/R/Rref; C<=H; qref>0 requires c>0. S=H-C=0 publishes edge-fraction carrier0/defined0. Negative E remains diagnostic and account_valid0, not clamped or reclassified as a valid partition. For active qref require finite positive Aeq; refuse overflow and underflow that erase expected positive area/power/peak. qref0 is dormant, never a physical heat-limit interpretation. Physical interpretation requires active source area-defined1, valid power account and a supported paired source profile. Preserve signed margins. Validate intermediate arithmetic as well as inputs.

[AGENT] Document full physical identity for target groups: deposited share s_j D, average s_j D/A_wet,j, peak k_j times average, maximum over groups. The absence of independently measured A_wet,j, k_j and s_j is the reason these are not executable design levers. The retained R-scaled shadow is a conditional peak with length proportional to R and held width/profile, never an average or a supported redesign. The 10 MW/m² predicate remains a necessary non-radiated transport screen; omitted radiation surface deposition prevents total target-load qualification.

## Consumers and integration

[AGENT] Canonical and exploration twins: analyses/mfe_divertor_heat.sysml, cost_structure/mfe_power_core.sysml, designs/stellarator_09/stellarator_plant.sysml. Enumerate all actual shared consumers. Generated package, strict manual seed inventory, independent oracle/output mapping, current regression ABI/census/snapshot/manifest and focused component/coupled tests must agree. Divertor destinations do not add to plant thermal generation. Retained versus total alpha boundary and inherited rounding difference remain disclosed. No new divertor coolant loop or area-cost law is implied; existing power-scaled cost remains unchanged.

## Acceptance and execution checklist

- [x] Original source/math release before implementation, including source pairs and 10 MW/m² interpretation; source-review.md.
- [x] Focused boundary/interface release with active-normalization and positive-area qualifications; source-review.md.
- [ ] Native model/twins and generated guarded ledger implement exactly the reviewed account; all prior manual bodies and20 predicates preserved.
- [ ] Component tests cover both source pairs, conservation, physical responses, zero/full-radiation/dormant boundaries, negative edge diagnostic and invalid/nonrepresentable inputs.
- [ ] Independent oracle rederives account and maps every new output; matched native/oracle and entering-preservation tests cover reference and selected named cases.
- [ ] Shared consumer checks, native validation, exact regeneration, current manifest/census/snapshot and traceable verification registry evidence; inherited limitations disclosed.
- [ ] Independent integrated audit; study-ready handoff. Native integration and bounded study follow in goal-owned tasks.

[AGENT] Use rtol1e-9/atol1e-9 for coupled scalar agreement and exact flags/predicates. Preserve exact entering values where the same arithmetic remains. No full geometry law, average-flux number or altered reference peak is part of this item. Spec combines design and checklist under MODELING_PROCESS scale guidance.
