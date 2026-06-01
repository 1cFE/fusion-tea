# 1costingfe Model Update: Negative Triangularity Tokamak

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: NT divertor advantage framing overstated — advanced PT divertors also achieve low heat flux
- **Target:** Section 2 (Challenge #5, "Divertor simplification") and Section 7 (Cross-concept notes, "Key divergences" paragraph on divertor)
- **Category:** analysis
- **Finding:** The analysis claims a "~5× reduction in peak heat flux" for NT vs. PT by comparing MANTA's 2.8 MW/m² to ARIES-ACT ACT1's 13.7 MW/m² and ACT2's 10 MW/m² (Section 7). However, the ARIES-ACT study (osti-servlets-purl-1127358, PPPL-5008) contains detailed divertor analysis showing that ARIES-ACT designs with orthogonal plates and wide slots achieve ~2 MW/m² on divertor target plates — comparable to MANTA's 2.8 MW/m² — by using 90% radiated power fractions in the divertor. The 13.7/10 MW/m² figures the analysis cites are the ITER-style inclined plate configuration (the baseline, not the optimized option). The current framing implies PT geometry inherently produces 5–10× higher heat flux, which is misleading: the NT advantage is not that heat flux is uniquely low, but that NT *passively* achieves low heat flux (from its inherently low P_SOL fraction of 5.2%) with a conventional tungsten monoblock divertor, while advanced PT designs achieving comparable flux numbers require sophisticated radiation management engineering (90% radiated power fraction, specialized plate geometry) that represents additional capital cost and operational complexity. This distinction matters for TEA: NT eliminates complex divertor engineering cost, not merely heat flux.
- **Recommendation:** In Section 2 (Challenge #5) and Section 7, revise the divertor advantage framing to: (a) note that advanced PT divertors with optimized geometry can approach comparable heat flux values (citing 2 MW/m² from PPPL-5008 orthogonal-plate configuration), (b) clarify that the NT advantage is specifically about achieving low heat flux with *conventional* hardware and *inherently* low P_SOL (no advanced radiation management required), not uniquely low heat flux vs. all PT options, and (c) frame the cost advantage accordingly — NT eliminates exotic divertor engineering costs while PT designs at equivalent heat flux require radiation-dominated operation that itself has engineering complexity and cost. The "~5× reduction" claim should be qualified to clarify it compares to the ITER-style PT baseline, not to the best achievable PT divertor design.
- **Priority:** important

### F-2: Compact copper-magnet NT device design study provides demonstrator-phase engineering anchors not in analysis
- **Target:** Section 1 (Data Availability) and Section 3 (NT Confinement at Reactor Scale — TRL 2–3)
- **Category:** analysis
- **Finding:** The analysis describes LUCIOLE prototype parameters as "proprietary" with "no published parameter set" (Section 5, Missing Parameters) and characterizes NT device-scale engineering as "on paper only." arxiv-2501-14682 (January 2025) presents a pre-conceptual design study for a compact copper-magnet NT tokamak device (R₀ = 1 m, a = 0.27 m, Bₜ = 3 T, Iₚ = 0.75 MA, 16 demountable copper TF coils, 8 PF coils) with explicit engineering analysis of vertical stability, PF coil force limits, and mechanical loads during current quench events. The study demonstrates that a ~75% reduction in vertical instability growth rates is achievable through passive stabilizing plates in a real device geometry, and concludes that "key capabilities required of a dedicated NT tokamak experiment can be realized with existing copper magnet technologies." This is a material upgrade to the data landscape: a published pre-conceptual engineering study now exists for a compact copper-magnet NT device at the scale and technology level of Firefly's LUCIOLE prototype target. The Section 3 TRL framing ("on paper only" for NT device-scale design) is no longer entirely accurate — pre-conceptual engineering design is now published and the vertical stability challenge is demonstrated to be manageable in a real device.
- **Recommendation:** In Section 1 (Published reference design subsection), add a paragraph noting that arxiv-2501-14682 provides a published pre-conceptual engineering design for a compact copper-magnet NT demonstrator device (R=1m, Bt=3T, Ip=0.75MA, 16 demountable TF coils) — this constitutes an additional engineering data point between current experiments (TCV/DIII-D) and the commercial plant (MANTA). In Section 3 (NT Confinement TRL), update the "on paper only" characterization of device-scale NT design to note that pre-conceptual engineering designs for copper-magnet NT demonstration devices are now published, which partially de-risks the demonstrator-phase path and provides public engineering anchors for the LUCIOLE class of devices. Also update the data gap table in Section 6 for "LUCIOLE prototype parameters" — it is no longer accurate that no published engineering parameters exist for devices of this class.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Plasma physics not wired to cost model — H_NA sensitivity untestable
- **Target:** Model sensitivity analysis and ohmic scenario branch
- **Category:** model
- **Finding:** The analysis correctly identifies NT confinement enhancement (H_NA) as the #1 NT-specific uncertainty (Section 2, items 1 and 3) and recommends it be treated as a scenario branch (Section 7). The ohmic scenario is now implemented as a binary switch ($150M ICRF eliminated), but the model still shows zero elasticity for every plasma parameter — T_e, n_e, B, plasma_volume, q95, f_GW all return +0.0000. This means the model cannot evaluate H_NA varying continuously from 1.0 (no NT advantage) to 2.0 (Ball et al. full benefit). The binary ohmic/ICRF switch only captures the extreme cases; a device operating at H_NA = 1.2–1.5 may require reduced auxiliary heating power (not zero) and achieve lower fusion power than the MANTA anchor — the intermediate risk regime that matters most for investment decisions. The Q_eng discrepancy (model: 1.74 vs. MANTA reference: 2.4) also goes unexplained and suggests the recirculating power accounting is not validated against the MANTA physics anchor.
- **Recommendation:** Wire H_NA as a sensitivity parameter that modulates P_fus and Q_eng in the model. A sweep from H_NA = 1.0 to 2.0 should show LCOE variation that spans between the full-ICRF and ohmic-only extremes, capturing the continuous risk profile the analysis identifies as critical. Additionally, document or correct the Q_eng = 1.74 vs. 2.4 discrepancy — either justify the difference with a recirculating power accounting note, or update the model so the native result validates against MANTA.
- **Priority:** blocking

### F-2: NT vertical stability infrastructure: gap identified but not bounded or modeled
- **Target:** Section 5 (parameter table), Section 6 (gap #15), Model (CAS22 sub-accounts)
- **Category:** analysis
- **Finding:** Section 2 item 7 and Section 6 gap #15 correctly identify passive stabilizer plate infrastructure as an NT-specific engineering cost absent from MANTA's cost accounting, citing Markovičiūtė et al. 2024. The analysis establishes this is real and flags it as "important" but then leaves the gap entirely open — no cost range appears in Section 5, and the model's CAS22 sub-accounts have no corresponding line. The analysis has enough source material to produce a rough bound: passive conducting plate hardware in comparable tokamaks (ITER, WEST, JT-60SA) is on the order of tens to low-hundreds of millions of dollars. Leaving an NT-specific cost item that the analysis itself identified as absent from MANTA unaddressed in both Section 5 and the model creates an implicit undercount in the overnight cost.
- **Recommendation:** Add a row to the Section 5 parameter table for "NT passive stabilizer plate cost" with a derivable rough range (e.g., $15–60M based on conducting shell/plate analogue from conventional tokamaks), confidence low, source Markovičiūtė et al. 2024 + tokamak hardware analogues. Add a corresponding CAS22 sub-account in the model so this NT-specific cost appears in the overnight total rather than being silently omitted. Even an explicit placeholder with wide uncertainty closes the gap the analysis itself opened.
- **Priority:** important

### F-3: Section 5 parameter table missing NT cost-delta rows for key TEA differentiators
- **Target:** Section 5 (parameter table — "Available Parameters")
- **Category:** analysis
- **Finding:** The checklist requires Section 5 to include parameters for all identified cost-relevant differentiators. The analysis identifies three NT-specific TEA advantages with capital cost implications — divertor simplification ($24M, 60% reduction vs. PT; C220108 in model), heating elimination ($150M ICRF capital; C220104 in model), and the ohmic-only saving ($150M eliminated if H_NA validated) — but these cost values appear only in the model output and in Section 7 narrative. Section 5's "Available Parameters" table contains only physics parameters and MANTA physical design values. As a result, the NT-vs-PT cost differential is not systematically tracked as a citable parameter. The "Divertor cost differential (NT vs. PT)" and "Auxiliary heating capital cost (NT reduction vs. PT)" entries in the missing parameters table are classified as "derivable / important" rather than being resolved and moved to the available parameters table.
- **Recommendation:** Move the resolved NT cost-delta values into the Section 5 "Available Parameters" table: (1) NT divertor capital cost — $24M (60% reduction vs. PT analogue), source MANTA $3.4B cost breakdown + NT P_SOL = 23.5 MW characterization, confidence medium; (2) ICRF auxiliary heating capital cost — $150M for 40 MW system, source MANTA §2.1 + industry analogue, confidence medium; (3) ohmic-only heating elimination saving — $150M capital avoided if H_NA ≥ 2 validated, confidence low. Remove or update the corresponding entries in the missing parameters table. This converts qualitative differentiators into trackable, citable TEA parameters.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_tokamak.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/iter-3/model_setup.py`
