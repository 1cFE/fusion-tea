# Evidence Map — for the fresh grader

**Created:** 2026-08-30 (rubric author). **Contains pointers only — no proposed scores.** Read the rubric first (`rubric.md`, at its frozen sha); score each cell by its anchor tests against the evidence below plus anything else you find. This map is a starting index, not a boundary: if it omits something relevant, cite what you actually read.

**Identity for runtime claims:** current executed baseline is the post-pumping-rebase package — `exploration/stellarator_e2e/studies/20260829-p-pump-fence/results/baseline_result.json` (model identity, exact point, per-module channels, six qualified verdicts). The discovery log is `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`. Unqualified filenames live in `models/library/analyses/`; "instance" is `models/designs/stellarator_09/stellarator_plant.sysml`; "plant" is `models/designs/generic_mfe/mfe_plant.sysml`.

## Row 1 — Plasma / operating point

- Calc defs: `mfe_plasma_scaling.sysml:4` (Plasma Geometry), `:132` (DT Fusion Power, Bosch-Hale, handwritten-seam impl at `exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py`), `:257` (Volume-Averaged Beta), `:328` (Conductor Peak Field).
- Confinement explicitly out of scope ("Rung C"): `mfe_plasma_scaling.sysml:150-166`.
- Constraints: `mfe_viability.sysml:40` (Beta Limit); asserted in instance (`beta_ok`, instance ~`:931`).
- Held: densities, temperature, profile exponents (instance `:335-524`).
- Study: field never rewarded through confinement — `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/synthesis.md:38-44,89-93`.

## Row 2 — Radial build / FW / blanket / shield / TBR / lifetime

- Calc defs: `mfe_plasma_scaling.sysml:44` (MFE Radial Build, 11 layers), `:221` (Neutron Wall Load); `mfe_account_costs.sysml:22` (Blanket Cost), `:52` (Shield Cost), `:794` (Levelized Replacement Cost — CAS72 life computed from fluence ÷ wall load).
- Part defs: blanket 3-attr part at `models/designs/generic_mfe/mfe_subsystems.sysml:26`; plant children `mfe_plant.sysml:44-103`.
- TBR held: instance `:922` (tbr = 1.074) vs `:926` (tbr_floor = 1.05), asserted bound-vs-bound at `:939` (`tbr_ok`); constraint def `mfe_viability.sysml:79`.
- Wall load: limit at instance `:911` area, assert `wall_load_ok` ~`:935`; constraint def `mfe_viability.sysml:60`.
- Studies: wall load binds repeatedly — `studies/20260821-power-cycle-ab/synthesis.md:122-139`; TBR structurally inert — `studies/20260829-p-pump-fence/synthesis.md:58-71`.

## Row 3 — Magnets / structures / power supplies / cryo

- Cost: `mfe_magnet_cost.sysml:4-60` (conductor kA·m × markup; markup swallows winding, quench, cryostat, testing — see doc comment). Part def: `models/library/cost_structure/mfe_power_core.sysml:65` (8 attrs). Power supplies: `mfe_account_costs.sysml:140`. Structure: `:81`.
- Physics: peak field computed (`mfe_plasma_scaling.sysml:328`); constraint `mfe_viability.sysml:97` (Conductor Peak Field Limit). Cryo chain: winding-pack heat → cryoplant electric, instance `:502-636` (q_nuc_cryo, vol_cold_cryo computed, f_carnot_cryo assumption).
- No stress, current-density, quench, or winding-pack feedback anywhere (verify by absence).
- Studies: magnet capital largest channel — `studies/20260829-p-pump-fence/results/baseline_result.json:43,60`; field errata moved $4.39B → $6.32B — `studies/DISCOVERY_LOG.md:19-23`; missing field/stress loops — `studies/20260823-magnet-technology-ab/synthesis.md:89-93`.

## Row 4 — Heating / CD / fueling / control

- Held: fixed ECRH power, `eta_pin = 0.5` wall-plug × coupling (instance `:499-501`, `:645-678`).
- Cost: `mfe_account_costs.sysml:196` (Heating Cost, linear installed-cost relation).
- Power balance receives input power: `mfe_power_balance.sysml:90-148`.

## Row 5 — Divertor

- Cost: `mfe_account_costs.sysml:168-194` (aggregate thermal-power relation); replacement grouping in `:794-880`.
- No divertor-specific geometry, heat-flux, or constraint (verify by absence).

## Row 6 — Vacuum vessel / vacuum

- Cost: `mfe_account_costs.sysml:108-138` (volume-based; doc comment explicitly omits gas-load pumping).
- Shell volume from radial build; no ports, conductance, structural sizing (verify by absence).

## Row 7 — Primary heat transport / power balance

- Calc: `mfe_power_balance.sysml:4-148` (fusion split, blanket multiplication, thermal/gross/net, parasitics, recirculating fraction).
- Held: `p_pump = 195.0` (instance `:502`, WI-033 helium-circulator basis, owner-ruled held), `p_cool` (~`:555-566`), `eta_p = 0.5` (`:496`).
- Constraints: `mfe_viability.sysml:4` (Net Power Positive), `:21` (Economic Recirculating Threshold) — check which operands are computed vs held.
- Costs: `mfe_account_costs.sysml:526` (Coolant), `:559` (Aux Cooling).
- Study: pumping rebase moved LCOE 21%, fence 32 → 184 violating points, 42 unevaluable negative-net points — `studies/20260829-p-pump-fence/synthesis.md:31-43`.

## Row 8 — Power conversion / electric / heat rejection / misc

- Held: `eta_th = 0.333` (instance `:493`).
- Costs: `mfe_account_costs.sysml:226` (Linear Power Cost — turbine, electric plant, heat rejection, misc via power scalings).
- Study: efficiency moved LCOE 13.3–23.4%; equipment rates ≤1.1% — `studies/20260821-power-cycle-ab/synthesis.md:63-76`.

## Row 9 — Buildings / site / hot cell / RH

- Costs: `mfe_account_costs.sysml:304` (Buildings, six grouped bases), `:366` (Preconstruction), `:476` (Remote Handling), `:503` (Installation Labor).
- Defect (evidence-integrity, not a level): CAS10 land expression can fail before `net_positive` reports — `studies/20260829-p-pump-fence/synthesis.md:41-43,64-81`.

## Row 10 — Fuel / tritium

- Cost: `mfe_account_costs.sysml:730-792` (DT Fuel — annual feed from fusion energy, burn fraction, recovery, availability).
- Instance fuel block: ~`:833-877`. No inventory, startup, processing, decay anywhere (verify by absence).

## Row 11 — Availability / replacement / maintenance

- Held: `availability = 0.85` (instance `:812`).
- Computed: replacement interval and levelized cost (`mfe_account_costs.sysml:794-880`); O&M `:403`.
- Study finding: `no_constraint_response` on availability; nothing couples it to core life or outage — `studies/20260821-power-cycle-ab/synthesis.md:159-170`.

## Row 12 — CAS rollup / financing / LCOE / estimate quality

- `models/library/cost_structure/cas_hierarchy.sysml` (CAS tree; 6-digit codes only in doc comments).
- `mfe_account_costs.sysml:255` (Contingency), `:276` (Indirect), `:643` (IDC), `:670` (Levelized Annual), `:891` (Annual Rollup), `:913` (Capital Charge), `:943` (1cfe-Form LCOE).
- Deterministic point assumptions; no estimate class or uncertainty treatment (verify by absence).
- Study: economic assumptions move the objective without changing physical verdicts — `studies/20260821-power-cycle-ab/synthesis.md:87-101`.
