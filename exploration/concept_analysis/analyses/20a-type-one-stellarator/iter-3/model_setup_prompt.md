# 1costingfe Model Update: QI Modular HTS Stellarator - Infinity Two

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Island divertor is two distinct design options with different TRL — not a single concept

- **Target:** Section 3 (Island Divertor at Burning Plasma Power Level — TRL 3–4) and Section 2
  (challenge 4, island divertor performance)
- **Category:** analysis
- **Finding:** The E67 paper defines two separate divertor designs under development for Infinity Two:
  (1) a classical island divertor following W7-X geometry (8 plates, 2 per field period), and (2) a
  novel Large Island Backside Divertor (LIBD) with a dome structure inserted inside the island interior
  plus active baffling, designed to improve neutral confinement and particle exhaust. The current
  analysis treats island divertor as a single TRL 3–4 system. In practice, these represent two
  scenario branches with substantially different risk profiles: the classical design is a direct
  W7-X extrapolation (TRL 4–5) but has critically poor particle exhaust efficiency (0.44–2.9%,
  W7-X scale), while the LIBD targets 12.6% exhaust efficiency but is TRL 2–3 and explicitly requires
  Infinity One experimental validation before Infinity Two final design commitment. The LIBD dome must
  survive deep inside the island interior with challenging active cooling access — a cooling access
  problem the E67 paper does not resolve and flags as future work. Choosing the classical divertor
  reduces TRL risk but may create a particle exhaust shortfall that affects steady-state operability
  and availability; choosing the LIBD preserves exhaust performance but adds a TRL 2–3 item to the
  critical path. This is a scenario-determining design choice, not a single system at a single TRL.
- **Recommendation:** Split the island divertor discussion in Section 3 into two named options
  (classical and LIBD) with separate TRL ratings (4–5 vs 2–3), separate validation requirements, and
  separate O&M implications. In Section 2, update challenge 4 to distinguish the exhaust efficiency
  gap as the core reason the LIBD exists and flag LIBD cooling-access uncertainty as an additional
  cost/schedule risk on top of the general island divertor unknowns. Add a row to the Section 6 data
  gap inventory for divertor design selection (classical vs LIBD) as a scenario branch with blocking
  criticality for the availability and O&M model.
- **Priority:** important

---

### F-2: Error field correction coil requirement is an unresolved capital cost risk — not mentioned anywhere in the analysis

- **Target:** Section 2 (Challenges) and Section 6 (Data Gap Inventory)
- **Category:** analysis
- **Finding:** E67 explicitly states that sensitivity of the Infinity Two divertor design to magnetic
  field errors is "left to future work." W7-X required auxiliary external correction coils to suppress
  low-order error modes (n/m=1) that would otherwise degrade island topology and divertor
  performance. The current Infinity Two design goal is to avoid such auxiliary coils, but this has not
  been validated — it is an open engineering question. If field errors at Infinity Two scale require
  correction coils, this is an unbudgeted capital item (additional coil systems, power supplies, and
  cryogenic infrastructure) with no cost estimate. The current analysis does not mention error field
  correction coil requirements anywhere in Sections 2, 3, 5, or 6.
- **Recommendation:** Add a brief item to Section 2 under challenge 1 or as a new challenge noting
  that error field tolerance for the Infinity Two island divertor topology is unvalidated, that W7-X
  required auxiliary correction coils, and that the need for equivalent coils in Infinity Two has not
  been assessed. Add a corresponding row to the Section 6 data gap inventory (gap type: truly-unknown,
  criticality: important) noting that if correction coils are required, this adds unbudgeted capital
  to CAS22 with no published cost basis.
- **Priority:** important

---

### F-3: Particle exhaust efficiency range (order-of-magnitude uncertainty) is an LCOE-relevant parameter missing from Section 5

- **Target:** Section 5 (LCOE-Relevant Parameters) and Section 2 (challenge 4)
- **Category:** analysis
- **Finding:** E67 quantifies the required particle exhaust efficiency for Infinity Two as 0.5%–5%
  (bracketing conservative and optimistic particle-transport assumptions), with W7-X-equivalent
  classical divertor achieving only 0.44%–2.9% and the LIBD targeting 12.6% (untested). This
  order-of-magnitude uncertainty in pumping efficiency directly sizes the vacuum pumping system — a
  larger pump installation is needed at lower exhaust efficiency — and affects whether steady-state
  helium ash removal is achievable at all with the classical design. The current analysis flags island
  divertor performance at burning plasma conditions as Impact: Moderate but does not capture exhaust
  efficiency as a specific parameter, does not quantify the vacuum pumping system cost sensitivity,
  and does not state that the classical divertor may be marginal for helium ash removal at burning
  plasma throughput. This gap leaves the Section 5 parameter table silent on a component cost driver
  that the primary source explicitly calls out as a major design uncertainty.
