---
ID: 07-maglif
Concept: MagLIF (Pacific Fusion)
Company: Pacific Fusion
Type: synthesis
Status: draft
Created: 2026-06-08
---

## 1. Executive Summary

- **Dominant risk:** Rep-rated chamber operations at GJ-scale yields are on-paper only (TRL 1–2). The entire economic case depends on achieving ~0.5–1 Hz with cryogenic targets that have never been tested, in chambers that have never operated at any rep rate. Without this, LCOE is uncompetitive.
- **Dominant advantage:** Eliminates superconducting magnets entirely — no HTS tape bottleneck, no years-long magnet fabrication, no quench risk. Driver is built from mass-producible capacitor bricks using commodity materials.
- **LCOE ballpark:** 125 $/MWh (1 GWe NOAK projection from library defaults). This is ~2× higher than the Z-IFE study's optimized single-chamber case (7.0 ¢/kWeh in 2005 dollars ≈ 12 $/MWh in 2024 dollars), because the library assumes lower rep rate and lower yield than the Z-IFE optimum.
- **Confidence verdict:** Low. The design point predates the MagLIF concept itself (dynamic hohlraum targets, not magnetized liner), no modern power plant study exists for the IMG + self-magnetizing target architecture Pacific Fusion is pursuing, and the two most leveraged parameters (rep rate and per-shot yield) are undemonstrated at power-plant scale.

## 2. What Matters Most for LCOE

### 1. Repetition rate (f_rep) — Elasticity: ~1.0

**Assumed value:** 0.1 Hz per chamber (Z-IFE baseline)
**Source:** SAND2006-7148 §3.1.1.6
**Sensitivity:** LCOE is inversely proportional to rep rate at constant driver cost. The Z-IFE study showed that a single-chamber plant at 0.5 Hz achieves 7.0 ¢/kWeh vs. 20 ¢/kWeh for a 10-chamber plant at 0.1 Hz — a 2.8× LCOE reduction from 5× rep rate increase.
**What would flip the conclusion:** Demonstrated chamber operation at ≥0.5 Hz with GJ-scale yields and cryogenic targets would bring LCOE into the competitive range. Failure to exceed 0.1 Hz makes the concept economically non-viable.

### 2. Per-shot yield (Q_yield) — Elasticity: ~0.5

**Assumed value:** 3–30 GJ range; library defaults select ~4 GJ based on archetype priors
**Source:** Z-IFE gain curve G = 30.15 × (E − 1.22)^2.038 for dynamic hohlraum (not MagLIF)
**Sensitivity:** Higher yield per shot directly increases net power output at constant rep rate and driver cost. The Z-IFE optimized case used 4600 MJ yield at 42 MJ driver energy. Halving the yield approximately doubles LCOE.
**What would flip the conclusion:** Experimental demonstration of >3 GJ yields on Z-scale machines with MagLIF targets (not dynamic hohlraums) would validate the physics basis. Current Z machine record yields are orders of magnitude below this threshold.

### 3. Driver capital cost (C220107) — Elasticity: ~0.15

**Assumed value:** $364.5M at 1 GWe NOAK (library default for MAGLIF archetype)
**Source:** No company-grounded value for IMG driver at Pacific Fusion scale. Z-IFE detailed estimate is $372M (2004$) for a single 1 PW LTD driver, but that driver is much larger than any of the 10 individual chamber drivers in the baseline plant. The systems model used $15/J parametric assumption.
**Sensitivity:** Driver capital is ~8% of CAS22 and ~4% of total overnight cost in the 1 GWe projection. A 2× driver cost increase would increase LCOE by ~15%.
**What would flip the conclusion:** A published bottom-up driver cost for IMG architecture at 50–100 MA and power-plant rep rates (0.5–1 Hz) would bound this uncertainty. If IMG brick costs don't reach the target ~$0.50/J (down from current ~$5/J), driver capital could be 5–10× higher than assumed.

### 4. Per-shot consumable cost (target + RTL) — Elasticity: ~0.2

**Assumed value:** Embedded in library defaults; no explicit override
**Source:** Z-IFE study used 2× General Atomics laser IFE capsule cost for dynamic hohlraum targets, but no $/shot figure is extracted
**Sensitivity:** At 0.1 Hz aggregate (10 chambers), the plant fires ~3.15M shots/year. At 0.5 Hz single-chamber, ~15.8M shots/year. If per-shot cost exceeds ~$10/shot, consumables become the dominant operating cost. Pacific Fusion's self-magnetizing targets (plastic + aluminum) eliminate beryllium and external coils, but cryogenic ice-layer fabrication adds cost. The Z-IFE study noted that steel RTL remanufacturing alone required 170 MWe recirculating power (17% of gross output).
**What would flip the conclusion:** Published target + RTL manufacturing cost at volume production (>10M units/year) would resolve this. If costs are demonstrably <$1/shot, this parameter becomes negligible. If >$50/shot, the concept is economically retired.

