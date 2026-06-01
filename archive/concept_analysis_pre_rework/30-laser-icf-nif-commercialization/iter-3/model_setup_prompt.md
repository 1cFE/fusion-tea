# 1costingfe Model Update: Laser ICF - NIF Commercialization (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: LIFE Heritage COE Economics Not Incorporated
- **Target:** Section 5 (Parameters table), Section 6 (Data Gap Inventory, gap #12), and Section 2 (energy balance/O&M discussion)
- **Category:** model
- **Finding:** OSTI-1022881 (Anklam, LLNL-TR-480444, 2011) is the LIFE Cost of Electricity study the analysis explicitly identifies as a critical unfilled gap (Section 6, gap #12: "LLNL LIFE plant engineering cost reports (capital cost by subsystem) still needed"). This source directly fills that gap. It provides a pre-conceptual bottom-up COE of **$69/MWhr (2011 dollars)** for a ~900 MWe LIFE plant, with a full cost fraction breakdown: laser system ~30% of COE (~$18/MWhr), targets (fuel) ~21% ($110M/yr annualized), fusion engine ~15%, power facilities ~12%, non-fuel O&M ~19%, capital ~60% of COE, tritium plant ~2.5%. It also establishes a two-state availability model (70% first unit, 92% NOAK) and confirms thermal efficiency at 44%. None of these heritage figures appear in the current Section 5 parameter table or Section 6 gap inventory, despite being directly applicable to the Inertia concept (same indirect-drive, liquid-Li architecture). The laser contributing 30% of COE and targets 21% are the two highest-leverage cost-fraction benchmarks for modeling.
- **Recommendation:** Add the following to Section 5: a row for "LIFE heritage COE (2011$)" = $69/MWhr citing OSTI-1022881; a row for "LIFE laser fraction of COE" = ~30% ($18/MWhr); a row for "LIFE target (fuel) annual cost" = $110M/yr at ~900 MWe; a row for "LIFE first-unit availability" = 70% (vs. NOAK 92%, already partially captured). In the model (model_setup.py), add the LIFE cost-fraction breakdown as a heritage calibration reference — the laser/target/O&M split provides an order-of-magnitude sanity check on modeled cost outputs. Update Section 6 gap #12 to "partially filled" and note OSTI-1022881 in Section 8 as the source. Cross-check whether the $110M/yr LIFE target fuel cost at ~900 MWe is consistent with the analysis's own $0.41/target × 315M/year × (1.5 GW / 0.9 GW) scaling.
- **Priority:** important

### F-2: NIF Gain Trajectory Through April 2025 Needed to Ground Physics Validation
- **Target:** Section 3 (Hybrid-E Target Physics subsection) and Section 5 (Parameters table)
- **Category:** analysis
- **Finding:** Wurzel & Hsu (2025, arxiv-2505-03834v5) compiles the complete NIF shot record through April 2025. The analysis currently describes NIF ignition as Q_target ≈ 1.54 (December 2022) and states "NIF highest shots are ≈3–5×, still being improved" (Section 3). However, as of April 7, 2025 (shot N250406), NIF achieved Q_sci = 4.13 (2.1 MJ input → 8.6 MJ fusion yield) — the current confirmed peak. The full record shows 8 shots above Q_sci = 1 since December 2022, with the progression 1.54 → 1.89 → 2.36 → 2.44 → 4.13 over 2.5 years. Two effects matter for the analysis: (a) the "3–5×" range in Section 3 is now accurate but understated — citing the specific 4.13 peak and improvement rate strengthens the physics validation case; and (b) all NIF ignition shots use ~2 MJ drive energy, while Inertia targets 10 MJ (5× more). The current analysis notes that gain "should improve with laser energy (power-law scaling from NIF data)" but has no quantitative anchor for this extrapolation. The Q_sci = 4.13 at 2 MJ is now that anchor, making the gap to Inertia's 18× pilot target explicit and quantifiable.
- **Recommendation:** Update Section 3 (Hybrid-E Target Physics — Demonstrated bullets) to replace "NIF highest shots are ≈3–5×" with the specific April 2025 result (Q_sci = 4.13, shot N250406, 2.1 MJ → 8.6 MJ) and note the improvement trajectory (1.54 → 4.13 in 2.5 years across 8 igniting shots). Add to the "Missing at scale" bullet that the current best Q_sci at NIF's 2 MJ drive energy (4.13) is still 4× below the 18× pilot target, and the gain scaling from 2 MJ to 10 MJ drive — while physically expected to increase — has not been demonstrated and represents the key near-term physics extrapolation risk. Add a row to Section 5: "Current peak NIF Q_sci (April 2025)" = 4.13 with source arxiv-2505-03834v5, confidence high, noting 2.1 MJ drive vs. Inertia's 10 MJ target. Cite Wurzel & Hsu (2025) in Section 8.
- **Priority:** important

### F-3: OSTI-1305833 Is Misaligned — Do Not Incorporate
- **Target:** Section 1 (Data Availability) and Section 8 (Sources)
- **Category:** analysis
- **Finding:** OSTI-1305833 (Meier, LLNL-TR-652984, 2014) covers tritium breeding blankets exclusively for MFE tokamaks using Dual-Cooled Lead-Lithium (DCLL) architecture. It explicitly scopes itself to tokamak designs and contains no data on laser ICF, IFE chamber design, DPSSL lasers, target economics, or any parameter relevant to the Inertia concept. The tokamak TBB design requirements (PbLi, 600°C outlet, ferritic steel, TBR > 1.1) are structurally different from the liquid-Li IFE first wall that Inertia uses (covered by the already-sourced OSTI-1028880 LIFE study). Attempting to incorporate this source would introduce tokamak-specific constraints into an IFE analysis where they do not apply.
- **Recommendation:** Do not incorporate OSTI-1305833 into the analysis. Add a one-line note in Section 8 (or Section 1) that this source was evaluated and found out of scope: it addresses MFE tokamak tritium breeding blankets, not IFE liquid-Li first-wall systems, and its parameters do not transfer to the Inertia concept.
- **Priority:** minor

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: FOAK laser cost scenario absent from model
- **Target:** model_setup.py — C220104 laser cost parameter and scenario sweep
- **Category:** model
- **Finding:** The analysis identifies the DPSSL laser at $7–10B FOAK ($700–1,000/J) as the dominant capital cost, yet the model anchors C220104 at $1.0B ($100/J NOAK). Consequently `driver_laser_per_mw` shows elasticity only +0.088 — consistent with $1B out of $8.2B total capital — but entirely unrepresentative of the FOAK regime where laser capital alone would approach or exceed the entire NOAK plant cost. The $120/MWh LCOE result is a mature-technology answer for a first-of-a-kind concept, and the model contains no scenario sweep across the FOAK-to-NOAK trajectory.
- **Recommendation:** Add a laser cost scenario sweep in the model: $700/J (FOAK) → $300/J (mid-stage) → $100/J (NOAK), holding all other parameters at base-case values. Report LCOE at each point and label the current base case explicitly as NOAK. This is the single most important cost uncertainty the analysis identifies and the scenario sweep will show the LCOE range this concept could plausibly occupy across its development timeline.
- **Priority:** blocking

### F-2: Diode periodic replacement capital excluded from model
- **Target:** model_setup.py — O&M / periodic capital replacement treatment
- **Category:** model
- **Finding:** The model output explicitly notes "Periodic capex: ~$1.0–2.3B over 30-yr life — NOT included in O&M model." The analysis (Section 4) quantifies the mechanism: at current diode lifetime (~1.4–2.9 GShots), full array replacement across 1,000 beamlines occurs every 4–9 years at ~$2.3B — the dominant single O&M event for the plant. Excluding this understates LCOE by $3–7/MWh and, more importantly, makes the sensitivity table unable to show what diode lifetime progress is worth in LCOE terms. The `om_cost_dt` elasticity (+0.455) already ranks above `q_eng` (−0.392), so the total O&M exposure is the second-largest lever in the model; the diode replacement omission compounds this understatement.
- **Recommendation:** Model diode replacement as an annualized periodic capital charge: `diode_capital / replacement_interval_yrs / annual_energy_MWh`. Parameterize `replacement_interval_yrs` with two scenarios — current-gen (4–9 yr) and target-met (44–63 yr) — and include in the sensitivity sweep. This converts a prose risk into a quantified cost lever and shows what closing the 7–10× diode lifetime gap is worth in LCOE.
- **Priority:** important

### F-3: O&M cost sensitivity ranking inverted relative to Q_target in Section 2 framing
- **Target:** Section 2 — sensitivity ranking and modeling approach note
- **Category:** analysis
- **Finding:** The model shows `om_cost_dt` elasticity of +0.455, ranking above `q_eng` at −0.392. At $1/target × 315M targets/year, target material cost alone contributes more LCOE sensitivity than Q_target gain. Section 2 item 6 correctly names availability as the top lever but then frames the Q_target gap (>30× vs. ~52× required) as the central modeling concern — the energy balance tension receives five paragraphs while O&M cost structure receives one title mention. This ranking inversion matters for Goal 4: improving target cost from $1 to $0.41/target (the Goodin NOAK bottom-up projection) has greater LCOE leverage per unit progress than improving Q_sci from 52× to 60×. The Modeling Approach Note states hypotheses A and B (target cost, diode lifetime), but does not rank them relative to Q_target as LCOE levers.
- **Recommendation:** In the Section 2 Modeling Approach Note, add an explicit sensitivity ranking derived from the model: (1) plant availability, (2) O&M cost structure (target material cost + diode replacement), (3) Q_target. State that reducing target cost from $1 toward $0.41 has higher LCOE leverage than Q_target improvement beyond closure, and that hypothesis A (target cost) should be prioritized in the sensitivity sweep above hypothesis B (diode lifetime) — both ahead of further Q_target exploration.
- **Priority:** important

---

<!-- SUPERSEDED FINDINGS FROM PRIOR ASSESSMENT PASS — RETAINED FOR TRACEABILITY -->
<!-- All three prior iter-1 findings were addressed in the iter-2 analysis pass. -->
<!-- The three carried-forward findings from the original assessment were also addressed. -->
<!-- New findings above replace prior findings. -->

### F-1: Chamber energy gain missing from energy balance analysis
- **Target:** Section 2 (energy balance) and Section 5 (missing parameters table)
- **Category:** analysis
- **Finding:** The LLNL LIFE chamber study (OSTI-1028880, Fusion Science and Technology 2010) — exactly the heritage source flagged as highest-priority in Section 8 gap #8 — provides a chamber energy gain of 1.10 (baseline), meaning the liquid Li breeding blanket delivers ~10% additional thermal energy above the fusion yield through exothermic Li-6 + n → T + He-4 reactions. The Section 2 energy balance calculation does not account for this: it sets net electric = Q_target × 0.10 × 0.45 × 10 MJ × 10 Hz − 1,000 MW, omitting the blanket multiplication. The LIFE study also provides: confirmed thermal efficiency design target ≥40% (800°C Li exit temperature), plant availability target ≥92%, TBR of 1.59 (baseline design), and tritium recovery inventory ~40 g (via Maroni process) — all of which map directly to "blocking" and "important" gaps listed in Section 6. None of these LIFE-sourced values appear in the Section 5 parameter table. The chamber energy gain of 1.10 modestly reduces the required Q_target (from ~56 to ~51), which does not resolve the energy balance tension but should be reflected accurately.
- **Recommendation:** (1) Revise the Section 2 energy balance calculation to include the 1.10 chamber energy gain factor: net electric = Q_target × 0.10 × 0.40 × 1.10 × 10 MJ × 10 Hz − 1,000 MW. State the updated required Q_target (~51) and note that the tension with the stated >30× threshold persists. (2) Add the following rows to the Section 5 available-parameters table, sourced to OSTI-1028880: chamber energy gain (~1.10), thermal efficiency target (≥40%), plant availability target (≥92%), TBR baseline (1.59), tritium recovery inventory (~40 g). (3) Update Section 8 source entry #8 ("NOT YET SOURCED") to reflect that OSTI-1028880 is now available, and note what LIFE.1/LIFE.2 architecture data it provides (chamber radii 3.4 m / 5.7 m, xenon gas fill strategy for ion damage mitigation).
- **Priority:** blocking

### F-2: Indirect drive target manufacturing cost ($0.41/target) distinguishable from economic criterion
- **Target:** Section 3 (target fabrication maturity) and Section 5 (LCOE-relevant parameters)
- **Category:** analysis
- **Finding:** The Goodin et al. (2004) source (OSTI-828518) — the document the analysis cites in footnote [2] for the Goodin economic criterion — contains a distinct and more useful data point: a projected nth-of-a-kind manufacturing cost of **$0.41 per target for indirect drive** (and $0.17 for direct drive). The analysis currently presents only the economic criterion ("target costs must be <10% of electricity generated ≈ $0.75/target") but does not report the manufacturing cost estimate. These are different quantities: the economic criterion is a market-viability ceiling, while $0.41 is a bottom-up manufacturing projection assuming full process maturity. For the indirect-drive Inertia concept, the relevant comparison is $0.41 (achievable nth-of-a-kind) vs. <$1.00 (Inertia's goal) — which shows the <$1 goal is consistent with but not conservative against the heritage estimate. The same source provides a target factory installed capital of ~$100M and annual operating cost of ~$31M for a 1,000 MW(e) direct-drive baseline, filling Section 6 gap #4 ("target fabrication facility capital cost — not-yet-sourced, blocking"). The 10,000× cost reduction required from today's $2,500 experimental target cost is not quantified anywhere in the current analysis.
- **Recommendation:** In Section 3 (target fabrication), add a sentence distinguishing the Goodin manufacturing cost projection ($0.41/target indirect drive, nth-of-a-kind) from the economic criterion ($0.25–$0.30 or $0.75 depending on plant output). Quantify the gap: current experimental cost is $2,500; nth-of-a-kind target is $0.41; required reduction is ~6,000×. In Section 5, add a row for "target factory capital cost (heritage analogue)" citing the ~$100M figure from Goodin et al. and note the adjustment needed for Inertia's indirect-drive design and higher throughput (315M vs. ~182M targets/year). Update Section 6 gap #4 status from "not-yet-sourced" to "partially sourced (direct-drive analogue; indirect-drive adjustment needed)."
- **Priority:** important

### F-3: Laser diode lifetime requirement and cost fractionation are absent from O&M discussion
- **Target:** Section 4 (materials and supply chain) and Section 5 (missing parameters)
- **Category:** model
- **Finding:** The Haefner ILT IFE Workshop source (2023) provides two parameters not present in the analysis that are material for O&M cost modeling. First, **laser diodes represent approximately one-third of total drive laser capital cost** — meaning if the total laser capital is ~$7B FOAK, ~$2.3B is attributable to diodes and ~$4.7B to other laser components (gain medium, optics, structure). The analysis models laser cost as a monolithic $700–$1,000/J estimate without any cost fractionation. Second, diodes require a **lifetime of 14–20 GShots**; current diodes fall 7–10× short of this target, implying a required lifetime of ~1.4–2.9 GShots today. At 10 Hz continuous operation, 1.4 GShots corresponds to ~4.4 years of operation — meaning first-generation diodes would require plant-wide replacement approximately once per decade, representing a multi-billion-dollar periodic capital expenditure. Section 5 lists "O&M cost breakdown (target material, laser diode replacement)" as a blocking gap, and Section 6 gap #6 calls this out — but the current analysis provides no quantitative framing for diode replacement frequency or cost, which this source now enables.
- **Recommendation:** In Section 4, add a paragraph on diode lifetime: state the 14–20 GShot target from the Haefner source, quantify the 7–10× gap in current devices, and calculate the implied replacement interval at 10 Hz (~4–6 years for current-generation diodes; ~44–63 years if the target is met). In Section 5, add a row "laser diode replacement interval" with a range bracketing the current-state and target-state cases. Add a model parameter in the missing-parameters table (or move to available with range): "diode fraction of laser capital cost: ~1/3" to enable the O&M sensitivity sweep to disaggregate diode replacement from other laser maintenance costs. This directly supports the model parameter work flagged in gap #6.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Model driver energy diverges from stated design point
- **Target:** model_setup.py / model_output.txt (energy balance parameters)
- **Category:** model
- **Finding:** The model uses `e_driver_mj = 7.60 MJ` rather than the stated Inertia design value of 10 MJ/shot, and then derives `Q_sci = 62.6` to close 1500 MWe net. This makes the laser electrical recirculating load 760 MW instead of the 1000 MW derived in the Section 2 energy balance calculation. The result is a model that appears more favorable than the analysis's own arithmetic: Q_eng in the model (2.77) implies a substantially lower recirculating power fraction than the analysis shows is required. The model note acknowledges this discrepancy but leaves it unresolved. Using a different driver energy than the stated design point undermines internal consistency and makes it impossible to validate the model against the Section 2 energy balance derivation.
- **Recommendation:** Set `e_driver_mj = 10.0` as the stated Inertia design parameter. Let the model derive the required `Q_sci` (~56×) to close to 1500 MWe net, which will naturally surface the tension with the stated ">30× threshold." Add a sensitivity sweep over `Q_sci` in the range 30–60× to show the LCOE and net power output across the plausible gain range, with a scenario at Q_sci = 30 showing the shortfall (~350 MWe net from a single system).
- **Priority:** blocking

### F-2: Plant availability dominates LCOE sensitivity but is absent from Section 2 ranking and Section 5 parameters
- **Target:** Section 2 (challenge ranking) and Section 5 (Available Parameters table)
- **Category:** analysis
- **Finding:** The model sensitivity analysis shows `availability` has elasticity −0.97 — the single strongest LCOE lever, roughly 3× the sensitivity of `q_eng` (−0.29). Yet Section 2 ranks "energy balance" (which drives q_eng) as the primary challenge with "Impact: Blocking," while O&M cost structure — which drives the availability and replacement-rate assumptions — is listed sixth at "Impact: High." This ranking inversion misrepresents the LCOE leverage hierarchy for this concept. Availability at 10 Hz is uniquely uncertain for this concept: final optics, laser diode modules, and target injection systems have no validated lifetime at commercial duty cycle. Section 5 has no row for capacity factor or plant availability, even though it is the dominant cost driver.
- **Recommendation:** Revise the Section 2 challenge ordering to reflect LCOE leverage: plant availability (driven by component replacement rates) should be elevated to co-equal or higher priority alongside energy balance. Add an explicit availability row to the Section 5 parameter table with a plausible range (e.g., 60–90%) and note that 10 Hz component cycling creates a fundamentally different replacement-rate exposure than any MFE concept. Add a paragraph in Section 2 connecting the final optics and laser diode replacement challenges (items 3 and 6 as currently written) to availability as the unifying LCOE lever.
- **Priority:** important

### F-3: No recommendation on 1costingfe vs. free-form modeling suitability
- **Target:** Section 2 (Modeling Approach) — currently absent
- **Category:** analysis
- **Finding:** The analysis does not address whether the 1costingfe framework is appropriate for this concept or whether free-form modeling is required (Goal 4 checklist). This is a consequential omission: the Inertia concept has no magnets, no plasma physics scaling relations, no cryogenic system, and a capital cost structure dominated by the laser driver (~$7–10B FOAK) and target factory — both of which have no counterpart in the tokamak-derived 1costingfe CAS accounts. The model output shows `C220104 = $1.0B` (NOAK laser) as the largest single CAS22 sub-account, but the basis for this figure is explicitly flagged as uncertain by 7–10×. Whether the 1costingfe structure can adequately represent the IFE cost architecture, or whether a free-form model with explicit laser-cost and target-factory accounts is more transparent, should be stated as a modeling recommendation.
- **Recommendation:** Add a short paragraph to the analysis (logically after Section 2 or as a modeling note in Section 5) stating which modeling approach is recommended and why. If 1costingfe is retained, explain which CAS accounts map to IFE-specific costs (laser driver → C220104, target factory → target_factory_base, target materials → om_cost_dt) and which accounts are structurally inapplicable (magnet-related accounts). If free-form is preferred, state what top-level cost categories the free-form model should track. This framing directly supports testable hypothesis construction (Goal 4).
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_laser_ife.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/iter-3/model_setup.py`
