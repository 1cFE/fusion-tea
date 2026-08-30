# Grading — Depth Rubric v1, Initial Scores

**Date:** 2026-08-30
**rubric_version:** `.project/active/demo-depth-rubric/rubric.md@dc0f0b6d`
**model_version:** `dc0f0b6d` (branch `feat/demo-maturation`; all `models/` files read at this commit)
**Package identity (for executed-behavior claims):** `exploration/stellarator_e2e/studies/20260829-p-pump-fence/results/baseline_result.json` — `executed_under.identity_digest f97f084818723224bdd7f604a63e1941dadeb3e99af0cca3c9c6d30280d312f0`, `case_id stellarator-baseline-point-v1:c0000`; semantic fingerprint `f08daa7b…` per `exploration/stellarator_e2e/studies/manifest.json` `recorded_provenance`. Baseline headline lcoe = 333.0670332813743, six verdicts all `satisfied`.
**Grader:** fresh grader session, 2026-08-30 (non-author; received the rubric and the pointer-only evidence map, no proposed scores; every citation below was opened and read by this session)

Scoring applied exactly as written: highest level whose full evidence test is satisfied, integers only, no partial credit; row-specific anchors are the operative tests; correctness defects recorded as evidence-integrity findings, never as levels.

## Summary table

| Row | Area | P score / P target | S score / S target |
|---|---|---|---|
| 1 | Plasma / operating point | **2** / 3 | not_applicable (confirmed) |
| 2a | Build & wall load | **3** / 3 | — |
| 2b | In-vessel material lifetime | **2** / 3 | — |
| 2c | Tritium breeding | **1** / 3 | — |
| 2 (S) | Blanket/shield structure & cost | — | **3** / 3 |
| 3 | Magnets, structures, PS, cryo | **1** / 3 | **2** / 3 |
| 4 | Heating / CD / fueling / control | **1** / 2 | **2** / 2 |
| 5 | Divertor | **1** / 3 | **2** / 2 |
| 6 | Vacuum vessel & vacuum | **1** / 2 | **2** / 2 |
| 7 | Heat transport / power balance | **1** / 3 | **2** / 3 |
| 8 | Power conversion / BOP | **1** / 2 | **2** / 2 |
| 9 | Buildings / site / hot cell / RH | not_applicable (confirmed) | **2** / 3 |
| 10 | Fuel & tritium cycle | **1** / 2 | **1** / 2 |
| 11 | Availability / replacement / maint. | **1** / 3 | **2** / 2 |
| 12 | CAS rollup / financing / LCOE | not_applicable (confirmed) | **2** / 3 |

Largest target-gaps (target − score = 2): R2c.P, R3.P, R5.P, R7.P, R11.P. No cell is `ungraded`.

---

## Row 1 — Plasma geometry, fusion performance, operating-point closure