### 5. Thermal-to-electric efficiency (eta_th) — Elasticity: ~0.4

**Assumed value:** 42% (Z-IFE baseline with F82H steel chamber); library default ~0.40
**Source:** SAND2006-7148 §3.1.1.3; combined Brayton-Rankine cycle recommended
**Sensitivity:** Net electric power = (fusion power − recirculating power) × eta_th. A 10 percentage point change in eta_th produces ~25% change in net output and ~40% change in LCOE.
**What would flip the conclusion:** Thermal buffering technology for pulsed-to-steady thermal conversion could enable advanced cycles (supercritical CO₂ Brayton at 50%+), improving LCOE by 20–30%. Conversely, if pulsed thermal cycling limits efficiency to <35%, LCOE increases proportionally.

## 3. Risk Verdicts

### Cryogenic DT ice-layer targets at mass production (TRL 1–2)
**Verdict:** Unlikely resolvable at required scale
**Rationale:** NIF's cryogenic target system takes 15–20 hours per target using precision cryostats. Scaling to 15M+ targets/year (0.5 Hz operation) requires a fundamentally different manufacturing paradigm — parallel batch cooling pipelines with robotic handling — that has never been designed, prototyped, or costed. Pacific Fusion's self-magnetizing composite targets have only been demonstrated at room temperature; compatibility with cryogenic ice layers is not publicly addressed. Sandia's MagLIF cryostat achieves ~5 minutes per target, but even at this rate, 0.5 Hz operation would require 150+ parallel cryostats operating continuously.
**What would retire this risk:** Demonstrated production of ≥1000 cryogenic MagLIF targets per day with quality assurance, automated insertion, and cost <$10/target.

### Rep-rated chamber operations at GJ-scale (TRL 1–2)
**Verdict:** Genuinely uncertain
**Rationale:** The physics of GJ-scale explosions in confined geometry with thick liquid walls is understood in principle. The engineering challenges (RTL insertion at <2 seconds, liquid curtain reformation, debris management, vacuum reconditioning, electrode lifetime under neutron + blast loading) are tractable in principle but have zero experimental validation. University of Wisconsin water jet experiments showed ~Hz-compatible reformation at reduced blast loads, but no GJ-scale experiments exist.
**What would retire this risk:** A subscale chamber demonstrator operating at ≥0.1 Hz with MJ-scale blasts (not full GJ yields but proportionally scaled) that validates RTL insertion, liquid wall cycling, and sustained operation over ≥10,000 shots.

### Driver brick lifetime (current: ~10⁴ shots; required: ~10⁹ shots)
**Verdict:** Likely resolvable
**Rationale:** Capacitor and switch degradation mechanisms are well-understood from decades of pulsed power engineering. Fuse Energy has already demonstrated >100 consecutive shots on TITAN I. The 1000× lifetime extension requirement (from 10⁴ to 10⁹ shots at 1 Hz ≈ 30 years) is a materials science and quality control challenge, not a fundamental physics barrier. Power electronics for grid-scale inverters and industrial motor drives routinely achieve >10⁸ cycle lifetimes.
**What would retire this risk:** Published accelerated lifetime testing results showing ≥10⁷ shot capacity for production IMG bricks under power-plant thermal and electrical stress conditions.

### Yield scaling from 20 MA (demonstrated) to 60+ MA (required)
**Verdict:** Genuinely uncertain
**Rationale:** The Z-IFE gain curve is based on dynamic hohlraum simulations, not MagLIF targets. MagLIF experiments on Z have demonstrated fusion-relevant conditions (nτ > 10²¹ keV m⁻³ s) but at yields far below the GJ threshold. Scaling to 60+ MA with ice-layer targets is supported by 2D simulations but has no experimental validation. Pacific Fusion's demonstration system (DS) is sized at >60 MA, so the company is betting on this scaling being correct.
**What would retire this risk:** Experimental yield measurements on Z-class machines (20–30 MA) with modern MagLIF targets that confirm the simulated gain-vs-current curve within 2× uncertainty, extrapolated to 60 MA with validated 2D hydro codes.

