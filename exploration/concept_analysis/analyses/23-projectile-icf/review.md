# Review: Projectile ICF (D-T)

**Iteration:** 5
**Date:** 2026-04-06
**Files reviewed:** analysis.md, model_setup.py, model_output.txt
**Source documents:** 11 files (iter-01 through iter-03 sources)

---

## Strategic Assessment

### 1. Modeling Approach

The modeling approach is the strongest element of this analysis. Recognizing that the two blocking unknowns — driver capital cost and target gain — have no published analogue cost basis, the analysis correctly rejects a false-precision bottom-up CAS estimate in favor of free-form scenario modeling. This is the right epistemological stance: the model explicitly sweeps over deeply uncertain free parameters and warns against treating the baseline LCOE as a prediction.

The CAS mapping choices are defensible and clearly annotated. Zeroing C220103 (coils) and C220104 (heating) is correct — projectile ICF has no magnets or NBI/RF preheat. Placing the EM driver in C220107 as an override with no published cost basis is the only honest approach. The per-shot consumable structure (C220108 target factory + C220 projectile) captures the novel recurring cost element that has no slot in conventional plant models. The flowing liquid lithium blanket as an integrated first-wall/breeding system (no vessel replacement, TRL 2-3) is correctly captured and its cost assumptions are clearly tagged HIGH or MODERATE UNCERTAINTY.

**One material omission:** The analysis identifies driver operational lifetime as the second-strongest LCOE lever (Hawker Pearson correlation −0.134 vs driver capital cost +0.075) and explicitly recommends sweeping it from 10⁴ to 10⁹ shots (Section 2, Hypothesis 3). The analysis text quantifies the consequences: a driver requiring barrel replacement every 10⁵ shots would impose 1,300 replacement cycles over plant life — "potentially dominant over initial capital cost." Despite this, the model does not implement this sensitivity. The model_output.txt sensitivity sweeps cover gain, driver capital cost, rep rate, driver efficiency, target cost, and availability — but not driver lifetime. The scheduled replacement line in the output shows $0/yr, which accounts only for the blanket (correctly noted as never replaced), leaving the driver replacement cost implicitly at zero. This is an internal inconsistency between the analysis recommendation and the model implementation.

**A secondary modeling concern:** the Conservative scenario (gain=200×, driver=$2B) produces 21 MWe net at fixed rep rate. This is physically correct given the inputs but represents a sub-minimum-viable-scale plant — the model doesn't adjust rep rate to recover target output, so the 2,507 $/MWh figure applies $4.6B of plant capital to a 21 MWe output. The analysis text notes that achieving 333 MWe at gain=200× would require rep rates above 0.1 Hz (potentially violating the chamber clearing constraint), but the model doesn't implement the gain/rep-rate coupling that makes this a cliff edge rather than a smooth slope. The conservative scenario number is technically correct as a fixed-rep-rate result; it should be labeled as "fixed rep rate" to avoid implying a 21 MWe plant is a viable operating scenario.

### 2. Strategic Positioning

The strategic positioning is accurate and well-calibrated. The analysis correctly characterizes this concept as currently without an active commercial pursuer — FLF has pivoted to FLARE, and NearStar is at SBIR Phase I with no demonstrated fusion. The framing of projectile ICF as a concept "provisionally abandoned by its inventor before completing the critical velocity/gain experiments" is the right characterization and is stated plainly without overreach.

The cross-concept comparison table (versus laser indirect-drive, laser direct-drive, heavy-ion, tokamak) is meaningful and accurate. The structural advantages (no precision beam optics, no magnets, no hohlraum, best-in-class TBR) are correctly identified alongside the primary penalty (unknown-cost driver with no industrial analogue at 60 km/s). The comparison axis that matters most — driver cost structure — is correctly flagged as the key differentiator for this concept within the IFE family.

The NearStar taxonomic note is appropriate: the analysis correctly identifies NearStar as a contextual comparator rather than a primary concept instance, and flags that a separate MIF taxonomy row for MTIF would be more accurate. This is honest taxonomy management.

The FLARE pivot as indirect economic evidence for driver unviability is well-handled. The analysis uses it correctly — as a lower bound on what FLF found unviable, not as a cost estimate — and anchors the pessimistic driver cost scenario accordingly.

### 3. Risk and Uncertainty Framing

