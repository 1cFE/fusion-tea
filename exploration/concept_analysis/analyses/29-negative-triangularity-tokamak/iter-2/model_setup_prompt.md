# 1costingfe Model Update: Negative Triangularity Tokamak

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Vertical Stability Challenge Absent from NT-Specific Risk Assessment
- **Target:** Section 2 (Challenges) and Section 3 (NT Confinement at Reactor Scale — TRL 2–3)
- **Category:** analysis
- **Finding:** arxiv-2401-15217 (Markovičiūtė et al. 2024) identifies that NT configurations are measurably less vertically stable than equivalent positive-triangularity equilibria — NT equilibria are described as "more susceptible to magneto-hydrodynamic instability" with reduced vertical stability at higher poloidal beta. Passive outboard stabilizer plates can mitigate this, reducing instability growth rates to ~16% of baseline, but this requires dedicated engineering hardware. The analysis lists six NT-specific challenges in Section 2 and assesses NT confinement maturity in Section 3 but does not mention vertical instability anywhere. This is an NT-specific engineering challenge — distinct from confinement scaling — with capital cost implications (passive conducting plate infrastructure) and design complexity implications (constrained coil geometry for NT-shape stabilization). It is also relevant to Goal 5 (risks and assumptions) and Goal 2 (key differentiators from conventional tokamak).
- **Recommendation:** Add a seventh challenge entry to Section 2 covering NT vertical stability (rank: Moderate impact). State that NT geometry is intrinsically less vertically stable than PT at comparable elongation and poloidal beta, that this requires passive outboard stabilizer plates or active vertical stabilization coils as engineering additions, and that this is an NT-specific cost item absent from the baseline MANTA cost breakdown. In Section 3 (NT Confinement at Reactor Scale — TRL 2–3), add "Vertical stability characterization and passive/active stabilizer design validation in NT geometry at reactor-relevant elongation" to the "Missing at scale" bullet list. Add a corresponding row to the Section 6 Data Gap Inventory (gap type: not-yet-sourced, criticality: important).
- **Priority:** important

### F-2: No Commercial-Scale PT Tokamak COE Benchmark to Contextualize MANTA's Pilot-Plant LCOE
- **Target:** Section 2 (Challenge 2: Net electric output and commercial scaling path) and Section 7 (Cross-concept notes — Key divergences)
- **Category:** analysis
- **Finding:** The ARIES-ACT study (osti-1178069, Najmabadi et al. 2015) provides COE data for a mature 1000 MWe advanced positive-triangularity tokamak: ~64 mills/kWh (~$64/MWh) for ACT1 (10th-of-a-kind, 58% thermal efficiency via SiC composite structure, wall-stabilized plasma, δ=0.63). Section 2 Challenge 2 discusses MANTA's $396/MWh pilot-plant LCOE and identifies the improvement levers (magnet lifetime, thermal efficiency, fusion power scaling), but the analysis has no commercial-scale PT tokamak reference point to anchor what "commercially viable" means for this technology family. Without this anchor, the discussion of MANTA's improvement pathway is framed only in relative terms ("3× offshore wind"). ARIES-ACT ACT1 represents the natural 10th-of-a-kind PT tokamak target, and the ~6× gap between $396/MWh and ~$64/MWh quantifies the NT scaling challenge more concretely. Additionally, ARIES-ACT documents peak divertor heat flux of 13.7 MW/m² for ACT1 without NT — directly contrasting with MANTA's 2.8 MW/m² and giving a concrete quantification of the NT divertor advantage cited in Section 2 Challenge 5 and Section 7 (where only qualitative comparisons are made).
- **Recommendation:** In Section 2 Challenge 2, after the MANTA $396/MWh figure, add a sentence citing ARIES-ACT ACT1's ~64 mills/kWh (~$64/MWh) as the comparable 10th-of-a-kind advanced PT tokamak benchmark, noting the key assumptions (58% thermal efficiency via SiC, 1000 MWe, wall-stabilized AT physics). In Section 7 (Key divergences), update the divertor comparison to include the concrete heat flux figures: MANTA NT at 2.8 MW/m² vs. ARIES-ACT ACT1 at 13.7 MW/m² — a ~5× reduction that directly quantifies the NT divertor advantage. Add ARIES-ACT to Section 8 (Sources).
- **Priority:** important