**cell_id:** R1.P
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "Fusion power, beta, wall load, peak field forward-computed from geometry, profiles, and field, verified in execution"
- **model_evidence:** fusion power: `models/library/analyses/mfe_plasma_scaling.sysml:132` ('DT Fusion Power', profile-integrated Bosch-Hale) **plus** its handwritten-seam executable `exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py` (`AUTO_IMPLEMENTED = False`, normative — both cited per the codegen-seam rule); volume: `mfe_plasma_scaling.sysml:4` wired at `models/designs/generic_mfe/mfe_plant.sysml:120`; beta: `mfe_plasma_scaling.sysml:257` wired at `mfe_plant.sysml:198`; wall load: `mfe_plasma_scaling.sysml:221` wired at `models/designs/stellarator_09/stellarator_plant.sysml:915`; peak field: `mfe_plasma_scaling.sysml:328` wired at `mfe_plant.sysml:213`; profile/geometry inputs bound from source at instance `:346-462`.
- **runtime_evidence:** baseline_result.json channels — `fusion__p_fus` = 2748.0568768605704, `geom__V` = 425.0000143721807, `beta_calc__beta` = 0.026834157382368398, `wall_load_calc__wall_load` = 3.131234717504045, `peak_field_calc__B_peak` = 24.9; study verification at this pin passed at worst rel. deviation 6.3463e-16 (`20260829-p-pump-fence/synthesis.md` §4).
- **study_evidence:** `beta_ok` and `wall_load_ok` produced real fence structure over swept (B, density) and (R, a) — `20260823-magnet-technology-ab/synthesis.md` §2/§4; `20260829-p-pump-fence/synthesis.md` §4.
- **why_not_next:** no confinement/transport relation links field and heating to density and temperature — densities, temperatures, and profile exponents are held source referents (instance `:450-462`), confinement is explicitly out of scope ("Rung C", `mfe_plasma_scaling.sysml:150-166` doc), and the committed study consequence is that field is never rewarded so the optimum drives to the lowest B the beta limit allows (`20260823-magnet-technology-ab/synthesis.md` finding #4).
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R1.S
- **score:** not_applicable — confirmed. The plasma has no hardware part or CAS account of its own; its structure is the calc spine (`mfe_plant.sysml:120-283`) and its cost lives in rows 3/4.
- **grader:** fresh grader session, 2026-08-30

## Row 2 — Radial build, FW, blanket, shield, TBR, lifetime

**cell_id:** R2a.P (build & wall load)
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 3
- **anchor_satisfied:** "2a: wall-load limit pushes back on the design" (P2 conjunct also verified: "build radii and wall load computed from geometry and power" — 11-layer cumulative radial build and wall load are forward-computed)
- **model_evidence:** radial build: `mfe_plasma_scaling.sysml:44` ('MFE Radial Build': cumulative radii, four CAS22 volumes, `wall_area`, `r_coil`) wired at `mfe_plant.sysml:145` from instance thicknesses `stellarator_plant.sysml:366-`; wall load computed from `fusion.p_fus` and `rb.wall_area` at instance `:915`; executable constraint `wall_load_ok` compares the **computed** operand to the engineering limit 4.05 MW/m² — constraint def `models/library/analyses/mfe_viability.sysml:60`, limit bound at instance `:911`, asserted at `:935`.
- **runtime_evidence:** `wall_load_calc__wall_load` = 3.1312 and `wall_load_ok` `satisfied` at the baseline point (baseline_result.json verdicts).
- **study_evidence:** the limit genuinely pushes back on design choices: `wall_load_ok` violated at 353 of 906 points (every a ≥ 1.70) and the constrained optimum sits on the wall-load fence in every arm — `20260821-power-cycle-ab/synthesis.md` §3/§4.2; re-confirmed at the current pin, `20260829-p-pump-fence/synthesis.md` §4 (violated 353/906, wall load 4.16469 at a = 1.70 vs limit 4.05).
- **why_not_next:** no neutronics/damage closure across the build (no transport/damage model connects the layer stack to fluence or DPA), and no design search with independent check over a justified uncertainty range exists.
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R2b.P (in-vessel material lifetime)
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "2b: lifetime computed from fluence and wall load"
- **model_evidence:** `models/library/analyses/mfe_account_costs.sysml:794` ('Levelized Replacement Cost': core_lifetime_FPY = clip(fluence_limit / max(q_n, 1e-6), …), q_n from p_fus and firstwall_area) **plus** the handwritten-seam executable `exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py` (`AUTO_IMPLEMENTED = False`, normative, guards carried verbatim — both cited per the codegen-seam rule); wired at `mfe_plant.sysml:735` with `fluence_limit` = 18.0 bound at instance `:863` and exact `ash_frac` at `:866`.
- **runtime_evidence:** `cas72_calc__cost` = 97066502.37 $/yr at the baseline point (baseline_result.json).
- **study_evidence:** `cas72` is a declared study objective and moved under swept geometry — manifest.json objective_catalog; `20260829-p-pump-fence` indicators cited in synthesis §3.
- **why_not_next:** the computed lifetime feeds the CAS72 replacement schedule but **not** availability — availability is held at 0.85 (instance `:812`) and carries `no_constraint_response` (nothing couples it to core life or outage; `20260821-power-cycle-ab/synthesis.md` finding #1, re-confirmed at the current pin in `20260829-p-pump-fence/synthesis.md` §3), so the "feeds replacement schedule and availability" conjunction of P3 fails.
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R2c.P (tritium breeding)
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 1
- **anchor_satisfied:** "Thickness, lifetime, or TBR held as cited values" — TBR = 1.074 held as a cited source value at instance `:922`, floor 1.05 at `:926`.
- **model_evidence:** `stellarator_plant.sysml:922` (tbr), `:926` (tbr_floor), `:939` (`tbr_ok` assert); constraint def `mfe_viability.sysml:79`. This is the rubric's named type case: a bound value checked against another bound value is not P3, and it is not P2 either — nothing computes TBR from blanket configuration; changing blanket thickness or breeder chemistry does not re-derive it.
- **runtime_evidence:** `tbr_ok` `satisfied` at the baseline (baseline_result.json verdicts) — but the operand is a constant, so the verdict carries no design response.
- **study_evidence:** `tbr_ok` structurally inert: `constraints_unreachable` for every swept axis, satisfied ×906 with bound-vs-bound flagged — `20260829-p-pump-fence/synthesis.md` §4; `20260821-power-cycle-ab/synthesis.md` §4.1 (bound vs bound).
- **why_not_next:** no calculation derives TBR from blanket configuration (breeder volume, enrichment, structure fraction) anywhere in `models/`.
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R2.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 3
- **anchor_satisfied:** "Replaceable units vs life-of-plant components separately sized; replacement logic follows computed life"
- **model_evidence:** the in-vessel component classes are independently sized from the radial build and separately costed: blanket (fw+blanket+reflector volumes → 'Blanket Cost' `mfe_account_costs.sysml:22`, wired `mfe_plant.sysml:326`), shield (ht+lt → 'Shield Cost' `:52`, wired `:334`), structure (`:81`/`:342`), vessel (`:108`/`:349`) — four distinct engineered volumes from `mfe_plasma_scaling.sysml:44`, not one lump inherited by children; the replaceable set (blanket C220101 + divertor C220108) is distinguished from the life-of-plant set (shield, structure, vessel) exactly as the CAS literature's replaceable/life-of-plant split, and its replacement cost follows the **computed** fluence life through CAS72 (`mfe_account_costs.sysml:794`; `replacement_cost_per_event` at `mfe_plant.sysml:723`); installation labor (`:492`) and spares (CAS50 spares_frac, `:622`) exist as explicit logic.
- **runtime_evidence:** per-account channels at the baseline: blanket $722.83M, shield $454.84M, structure $30.89M, vessel $107.11M, `replacement_cost_per_event` $832.41M, `cas72_calc__cost` $97.07M/yr (baseline_result.json).
- **study_evidence:** CAS72 responds to swept geometry as an objective (manifest.json objective_catalog; `20260829-p-pump-fence/synthesis.md` §3).
- **why_not_next:** no design-based estimate per component class — costs are volume × representative installed unit costs (the conceptual-study fallback the S3/S4 boundary names), with no fabrication basis or stated estimate uncertainty.
- **grader:** fresh grader session, 2026-08-30

## Row 3 — Magnets, structures, power supplies, cryogenics

**cell_id:** R3.P
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 1
- **anchor_satisfied:** "Field a cited input; nothing derives it" — B = 9.0 T is a cited source constant (instance `:133`); no calculation derives field from coil geometry or coil current anywhere (the ampere-meter quantity in the cost model is derived **from** B, `mfe_magnet_cost.sysml:44`, never the reverse).
- **model_evidence:** the P2 test is a conjunction and its first half fails: "peak field computed from geometry and coil current" — `B_peak = B_axis × peak_ratio` (`mfe_plasma_scaling.sysml:328`) multiplies a held field (instance `:133`) by a held coil-set ratio (`:153`, the IEEE-exact 24.9/9.0); changing coil geometry or current re-derives nothing. The second half **is** met: cryo load computed from winding-pack heat — `models/library/analyses/mfe_cryo_plant.sysml:4` wired at `mfe_plant.sysml:272` from q_nuc_cryo (instance `:588`), vol_cold_cryo (`:591`, held input per study finding), f_carnot (`:630`). `peak_field_ok` (`mfe_plant.sysml:836`) compares held × held against held B_max = 24.9 (instance `:161`) — the scoring rule "a bound value checked against another bound value is not P3" applies (margin is 0.0 at the design point by construction of the literal ratio). No stress, current-density, quench, or winding-pack feedback exists anywhere in `models/` (verified by absence across mfe_plasma_scaling, mfe_magnet_cost, mfe_viability, mfe_plant, the instance).
- **runtime_evidence:** `peak_field_calc__B_peak` = 24.9 exactly; `cryo_elec__p_elec` = 0.8643516 MW (baseline_result.json).
- **study_evidence:** `20260823-magnet-technology-ab/synthesis.md` findings #3 (no coil-thickness/radial-build/stress coupling; B_max only a verdict bound) and #4 (B reaches no plasma channel but beta; optimum always the lowest B the beta limit allows); DISCOVERY_LOG.md rows of 2026-08-23.
- **why_not_next:** P2 needs the peak field derived from coil geometry and current — it is a held axis field times a held ratio — and P3 additionally needs a stress or current-density limit pushing back on coil sizing, which does not exist.
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R3.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "Cost follows an engineered quantity (e.g. conductor kA·m) with source basis"
- **model_evidence:** 'Magnet Coil Cost' `models/library/analyses/mfe_magnet_cost.sysml:4-49`: total_kAm = G·B·R0·r_coil/(μ0·1000) from Ampère's law, cost = kA·m × $/kA·m × markup, with r_coil forward-computed from the radial build (`mfe_plant.sysml:50,316`); full source citations to cas22.py. Separately homed siblings exist: power supplies (`mfe_account_costs.sysml:140`, wired `mfe_plant.sysml:356`), primary structure (`:81`/`:342`), cryoplant capital (C220302 inside 'Aux Cooling Cost' `:559`, wired `:513`, driven by the **computed** p_cryo).
- **runtime_evidence:** `magnet_cost__capital_cost` = $6.3235B (largest single channel, 50%+ of power-core capital: `powercore_capital` = $8.093B), `power_supplies_cost__cost` = $80.54M, `aux_cooling__cost` = $20.37M (baseline_result.json).
- **study_evidence:** magnet capital moved $4.39B → $6.32B on the single field errata (DISCOVERY_LOG context; instance doc history at `stellarator_plant.sysml:60-75`) — depth here is load-bearing.
- **why_not_next:** S3 requires winding pack, structure, power supplies, and cryoplant as separately sized sub-accounts — the winding pack, quench protection, cryostat, and testing are all swallowed by the single 5.87 markup (`mfe_magnet_cost.sysml` doc; instance `:147`), so the magnet itself is one engineered-quantity lump.
- **grader:** fresh grader session, 2026-08-30

## Row 4 — Heating, current drive, fueling, plasma control

**cell_id:** R4.P
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 1
- **anchor_satisfied:** "Injected power and efficiencies held as cited constants" — p_input = 50 MW (instance `:487`), p_ecrh = 50 MW (`:677`), eta_pin = 0.5 (`:499`, gyrotron wall-plug × coupling 1.0) all held.
- **model_evidence:** there is no heating-system calc: the only arithmetic is the `p_input_in / eta_pin_in` term inside the power-balance recirculating sum (`mfe_power_balance.sysml:117-121` region, recirculating expression) — the governing outputs (installed power, coupled power) are held constants, and changing the plasma or launcher design re-derives nothing. The P2 anchor's "wall-plug → coupled-power chain computed with a stated deposition assumption, verified" is not met by a single held-ratio division with no chain elements (source, transmission, launcher, deposition) represented; the deposition assumption exists only as prose in the eta_pin binding doc (instance `:499-501`).
- **runtime_evidence:** the held values enter the executed recirculating sum (rec_frac verdicts at baseline; oracle-side wall-plug 100 MW documented in DISCOVERY_LOG 2026-08-28 row's recirc recipe).
- **study_evidence:** none load-bearing beyond the recirc term.
- **why_not_next:** P2 needs a computed wall-plug → coupled-power chain with a stated deposition assumption verified in execution; no such calc def exists (the seam would need at minimum a heating-chain calc whose output re-derives when efficiencies or delivered power change independently).
- **grader:** fresh grader session, 2026-08-30 — see grader note G1 (this cell is the closest judgment call in the report).

**cell_id:** R4.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "Cost follows installed heating power with source basis"
- **model_evidence:** 'Heating Cost' `mfe_account_costs.sysml:196`: per-method installed power × ITER-procurement-calibrated $/MW; wired at `mfe_plant.sysml:379`; ECRH rate $5.2829M/MW × 1e6 bound at instance `:674`, ECRH-only mix (nbi/icrf/lhcd zeroed with source rationale, instance `:645-678`).
- **runtime_evidence:** `heating_cost__cost` = $264.145M = 5282900 × 50 exactly (baseline_result.json).
- **why_not_next:** S3 requires sources, transmission, launchers costed separately with replacement logic on replaceable components — the account is one linear per-MW line and heating is not in the CAS72 replaceable set (`mfe_plant.sysml:723`).
- **grader:** fresh grader session, 2026-08-30

## Row 5 — Divertor and plasma-facing maintenance

**cell_id:** R5.P
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 1
- **anchor_satisfied:** "Divertor loads held or implied by a fixed share" — the divertor's thermal duty is implied only through the cost relation's plant-thermal power-law (base × (p_th/1000)^0.5) and its damage life only through membership in the FW-fluence CAS72 group.
- **model_evidence:** `mfe_account_costs.sysml:168-194` ('Divertor Cost', power-law in plant p_th); replaceable grouping at `mfe_plant.sysml:723` (blanket + divertor share one fluence-limited event). No divertor geometry, exhaust-power split, heat-flux estimate, or divertor-specific constraint exists anywhere in `models/` (verified by absence: mfe_plasma_scaling, mfe_power_balance, mfe_viability, the instance).
- **runtime_evidence:** `divertor_cost__cost` = $109.57M (baseline_result.json).
- **why_not_next:** P2 needs divertor heat flux estimated from exhaust power and geometry, verified — no exhaust-power channel or divertor area exists to compute one.
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R5.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "Cost follows divertor thermal power or area with source basis" — met under the source's own account definition: the driver is the computed plant thermal power (the 1cfe divertor account's stated scaling basis, cas22.py:570), a computed performance driver with explicit CAS home (CAS22.1.8) and source basis.
- **model_evidence:** `mfe_account_costs.sysml:168-194`; wired at `mfe_plant.sysml:364` from the computed p_th; base bound at instance `:682`.
- **runtime_evidence:** `divertor_cost__cost` = $109.57M tracks the computed p_th (baseline_result.json).
- **why_not_next:** S3 needs targets/cassettes as replaceable units with replacement logic from **computed divertor** life — the divertor inherits the first-wall fluence life inside a grouped event, with no divertor-specific life or unit decomposition.
- **grader:** fresh grader session, 2026-08-30 — see grader note G2 (plant p_th vs divertor thermal power).

## Row 6 — Vacuum vessel and vacuum systems

**cell_id:** R6.P
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 1
- **anchor_satisfied:** "Vessel dimensions held; vacuum system absent" — vessel thickness held (instance `:366-` block, vessel_t = 0.10), radii derived from held thicknesses; the vacuum system (gas load, pumping) is absent by explicit doc ("the gas-load pumping sub-term … is omitted", `mfe_account_costs.sysml:108-138`).
- **model_evidence:** shell volume **is** forward-computed from the radial build (`mfe_plasma_scaling.sysml:44` → vessel_vol; wired `mfe_plant.sysml:74,349`), which satisfies half of P2, but the P2 conjunction also requires "a computed gas-load/pumping estimate, verified" and none exists anywhere in `models/` (verified by absence).
- **runtime_evidence:** `vessel_cost__cost` = $107.11M from the computed vessel_vol = 157.933 m³ (baseline_result.json; instance doc `:223`).
- **why_not_next:** no gas-load/pumping estimate exists; the vessel cost doc marks it a Stage-3 deepening item.
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R6.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "Cost follows computed shell volume/mass with source basis"
- **model_evidence:** 'Vessel Cost' `mfe_account_costs.sysml:108`: unit_cost × vessel_vol × (p_et/ref)^0.6, vessel_vol from the radial build; unit cost sourced at instance `:223`.
- **runtime_evidence:** `vessel_cost__cost` = $107.11M (baseline_result.json).
- **why_not_next:** S3 needs shell, ports, and pumping train as separately sized subaccounts — only the shell exists.
- **grader:** fresh grader session, 2026-08-30

## Row 7 — Primary heat transport and plant power balance

**cell_id:** R7.P
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 1
- **anchor_satisfied:** "Pumping, parasitics, efficiencies held as cited constants" — p_pump = 195.0 held by owner ruling (instance `:502`, WI-033), p_tfcool = 15.0 (`:551`), p_trit = 10.0 (`:569`), p_house = 4.0 (`:572`), eta_p = 0.5 (`:496`), eta_th = 0.333 (`:493`) all held with citations.
- **model_evidence:** the power-balance aggregation itself is fully computed and executed ('MFE Power Balance Calc' `models/library/analyses/mfe_power_balance.sysml:4`, wired `mfe_plant.sysml:283`; auto-generated impl `handwritten/mfe_power_balance/mfe_power_balance_calc_impl.py` `AUTO_IMPLEMENTED = True`), and the cryo parasitic is derived (`mfe_cryo_plant.sysml:4`), but the row's P2 test — "pumping and parasitic loads forward-computed from loop flow and pressure drop" — fails: there is no loop model (no flow, no pressure drop, no ΔT), and the dominant load p_pump is a held scalar. The P3 test fails for the same reason: `recirc_ok` (`mfe_plant.sysml:830`; def `mfe_viability.sysml:21`) receives a computed rec_frac, but its pumping operand is a held constant, so coolant choices cannot push back — the rubric's row text names exactly this bar.
- **runtime_evidence:** six verdicts at baseline including `recirc_ok` and `net_positive` `satisfied` (baseline_result.json); rec_frac/p_net operand values recoverable via the oracle recipe (DISCOVERY_LOG 2026-08-28 `declared seam` row) — see evidence-integrity finding EI-2.
- **study_evidence:** the strongest error-history signal in the repo: re-basing held pumping 1 → 195 MW moved LCOE +21.0% (275.264 → 333.067), grew the `recirc_ok` fence from 32 to 184 violating points reaching the window's full R extent, and exposed 42 unevaluable negative-net points — `20260829-p-pump-fence/synthesis.md` §§1-2, §6; DISCOVERY_LOG rows 2026-08-28/29. A held input moving the objective by a fifth is precisely the depth gap this row measures.
- **why_not_next:** P2 needs pumping computed from loop pressure drop and flow; the owner ruled p_pump stays held (WI-033, instance `:502` doc), so a goal here must respect or explicitly reopen that ruling.
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R7.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "Costs follow loop thermal power or flow quantities with source basis"
- **model_evidence:** 'Coolant Cost' `mfe_account_costs.sysml:526` (primary linear in computed p_net + intermediate power-law in computed p_th, wired `mfe_plant.sysml:501`); 'Aux Cooling Cost' `:559` (linear in computed p_th + cryoplant power-law in the **computed** p_cryo, wired `:513`); bases sourced at instance `:754-766` region.
- **runtime_evidence:** `coolant__cost` = $164.44M, `aux_cooling__cost` = $20.37M (baseline_result.json).
- **why_not_next:** S3 needs pumps, piping, and heat exchangers as separately sized subaccounts — the accounts are two power-law lumps with no component sizing.
- **grader:** fresh grader session, 2026-08-30

## Row 8 — Power conversion, electric plant, heat rejection, misc BOP

**cell_id:** R8.P
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 1
- **anchor_satisfied:** "Thermal efficiency held as a cited constant" — eta_th = 0.333 held (instance `:493`, Stellaris steam cycle 1/3).
- **model_evidence:** no cycle model exists; eta_th is a plain input to the power balance (`mfe_power_balance.sysml`, eta_th_in). No coolant outlet temperature exists anywhere in `models/` to compute a cycle from (verified by absence).
- **runtime_evidence:** the held 0.333 propagates to p_the/p_et in the executed balance (baseline_result.json channels).
- **study_evidence:** efficiency moved LCOE −13.3% to −23.4% in feasible space while equipment rates moved it ≤ ~1.1% — `20260821-power-cycle-ab/synthesis.md` §2.2 — confirming the physics side is where this row's depth matters.
- **why_not_next:** P2 needs cycle efficiency computed from coolant outlet temperature under a stated cycle model, verified; neither the temperature nor the cycle model exists.
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R8.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "Costs follow computed gross/net power with source basis"
- **model_evidence:** 'Linear Power Cost' `mfe_account_costs.sysml:226`, used four times (`mfe_plant.sysml:394-412`): turbine ← computed p_the, electric ← p_et, heat rejection ← p_th, misc ← p_et; per-MW rates sourced at instance `:247-274`.
- **runtime_evidence:** turbine $225.27M, electric $95.96M, heat rejection $116.93M, misc $58.41M; `bop_capital` = $496.56M (baseline_result.json).
- **why_not_next:** S3 needs turbine island, electrical plant, and heat sink as separately **sized** subaccounts (equipment decomposition), not four per-MW lines.
- **grader:** fresh grader session, 2026-08-30

## Row 9 — Buildings, site, hot cell, remote handling

**cell_id:** R9.P
- **score:** not_applicable — confirmed. Buildings carry no plasma physics; the row's depth is structural (the rubric's single-ladder form for this row is correct).
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R9.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "Grouped building bases scaled by plant power with source basis"
- **model_evidence:** 'Buildings Cost' `mfe_account_costs.sysml:304` — exact 6-term grouped collapse of the 18-building loop, each group scaled by a computed power (p_fus/p_the/p_th/p_et/staff-sqrt), wired at `mfe_plant.sysml:422`; per-building base sums with line-level citations at instance `:300-343` region (bldg_fixed_base … bldg_et_base); remote handling `mfe_account_costs.sysml:476` (wired `:478`), preconstruction `:366` (wired `:437`), installation labor `:503` (wired `:492`).
- **runtime_evidence:** `buildings_cost__cost` = $644.17M, `remote_handling__cost` = $150.72M, `precon_cost__cost` = $18.17M, `installation__cost` = $1154.18M (baseline_result.json).
- **why_not_next:** S3 needs the building set sized by volume/function from layout drivers (power-core dimensions, hot-cell throughput, RH equipment paths) — hot cell is a $104M base inside the p_fus-scaled group and remote handling is a gross-electric power law; no volume or layout sizing exists.
- **evidence-integrity:** EI-1 attached (CAS10 land term, below).
- **grader:** fresh grader session, 2026-08-30

## Row 10 — Fuel and tritium cycle

**cell_id:** R10.P
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 1
- **anchor_satisfied:** "Annual feed from fusion energy with held burn/recovery fractions" — 'DT Fuel Cost' `mfe_account_costs.sysml:730` computes the annual feed from the computed p_fus with held burn_fraction = 0.05 (instance `:855`), fuel_recovery = 0.99 (`:858`), availability = 0.85 (`:812`); wired at `mfe_plant.sysml:695`.
- **model_evidence:** no tritium inventory, startup requirement, processing throughput, or decay exists anywhere in `models/` (verified by absence; the CAS50 startup line is a held cost, instance `:779`, not a computed inventory).
- **runtime_evidence:** `fuel_calc__annual_fuel` = $537,187/yr (baseline_result.json).
- **why_not_next:** P2 needs tritium inventory, startup requirement, and processing throughput forward-computed and verified; none is represented. (TBR feedback belongs to R2c; the P3 self-sufficiency coupling would join the two.)
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R10.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 1
- **anchor_satisfied:** "Annual fuel cost line with a CAS home" — CAS80 raw annual fuel levelized through 'Levelized Annual Cost' (`mfe_account_costs.sysml:670`, wired `mfe_plant.sysml:705`).
- **model_evidence:** the S2 test — "processing-plant cost follows computed throughput with source basis" — fails: no throughput is computed anywhere; the fuel-handling account C220500 scales with net electric power (`mfe_plant.sysml:531`, base × (p_net/1000)^0.7), a power proxy, not a computed processing throughput.
- **runtime_evidence:** `fuel_handling__cost` = $98.33M, `fuel_calc__annual_fuel` = $537,187/yr (baseline_result.json).
- **why_not_next:** S2 needs a computed processing throughput for the processing-plant cost to follow; the model has no throughput quantity.
- **grader:** fresh grader session, 2026-08-30 — see grader note G3.

## Row 11 — Availability, scheduled replacement, maintenance, decommissioning

**cell_id:** R11.P
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 1
- **anchor_satisfied:** "Availability held as a cited constant" — availability = 0.85 held (instance `:812`, 1costingFE reference).
- **model_evidence:** the P2 conjunction — "outage durations **and** replacement schedule computed from component lifetimes, verified" — is half-met: the replacement schedule is computed (n_rep from the fluence-limited life, `mfe_account_costs.sysml:794` + the normative handwritten impl), but outage durations are represented nowhere and availability is decoupled from the schedule entirely.
- **runtime_evidence:** `cas72_calc__cost` = $97.07M/yr computed; availability enters it and the fuel/energy denominators only as the held 0.85 (baseline_result.json).
- **study_evidence:** the committed finding this row's target names: `availability` is `no_constraint_response` — 0 of 6 constraints, objectives cas72/fuel/lcoe/lcoe_1cfe only — confirmed at the original pin (`20260821-power-cycle-ab/synthesis.md` §3, finding #1) and re-confirmed at the current pin (`20260829-p-pump-fence/synthesis.md` §3); DISCOVERY_LOG 2026-08-29 row: "standing, re-confirmed; gap unchanged".
- **why_not_next:** P2 needs outage durations computed from component lifetimes; P3 additionally needs availability derived from the maintenance/replacement schedule and feeding the economics — nothing couples the computed core life to the held capacity factor.
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R11.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "Levelized replacement follows computed component life"
- **model_evidence:** CAS72 levelized replacement is driven by the computed fluence life with discrete per-event discounting and a live n_rep (`mfe_account_costs.sysml:794` + `levelized_replacement_cost_impl.py`, guards verbatim); O&M CAS70/71 (`:403`, `:670`; wired `mfe_plant.sysml:444,674`) and decommissioning provision (CAS50 decom_base, instance `:785` region) have CAS homes.
- **runtime_evidence:** `cas72_calc__cost` = $97.07M/yr, `om_cost__annual_om` = $47.62M/yr (baseline_result.json).
- **why_not_next:** S3 needs replacement per component class (blanket and divertor are one grouped event at one shared FW life) plus decomposed O&M (one staffing power-law lump) and decommissioning (one fixed provision).
- **grader:** fresh grader session, 2026-08-30

## Row 12 — Integrated CAS rollup, financing, LCOE, estimate quality

**cell_id:** R12.P
- **score:** not_applicable — confirmed. The economics layer has no physics dimension; its depth is structural.
- **grader:** fresh grader session, 2026-08-30

**cell_id:** R12.S
- **rubric_version:** rubric.md@dc0f0b6d · **model_version:** dc0f0b6d + package f97f0848…/c0000
- **score:** 2
- **anchor_satisfied:** "2-digit CAS coverage with computed contingency, indirects, IDC, levelization, and LCOE"
- **model_evidence:** full 2-digit coverage with the 1cfe overnight assembly: CAS10 (`mfe_account_costs.sysml:366`), CAS20/21/22 incl. the C2201xx–C220700 tail, CAS23-28, CAS29 contingency (`:255`, wired `mfe_plant.sysml:582`), CAS30 indirect (`:276`/`:596`), CAS40/CAS50 (`:591`/`:622`), CAS60 IDC closed form (`:643`/`:645`, reported line), CAS70/71/72/80 levelization (`:670`, `:730`, `:794`; wired `:674-746`), CAS90 + two LCOE forms (`:913`, `:943`; DCF core `models/library/analyses/mfe_lcoe_dcf.sysml:4`, wired `mfe_plant.sysml:779-818`); CAS tree types in `models/library/cost_structure/cas_hierarchy.sysml`.
- **runtime_evidence:** the whole rollup executes: `cas2x_pre_contingency` $10.949B → `contingency` $1.095B → `cas20_capital` $12.044B → `indirect` $3.212B → `overnight_capital` = `total_capital` = $16.090B; `idc__cost` $4.545B (reported); `lcoe_calc__lcoe` 333.067, `lcoe_1cfe_calc__lcoe` 326.512 (baseline_result.json).
- **study_evidence:** economic assumptions move the objective without changing physical verdicts (`20260821-power-cycle-ab/synthesis.md` §3, oracle scan; `discount_rate` `no_constraint_response`).
- **why_not_next:** S3 is a conjunction and its second half fails: functional 3-digit subaccounts exist where cost concentrates (the CAS22 tail), but there is no stated estimate class, no parameter-uncertainty treatment, and no schedule risk anywhere — deterministic point assumptions throughout (verified by absence).
- **grader:** fresh grader session, 2026-08-30

---

## Evidence-integrity findings (per protocol §6 — recorded, never scored)

**EI-1 — CAS10 land term masks negative-net points.** 'Preconstruction Cost' takes `(p_net × …) ** 0.5` (`mfe_account_costs.sysml:366-402`), so a net-negative point returns `execution_failed` before `net_positive` can read `violated`; at the current pin this excludes 42 points from the standard window, and the exclusion **manufactures** `net_positive`'s clean sheet across the 906 evaluated points (`20260829-p-pump-fence/synthesis.md` §2, §5 finding #1; DISCOVERY_LOG rows 2026-08-29; minted as WI-034 `[OWNER 2026-08-29]`). Attached to: **R9.S** (the account's home) and **R7.P** (the `net_positive` runtime evidence for the power balance must be read with this caveat). Does not change either score.

