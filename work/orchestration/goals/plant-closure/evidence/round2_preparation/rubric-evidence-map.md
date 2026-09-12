# Consolidated rubric evidence map — preparation only

[AGENT] Pointer-only map for the later fresh non-author grader. No proposed scores. All line references below are at preparation base `45003717a0e566a6a0b4d7d24a1480dc4db148ba`, unless another revision is given. Re-resolve lines and runtime identity at the final pin. Correctness and source gaps attach as evidence-integrity findings under the grading protocol; historical credit does not prove current execution.

## Governing references

- Yardstick: `.project/active/demo-depth-rubric/rubric.md@dc0f0b6d`, all row anchors and Grading protocol. Preserve the full conjunctive anchor, especially fuel inventory/startup/throughput and vacuum gas-load/pumping.
- Historical readings: `.project/active/demo-depth-rubric/grading.md@fc80e5b2`, `grading-r1-regrade.md`, `grading-r3-regrade.md`, `grading-r4-regrade.md` as present at preparation base. These are cross-PM evidence citations, not coding-PM state mutations.
- Historical runtime: `work/orchestration/goals/plant-closure/evidence/T-007_pin/@9dd59883`; WI-045 `plan.md@693a4dff`, WI-046 `plan.md@1c87c343`, WI-047 `plan.md@0b9a2e1c`, with their adjacent evidence. Retain compatibility mappings and the absent Round 1 study distinction.
- Current operating-heating evidence: `work/active/WI-050_mfe-coherent-operating-heating/audit.md@55456198`; `.project/active/mfe-operating-heating-study-package/audit.md` at preparation base; `exploration/stellarator_e2e/studies/20260911-operating-heating/record.md@91b0d96e` and `synthesis.md@a408429a`.
- Final runtime placeholder: no accepted radius candidate exists in this packet. Use `study-contract.md` Package acceptance and `output-contract.md` for the final evidence to supply, not T-007 or the preparation base as a substitute.
- Reveal frame: `.project/completed/20260821_demo-anchor-acceptance-spec/spec.md@5247e0819b34fef65ce4e5081d04d71f8c8665c1`, B-2/B-3/B-4 and the ratification table. No hold-out source was read. `knowledge/holdout/aries-cs/PROTOCOL.md` remains the gate.

## Twelve historically below-target cells

| Cell | Canonical / native pointer | Runtime or source evidence to read | Evidence still needed at final pin |
|---|---|---|---|
| R2b.P | `models/library/analyses/mfe_lifecycle.sysml:4`; `models/designs/generic_mfe/mfe_plant.sysml:1138`; WI-046 plan Phase 3 | `work/active/WI-046_lifecycle-calendar/evidence/compat_mode/diff_vs_before.json`, `evidence/baseline_live/`, `evidence/offdesign_points/`, `evidence/stepping_points/` at `1c87c343` | Final event/time/availability evidence at lifetime perturbations; inherited-window consequence separately measured |
| R2c.P | `models/library/analyses/mfe_fuel_cycle.sysml:4`; stellarator TBR binding/comment near `models/designs/stellarator_09/stellarator_plant.sysml:1307` | WI-047 design/spec and source-conditioned achieved-TBR rationale; fuel required-TBR outputs | Final held achieved versus conditional required TBR; no computed neutronics evidence supplied |
| R5.P | `models/library/analyses/mfe_divertor_heat.sysml:4`; generic wiring `:1091`; stellarator target cases `:1537` | WI-047 `evidence/source_case/` and `evidence/offdesign_points/` at `0b9a2e1c`; operating-heating record | Final flux/margin/qualified fence, operating heat basis, fixed-target versus area-shadow distinction |
| R6.P | `models/library/analyses/mfe_vacuum.sysml:4`; generic wiring `:1109`; stellarator gas convention `:1550` | WI-047 design/spec, missing pressure/conductance declarations, `vacuum__*` outputs | Final conditional pumping estimate plus explicit missing pressure/installed train limits |
| R7.P | `models/library/analyses/mfe_primary_loop.sysml:4`; generic wiring `:550`; stellarator circuit `:821–934` | WI-045 source reference/prototype/plan at `693a4dff`; WI-050 operating-source ledger | Final flow/pressure/draw/IHX and constraint response across loop interventions |
| R7.S | `models/library/analyses/mfe_account_costs.sysml`; generic heat-transport/coolant accounts | WI-045 exclusions and ground proposal source gaps; model functional cost map | Evidence of separately sized/priced pumps, pipes, IHX is missing; final cost proxy boundaries |
| R8.P | `models/library/analyses/mfe_power_cycle.sysml:4`; generic wiring `:567`; stellarator fit `:933–952` | WI-045 design/plan/source Table 4; `knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md:355` as registered before WI-045 | Final temperature/efficiency/domain evidence on the same heat, with source/materials transfer limits |
| R9.S | `models/library/analyses/mfe_account_costs.sysml` Buildings Cost / Remote Handling; initial grading Row 9 | Final grouped account outputs and historical disclosure in `grading.md` | Building volume/function/layout/hot-cell sizing basis remains missing |
| R10.P | `models/library/analyses/mfe_fuel_cycle.sysml:4`; generic wiring `:1068` | WI-047 spec/design/plan, flow conservation outputs and missing residence-time declarations | Inventory and startup requirements in the full P2 anchor remain missing even if throughput verifies |
| R10.S | `models/library/analyses/mfe_account_costs.sysml` DT Fuel Cost / fuel-handling proxy | WI-047 exclusions, annual fuel/account outputs | Processing-plant equipment cost versus throughput basis remains missing |
| R11.P | `models/library/analyses/mfe_lifecycle.sysml:4`; generic calendar and consumers `:1023,1138` | WI-046 event/time/energy evidence, especially strict restart/horizon tests; native plan | Final availability reaches actual fuel/economics consumers; residual unplanned fraction is an assumption |
| R12.S | `models/library/analyses/mfe_lcoe_dcf.sysml`, `mfe_account_costs.sysml`; generic cost rollups | Historical grading Row 12; WI-050 independent finance/attribution evidence and current study expectations | Final concentrated-account decomposition, monetary/construction basis and explicit estimate-maturity/uncertainty treatment |

