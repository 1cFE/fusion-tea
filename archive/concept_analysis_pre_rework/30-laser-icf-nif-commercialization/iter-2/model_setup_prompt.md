# 1costingfe Model Update: Laser ICF - NIF Commercialization (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

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
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/iter-2/model_setup.py`
