---
date: 2026-08-21T14:14:39-07:00
researcher: Claude
topic: "Which A/B technology comparison should RUN-STUDY Item 6 run on the Stellaris (concept 09) model, and what modeling changes would each candidate need?"
tags: [research, run-study, stellarator, item-6, magnet-technology, model-development]
status: complete
last_updated: 2026-08-21
---

# Research: Item 6 A/B candidates on the Stellaris model

**Date**: 2026-08-21 (PDT)
**Researcher**: Claude
**Research Type**: Codebase / Domain (model-development feasibility)

## Research Question

Which A/B technology comparison should RUN-STUDY Item 6 run on the Stellaris (concept 09) model, and what modeling changes would each candidate need? Four candidates were given: (1) HTS REBCO 20 K vs LTS Nb3Sn 4.5 K magnets, (2) steam Rankine vs helium Brayton / sCO2 power cycle, (3) ECRH vs NBI heating, (4) REBCO at 20 K vs 4.5 K. Each is judged on physical honesty in the current model, the exact modeling changes needed, second-arm data availability from admissible sources, and whether the swap block reaches an executing constraint.

**Hard rules honored.** Nothing under `knowledge/holdout/` was read. The out-of-holdout ARIES-CS extractions (`09-qi-stellarator-hts/iter-02/sources/aries-cs-*`, the `helios-stellarator-comparison` extraction in the same directory, and `36-helical-coil-stellarator/iter-02/sources/academia-144327326-*`) were not opened; all three are already on the barred list (`.project/completed/20260821_aries-cs-holdout/spec.md:35`, `design.md:116`). Disclosure: one `grep` for the concept-36 filename matched a line in `knowledge/holdout/aries-cs/PROTOCOL.md:37`; that single line (a barred-list entry) is the only holdout-directory content touched. Upstream 1costingFE values are quoted with line numbers from `/home/reid/1cfe/1costingfe/src/costingfe/` at the pinned commit `02543850`.

## Summary