### F-3: Thermal Efficiency Analogue Available but Not Incorporated into Missing Parameters
- **Target:** Section 5 (Missing Parameters table) and Section 2 (Challenge 2 — commercial scaling path)
- **Category:** model
- **Finding:** Section 5 lists "Thermal efficiency for NT tokamak commercial plant" as a BLOCKING missing parameter with gap type "not-yet-sourced" and no analogue provided. ARIES-ACT (osti-1178069) supplies directly relevant analogue data: 58% for ACT1 (SiC composite structure, self-cooled Pb-Li blanket at high outlet temperature) and 45% for ACT2 (RAFM steel, dual-cooled Pb-Li at lower temperature). The MANTA FLiBe blanket architecture is closer to a self-cooled molten-salt design, but at lower outlet temperature than ACT1's SiC design, placing plausible commercial NT thermal efficiency in the 45–55% range. This range is derivable from ARIES-ACT and should be reflected in the model setup's commercial LCOE scenario rather than left as an open gap. The improvement from MANTA's pilot-scale Rankine efficiency to a commercial 45–55% cycle is one of the three levers MANTA itself identifies for reaching commercial viability, and anchoring it changes the LCOE scenario range meaningfully.
- **Recommendation:** In Section 5 (Missing Parameters), update the "Thermal efficiency for NT tokamak commercial plant" row: change gap type from "not-yet-sourced" to "derivable", cite ARIES-ACT ACT1 (58%, SiC/Pb-Li) and ACT2 (45%, RAFM/Pb-Li) as the bounding analogues, and note 45–55% as the plausible NT commercial range given FLiBe's outlet temperature constraints relative to ACT1. In Section 2 Challenge 2, add that commercial thermal efficiency analogues from ARIES-ACT suggest 45–58% is achievable depending on blanket and structural material choices — compared to MANTA's lower steam Rankine estimate — and that this gap is one of the quantifiable levers in the commercial scaling path. In model_setup.py, add thermal_efficiency as a scenario parameter with the 45–58% analogue range and ARIES-ACT as the source.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Ohmic-only scenario absent from model despite being the primary NT differentiator
- **Target:** model_setup.py / model output (Section 7 recommendation)
- **Category:** model
- **Finding:** Section 7 explicitly states "a two-branch TEA model (with/without heating system) should capture the Q ≈ 30 (with ICRF) vs. Q ≈ 500 (ohmic) divergence." The model output confirms this is unimplemented: "Ohmic-only scenario (not modeled here)." The ohmic-only branch is the single most NT-specific economic hypothesis in the entire analysis — it eliminates $150M in heating capital and dramatically changes Q_eng — yet the model has no representation of it whatsoever. The sensitivity table shows `heating_icrf_per_mw` elasticity of only +0.008, which understates the impact because it only perturbs unit cost, not whether the system exists at all.
- **Recommendation:** Implement the ohmic-only scenario as a model branch: set `p_icrf = 0` and `C220104 = $0` in one branch, then compare LCOE, overnight cost, and Q_eng against the ICRF baseline. The branch should also reflect the Q improvement (from ~30 to ~500 per Ball et al.), which changes recirculating power fraction and Q_eng substantially. Flag H_NA as the gate parameter controlling which branch is credible.
- **Priority:** blocking

### F-2: Plasma physics parameters have zero LCOE elasticity — model does not connect physics to cost
- **Target:** model_setup.py sensitivity sweep / CAS22 coil account
- **Category:** model
- **Finding:** The sensitivity output shows B, T_e, n_e, Z_eff, plasma_volume, tau_ratio, disruption_rate_base, disruption_steepness, disruption_damage, disruption_downtime, R_w, T_edge, q95, f_GW, and M_ion all with elasticity exactly 0.0000. For a tokamak model these should drive fusion power, shielding volume, and disruption-driven availability. The TF coil account (C220103) is hardcoded at $1,500M directly from MANTA — it does not vary with B or R0, yet R0 has non-zero elasticity (+0.107), implying some geometry scaling occurs without the coil cost responding to it. This means the model's most cost-dominant account ($1.5B of $3.4B) is a fixed input, not a computed output. Disruption parameters being inert is also notable given that NT disruption characterization is listed as a data gap in Section 6.
- **Recommendation:** Wire plasma physics parameters into the cost calculation chain. At minimum: (1) make C220103 a function of B, R0, and REBCO volume rather than a hardcoded constant; (2) connect disruption parameters to availability, which is the highest-elasticity engineering lever (-0.97). If the model cannot derive coil cost from physics, at least add a sensitivity sweep that varies C220103 ±50% to capture the MANTA cost uncertainty band explicitly.
- **Priority:** blocking

### F-3: Nearest-neighbor concepts for comparison not explicitly identified
- **Target:** Section 7 (Cross-Concept Notes) / overall analysis framing
- **Category:** analysis
- **Finding:** The analysis compares only to `21-spherical-tokamak-hts` because it is the sole approved analysis, but does not name the actual structural nearest neighbors. For an NT tokamak, the primary comparison should be a conventional positive-triangularity HTS tokamak at similar field strength and aspect ratio — specifically `01-hts-compact-tokamak` (CFS ARC-class, conventional PT). This is the concept from which NT is defined as a departure; every NT differentiator (divertor simplification, L-mode vs H-mode, ohmic heating possibility) is most meaningfully framed as a delta against a conventional PT HTS compact tokamak, not a spherical tokamak. Secondary neighbors are `28-hts-tokamak-full-hts` (same HTS compact tokamak family) and `33-state-backed-tokamak-best` (conventional standard-aspect tokamak for the larger-scale reference). Without naming these, the analysis cannot credibly quantify whether NT's claimed advantages are real improvements over the actual comparison class.
- **Recommendation:** Add a sentence in Section 7 explicitly naming 01-hts-compact-tokamak as the primary structural nearest neighbor (conventional PT HTS compact tokamak, same family, defines the PT baseline from which NT departs). Note that it is in the in-progress pool so full cross-reference is not yet available, but flag it as the reference concept for NT-vs-PT cost differentials. This will also clarify why the ST-HTS comparison is secondary, not primary.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_tokamak.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/iter-2/model_setup.py`
