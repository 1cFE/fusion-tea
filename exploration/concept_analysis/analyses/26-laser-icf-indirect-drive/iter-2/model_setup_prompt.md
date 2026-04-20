# 1costingfe Model Update: Laser ICF - Indirect Drive (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/26-laser-icf-indirect-drive/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/26-laser-icf-indirect-drive/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Target factory capital cost gap is now fillable from Goodin 2007
- **Target:** Section 5 (Parameters — Missing Parameters table, gap #5) and Section 6 (Data Gap Inventory, gap #5)
- **Category:** model
- **Finding:** The Goodin 2007 FPA presentation (fire-fpa07-goodin-icf-fuel.md) provides nth-of-a-kind target factory cost estimates for laser fusion: ~$97M installed capital, ~$19M/yr operating costs, for 500,000 targets/day serving a ~1 GWe plant. The per-target cost in this study is 16.6¢ — well under the Goodin 10% economic threshold — but this assumes nth-of-a-kind production with "a major paradigm shift from current day." The study also identifies that injection accuracy is still ~125 µm (6× off the 20 µm goal), confirming the TRL gap in Section 3. The existing analysis correctly cites the 10% threshold but leaves the factory capital cost as a blocking unknown; this source provides a concrete, citable baseline.
- **Recommendation:** Add a row in the Section 5 Available Parameters table for "Target factory capital cost (laser IFE, nth-of-a-kind)" with value ~$97M, source fire-fpa07-goodin-icf-fuel.md, confidence low (NOAK assumption, 2007 dollars). Add a second row for "Target factory annual O&M" at ~$19M/yr. Update gap #5 in Section 6 from "not-yet-sourced / blocking" to "sourced / important" and note that the FOAK premium above this NOAK baseline is not quantified. In Section 5 model_setup.py, add target_factory_capex as a sensitivity parameter anchored at $97M with a 3–10× FOAK multiplier range.
- **Priority:** blocking

### F-2: Hawker model provides O&M baseline, plant capital proxy, and reframes driver risk
- **Target:** Section 2 (Dominant LCOE uncertainty 1 — Laser driver cost) and Section 5 (Parameters — Missing Parameters)
- **Category:** analysis
- **Finding:** The Hawker PMC article (pmc-articles-pmc7658748.md) is already referenced in Section 1 as existing IFE LCOE methodology, but the analysis does not incorporate any of its quantitative outputs. Three findings are material: (1) O&M cost default of $30/kWe-yr (the only IFE-specific O&M figure available, filling the "important" gap in Section 5); (2) HYLIFE-II plant cost inflated to 2020 dollars excluding driver is $3,600/kWe (the only IFE non-driver capital cost proxy available, filling the missing parameter gap for chamber/BOP capital); (3) Hawker's sensitivity analysis shows driver *lifetime* has a stronger correlation with LCOE (−0.134) than driver unit *cost* (+0.075) — the threshold being ~5 years / 30 million shots. Section 2's framing of driver cost as the dominant uncertainty is therefore incomplete: at Inertia's 10 Hz rep rate, 30M shots represents only ~35 days of operation, making driver operational durability a more acute LCOE risk than the absolute cost per joule.
- **Recommendation:** In Section 2, add a paragraph after the driver cost discussion noting that Hawker's sensitivity analysis identifies driver lifetime as a stronger LCOE lever than unit cost, and that at 10 Hz, the 30M-shot reliability threshold corresponds to ~35 operating days — far below any commercial requirement. Frame this as a sixth dominant LCOE uncertainty: driver operational durability and replacement cadence. In Section 5, add rows for "O&M cost (IFE proxy)" at $30/kWe-yr and "Non-driver plant capital (HYLIFE-II 2020$)" at $3,600/kWe, both sourced to the Hawker paper. Remove O&M from the Missing Parameters table if the $30/kWe-yr figure is deemed adequate as a placeholder.
- **Priority:** important

### F-3: Tritium processing system capital cost now available for FLiBe designs
- **Target:** Section 5 (Parameters — Missing Parameters, gap #10) and Section 4 (FLiBe Molten Salt)
- **Category:** model
- **Finding:** The OSTI source (osti-biblio-10179076.md) covers the HYLIFE-II tritium management system and provides the first quantified cost for this subsystem: $92M total, dominated by vacuum disengagers ($52M). It also quantifies recirculating pump power for the vacuum disengager at 6.6 MW — a non-trivial contribution to recirculating power fraction — and notes that a demonstration experiment for vacuum disengager operation with FLiBe was still needed as of publication (early 1990s), placing this subsystem at TRL 3–4. The existing analysis flags tritium processing capital cost as an "important" gap (gap #10) and correctly notes TBR > 1.2 for HYLIFE-III, but has no cost figure or recirculating power estimate for the tritium extraction system.
- **Recommendation:** Add a row in Section 5 Available Parameters for "FLiBe tritium processing system capital cost (HYLIFE-II)" at $92M, sourced to osti-biblio-10179076.md, confidence low (1990s dollars, HYLIFE-II architecture). Add a note that 6.6 MW of recirculating pump power for tritium extraction should be included in the recirculating power budget. In Section 4 (FLiBe section), add a sentence noting that the tritium extraction subsystem (vacuum disengager) cost is ~$92M based on HYLIFE-II, and that TRL is ~3–4 (demonstration still needed). Update gap #10 in Section 6 from "not-yet-sourced / important" to "partially sourced / important" noting that HYLIFE-III may supersede these 1990s estimates.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Laser driver override freezes the dominant cost item out of sensitivity sweeps
- **Target:** model_setup.py — C220107 override and sensitivity sweep design
- **Category:** model
- **Finding:** The laser driver is modeled as a fixed $3,000M override on C220107. The sensitivity output shows `driver_laser_per_mw` elasticity of only +0.045, which is physically inconsistent: a $3B item representing ~58% of CAS22 should dominate the sensitivity table, not rank below interest rate, availability, and construction time. The override bypasses parameterization entirely, so the reported sensitivity results do not reflect the actual LCOE uncertainty from laser cost — which the analysis correctly names as "the cost driver with no analogue in the rest of the fusion landscape." The model assumptions note a range of $1,400M (optimistic) to $8,500M (FOAK), a 6× spread that would overwhelm every other parameter in the table.
- **Recommendation:** Replace the fixed override with a parameterized laser cost calculation (e.g., laser_cost_per_j × laser_energy_j, where laser_cost_per_j is swept from $60/J NOAK to $700/J FOAK). Include this parameter in the sensitivity sweep. The model assumptions already document the bounding values — they need to drive the computation, not sit as footnotes while a hardcoded constant is reported.
- **Priority:** blocking

### F-2: Target factory capital cost is implausibly low by ~2 orders of magnitude
- **Target:** model_setup.py — C220600 and target factory cost parameterization
- **Category:** model
- **Finding:** C220600 (target factory) = $15.9M. The analysis identifies target factory as a blocking gap and shows that Inertia must produce 864,000 cryogenic DT targets/day at <$0.75/target to be economical. A factory at that throughput — with automated cryogenic layering, precision capsule assembly, quality control, and in-facility tritium handling — would represent a capital investment multiple orders of magnitude larger than $15.9M. The sensitivity coefficient for `target_factory_base` (+0.053) is low, which follows from the underweighted baseline, but this inverts the analysis narrative, which treats target factory cost as a primary LCOE constraint. The Goodin (2004) rule and the GEM bottom-up model are identified as the right frameworks for this number — neither is reflected here.
- **Recommendation:** Derive a plausible target factory capital cost range using the Goodin constraint as a back-calculation anchor (e.g., at $0.75/target × 864,000/day × 365 days = $236M/yr in target costs, what factory CAPEX at a 15% annual carrying charge implies $1.6B?), or use a scenario branch with low/central/high factory costs. Include target factory cost in the sensitivity sweep. The current $15.9M value makes target economics invisible in the model output, contradicting the analysis's own blocking-gap rating.
- **Priority:** blocking

### F-3: Availability dominates model sensitivity but is unaddressed in the analysis framing
- **Target:** Section 2 (Dominant LCOE Uncertainties) and Section 5 (Missing Parameters)
- **Category:** analysis
- **Finding:** The model's sensitivity sweep shows availability with elasticity -0.97 — the single largest driver, larger than laser cost (0.045), target gain (q_eng = -0.18), or thermal efficiency (-0.18). The analysis acknowledges capacity factor as a blocking gap (Section 6, Gap #3) but does not discuss it as a dominant LCOE sensitivity in Section 2, which lists five uncertainties without mentioning availability. This is a structural inconsistency: the model is most sensitive to a parameter the analysis barely discusses, while the analysis foregrounds parameters (laser cost, target gain) that are minor in the model. The gap exists partly because availability is hardcoded at 75% without a rep-rate-coupled model — but that makes the sensitivity result even more important to flag, since the assumed value is unvalidated.
- **Recommendation:** Add availability as a sixth dominant LCOE uncertainty in Section 2 (or promote it to the top of the list given the model result). Explain the 75% assumption and its physical basis — or explicitly note that it is an unvalidated placeholder. Identify the range: a plant requiring 3–5 year chamber replacements (Inertia claim) may have availability significantly below 75%, while a liquid-wall design with no chamber replacement (Xcimer) could be higher. State this as a testable scenario branch: availability is a first-order LCOE driver, and the model confirms it quantitatively.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/26-laser-icf-indirect-drive/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_laser_ife.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/26-laser-icf-indirect-drive/iter-2/model_setup.py`