- **Recommend candidate 1 (REBCO 20 K vs Nb3Sn 4.5 K), in a reduced honest form.** Today it is a cost-only swap that reaches no constraint (the Align's finding). It becomes honest with two small model additions, both inside the codegen arithmetic envelope: a closed-form volume-averaged beta computed from the profile referents and B (replacing the bound `beta`), and a conductor peak-field limit `B_axis * 2.767 <= B_max`. With those, the Nb3Sn arm is forced to 4.70 T on axis, its Point-A pressure violates the beta limit (beta ≈ 0.10 vs 0.05), and a per-arm density sweep shows the real trade: a $0.46B magnet set against roughly a quarter of the fusion power. One `work/` item, medium effort, one regenerated package, one store (the A/B stays values-only on the new package).
- **Candidates 2 (power cycle) and 3 (heating) run today with no model change** and both reach `net_positive` and `recirc_ok`. Both are sign-known scalar sensitivities dressed as A/Bs: every swapped value favors the same arm a priori. Candidate 3 also contradicts the Stellaris paper's own engineering argument against NBI (port size, TBR, neutron streaming), none of which the model can represent because TBR is bound.
- **Candidate 4 (REBCO 20 K vs 4.5 K) is not runnable honestly**: its only discriminating value ($/kA·m at 4.5 K) has no source in the repo, and its physics leverage is about 3 MW of cryo power out of 1078 MW gross.
- **Fifth candidate found: Stellaris operating Point A vs Point B** (Table 5 image). Every arm value is sourced, it reaches 4 of 5 constraints with no model change, and it is the best zero-modeling fallback. It is an operating-point comparison, not a technology one, so it does not satisfy the epic's "magnet-technology A/B" framing on its own; it pairs well with candidate 1 as a verification of the computed beta.
- **Blanket/breeder and fuel swaps are not viable**: TBR (1.074) and the blanket multiplier (1.2) are bound Stellaris neutronics results with no counterpart for any other breeder in an admissible source, and D-T is hard-wired (ash split 3.52/17.58 in the power balance, Bosch-Hale D-T coefficients in the handwritten reactivity, D-T fuel chemistry in CAS80).

## Detailed Findings

### 1. What the current model can and cannot see (the spine, in one paragraph)

Geometry (`R`, `a`, `kappa`, `f_shape`) gives plasma volume; the radial build gives layer volumes, wall area, and the coil bore `r_coil` (`mfe_plasma_scaling.sysml:4-130`). Fusion power integrates Bosch-Hale over the bound profile referents `n_D0`, `n_T0`, `T_i0`, `alpha_n`, `alpha_T` in a handwritten impl (`:132-219`); B does not enter it. The power balance turns `p_fus` into `p_net`, `rec_frac` via `eta_th`, `eta_pin`, `p_pump`, the coil/cooling/cryo loads (`mfe_power_balance.sysml:118-147`). The cryo chain turns `q_nuc_cryo`, `vol_cold_cryo`, `T_cold_cryo`, `f_carnot_cryo` into `p_cryo` (`mfe_cryo_plant.sysml:196-200`). Magnet cost is `G*B*R0*r_coil/(mu0*1000) * cost_per_kAm * coil_markup` (`mfe_magnet_cost.sysml:246-249`). The five constraints are inequalities on `p_net`, `rec_frac`, `beta`, `wall_load`, `tbr` (`mfe_viability.sysml`). Two of the five compare bound inputs: `beta_ok` reads `beta = 0.0276` and `tbr_ok` reads `tbr = 1.074` (`stellarator_plant.sysml:828,865,874-885`). So the only physics any magnet swap can reach today is the cryo term in the power balance.

Reachability as run for this research (`scripts/study/indicators.py`, report at `/tmp/claude-1000/-home-reid-1cfe-fusion-tea/509d7a47-428c-4aa4-b55b-b5c10e6fcbce/scratchpad/indicators.item6.json`, axes in `axes.item6.json` beside it):

| group (keys, `stellarator_09__stellaris__` prefix dropped) | constraints reachable | objectives reachable |
|---|---|---|
| c1 cost-only: `magnet__cost_per_kAm`, `magnet__coil_markup` | **none** (`no_constraint_response`, sound negative) | lcoe, lcoe_1cfe, total_capital |
| c1 full, current model: + `magnet__B`, `T_cold_cryo`, `f_carnot_cryo` | net_positive, recirc_ok (via the cryo term only) | + cas72 |
| c2 power cycle: `eta_th`, `turbine__cost_per_mw`, `heat_rejection__cost_per_mw`, `p_pump`, `eta_p` | net_positive, recirc_ok | cas72, lcoe, lcoe_1cfe, total_capital |
| c3 heating: `eta_pin`, `heating_nbi_per_mw`, `heating_ecrh_per_mw`, `p_nbi`, `p_ecrh` | net_positive, recirc_ok | same |
| c4 REBCO temperature: `magnet__cost_per_kAm`, `T_cold_cryo`, `f_carnot_cryo` | net_positive, recirc_ok | same |
| c5 Point A vs B: `n_D0`, `n_T0`, `n_e`, `T_i0`, `beta`, `p_input`, `p_ecrh` | beta_ok, net_positive, recirc_ok, wall_load_ok | + fuel |
| density fan-out: `n_D0`, `n_T0`, `n_e` | net_positive, recirc_ok, wall_load_ok | + fuel |

A reachable constraint is a possible module-graph path, never a claim that the axis responds (the tool's own disclosure). The "responds" judgments below are mine, from the equations.

### 2. Two facts that decide candidate 1

**(a) A computed beta is closed-form and stays in the envelope.** With the model's own profiles `n(rho) = n0 (1-rho^2)^alpha_n` and `T(rho) = T0 (1-rho^2)^alpha_T`, the volume average of `n*T` is `n0*T0 / (1 + alpha_n + alpha_T)` (the `u = 1-rho^2` substitution the fusion calc already documents at `mfe_plasma_scaling.sysml:142-143`). So

```
beta = 2*mu0 * sum_s [ n_s0 * T_s0 * e_keV / (1 + alpha_n,s + alpha_T) ] / B^2
```

uses only `+ - * / **`. Checked against the Table 5 image (`09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_009_table_0.png`, Point A: peak n_e 5.06e20, peak D and T 1.96e20 each, peak He 0.56e20, peak T_e 15.40 keV, peak T_i 14.63 keV, vol-av beta 2.76 %, B_0 9.0 T): with every species at alpha_n = 0.33 it gives 0.0283 (+2.5 %); with the electron exponent taken from the printed vol-av/peak pair (3.17/5.06 gives alpha_n,e = 0.596) and helium treated like electrons it gives 0.0267 (-3.3 %). Point B with the same recipe: 0.0285 vs printed 0.0281. The bound 0.0276 becomes a cross-check, not an input. That is exactly the policy's "internalize, retire the axis" move (`demo-study-parameterization-policy/policy.md` § 2.3).

**(b) The Nb3Sn arm cannot hold 9 T on axis.** Stellaris prints 24.9 T peak on the conductor at 9.0 T axis-averaged (Table 2 image, `images/page_002_table_0.png`), ratio 2.767. 1costingFE's sourced ceilings are REBCO 23.0 T, Nb3Sn 13.0 T, NbTi 9.0 T (`defaults.py:610-614`). So an honest Nb3Sn arm sits at B_axis ≤ 13.0/2.767 = **4.70 T**. At Point-A density and temperature that is beta ≈ 0.0276 × (9/4.70)² = **0.101**, violating the 0.05 limit. Holding beta at the limit allows 0.494× the Point-A pressure, which at fixed temperature is 0.494² ≈ 0.24× the fusion power, about **670 MW**. The magnet set at 4.70 T and $7/kA·m costs about $0.46B against today's $6.32B. Hand estimate of the LTS arm at the beta limit: p_th ≈ 830 MW, gross ≈ 275 MW, recirculating ≈ 140 MW, p_net ≈ 135 MW, rec_frac ≈ 0.5, so `recirc_ok` is marginal and LCOE is far higher despite the cheap magnets. Both arms' verdict columns carry information. This is a real design trade, not a unit-cost sensitivity.

**A finding the owner must rule on:** Stellaris's own 24.9 T peak exceeds 1costingFE's REBCO ceiling of 23.0 T (`defaults.py:605-612`, "engineering ceilings"). A peak-field constraint bound to the upstream table would flag the HTS arm itself. The per-coil peaks in the paper's Table 8 run 19.5–24.6 T (extraction `stellaris-design-details.md:1906-1920`; Table 8 image `images/page_022_table_0.png`). Options: (i) bind the REBCO arm's `B_max` to the Stellaris design value (24.9 T, the field it designs to) and disclose that it is above the upstream ceiling; (ii) bind 23.0 and let the HTS arm report `violated` at 9.0 T (it would pass at ≤ 8.31 T). Either is sourced; the choice is a ruling, not a lookup.

### 3. Candidate 1: HTS REBCO (20 K) vs LTS Nb3Sn (4.5 K)

**Honesty verdict.** Dishonest as-is (cost-only, no constraint responds, `no_constraint_response` on the cost block). Honest with (i) the peak-field limit and (ii) the computed beta. Sub-change (iii), a coil nuclear-heating budget forcing a thicker shield, is *not needed for the smallest honest version*: the Stellaris paper itself supplies the 4 K budget (EU DEMO ≈ 50 W/m³ peak nuclear heating, "designed for a 4 K cryogenic environment", `stellaris-design-details.md:1701-1710`) and the modeled 35.5 W/m³ sits under it, so the constraint would be satisfied in both arms at this radial build and has no discriminating power. It can be added as a cheap extra verdict (5 lines) but should not drive shield thickness without a neutronics model the repo does not have.

**Modeling changes (one `work/` item).**

| # | change | file | size | envelope |
|---|---|---|---|---|
| 1 | `calc def 'Volume-Averaged Beta'`: inputs `n_e0`, `T_e0`, `n_D0`, `n_T0`, `n_He0`, `T_i0`, `alpha_n_fuel`, `alpha_n_e`, `alpha_T`, `B`; defaulted `mu0`, `keV_J` (1.602176634e-16) declared last; out `beta` per § 2(a) | `models/library/analyses/mfe_plasma_scaling.sysml` (after `'Neutron Wall Load'`) | ~30 lines incl. MR-4 doc | yes: `+ - * / **` only; no function calls; defaults last per the migration rule (`mfe_plasma_scaling.sysml:33-38`) |
| 2 | `constraint def 'Conductor Peak Field Limit'`: `B_axis_in * peak_ratio_in <= B_max_in` | `models/library/analyses/mfe_viability.sysml` | ~15 lines | yes: the predicate compiler admits arithmetic operands (`/home/reid/1cfe/sysml-codegen/src/sysml_codegen/generation/predicate_compiler.py:52,160-174`) |
| 3 | Plant wiring: new attributes `n_e0`, `T_e0`, `n_He0`, `alpha_n_e` (the existing `n_e` is the vol-average, reference-only in profile mode, `stellarator_plant.sysml:385-387`); `calc beta_calc : 'Volume-Averaged Beta'` reading `magnet.B` the way `magnet_cost` does (`mfe_plant.sysml:282-289`) | `models/designs/generic_mfe/mfe_plant.sysml` | ~25 lines | yes |
| 4 | Instance: bind `n_e0 = 5.06e20`, `T_e0 = 15.40`, `n_He0 = 0.56e20`, `alpha_n_e = 0.596` (Table 5 image, all Point A); rewire `beta_ok` to `beta_calc.beta` and demote `beta = 0.0276` to a doc cross-check; bind `peak_ratio = 2.7667` (Table 2 image) and `B_max` (ruling, § 2); `assert constraint peak_field_ok` | `models/designs/stellarator_09/stellarator_plant.sysml:826-834,874-877` | ~30 lines | yes |
| 5 | Regenerate the package, re-pin `studies/manifest.json` and the known-answer fixtures (`tests/study/data/`), extend the oracle (`exploration/stellarator_e2e/verify_stellaris.py`) with the beta channel and the new constraint's operand binding (`oracle_entry.py`), update `tests/models/test_model_family_spines.py` | package + tests | mechanical | n/a |

Entry-point consequence: `beta` leaves the contract (the axis retires, policy § 2.3); `n_e0`, `T_e0`, `n_He0`, `alpha_n_e`, `peak_ratio`, `B_max` join it. The A/B then runs values-only on the regenerated package: **one fingerprint, one store**, no cross-fingerprint correlation section (the Align's two-store case does not arise).

**Second-arm data (Nb3Sn at 4.5 K).**

| value | arm B | source |
|---|---|---|
| `magnet__cost_per_kAm` | 7.0 $/kA·m | `costing_constants.yaml:57` (`conductor_cost_nb3sn`); `defaults.py:85` |
| `B_max` | 13.0 T | `defaults.py:613` (`MAGNET_TABLE["nb3sn"].b_max`) |
| `T_cold_cryo` | 4.5 K | `defaults.py:613` (`cryo_temp_k`) |
| `magnet__B` (axis) | ≤ 4.70 T | derived: 13.0 / (24.9/9.0); Table 2 image for the ratio |
| `magnet__coil_markup` | 5.87 (unchanged) | `costing_constants.yaml:60-75`: markup is keyed by concept, applied on the $/kA·m path for any SC conductor; the NCSX non-planar fabrication penalty is conductor-independent by the upstream's own structure |
| `p_tf` | 0.0 (unchanged) | `defaults.py:611-614` (`recirc_power_factor = 0.0` for every SC grade) |
| `q_nuc_cryo` | 35.5 W/m³ (unchanged) | Stellaris Table 6 image; a shield-neutronics result independent of conductor |
| coil heating budget at 4 K (optional constraint) | 50 W/m³ | `stellaris-design-details.md:1701-1710` (EU DEMO reference, 4 K) |
| `f_carnot_cryo` at 4.5 K | **no source in repo** | the model's declared assumption 0.20 (WI-024 D4, `stellarator_plant.sysml:573-586`) would be carried to both arms and disclosed; the ITER cryoplant calibration in the upstream (`cas22.py:690`, `docs/account_justification/CAS22_plant_systems.md:222-226`: 75 kW at 4.5 K, EUR 148M) and W7-X (7 kW at 4.5 K, `09-qi-stellarator-hts/iter-02/sources/pure-rest-items-item-2140562-component-file-2140561-content/output.md:223-225`) give capacity and cost, not electrical power, so no COP. A plant-efficiency datasheet or an ITER cryoplant power figure would supply it. Sensitivity: p_cryo 0.86 → 4.05 MW (of 1078 MW gross) |
| `vol_cold_cryo` | 136.56 m³ (held) | Nb3Sn's lower J_op would enlarge the winding pack in reality; Stellaris prints J_op 112–124 A/mm² for REBCO only (`stellaris-design-details.md:1906-1915`); no Nb3Sn winding-pack source in repo; held and disclosed |

**Constraint reach.** After the change: `peak_field_ok` (new, responds to `B`, `B_max`), `beta_ok` (responds to `B` and the densities), `net_positive`/`recirc_ok` (respond through `p_fus` once density is swept, plus the cryo term). `wall_load_ok` responds to the density sweep. Only `tbr_ok` stays inert.

**Per-arm sweep shape.** Each arm sweeps density as one tied fan-out {`n_D0`, `n_T0`, `n_e0`, `n_He0`} at fixed temperature (quasineutrality at the peak, 2×1.96 + 2×0.56 ≈ 5.06, is a scale-invariant tie). Arm B additionally either pins `B = 4.70` or sweeps `B` and lets `peak_field_ok` bind; the sweep is the better search framing (policy H1's 5–95 % feasible-fraction bar). A single point per arm would only show the LTS arm violating beta.

**Effort:** medium (library calc + constraint, plant wiring, instance rebind, regeneration, oracle, fixtures). **Risk of unit-cost sensitivity dressed as A/B:** low in this form (the constraint outcome dominates; magnet cost and fusion power move in opposite directions); high in the cost-only form.

### 4. Candidate 2: steam Rankine vs sCO2 Brayton

**Honesty verdict.** Runnable with no model change; physically coherent (the HCLL blanket is helium-cooled on the primary side, `stellaris-design-details.md:1342`, so either secondary cycle fits). But it is three scalars whose signs are known before the run.

**Modeling changes:** none. Swap block: `eta_th`, `turbine__cost_per_mw`, `heat_rejection__cost_per_mw` (the `Linear Power Cost` inputs, `mfe_plant.sysml:360-374`).

**Second-arm data.**

| value | arm B (sCO2) | source |
|---|---|---|
| `eta_th` | 0.47 | `defaults.py:583-584` (`POWER_CYCLE_DEFAULTS[BRAYTON_SCO2]`); justification `CAS23_26_balance_of_plant.md:188-199` |
| `turbine__cost_per_mw` | 0.15908 M$/MW → 159,080 $/MW | `defaults.py:585` |
| `heat_rejection__cost_per_mw` | 0.02258 M$/MW → 22,580 $/MW | `defaults.py:586` |
| `p_pump` under sCO2 | **no source in repo** | upstream injects only `eta_th`, `turbine_per_mw`, `heat_rej_per_mw` per cycle (`model.py:888-899`); `p_pump = 1.0` comes from the concept YAML regardless of cycle (`steady_state_stellarator.yaml:21`). Helios prints 22 MW coolant pumping for its 1.1 GWth PbLi/He Rankine plant (`05-planar-coil-stellarator/iter-01/sources/thea-energy-helios-arxiv-2512-08027/output.md:359`), but that is another plant; applying it here would be a fallback. Keep 1.0 in both arms and disclose |
| `eta_p` | unchanged | no cycle dependence in any source |
| the "Combined" preset | 0.53 / 0.24118 / 0.01847 | `defaults.py:588-592`, a third arm if wanted |

**Provenance wrinkle.** Arm A's `eta_th = 0.333` is the Stellaris paper's "single-element conversion efficiency of 1/3" (`stellaris-design-details.md:251`), not the upstream Rankine preset 0.40 (`defaults.py:579`). An A/B that pairs the paper's 1/3 with the upstream's 0.47 mixes provenance; the honest framing runs arm A at the paper's value and states that the upstream's own Rankine-vs-sCO2 delta is 0.40 → 0.47, or runs a third point at 0.40.

**Constraint reach:** `net_positive`, `recirc_ok` (through `p_et`); both respond. **Effort:** small. **Risk of unit-cost sensitivity dressed as A/B:** high. `eta_th` is a multiplier on gross power; the BOP rates fall; every term favors arm B, so the study can only report the magnitude of a foregone conclusion. Also the Kovari power-conversion paper in the repo (`09-qi-stellarator-hts/iter-02/sources/arxiv-1401-4232/`) is an abstract-only extraction with no numbers, and the ScienceDirect "optimized power conversion system for a stellarator" item (`sciencedirect-science-article-pii-s0196890422013504/output.md`) is a paywalled stub, so no stellarator-specific cycle data exists beyond Helios's Rankine figures (460 MW electric from 1094 MW thermal, `output.md:359`).

### 5. Candidate 3: ECRH vs NBI

**Honesty verdict.** Runnable with no model change, but not honest as a technology comparison. The Stellaris paper rejects NBI on grounds the model cannot represent: large ports that hurt tritium breeding and stream neutrons, MeV negative-ion capital, and wall-plug efficiency "typically below 30 %" (`stellaris-design-details.md:881-884`). TBR is bound (1.074), there is no port or streaming model, and the heating cost is linear per MW, so the model sees only two scalars.

**Modeling changes:** none. Swap block: `eta_pin`, `heating_nbi_per_mw`, `heating_ecrh_per_mw`, `p_nbi`, `p_ecrh` (`mfe_plant.sysml:337-354`; `p_input` stays 50).

**Second-arm data.**

| value | arm B (NBI) | source |
|---|---|---|
| `heating_nbi_per_mw` | 7.4639 M$/MW → 7,463,900 $/MW | `defaults.py:96`; `CAS22_reactor_components.md` (ITER NBI procurement basis) |
| `p_nbi` / `p_ecrh` | 50 / 0 | slots already exist; 50 MW is the Stellaris installed heating (Table 2 image) |
| `eta_pin` | **conflicting sources** | upstream: `eta_source_nbi = 0.60` (`costing_constants.yaml:103`, `defaults.py:105`) × `eta_couple`, where the stellarator's `eta_couple = 1.0` is an ECRH value (`steady_state_stellarator.yaml:15`; `docs/account_justification/heating_efficiency.md` table) and the tokamak NBI coupling 0.8333 is a back-fit to 0.50. No stellarator NBI coupling exists in the repo. Stellaris itself bounds NBI wall-plug at < 0.30 (`:883-884`). A study would have to pick one and carry the other as a disclosed disagreement |
| W7-X NBI | qualitative only | the paper mentions NBI as a W7-X fueling/density-control tool (`:810-811`); no efficiency or cost figure in any admissible source |

**Constraint reach:** `net_positive`, `recirc_ok` (the `p_input/eta_pin` term, `mfe_power_balance.sysml:134-136`); both respond. **Effort:** small. **Risk of unit-cost sensitivity dressed as A/B:** high, and the result would be read as the model endorsing or rejecting NBI on grounds it does not contain.

### 6. Candidate 4: REBCO at 20 K vs REBCO at 4.5 K

**Honesty verdict.** Not runnable honestly. The premise ($/kA·m falls at 4.5 K because J_c rises) has no value in the repo: the upstream carries one REBCO price (50, `costing_constants.yaml:56`) with a market range and long-term target but no temperature dependence (`CAS22_reactor_components.md:241-251`); the Stellaris paper gives J_op at 20 K only (`:1906-1915`) and no tape cost; the Faraday Factory tape-supply press item in the dossier (`09-qi-stellarator-hts/dossier.md:55-56`) has no price. A conductor J_c(B,T) datasheet or a tape price-per-kA·m at 4.2 K and 20 K would supply it.

**Modeling changes:** none. Swap block: `magnet__cost_per_kAm`, `T_cold_cryo`, `f_carnot_cryo`.

| value | arm B | source |
|---|---|---|
| `magnet__cost_per_kAm` at 4.5 K | **no source in repo** | see above |
| `T_cold_cryo` | 4.5 K | `defaults.py:613` is the LTS temperature; no source says REBCO is run at 4.5 K in a stellarator |
| `f_carnot_cryo` at 4.5 K | **no source in repo** | same gap as candidate 1 |

**Constraint reach:** formally `net_positive`, `recirc_ok`; the response is p_cryo 0.86 → 4.05 MW at the model's f_carnot, i.e. rec_frac moves by ~0.003. **Effort:** small. **Risk:** the whole comparison is one missing unit cost.

### 7. Fifth candidate: Stellaris operating Point A vs Point B

The Table 5 image prints two operating points of the same machine. Point B: vol-av n_e 4.21e20, peak n_e 6.89e20, peak D and T 2.60e20, peak He 0.83e20, peak T_e 12.25 keV, peak T_i 11.64 keV, vol-av beta 2.81 %, aux power 14.77 MW, fusion power 2700 MW, Q = 182. Every arm value is sourced from one image; nothing is upstream. With no model change the block reaches `beta_ok`, `net_positive`, `recirc_ok`, `wall_load_ok`. Notes: the model binds `p_input = 50` for Point A although the table prints 0 MW aux at operation (ignited), so the study must decide whether `p_input` is installed or absorbed power; Point B's printed beta (0.0281) would be a bound value unless candidate 1's beta calc lands first, in which case Point B becomes a verification (computed 0.0285). This is an honest, zero-modeling study but it is an operating-point comparison, not a technology A/B, and the epic's Item 6 objective is explicitly the "magnet-technology A/B" (`.project/backlog/epic_run_study_capability.md:386`).

### 8. Why blanket/breeder and fuel swaps are not viable

- **Blanket/breeder.** `tbr = 1.074` and `tbr_floor = 1.05` are bound (`stellarator_plant.sysml:865-871`), from the paper's 3D neutronics of the HCLL build; `mn = 1.2` likewise (`:454-456`). No admissible source gives a TBR or multiplier for a different breeder in this geometry, and the model has no neutronics, so the TBR verdict cannot move and a breeder arm would be a CAS27/CAS22.1.1 unit-cost swap (`cas27_fill_materials`, `costing_constants.yaml:203-214`) with no physics.
- **Fuel.** D-T is hard-wired: the ash fraction 3.52/17.58 in the power balance (`mfe_power_balance.sysml:92-101`), the D-T fusion energy `E_fus` and Bosch-Hale D-T coefficients in the handwritten reactivity (`mfe_plasma_scaling.sysml:150-158`), the D-T fuel chemistry in CAS80 (`stellarator_plant.sysml:777-803`), and the tritium constraint itself. A D-D or D-He3 arm would need a new reactivity impl and a new power split; that is a model family, not an A/B.

## Code References

- `models/library/analyses/mfe_plasma_scaling.sysml:132-219` — fusion power; B absent; profile forms that make the beta average closed-form (`:141-146`)
- `models/library/analyses/mfe_magnet_cost.sysml:246-249` — the only place B enters today
- `models/library/analyses/mfe_cryo_plant.sysml:196-200` — Carnot chain; T_cold and f_carnot
- `models/library/analyses/mfe_power_balance.sysml:118-147` — eta_th, eta_pin, p_cryo in the recirculating sum
- `models/library/analyses/mfe_viability.sysml:291-346` — `Beta Limit` and `TBR Floor` read bound inputs
- `models/designs/stellarator_09/stellarator_plant.sysml:90-148` — magnet bindings and the B-vs-peak mapping trap; `:457-465` eta_th/eta_pin; `:531-586` cryo chain; `:597-622` heating slots; `:826-885` beta/wall-load/TBR
- `models/designs/generic_mfe/mfe_plant.sysml:282-289` — `magnet_cost` reads `magnet.B` (the idiom a beta calc reuses); `:337-354` heating; `:360-374` BOP per-MW
- `exploration/stellarator_e2e/generated/contracts/model_contract.json` — 166 entry points; `beta`, `tbr` are design attributes; `recirc_ok__threshold` is a library default
- `scripts/study/indicators.py` — reachability tool; `tests/study/data/axes.known_answers.json` — axis format
- `/home/reid/1cfe/1costingfe/src/costingfe/defaults.py:578-592` — `POWER_CYCLE_DEFAULTS`; `:596-619` — `MagnetProperties` / `MAGNET_TABLE`; `:84-107` — conductor costs, heating per-MW, `eta_source_*`
- `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml:54-75` — conductor costs and concept-keyed markup; `:101-106` heating efficiencies
- `/home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py:271-295` — why peak-on-conductor does not enter the kA·m quantity (conductor derating "not modeled here")
- `/home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py:189-207` — the upstream's own `B0 = B_max * R_coil_inner / R0` form, the tokamak analogue of the peak-ratio constraint
- `/home/reid/1cfe/sysml-codegen/src/sysml_codegen/generation/predicate_compiler.py:50-52,160-174` — arithmetic admitted inside constraint predicates
- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_002_table_0.png`, `page_009_table_0.png` — Table 2 (24.9 T peak, 9.0 T axis) and Table 5 (Points A/B)
- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md:881-897` (NBI rejection), `:1701-1710` (4 K heating budget), `:1904-1920` (per-coil peak fields, J_op)

## Architecture Insights

- The policy's R1 example already anticipates candidate 1's mechanism: on-axis B is the lever, and conductor feasibility "enters as an inequality (B_conductor ≤ B_max,HTS), not as a solve" (`policy.md` § 4 R1). The peak-field constraint is that inequality, with the peak ratio a bound geometry fact rather than a computed field.
- Computing beta is an internalization in the policy's sense (§ 2.3, § 3 row 3): the bound `beta` was an axis the model could not defend, and the calc replaces it with physics the model derives from its own referents. It also converts `beta_ok` from an input check into a verdict that responds to B and density.
- `magnet.B` is the plant's only field; candidate 1 reuses it for physics by reading the part attribute into a calc, the pattern `magnet_cost` already uses. No new B attribute and no tie declaration is needed.
- Because the model change lands once and both arms run on the regenerated package, the A/B stays a values-only swap with one compatibility tuple. The Align's two-store case arises only if arms are run across the old and new packages, which nothing here requires.
- The upstream's sourced `MAGNET_TABLE` (ceilings and cryo temperatures) and `POWER_CYCLE_DEFAULTS` are the cleanest second-arm sources in the repo. They are sourced by the task's rule, but the REBCO ceiling (23 T) disagrees with the Stellaris design (24.9 T), which is itself a reportable model-development finding.

## Feasibility Assessment

- **Candidate 1, honest form:** feasible. Every executable expression stays in `+ - * / **`; defaults-last ordering is respected; the predicate arithmetic is admitted; the new inputs are all on the Table 5 / Table 2 images. The two unsourced quantities (f_carnot at 4.5 K, the Nb3Sn winding-pack volume) affect only the cryo term, whose whole swing is ~3 MW, and are carried as disclosed holds. Prerequisite: the stellarator-model-migration audit certification (SC2, SC11 open per `CURRENT_WORK.md`), since the work item regenerates the package on the same pin.
- **Candidates 2 and 3:** feasible now; they pass the runbook's step-4 gate without a ruling (constraints reachable) but fail the honesty bar the owner set ("a sensical comparison").
- **Candidate 4:** blocked on a missing value.
- **Candidate 5:** feasible now; honest; off the epic's stated framing.

## Recommendations

**Ranking.** 1. Candidate 1 in the reduced honest form. 2. Candidate 5 (Point A vs B) as the zero-modeling fallback and as candidate 1's beta verification. 3. Candidate 2. 4. Candidate 3. 5. Candidate 4.

**Smallest honest version of candidate 1.**

1. One `work/` item: `'Volume-Averaged Beta'` calc def, `'Conductor Peak Field Limit'` constraint def, plant wiring, instance rebind (Table 5 peaks, `alpha_n_e`, peak ratio 2.7667, `B_max`), `beta_ok` rewired, `beta` demoted to a doc cross-check, regeneration, manifest and fixture re-pin, oracle beta channel. Leave out the coil heating-budget constraint and any shield re-sizing.
2. Owner rulings before the item is planned: (a) REBCO arm `B_max`: Stellaris 24.9 T (designs-to) or upstream 23.0 T (ceiling, HTS arm then violates at 9 T); (b) `f_carnot_cryo` carried at the model's declared 0.20 in both arms with the 3 MW sensitivity disclosed; (c) Nb3Sn winding-pack volume held at 136.56 m³, disclosed.
3. Study shape: two arms on the regenerated package, one store. Arm A: REBCO block (`cost_per_kAm` 50, `T_cold_cryo` 20, `B_max` per ruling). Arm B: Nb3Sn block (`cost_per_kAm` 7, `T_cold_cryo` 4.5, `B_max` 13.0), `coil_markup` 5.87 and `p_tf` 0 in both. Each arm sweeps the tied density fan-out {`n_D0`, `n_T0`, `n_e0`, `n_He0`} at fixed temperature; arm B also sweeps `magnet__B` so `peak_field_ok` binds at 4.70 T rather than being pinned by hand. Report LCOE and all six verdicts per arm; expected first-order result: the LTS arm's feasible region sits at ≤ 0.49× the Point-A pressure and ~0.24× the fusion power, with `recirc_ok` marginal.
4. Oracle coverage: add `beta_calc__beta` and `magnet_capital` to the manifest's objective catalog for this demo (a magnet study moves magnet capital first; the Align left this to design).

**Alternatives.** If the owner declines new modeling for Item 6, run candidate 5 (honest, sourced, four constraints) and file candidate 1's two model additions as the model-development finding the record must carry for the `no_constraint_response` cost block.

**Next steps.** Take the rulings in (2) to the owner with this document; then `/_my_design` records the comparison and names the `work/` item; Item 6 pauses until that item closes and the package is regenerated (spec [NEED], Align § 2).

## Open Questions

- REBCO `B_max` for arm A (24.9 T design value vs 23.0 T upstream ceiling). A ruling, not a lookup.
- Whether helium ash should share the electron density exponent (0.596, derived from the printed vol-av/peak pair) or the fuel exponent (0.33); the two choices bracket the printed beta at -3.3 % / +2.5 %. The design should pick one and record the other as the tolerance.
- Whether `p_input = 50` is installed heating or absorbed power at the operating point (Table 5 prints 0 MW aux at Point A). Affects candidate 5 and the recirculating term in every candidate; today the model treats it as installed and always drawn.
- A sourced fraction-of-Carnot at 4.5 K (ITER or W7-X cryoplant electrical power) would close the one disclosed hold in candidate 1; none is in the repo.
- The dossier's WCLL inference (`09-qi-stellarator-hts/dossier.md:43-44`) disagrees with the paper's HCLL (`stellaris-design-details.md:1342`); the model follows the paper. Worth a dossier correction, outside this item.