The risk framing is a strength of this analysis. The five LCOE challenges are ranked by impact with appropriate calibration: driver cost and target gain are correctly labeled "critical," liquid lithium chamber and rep rate coupling are "high," and the abandoned-concept problem is given its own challenge slot (correctly, since it's a structural risk of a different character from the technical ones).

TRL assessments are conservative and defensible:
- EM gun driver: TRL 2-3 (60 km/s never built — correct)
- Target physics: TRL 3-4 (50 neutrons demonstrated; 200–1000× gain required — correct framing of the extrapolation scale)
- Liquid Li chamber: TRL 2-3 (validated computationally, not demonstrated under fusion neutron flux — correct)

The consequence-of-failure analysis for the liquid Li curtain (Section 2, Challenge 4) is well-developed: the dual failure scenario (solid-wall fallback adds recurring replacement cost; TBR fallback eliminates the tritium surplus advantage) correctly identifies that the flowing Li curtain is not merely a cost optimization but the mechanism by which this concept sidesteps the D-T fleet-scaling bottleneck. This is the kind of structural reasoning that makes the analysis genuinely useful.

Tritium surplus revenue is correctly modeled as a scenario branch at $0/g base (fleet saturation) and swept to $30,000/g (current scarcity). The analysis correctly notes that the price is structurally self-undermining at fleet scale — at current scarcity pricing, 25 kg/year surplus approaches 60% of electricity revenue, but fleet deployment collapses the price. This is handled with appropriate nuance.

The confidence ratings in the Section 5 parameter table are well-calibrated. High-confidence values (steam Rankine cycle choice, TBR 1.8 TÜV validation, demonstrated Machine 3 velocity) are correctly rated "high." Low-confidence values (rep rate among three conflicting figures, LCOE target with no bottom-up backing) are correctly rated "low."

### 4. Data Sufficiency

The analysis makes good use of an unusually rich source base for a private fusion concept. The Hawker (2020) paper — authored by FLF's CEO and the primary peer-reviewed analytical foundation for FLF's economic claims — is used as the quantitative anchor throughout. Specific data points (Pearson correlations for LCOE levers, IFE driver cost range $2–10/J, parameter sweep ranges) are cited to specific sections and tables, not just to the paper as a whole.

The HYLIFE UCRL-53356 source is used appropriately to rough-bound Li pump power — a genuinely unknown parameter — using the closest available analogue (same fluid, same reactor class). The resulting estimate (14.5 MW total pump power, ~1-2% recirculating fraction) is flagged as an analogue, not a direct measurement. This is the right epistemic posture.

The analysis correctly acknowledges that no peer-reviewed plant study for projectile ICF exists. The 50-neutron yield from the 2022 Machine 3 demonstration is contextualized correctly: "many orders of magnitude below commercial thresholds." The analysis notes that NIF's ignition shot produced roughly eight orders of magnitude more neutrons — this is an accurate calibration of how far the demonstrated result is from commercial relevance.

The gap inventory (Section 6) is thorough and honestly categorized. The distinction between "truly-unknown" (no public source; would require proprietary data) and "not-yet-sourced" (public source likely exists) is useful. The two "blocking" unknowns that have no public source path (driver capital cost, gain vs. velocity scaling) are correctly isolated.

One sourcing note: the Goodin et al. (2004) target cost economic bound is cited in the model docstring but the underlying citation appears to be borrowed from the laser ICF analysis rather than a direct source review. If the Goodin bound is going to be used to constrain per-target cost ($13.75 ceiling at optimistic gain), the original paper should appear in the sources list. This is minor but affects traceability.

### 5. Cross-Concept Consistency

This is among the first reviews, so there are no approved cross-concept comparisons to check against. The analysis draws on two prior concept analyses internally (07-maglif for pulsed architecture framework; 26-laser-icf-indirect-drive for driver efficiency and final optics comparison). Both comparisons are appropriate and the cross-references are specific.

The reuse of the MagLIF pulsed architecture framework is explicitly flagged (`Reuses: [07-maglif]` in the frontmatter and a dedicated Divergences section). The key difference — MagLIF's capacitor-based driver has a manufacturing scale-up roadmap; projectile ICF's EM launcher at 60 km/s has none — is correctly identified as the most significant structural divergence.

Shared financial parameters (8% discount rate, 40-year lifetime, 6-year construction, NOAK assumptions) are standard and consistent with other analyses. The 85% availability assumption (from Z-IFE study) is a reasonable analogue and flagged as such.

The blanket energy multiplication (1.10) is slightly low for an ⁶Li-enriched design but may be appropriate if natural lithium is assumed. Since the analysis presents the $70M natural Li case as the base in CAS27, the multiplication factor should be consistent with natural Li enrichment (7.5% ⁶Li), which yields lower multiplication than enriched designs. The choice is defensible but the connection between the CAS27 cost scenario and the blanket multiplication parameter isn't explicit in the model.

---

## Verdict

VERDICT: PROCEED

This analysis is strategically sound. The concept is correctly characterized as commercially dormant (no active pursuer after FLF's FLARE pivot), the free-form scenario modeling approach is the right response to two blocking unknowns with no published analogues, the source utilization is strong relative to what exists in the public domain, and the risk framing — particularly the liquid Li curtain failure mode analysis and the FLARE pivot as indirect economic evidence — is genuinely useful for cross-concept comparison. The minor fixes below address an internal gap (driver lifetime sweep not implemented despite being identified as the second-strongest LCOE lever) and a scenario labeling concern, neither of which changes the fundamental positioning or conclusions.

---

## Minor Fixes (PROCEED only)
<!-- MACHINE-PARSED: use exactly "## Minor Fixes" as the heading -->

### PA-1: Add driver lifetime sensitivity sweep or document the omission
- **Category:** improvement
- **Severity:** minor
- **Location:** model_setup.py, model_output.txt
- **Finding:** The analysis identifies driver operational lifetime as the second-strongest LCOE lever (Hawker Pearson −0.134, stronger than driver capital cost at +0.075), quantifies the uncertainty span as 10⁴–10⁹ shots, and explicitly recommends sweeping it (Section 2, Hypothesis 3). The model does not implement this sensitivity. The scheduled replacement line in model_output.txt ($0/yr) accounts for the blanket but leaves driver barrel replacement implicitly at zero — inconsistent with the analysis text, which calls it "potentially dominant over initial capital cost."
- **Proposed Fix:** Either (a) add a `driver_lifetime_shots` parameter and compute annual driver replacement cost (driver_cost_M_USD / driver_lifetime_shots × shots_per_year), then sweep from 10⁴ to 10⁹ shots; or (b) add a note in model_output.txt's Critical Framing block stating "Driver lifetime sweep not yet implemented — see analysis.md §Section 2, Hypothesis 3. Under pessimistic lifetime assumptions (10⁵ shots), replacement cost would exceed driver capital cost."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: Label Conservative scenario as fixed-rep-rate result
- **Category:** improvement
- **Severity:** minor
- **Location:** model_output.txt, §Scenario Comparison
- **Finding:** The Conservative scenario (gain=200×, driver=$2B) produces 21 MWe net — sub-minimum viable plant scale — because the model holds rep rate fixed at 0.033 Hz rather than adjusting it to recover target output. The LCOE of 2,507 $/MWh at 21 MWe reflects a real physical constraint (you can't reach 333 MWe at gain=200× and 0.033 Hz), but the scenario label doesn't communicate this. A reader might interpret 2,507 $/MWh as the conservative LCOE for a full-sized plant.
- **Proposed Fix:** Add a parenthetical to the Conservative row: "(21 MWe at fixed rep rate — sub-minimum viable scale; achieving 333 MWe at gain=200× requires rep rate >0.1 Hz, see Constraint 3)".
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-3: Add Goodin (2004) to sources list or clarify the citation chain
- **Category:** inconsistency
- **Severity:** minor
- **Location:** analysis.md §Section 8, model_setup.py docstring §target_cost_USD
- **Finding:** Goodin et al. (2004) is cited in the model docstring for the target cost economic ceiling ($13.75 at optimistic gain), but the paper does not appear in the Section 8 sources list — only a reference noting it is "referenced in 26-laser-icf-indirect-drive." If the bound is being applied directly to this concept's cost model, the source should be traceable from this analysis rather than borrowed from a sibling analysis.
- **Proposed Fix:** Add Goodin et al. (2004) as a formal source entry in Section 8, with a note on which specific figure is being applied and the source path. If the paper has already been extracted to the knowledge base, cite it directly; if not, flag it as "not-yet-extracted" with the DOI or journal reference.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_