### Per-shot consumable cost floor
**Verdict:** Likely resolvable
**Rationale:** Pacific Fusion's self-magnetizing targets eliminate the two most expensive per-shot components from traditional MagLIF: beryllium liners (~$800/kg) and external copper coils. The remaining bill of materials is plastic, aluminum (commodity metals), and DT fuel (negligible cost per shot). The RTL material (FLiBe in Z-IFE frangible concept) is recycled within the coolant loop. The dominant remaining cost is cryogenic target fabrication labor and energy, which is fundamentally a manufacturing-scale problem, not a materials bottleneck.
**What would retire this risk:** Published cost breakdown showing <$5/shot for target + RTL at ≥1M units/year production volume, including cryogenic fabrication.

## 4. Structural Advantages and Disadvantages

### Advantages vs. D-T tokamak baseline:

**1. Eliminates superconducting magnet supply chain constraint (~15–25% of tokamak capital)**
No HTS tape, no Nb₃Sn, no multi-year magnet fabrication timelines, no quench risk. The pulsed power driver is built from commodity capacitors and switches amenable to automated mass production. This is the single largest structural cost difference.

**2. Eliminates divertor and plasma-facing component replacement cycle (~10–20% tokamak availability loss)**
The thick liquid FLiBe wall shields all structural components from direct neutron and plasma exposure. If the liquid wall operates as designed, there is no periodic blanket module replacement analogous to tokamak DEMO projections (which assume ~10–20% of operational lifetime spent replacing blanket sectors). Chamber availability is limited by driver reliability and RTL insertion cycle time, not by material degradation.