## Eleven historically at-target cells to reconfirm

These rows specify where to look; they do not import a prior score into the final grading.

| Cell | Pointer for anchor and declared structure | Final-pin reconfirmation |
|---|---|---|
| R1.P | `grading-r1-regrade.md`; `models/library/analyses/mfe_plasma_sustainment.sysml`; generic sustain `:245` | Demand, W basis, confinement/radiation and operating/capacity verdict operands; radius propagation and numerical limits |
| R2a.P | `grading.md` Row 2a; radial build, wall-average/peak calculations and source-anchor binding in stellarator instance | Build ordering, wall-load geometry response and qualified wall fence at current inputs |
| R2.S | `grading.md` Row 2; `mfe_account_costs.sysml` in-vessel component accounts and generic cost-per-event/calendar wiring | Replaceable versus life-of-plant account mapping and final replacement numerator |
| R3.P | `grading-r3-regrade.md`; magnet-field/stress/strain calculations and WI-044 native records | Current R-only/B/a geometry responses, complete verdicts and F07/F14 limitations |
| R3.S | `grading-r3-regrade.md`; `mfe_magnet_cost.sysml` winding/structure; power supplies and cryo accounts | Four separately driven cost channels and rollup identity; retained calibration and fabrication assumptions |
| R4.P | `grading-r4-regrade.md`; `models/library/analyses/mfe_heating_chain.sysml`; generic `:513,524` | Installed and operating powers under independent reserve/demand/efficiency changes |
| R4.S | `grading-r4-regrade.md`; generic heating cost `:707`; WI-050 procurement classification | Installed delivered capacity still prices equipment; demand alone does not substitute procurement |
| R5.S | `grading.md` Row 5; divertor account and calendar cost-per-event | Thermal/area proxy meaning and replacement account inclusion remain explicit |
| R6.S | `grading.md` Row 6; vessel-shell volume/cost and radial build | Final computed shell geometry and cost source; separate absence of pump equipment |
| R8.S | `grading.md` Row 8; turbine/electric/heat-rejection/misc accounts | Current design-point versus operating sizing classification and four cost-driver mappings |
| R11.S | `grading.md` Row 11; calendar CAS72, O&M and decommissioning | Final lifetime-dependent levelization/account basis; exact-dated shadow separately labeled |

[INHERITED] Reconfirm R1.S, R9.P and R12.P as `not_applicable` against the rubric, not as missing numeric scores. The final grader supplies every protocol field for all 23 scored cells plus those three applicability records: exact rubric/model versions, score, anchor, canonical/runtime/study evidence, why-not-next and grader. No final score or owner acceptance is supplied by this map.