**EI-2 — power-balance operands not stored as channels.** `net_positive` and `recirc_ok` read `pb__p_net` / `pb__rec_frac`, which the study store does not record as per-point values; verdicts were verified by oracle re-derivation and the operands are recoverable by the recipe in the DISCOVERY_LOG 2026-08-28 `declared seam` row (`20260821-power-cycle-ab/synthesis.md` finding #5). Attached to: **R7.P**, **R1.P**. Runtime claims in those cells rest on the verified baseline_result.json and the re-derivation, which the study record certifies; noted so the reveal does not overstate per-point evidence.

**EI-3 — model wall-load average vs source shaped-wall average.** The model's flat-wall average 3.13 MW/m² sits above the source's printed 2.87 average and is compared against the printed 4.05 peak limit (instance doc `:900-911` region). A disclosed geometry simplification, not a defect; recorded here because R2a.P's pushback evidence rides on this operand. Attached to: **R2a.P**. Does not change the score.

## Grader notes (judgment calls for the author's disposition pass)

**G1 — R4.P scored 1, not 2.** The alternative reading: eta_pin = eta_source × eta_couple is documented, and `p_input/eta_pin` executes inside the power balance, so one could call the wall-plug → coupled chain "computed with a stated deposition assumption." I scored 1 because the general P2 ladder requires a forward calculation deriving the governing output, and here every governing quantity (installed power, coupled power) is a held constant — the only arithmetic is a held ratio inside another subsystem's sum, and no heating-chain element exists as a model object. If the author reads the row anchor as satisfied by that division, R4.P becomes 2 and meets target; the disagreement protocol (§5) applies.

**G2 — R5.S scored 2 on a proxy reading.** The anchor says "divertor thermal power or area"; the model's driver is **plant** thermal power. I granted S2 because the source account itself (cas22.py:570) defines divertor cost on plant-thermal scaling and the driver is a computed performance driver with CAS home and source basis. A stricter letter-reading gives S1 and opens a gap under a met target — worth an explicit disposition.

**G3 — R10.S scored 1, not 2.** The fuel-handling account does follow a computed quantity (p_net^0.7), which meets the *general* S2 ladder; the row anchor's specific test ("processing-plant cost follows computed throughput") fails because no throughput exists. I followed the row anchor. If the author intended the general ladder to suffice, R10.S becomes 2.

**G4 — R2.S scored 3 despite two rough edges.** (a) The first wall is not sized separately from the blanket — its volume folds into the blanket aggregate (three layers, one cost); (b) the divertor member of the replaceable set is power-law-costed, not sized, and belongs to row 5. I scored 3 because within row 2's scope the replaceable/life-of-plant split is real, the four component classes carry independent engineered volumes, and replacement follows computed life — which is the anchor's full conjunction. A stricter reading of "replaceable units … separately sized" (demanding a separately sized first wall) gives S2.

**G5 — R3.P's cryo chain earns no credit at the row level.** The WI-024 cryoplant derivation (heat inventory → COP → p_elec, executed) satisfies the second conjunct of the row's P2 anchor on its own, but the anchor is a conjunction with the field derivation, which fails. If the author ever splits row 3 into subcells (the row-2 pattern), the cryo chain is a defensible P2.

**G6 — R2a.P's "pushes back on the design."** The wall-load limit 4.05 is itself a held design value (source Table 2), but the P3 test requires only the **operand** computed against a physical/engineering limit, and the limit binds hard in both committed studies (it sets the feasible-region boundary and the constrained optimum). I read that as full satisfaction; noting it because the tbr_ok scoring rule shows held-vs-held is the failure mode, and here only one side is held.

---

## Author dispositions (rubric author, 2026-08-30 — per protocol §5)

No score changes. All six flagged calls resolve by applying the written anchor; two produce clarification notes for any future rubric v2. Disagreement records:

- **G1 / R4.P** — author_reading: agree with grader. grader_score: 1. resolution: **1 stands** — the row's P2 anchor requires a computed wall-plug → coupled-power *chain*; a held ratio dividing one held constant inside another subsystem's sum derives nothing, and no chain element exists as a model object.
- **G2 / R5.S** — author_reading: the anchor's intent was "cost follows a computed performance driver with source basis"; the source account's own stated basis is plant-thermal scaling, so the proxy satisfies it. grader_score: 2. resolution: **2 stands**; v2 clarification candidate — reword the anchor to "divertor thermal power, area, or the source account's stated plant-thermal basis" so letter and intent match.
- **G3 / R10.S** — author_reading: agree; the row anchor names computed processing throughput deliberately — the absent fuel cycle is what this row exists to measure, and a p_net^0.7 power proxy is not a throughput. grader_score: 1. resolution: **1 stands** (row anchor over general ladder, as the rubric specifies).
- **G4 / R2.S** — author_reading: agree; within row scope the replaceable/life-of-plant split is real, four component classes carry independent engineered volumes, and replacement follows computed life — the full conjunction. The folded first wall is captured in why_not_next territory, not the score. grader_score: 3. resolution: **3 stands**.
- **G5 / R3.P** — author_reading: agree; the row's P2 is a conjunction and the field derivation fails. The computed cryo chain is recorded and would earn P2 under a subcell split. resolution: **1 stands**; v2 candidate — split row 3 into field/stress and cryo subcells if the row's single score starts hiding progress.
- **G6 / R2a.P** — author_reading: agree; P3's test is a *computed operand* against an engineering limit — limits are, by nature, held values. Held-vs-held (tbr_ok) is the failure mode; computed-vs-held is the ladder working. grader_score: 3. resolution: **3 stands**.