**3. Driver modularity enables incremental capacity scaling**
Adding chambers is a parallelization problem, not a physics-scale problem. A tokamak must be built at its design scale (you can't build "half an ITER"). A MagLIF plant can start with 1–2 chambers and add more as demand and capital allow, each with independent driver, thermal cycle, and power conversion. This changes the risk profile of first-of-a-kind deployment.

### Disadvantages vs. D-T tokamak baseline:

**1. Rep rate as LCOE bottleneck (~2–10× LCOE swing from 0.1 Hz to 0.5 Hz)**
Tokamaks operate at steady state; their LCOE is insensitive to "pulse rate." MagLIF's pulsed architecture makes rep rate the most leveraged parameter in the entire cost model. Achieving high rep rate requires solving chamber clearing, target insertion, and cryogenic fabrication at industrial scale — none of which are needed for steady-state concepts.

**2. Per-shot consumables create operating cost floor (~10–30% of LCOE)**
Every shot destroys the target and (depending on RTL design) potentially the transmission line. At 15M+ shots/year, even $1/shot becomes a $15M/year operating cost. Tokamaks have no per-pulse consumables (fuel cost is negligible for D-T). This fundamentally changes the operating cost structure.

**3. Yield scaling is extrapolated from simulation, not experimental validation**
Tokamak Q>1 has been demonstrated experimentally (JET, JT-60SA). MagLIF's GJ-scale yields at 60+ MA are supported by simulations but have never been measured. The current experimental yield record on Z is orders of magnitude below the power-plant requirement. This is a confidence issue, not a cost issue, but it affects financability.

**4. Cryogenic target fabrication is a novel manufacturing challenge**
Tokamaks require continuous D-T fueling (gas puffing or pellet injection) but not precision cryogenic assemblies. MagLIF requires a cryogenic ice layer frozen to <100 μm uniformity on the inner liner wall, fabricated at ≥1 Hz if operating at 1 Hz. No manufacturing process exists for this at scale.

## 5. Cross-Concept Positioning

MagLIF occupies a unique position in the fusion landscape: it is the only pulsed-power-driven magneto-inertial fusion concept under commercial development.

**Shares with laser ICF (NIF-style):**
- Pulsed operation with per-shot consumables
- Cryogenic DT target fabrication requirement
- Liquid-wall chamber concept (though NIF uses direct-drive gas-filled hohlraums, not liner compression)
- Gain scaling extrapolated from simulations, not experimental demonstrations

**Diverges from laser ICF:**
- Driver technology: electrical (capacitors) vs. optical (lasers) — fundamentally different supply chains and cost structures
- Target coupling: physical RTL contact vs. free-flight laser beams — different alignment tolerances and failure modes
- Rep-rate regime: sub-Hz vs. 1–10 Hz (laser IFE targets 10 Hz for economic viability)

**Shares with tokamaks/stellarators:**
- D-T fuel cycle, tritium breeding requirement, thermal energy conversion
- Neutron shielding and activation challenges

**Diverges from tokamaks/stellarators:**
- No superconducting magnets, no steady-state plasma control, no divertor
- Pulsed vs. continuous operation — changes thermal cycle design and availability drivers
- Modular chamber scaling vs. monolithic reactor design

**Most similar concept (in economic structure):** Heavy-ion ICF, if it were being pursued commercially. Both use electrically-driven pulsed compression with per-shot consumables and rep-rate-dominated LCOE. Heavy-ion ICF is not under active commercial development.

**Least similar concept:** High-field tokamaks (CFS, Tokamak Energy). Those concepts maximize magnetic field to minimize reactor size, accepting HTS supply chain constraints. MagLIF eliminates magnets entirely, accepting pulsed-operation complexity instead. The cost structures are orthogonal.

## 6. Modeling Confidence

**Rating: Low**

**Data-anchored parameters (5 of ~15 key parameters):**
- Thermal-to-electric efficiency (42%, published in Z-IFE study with detailed cycle analysis)
- FLiBe blanket thickness (1 m, Z-IFE chamber design)
- Chamber structural material (F82H, with fatigue analysis)
- Driver architecture at sub-scale (IMG demonstrated at 1 TW; scaling laws understood)
- Plant capacity factor (85%, standard assumption but traceable to Z-IFE)

**Speculative parameters (10 of ~15 key parameters):**
- Per-shot yield at 60+ MA (simulation-based, no experimental validation)
- Repetition rate at GJ-scale (undemonstrated at any scale)
- Driver capital cost for IMG at power-plant scale (no published estimate)
- Per-shot consumable cost for cryogenic targets + RTL (no volume production data)
- Chamber lifetime under combined pulsed shock + neutron + corrosion loading (uncharacterized)
- Electrode/power-feed lifetime (no experimental analogue exists)
- Tritium breeding blanket design for MagLIF chamber (no published design)
- RTL insertion cycle time at scale (conceptual only)
- Cryogenic target fabrication throughput and cost (NIF analogue is 15–20 hours/target)
- Thermal buffering cost for pulsed-to-steady conversion (not characterized in Z-IFE study)

**Dominant source of LCOE uncertainty:** Rep rate and per-shot yield are correlated — both depend on achieving reliable GJ-scale operation. If rep rate is limited to 0.1 Hz (as in the Z-IFE baseline), LCOE is ~2× higher than competitive. If rep rate reaches 0.5–1 Hz (as Pacific Fusion implicitly requires for commercial viability), but yields are lower than simulated, LCOE still fails. Both parameters must hit their targets simultaneously, and neither is experimentally validated.

**Design-point vintage mismatch:** The only published power plant study (Z-IFE, 2006) predates the MagLIF concept itself (2010) and used dynamic hohlraum targets with LTD drivers — not the IMG + self-magnetizing target architecture Pacific Fusion is pursuing. This is not a minor version difference; it's a fundamental mismatch between the reference design point and the commercial concept being modeled.

## 7. What Would Change My Mind

### 1. Demonstrated rep-rated chamber operation at subscale (0.1–0.5 Hz, MJ-scale blasts, >1000 shots)
**Direction:** Would increase confidence if successful; confirm economic non-viability if fails.
**Mechanism:** A subscale demonstrator that validates RTL insertion, liquid wall reformation, debris management, and vacuum reconditioning at ≥0.1 Hz over sustained operation (days to weeks) would retire the single largest engineering uncertainty. If such a demonstrator cannot exceed 0.01 Hz, the concept is economically dead regardless of driver cost or yield improvements.

### 2. Published IMG driver cost at power-plant scale (50–100 MA, 0.5–1 Hz, ≥10⁹ shot lifetime)
**Direction:** Could swing LCOE estimate by ±50%.
**Mechanism:** The Z-IFE LTD cost estimate is outdated (2004 dollars) and applies to the wrong driver architecture. Pacific Fusion's IMG architecture claims 90% energy delivery efficiency (vs. 60% for LTD), which changes recirculating power substantially. If IMG brick costs are demonstrated at <$0.50/J with ≥10⁹ shot lifetime, driver capital becomes a smaller fraction of total plant cost than currently assumed. If brick costs remain >$5/J or lifetimes are limited to <10⁷ shots, driver capital could be 5–10× higher.

### 3. Experimental yield measurements at 30–40 MA with modern MagLIF targets (ice-layer, self-magnetizing liner)
**Direction:** Would validate or invalidate the simulated gain curve.
**Mechanism:** The Z-IFE gain curve is for dynamic hohlraum, not MagLIF. Current Z machine experiments (20–27 MA) are too far below the 60+ MA power-plant regime to validate scaling. If Pacific Fusion's demonstration system (>60 MA, commissioning target ~2030) achieves yields within 2× of simulated predictions at 30–40 MA intermediate milestones, confidence in the 60+ MA extrapolation increases significantly. If yields are an order of magnitude below simulations, the physics basis collapses.
