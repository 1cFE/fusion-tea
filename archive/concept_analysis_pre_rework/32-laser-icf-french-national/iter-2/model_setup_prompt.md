# 1costingfe Model Update: Laser ICF - French National Direct Drive (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Shock ignition hot-electron preheat risk is experimentally mitigated — analysis overstates uncertainty

- **Target:** Section 2 (Challenge #4: Shock ignition LPI risk) and Section 3 (Shock Ignition Target Physics — TRL 2–4)
- **Category:** analysis
- **Finding:** The OSTI source (LA-UR-21-22970, published PRL 127, 065001, 2021) presents experimental results from ignition-scale plasma experiments at OMEGA showing that hot electrons generated during shock ignition do NOT significantly preheat the fuel. Hot-electron conversion efficiency was measured at 1–2.5% of laser energy, temperatures at 35–45 keV, and hydro-simulations using those measured characteristics show "very little degradation in the density profile" — described as "an encouraging result for future MJ-scale shock-ignition experiments." The analysis currently frames LPI hot-electron preheat as an unresolved risk that "can spoil the compression," which is accurate but does not reflect that the dominant failure mode has been experimentally tested at ignition-scale conditions and found manageable. The dominant instability regime also shifts from TPD (short scale-length) to convective SRS (long scale-length) as scale-length increases — a nuance missing from the current description.
- **Recommendation:** Update Section 2 Challenge #4 and the Section 3 TRL description for shock ignition to reflect this experimental result. The risk framing should shift from "hot-electron preheat is an unresolved concern" to "hot-electron preheat has been tested at ignition-scale plasmas and found manageable at 1–2.5% conversion efficiency and 35–45 keV temperatures, though statistical confidence requires higher-rep-rate experiments." Note the instability regime shift (TPD → convective SRS) as scale-length increases. This affects Goal 5 (risks and assumptions) — the shock ignition preheat risk should be reclassified from unknown to partially de-risked, which has downstream implications for gain uncertainty modeling.
- **Priority:** important

---

### F-2: Li-6 supply chain lacks quantified demand and omits emerging Western enrichment alternatives

- **Target:** Section 4 (Li-6 Enrichment for Tritium Breeding)
- **Category:** analysis
- **Finding:** The NEI Magazine source (neimagazine enriched lithium article) provides two material data points absent from the analysis: (1) a DEMO-scale demand estimate of >60 tonnes per GW of enriched lithium, and (2) the existence of Hexium, a US startup developing AVLIS-based lithium isotope separation with $12M in funding and a stated 3–5 year timeline to substantially reduce Western dependence on Russian/Chinese Li-6 production. The current Section 4 accurately states that no Western industrial-scale Li-6 enrichment facility operates but presents this as a static constraint without acknowledging active mitigation efforts or quantifying how much enriched lithium a commercial plant would actually require. The >60 t/GW figure is directly LCOE-relevant as a blanket material cost driver and supply sequencing constraint.
- **Recommendation:** Add the >60 t/GW enriched lithium demand figure to Section 4 and the Section 5 missing parameters table (or as a note in the Li-6 supply chain row). Update Section 4 to acknowledge Hexium/AVLIS as an emerging Western enrichment pathway with a 3–5 year development horizon, alongside the existing description of Russian/Chinese COLEX dominance. This serves Goal 3 (TEA implications) by quantifying a blanket material cost input, and Goal 5 (risks) by distinguishing between the current supply gap and the active mitigation timeline.
- **Priority:** important

---

### F-3: Laser system MTTF requirement (gigashot reliability) is absent from O&M and capacity factor framing

- **Target:** Section 2 (Challenge #5: First wall and final optics) and Section 5 (Missing Parameters: Capacity factor, Laser optics replacement)
- **Category:** analysis
- **Finding:** The ARPA-E Zuegel document specifies that IFE laser drivers must achieve a gigashot mean time to failure (MTTF), defined as 1 year at 10 Hz = 315 million shots. This is a formal reliability target from the ARPA-E IFE driver roadmap and is directly relevant to capacity factor and O&M cost modeling. The analysis discusses optics replacement and laser uptime as missing parameters but does not frame them against this specific reliability requirement. At gigashot MTTF, a system operating 10 years at 10 Hz must survive 3.15 billion shots — no laser component has been demonstrated near this lifetime. The document also introduces Line Replaceable Unit (LRU) modular architecture (10.5 × 2.2 × 1.35 m³ per unit) as the proposed O&M strategy, enabling module swap-out rather than in-situ repair, which is the assumed maintenance model but has not been cited in the analysis.
- **Recommendation:** Add a brief note in Section 2 Challenge #5 or the Section 5 missing parameters table that the IFE driver reliability target is gigashot-class (315M shots/year), and that no laser component has demonstrated this lifetime, establishing the gap magnitude. Reference the LRU modular swap architecture as the assumed maintenance model for laser O&M cost purposes. This supports Goal 5 (risks) by giving a concrete reliability gap metric for the capacity factor sensitivity parameter.
- **Priority:** minor

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Laser driver CAPEX is hardcoded — cannot test the top cost uncertainty
- **Target:** model_setup.py / model output (C220107 and sensitivity sweep)
- **Category:** model
- **Finding:** The model output shows `C220107 Laser driver (DPSSL) [OVERRIDE] 1000.0` — a flat $1B override rather than a parameter-driven calculation. The sensitivity table confirms this: `driver_laser_per_mw` has elasticity of only +0.03, far below availability (-0.90) and chamber radius (+0.60). Yet the analysis correctly identifies laser system CAPEX as challenge #1 — the dominant uncertainty, spanning $900M (NOAK floor) to $3B (FOAK mid) by the analysis's own estimate. The model as built cannot test this range. The most important economic uncertainty identified by the analysis is structurally inaccessible to the model's sensitivity sweep.
- **Recommendation:** Replace the override with a parameter-driven calculation: `laser_cost = E_d_MJ * 1e6 * laser_cost_per_J`, where `laser_cost_per_J` is a sweep parameter spanning the analysis-documented range ($100–$1,000/J from NOAK floor to FOAK mid). This makes the laser driver respond to the sensitivity sweep and allows the model to show LCOE as a function of the one parameter the analysis identifies as most uncertain and most impactful. Remove the [OVERRIDE] flag once parameter-driven.
- **Priority:** blocking

### F-2: Concept 31 (direct drive laser IFE) missing from nearest-neighbor comparison
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** Section 7 names concept 26 (indirect drive) and concept 17a (hybrid drive / KrF excimer) as the laser IFE comparators, but omits concept 31 (Blue Laser Fusion, OEC Architecture, direct drive D-T), which is at iter-3 in the concept landscape. Concept 31 shares the same confinement family, drive scheme (direct drive), and fuel (D-T) as GenF/TARANIS — it is the closest structural neighbor within the IFE family. The checklist requires 2-3 nearest neighbors; omitting the most similar direct-drive concept leaves a gap in the comparative framing that matters for TEA (Goal 1, Goal 2): both direct-drive laser IFE concepts share laser uniformity constraints, coupling efficiency advantages over indirect drive, and first-wall challenges, but they differ in laser technology (CBC fiber + OEC vs. DPSSL) and energy capture mode (hybrid thermal/direct vs. thermal-only).
- **Recommendation:** Add a comparison paragraph for concept 31 in Section 7 covering: (a) shared direct-drive coupling efficiency and LPI challenges, (b) laser technology difference (CBC fiber OEC vs. DPSSL — implications for $/J cost trajectory), and (c) energy capture difference (concept 31 uses hybrid thermal + direct; GenF is thermal-only — cost and Q_eng implications). Reorder the nearest-neighbor list so concept 31 appears first as the primary same-family comparator.
- **Priority:** important

### F-3: Section 2 challenges not mapped to top LCOE-sensitive parameters
- **Target:** Section 2 (Challenges in Capturing System Function)
- **Category:** analysis
- **Finding:** Section 2 ranks 6 challenges by "impact" but does not translate them into the 2-3 parameters with highest LCOE sensitivity — which the checklist requires (Goal 4). The model's actual sensitivity results show the top engineering levers are availability (-0.90), chamber radius/plasma_t (+0.60), and thermal efficiency (-0.28). These are not the challenges Section 2 leads with (laser cost dominates #1, tritium #2, target gain #3). Availability is Section 2's challenge #5 (first wall survivability) — buried, not called out as the highest LCOE lever. Chamber radius appears only as a physics parameter in Section 5, with no discussion of its LCOE sensitivity. This misalignment means modelers reading Section 2 will prioritize laser cost and tritium — which are real risks but not the top model levers — while underweighting availability and chamber size, which drive LCOE most directly.
- **Recommendation:** Add a closing paragraph to Section 2 (or a brief "Top Modeling Levers" subsection) that explicitly names the 2-3 parameters with highest expected LCOE sensitivity and explains why: availability (first wall lifetime gates capacity factor, the dominant LCOE lever), chamber radius (blanket/shield volume scales as R³, doubling the default), and laser $/J cost (largest CAPEX uncertainty). This frames Section 2's qualitative challenges in terms that directly guide what to sweep in the model.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_laser_ife.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/iter-2/model_setup.py`