- **Recommendation:** Add a row to the Section 5 available/missing parameters table for particle
  exhaust efficiency, with value 0.44%–12.6% depending on divertor design choice, source E67, and
  low confidence. In Section 2, update challenge 4 to state that classical divertor exhaust efficiency
  (W7-X analogue) is at the low end of the required 0.5%–5% range and may require LIBD to ensure
  reliable helium ash removal over a 2-year operating cycle. Add exhaust efficiency as a scenario
  parameter in Section 6 linked to the divertor design selection gap.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Model operating point inconsistent with published fusion power and analysis-derived thermal efficiency
- **Target:** Model output (η_th, fusion power)
- **Category:** model
- **Finding:** The model uses η_th = 0.40 and derives fusion power = 955 MW to yield 350 MWe net. But Section 2 works through the power balance from the *published* 800 MW fusion power and correctly derives implied thermal efficiency ≈ 45%: gross electric ≈ (350 + ~65 recirculating) = 415 MWe / thermal 920 MW (800 × 1.15 blanket multiplier) = 45%. These are inconsistent — the model and analysis are implicitly using different fusion powers and different thermal efficiencies. At η_th = 0.40 and published 800 MW fusion power, the net-minus-recirculating equation closes only if recirculating power is ~18 MWe, which is implausibly low given ECRH alone draws ~38–40 MWe electrically. The model is internally consistent at its own operating point (955 MW, η_th = 0.40), but that point does not match the published Infinity Two design. The LCOE result is therefore computed from a different plant than the one the analysis describes.
- **Recommendation:** Reconcile the model's thermal efficiency with the Section 2 power balance derivation. Preferred fix: use the published 800 MW fusion power as a fixed input and update η_th to ~0.45 (consistent with Section 2's inference). If the framework cannot accept fusion power as a fixed parameter, document explicitly in the model output that the operating point (955 MW, 40%) differs from the published design (800 MW, ~45%) and estimate the LCOE impact of the discrepancy. The "Key Assumptions" block should note this inconsistency rather than presenting both values as if they are consistent.
- **Priority:** important

### F-2: Modeling approach rationale not stated
- **Target:** Section 2 (modeling recommendations)
- **Category:** analysis
- **Finding:** The analysis identifies the top 3 LCOE sensitivity parameters and recommends uncertainty ranges, but does not state whether 1costingfe framework or free-form modeling is appropriate for this concept, nor why. The model output labels nearly all capital accounts as "FRAMEWORK DEFAULTS" and acknowledges the dominant cost item (C220103, 3D HTS coils) as a structural lower bound with no cost precedent. For a concept where the framework was built primarily from tokamak/LTS reference data and the stellarator-specific cost structure (no central solenoid, no current drive system, island divertor vs. tokamak divertor) differs materially, the choice to use 1costingfe deserves explicit justification against the alternative of a stellarator-adapted parametric model anchored to ARIES-CS and Brown (2018). The checklist requires this rationale (Goal 4).
- **Recommendation:** Add a short paragraph to Section 2 after the top-sensitivity-parameter discussion stating: (a) 1costingfe is used because no stellarator-specific commercial cost database exists; (b) C220103 (3D HTS coils) is the primary account where the framework default is a known lower bound; (c) ARIES-CS and Brown (2018) could anchor a free-form alternative if higher cost-structure fidelity is needed and should be the reference for any concept-specific CAS adjustment. If free-form would better capture the stellarator cost structure (e.g., zero out central solenoid, add island divertor as distinct line item), recommend that instead with brief reasoning.
- **Priority:** important

### F-3: Availability not scenario-bracketed despite sensitivity equal to coil cost
- **Target:** Model output / Section 2 (top LCOE sensitivity parameters)
- **Category:** model
- **Finding:** Availability (elasticity −0.93) is identified as the second-highest LCOE sensitivity parameter — nearly equal to 3D HTS coil cost (elasticity +0.99) — but the model sweeps only coil cost (1×, 3×, 5×). Availability is fixed at a single point estimate (87%) with no scenario bracket, despite the analysis correctly flagging it as unconstrained: the 2-year cycle implies ~96% theoretical maximum but actual availability from ECRH failures, tritium processing interruptions, and island divertor degradation is unknown. The coil cost sweep shows LCOE ranging from 311 to 846 $/MWh (350 MWe basis). An availability sweep from pessimistic to aspirational would produce a comparable range. Without it, one major uncertainty is bracketed and the other is hidden as a fixed assumption.
- **Recommendation:** Add an availability scenario sweep to the model output analogous to the coil cost sweep: for example, 80% (pessimistic — comparable to early-stage D-T MCF plant per Araiinejad & Shirvan 2025), 87% (current model default), 93% (mid-range), 96% (aspirational, 2-year cycle theoretical maximum). Present the resulting LCOE range to show both primary uncertainties are bracketed. The Section 2 narrative already recommends modeling availability as an uncertainty range — the model output should fulfill that recommendation.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_stellarator.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/iter-3/model_setup.py`
