# 1costingfe Model Update: Laser ICF - OEC Architecture (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: He Brayton efficiency analog fills a named not-yet-sourced gap
- **Target:** Section 3 (He-Gas Turbine Power Conversion and Balance of Plant), Section 5 (η_th* parameter row), Section 6 data gap #14
- **Category:** analysis
- **Finding:** Source `osti-servlets-purl-1323907.md` (Wright et al., Sandia SAND2006-4147) is the HTGR/VHTR He Brayton analog that data gap #14 explicitly calls for ("HTGR literature provides analogs; not yet applied to BLF-specific geometry"). It provides concrete efficiency benchmarks for helium Brayton cycles under nuclear heat-source conditions: 42.8% for a simple recuperated He Brayton, 45.8% for a two-compression/one-turbine interstage-heating-cooling (IHC) cycle, and 50.4% for a six-compression/three-turbine IHC cycle. The BLF claimed η_th* = 0.44 sits squarely between the simple and first-IHC configurations. Section 3 currently states "44% is consistent with He-Brayton at high outlet temperatures" without a supporting citation; data gap #14 is explicitly marked "not-yet-sourced, important."
- **Recommendation:** (1) In Section 3 (He-Gas Turbine subsystem), add one sentence citing the Sandia VHTR study as the He Brayton analog: the simple recuperated cycle achieves 42.8% and moderate IHC configurations reach 45–50%, bracketing the BLF 44% claim as consistent with a near-simple-cycle design. (2) In Section 5, upgrade η_th* confidence from "medium" to "medium" with a note that the Sandia analog supports the stated value. (3) In Section 6 gap #14, change status from "not-yet-sourced" to "partially sourced — Sandia VHTR Brayton analog available; BLF-specific geometry integration and cost remain unknown." Add the source to Section 8. Note: this source addresses only the thermal efficiency plausibility; He Brayton integration cost for BLF geometry remains unresolved.
- **Priority:** minor

---

**Notes on the two MFE blanket sources:**

`osti-servlets-purl-1165762.md` (Meier, LLNL-TR-658973, 2014) and `osti-servlets-purl-1305833.md` (Meier, LLNL-TR-652984, 2014) are both MFE tokamak tritium breeding blanket assessments for steady-state Dual-Cooled Lithium-Lead (DCLL) systems. They do not address laser ICF, pulsed loading, target fabrication, laser efficiency, direct energy conversion, or OEC mirror technology. The PbLi operating parameters they contain (600°C outlet, 8 MPa He, TBR > 1.1 target) are consistent with what the analysis already states for BLF's LiPb blanket but are derived from steady-state MFE conditions that do not transfer directly to IFE pulsed-neutron operation. Neither source changes any conclusion in the analysis.

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: eta_dec shows zero sensitivity despite DEC providing 30% of net electricity
- **Target:** Model sensitivity sweep / power balance computation
- **Category:** model
- **Finding:** The sensitivity table reports `eta_dec = +0.0000` elasticity. Yet Section 2 explicitly states that the 30% DEC channel "represents ~840 MWe at the 10 Hz design point" and that if DEC fails "net electric output falls proportionally." A parameter that governs 30% of gross electricity output cannot have zero LCOE elasticity unless the model is not using `eta_dec` in its power-balance or net-output calculation — i.e., eta_dec is declared but not wired into the computation. This is a model integrity failure: the LCOE is being computed as if DEC efficiency is irrelevant, directly contradicting the analysis narrative (Goal 5).
- **Recommendation:** Audit the power-balance code path. Net electric output should be computed as `P_net = P_fus × (f_neutron × η_th + f_charged × η_DEC) - P_recirc`, where varying `η_DEC` changes `P_net` and therefore LCOE. Confirm that `f_charged = 0.30` and `f_neutron = 0.70` are actually applied in the computation. After the fix, `eta_dec` should show negative elasticity comparable in magnitude to `eta_th` (currently −0.258), since both channels have equal efficiency (0.44) but different power fractions (70%/30%). The DEC Capital Cost Scenarios table can remain as-is.
- **Priority:** blocking

### F-2: (G, f_rep) scenario grid holds output fixed — viability cliff is invisible
- **Target:** (G, f_rep) Scenario Grid in model output
- **Category:** model
- **Finding:** The grid title states "@ 2800 MWe" — capital is rescaled to maintain constant output across all (G, f_rep) cells. This explains why the LCOE variation is small (48.1 to 60.7 $/MWh across the full grid). But Section 7 explicitly identifies the key modeling insight as the *same-capital viability cliff*: "dropping from 10 Hz to 1 Hz while holding G = 160 cuts net output by 27× from the same capital base, effectively tripling or more the LCOE." That scenario — 5 MJ laser, G=160, f=1 Hz, ~102 MWe output, same overnight capital — does not appear anywhere in the model output. The note about "50 MJ/shot" for the 1 Hz row confirms the grid is interpreting 1 Hz as requiring a larger laser, not as running the same laser at lower rep rate. This misses the entire point of the joint (G, f) analysis (Goal 4).
- **Recommendation:** Add a second scenario table — "Same-Capital Viability Scenarios" — that holds overnight capital constant at the 2800 MWe/10 Hz value and reports LCOE at reduced output: (G=160, f=1 Hz → ~102 MWe), (G=80, f=10 Hz → ~1400 MWe), (G=80, f=1 Hz → ~51 MWe). These four cells expose the viability cliff and make the joint G×f interaction visible. The existing constant-output grid can remain as a companion table.
- **Priority:** important

### F-3: Per-shot target OPEX near-zero despite Goodin criterion flagging it as a cost-floor constraint
- **Target:** Sensitivity sweep (`p_target`) / OPEX computation
- **Category:** model
- **Finding:** The sensitivity table shows `p_target = −0.0001` elasticity — effectively zero. Section 2 (and the target maturity section) cites the Goodin criterion: targets must cost less than ~$0.035 each for economic viability, while current research targets cost $1M+. At 10 Hz, 75% availability, and 30-year plant life, the plant fires ≈7 billion shots. Even at $0.10/target (well above the Goodin floor), target OPEX would be ~$700M over plant life — comparable to several CAS accounts in the cost breakdown. The near-zero elasticity means `p_target` is either set to a negligible default value or is not correctly scaled by rep rate × availability × plant life in the OPEX calculation. This makes the model blind to one of the two consumption-cost analogues the analysis draws from the MagLIF pattern (Goal 4: "OPEX scales linearly with rep rate").
- **Recommendation:** Verify that `p_target` OPEX is computed as `p_target_per_shot × f_rep × availability × seconds_per_year × plant_life_yr` and fed into the annualized O&M cost. Set the default `p_target` to a non-zero placeholder consistent with the current state (e.g., $1/target as a near-term proxy) and include a sensitivity sweep from $0.01 to $1.00 per target. The analysis already flags this in the missing parameters table as blocking; the model should reflect the same severity.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_laser_ife.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/iter-3/model_setup.py`
