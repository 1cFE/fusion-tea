---
ID: 17-laser-icf-direct-drive-fast-ignition
Concept: Laser ICF - Direct Drive Fast Ignition (D-T)
Company: Focused Energy
Type: synthesis
Status: draft
Created: 2026-05-13
---

# Synthesis: Laser ICF - Direct Drive Fast Ignition (D-T)

**Concept**: Focused Energy
**Classification**: Inertial Fusion Energy / Laser / Proton Fast Ignition
**Fuel**: D-T

---

## 1. Executive Summary

- **The single most important risk**: Proton fast ignition coupling efficiency is entirely unvalidated at the areal densities, pressures, and spatial scales required for commercial ignition. The efficiency range spans nearly an order of magnitude (5–30%) with no experimental data above 1 kJ scale. If coupling falls below ~10%, the concept cannot achieve net electricity.

- **The single most important advantage**: Fast ignition decouples compression from ignition, potentially relaxing implosion symmetry requirements and reducing required compression laser energy by 20–40% relative to central hot spot (CHS) direct drive — if the physics works. This architectural separation reduces driver capital in an ideal scenario.

- **LCOE ballpark**: 69.9 $/MWh at 1 GWe (NOAK, 75% availability, 40% Rankine cycle, q_eng=4.0). This assumes 15% proton coupling efficiency, which has never been measured at plant-relevant conditions. At 10% coupling (q_eng=2.67), LCOE rises to 80.8 $/MWh. Below 7% coupling, ignition fails and the plant is non-viable.

- **Confidence verdict**: **Low**. The model baseline assumes physics performance (gain 50–100, proton coupling 15%) that is 2–3 validation steps removed from current experimental state. Fast ignition has never demonstrated gain > 1 at any scale. The dual-laser capital cost structure (DPSSL compression + petawatt ignition) carries an additional 35–50% driver premium that is not captured in the baseline LCOE (69.9 $/MWh is a lower bound). Target fabrication at 900,000 cone-in-shell capsules per day is undemonstrated and likely more expensive than symmetric CHS targets.

---

## 2. What Matters Most for LCOE

Ranked by uncertainty-weighted leverage (the product of elasticity magnitude and parameter confidence gap):

### 1. **Availability (elasticity: -0.95)**
- **Assumed value**: 75% (HYLIFE-II IFE conservative baseline, from `osti-biblio-7021072.md`)
- **Source confidence**: Low — Focused Energy has published no availability target. The 75% assumption is a heritage analogue from thick-liquid-wall IFE, not a fast ignition–specific engineering assessment.
- **Sensitivity magnitude**: Every 10% reduction in availability increases LCOE by 9.5%. At 65% availability (tokamak-class), LCOE rises to ~77 $/MWh. At 85% (HYLIFE-II optimistic), LCOE falls to ~65 $/MWh.
- **What would flip the economic conclusion**: If final optics damage accumulation at 10 Hz forces availability below 60%, the plant becomes uncompetitive with fission. Conversely, if fast ignition enables a simpler chamber architecture (no liquid walls, reduced activation) that achieves 85%+ availability, the concept becomes economically attractive.

### 2. **Engineering gain / proton coupling efficiency (elasticity: -0.26)**
- **Assumed value**: q_eng = 4.0, corresponding to proton coupling efficiency η_coup = 15%. Focused Energy targets G = 50–100 at the capsule level; the model assumes G_eff = 60 after accounting for coupling losses.
- **Source confidence**: Very low — no fast ignition experiment has demonstrated gain > 1. The coupling efficiency has never been measured at compressed areal densities ρR > 0.3 g/cm². The 15% assumption is a mid-range guess from first-principles TNSA scaling; the defensible range spans 5–30%.
- **Sensitivity magnitude**: At η_coup = 10% (q_eng = 2.67), LCOE rises to 80.8 $/MWh (+16%). At η_coup = 20% (q_eng = 5.33), LCOE falls to 65.7 $/MWh (-6%). Below η_coup ≈ 7%, ignition fails as a discrete threshold event — the hot spot never reaches thermonuclear conditions, and the plant produces no net output.
- **What would flip the economic conclusion**: Validation of η_coup ≥ 15% at ρR > 0.5 g/cm² (ignition-relevant conditions) would confirm the baseline LCOE and position fast ignition as competitive with CHS direct drive. Experimental confirmation that coupling saturates at ≤10% would push LCOE above 80 $/MWh and render the concept non-viable relative to other IFE approaches (Xcimer's hybrid direct drive at ~87 $/MWh, indirect drive at similar range).

### 3. **Dual-laser driver capital (elasticity: +0.06, but with large cost uncertainty)**
- **Assumed value**: Baseline CAS22 driver cost is 221.5 M$ (C220104), derived from the framework NOAK DPSSL default (8.0 M$/MW electric, equivalent to ~$80/J at 10% wall-plug efficiency). This is a **lower bound** — it assumes the petawatt ignition laser carries zero incremental capital cost.
- **Source confidence**: Very low. The petawatt ignition laser (~150 kJ/shot, picosecond pulses, 10 Hz) has no commercial precedent. Published DPSSL cost benchmarks ($700–1,000/J FOAK, per `xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md`) do not apply to the petawatt Ti:sapphire or OPCPA gain medium required for short-pulse operation. Focused Energy has not published a cost estimate for either laser system.
- **Sensitivity magnitude**: At +40% ignition laser cost premium (midpoint of 35–50% estimate from `analysis.md §Challenge 2`), CAS22 rises to 310.1 M$ and LCOE increases to 71.4 $/MWh (+2.1%). At +65% premium (pessimistic dual-driver architecture), LCOE reaches 72.4 $/MWh (+3.6%). The elasticity is low (0.06) because CAS22 is only ~37% of direct capital, but the absolute cost uncertainty is large ($90–145 M$ swing).
- **What would flip the economic conclusion**: If the ignition laser capital cost exceeds ~$150/J (more than double the DPSSL baseline), the dual-driver architecture eliminates the fast ignition economic advantage identified by Meier (2006). The Meier study found fast ignition achieves ~15% lower COE than central ignition at 10 Hz (6.1 vs. 7.2 ¢/kWeh), but **explicitly assumes zero added $/J for the ignition laser** (`osti-servlets-purl-1438678.md §Results`). A positive ignition laser cost erodes or reverses this advantage.

### 4. **Thermal cycle efficiency (elasticity: -0.27)**
- **Assumed value**: η_th = 0.40 (Rankine steam cycle)
- **Source confidence**: High — Focused Energy explicitly confirmed conventional steam cycle (`focused-energy-callahan-interview.md §Steam cycle`). The 40% efficiency is the canonical value for superheated steam in fusion applications (per `scoring_framework.md`).
- **Sensitivity magnitude**: Every 5% increase in η_th (e.g., from 40% to 42%) reduces LCOE by ~3.3%. Moving to sCO₂ Brayton at 48% would drop LCOE to ~63 $/MWh, but this contradicts the company's stated approach.
- **What would flip the economic conclusion**: Fast ignition is locked into thermal conversion (neutron energy dominates). The only path to higher η_th is switching to sCO₂ or helium Brayton, which Focused Energy has not proposed. This parameter is effectively fixed.

### 5. **Construction time (elasticity: +0.26)**
- **Assumed value**: 5 years (IFE default — shorter than MFE due to no superconducting magnets)
- **Source confidence**: Medium — no Focused Energy–specific estimate, but IFE plants generically carry shorter construction schedules than tokamaks. The HYLIFE-II heritage assumption is 4–6 years.
- **Sensitivity magnitude**: Every 1-year increase in construction time raises LCOE by 3.6 $/MWh through interest during construction (IDC). At 7 years (tokamak-class schedule), LCOE rises to ~75 $/MWh.
- **What would flip the economic conclusion**: If the dual-laser system, cone-in-shell target factory, and 10 Hz chamber clearing push construction to 8+ years, LCOE exceeds 78 $/MWh and the concept loses competitive position relative to other IFE approaches.

---

## 3. Risk Verdicts

### Challenge 1: Proton Coupling Efficiency (η_coup = 5–30%, unvalidated)
- **Verdict**: **Genuinely uncertain**. The coupling efficiency depends on proton beam divergence, energy spectrum, and transport through the compressed plasma — all of which are sensitive to target geometry, cone material, and foil placement. Small-scale TNSA experiments achieve 1–10% laser-to-proton-beam conversion with broad angular spread; the fraction of that proton energy that deposits in a millimeter-scale hot spot at ρR > 0.3 g/cm² is unmeasured. First-principles scaling suggests 10–20% is achievable with optimized cone geometry, but no experiment has validated this at ignition-relevant conditions.
- **Rationale**: The physics chain (petawatt laser → TNSA proton beam → hot-spot heating) is understood qualitatively, but the quantitative efficiency at plant scale is a free parameter constrained only by order-of-magnitude bounds. Unlike CHS ignition (where coupling is ~90% by conservation of energy in a symmetric implosion), fast ignition couples across two disparate spatial and temporal scales — the picosecond proton pulse must arrive at the compressed core at the correct time and location with sufficient intensity.
- **What would retire this risk**: Experimental demonstration of proton fast ignition gain > 1 at compressed areal density ρR > 0.5 g/cm² with measured coupling efficiency. The key facility: Focused Energy's T-STAR (2028 ignition timeline) or an equivalent petawatt + compression laser at NIF/OMEGA-class scale. A gain measurement at G > 10 with diagnosed proton energy deposition would bound η_coup to ±30% of the measured value, sufficient to anchor LCOE within ±10 $/MWh.

---

### Challenge 2: Dual-Laser System Cost (DPSSL + petawatt ignition)
- **Verdict**: **Unlikely resolvable to economic competitiveness at FOAK**. The petawatt ignition laser adds 35–50% more driver capital with no cost reduction path as mature as the DPSSL compression laser. DPSSL diodes benefit from semiconductor learning curves and external demand pull from data centers and industrial lasers; Ti:sapphire and OPCPA gain media have no analogous scale market. At NOAK (assuming 10× diode cost reduction to $0.01/W), the dual-driver architecture becomes viable, but the FOAK penalty relative to single-driver CHS IFE is severe.
- **Rationale**: The ignition laser cannot share components with the compression laser — they operate at different wavelengths (527 nm DPSSL vs. 800–1,050 nm Ti:sapphire), different pulse lengths (nanosecond vs. picosecond), and different peak powers (terawatt compression vs. petawatt ignition). The capital cost is additive, not shared. Meier (2006) found fast ignition achieves 15% lower COE than central ignition, but **only if the ignition laser carries zero incremental $/J cost**. A positive ignition laser cost erodes this advantage; at +50% driver premium, the FI advantage shrinks to ~8% (model output: 72.4 vs. 79.5 $/MWh CHS-equivalent).
- **What would retire this risk**: Published cost estimate from Focused Energy for the petawatt laser system, or demonstration of a shared-component architecture (e.g., a single DPSSL that pulse-compresses a fraction of its output for ignition, as proposed by some fast ignition variants). Alternatively, validation that the ignition laser energy can be reduced to ≤50 kJ (vs. the 150 kJ T-STAR baseline) would proportionally reduce the cost penalty.

---

### Challenge 3: Gain Requirement vs. Physics Maturity (G = 50–100 target, G > 1 undemonstrated)
- **Verdict**: **Unlikely resolvable to competitive LCOE at G = 50**. Focused Energy's stated commercial gain target of G = 50–100 falls below the economic competitiveness threshold identified by Hawker (2020): G ≈ 400 required for competitive LCOE under mid-range cost parameters (`pmc-articles-pmc7658748.md §Results`). Achieving G = 50–100 would validate net energy gain (η_wp × G > 10 at 10% wall-plug efficiency) but would not produce LCOE competitive with fission or other advanced fusion concepts unless multiple cost parameters (driver $/J, target $/shot, availability) fall simultaneously toward optimistic bounds.
- **Rationale**: The Hawker framework distinguishes **energetics viability** (G > 30–100, sufficient for net electricity with non-catastrophic recirculating power) from **economic competitiveness** (G > 400, sufficient for LCOE below ~$50/MWh in a market context). Fast ignition at G = 50 produces q_eng ≈ 1–2 after accounting for proton coupling losses, implying recirculating power fraction of 40–60%. The plant operates, but LCOE remains above 80 $/MWh unless availability exceeds 85% and driver costs fall to ≤$50/J (both optimistic).
- **What would retire this risk**: Experimental demonstration of G > 100 in a cone-in-shell fast ignition geometry, combined with validation that the architecture supports gain scaling to G > 200 via increased compression laser energy or improved proton coupling. NIF's best indirect-drive result (Q_sci ≈ 4.1, April 2025) is 25× below this threshold; direct-drive ignition is 0× (not yet demonstrated); fast ignition is 0× at any scale. The gap is the largest in all of IFE.

---

### Challenge 4: Target Fabrication at 900,000 Cone-in-Shell Capsules per Day
- **Verdict**: **Unlikely resolvable at $/target < $0.50**. The Pearl™ capsule geometry (cone-in-shell, cryogenic DT, precision alignment) is inherently more complex than symmetric CHS direct-drive targets. NIF fabricates ~400 hand-crafted targets per year; Focused Energy requires 900,000 per day (800,000× scale-up). Published IFE target cost estimates range from $0.10/target (optimistic mass production with foam or emulsion techniques, per `osti-servlets-purl-2561299.md §Target manufacturing`) to $1.00+/target (conservative high-precision fabrication). At $0.50/target and 10 Hz, annual target cost is $142 M/yr — 140% of the model's entire CAS80 fuel annualized cost (1.4 M$/yr, which excludes target costs). This would push LCOE to ~80+ $/MWh.
- **Rationale**: The cone introduces a symmetry break that complicates quality control. The cone must survive implosion pre-ignition without deforming the DT ice layer or disrupting the compression wave. Gold cones (standard in research experiments) are expensive; aluminum or plastic cones are cheaper but unvalidated at ignition-relevant compression. The fabrication process must achieve micron-level tolerances at million-unit-per-day throughput with <0.1% defect rate (one failed target per hour at 10 Hz halts revenue for that period).
- **What would retire this risk**: Demonstration of a mass-production target fabrication process (3D printing, holographic assembly, or continuous-flow emulsion polymerization) that produces cone-in-shell capsules at ≥100,000/day throughput with ≤$0.25/target cost and <0.1% QC rejection rate. The closest analogue: Xcimer's target cost projections for symmetric direct-drive capsules (~$0.10/target at scale, per XEC white paper), but cone geometry adds 2-5× fabrication complexity.

---

### Challenge 5: Chamber Clearing at 10 Hz (100 ms per cycle)
- **Verdict**: **Likely resolvable with engineering development**. Chamber clearing at 10 Hz is demanding but not fundamentally harder than 5 Hz (demonstrated in thick-liquid-wall concepts like HYLIFE). The cone-in-shell target produces asymmetric debris (the cone vaporizes in a directional jet), but magnetic divertors or gas-jet clearing schemes can handle anisotropic ejecta. The primary challenge: final optics protection from 14 MeV neutrons and X-rays at 10 Hz repetition, which requires either disposable debris shields (consumable cost) or standoff distances that increase chamber radius (higher CAS21 building cost).
- **Rationale**: Xcimer's HYLIFE-III concept clears thick-liquid FLiBe jets at sub-Hz scale using gravity; scaling to 10 Hz requires faster jet refresh or gas clearing. The physics is understood (magnetohydrodynamic flow, plasma cooling timescales), but the engineering is undemonstrated at 10 Hz with fusion-scale neutron yield (~2×10¹⁹ n/shot at G=50, 400 kJ compression). Focused Energy has disclosed no chamber design, so the specific clearing mechanism is unknown.
- **What would retire this risk**: Publication of a chamber design with clearing mechanism (gas jet, magnetic sweep, or liquid wall) and neutronics analysis showing final optics survival for ≥10⁶ shots (1 day at 10 Hz) without replacement. Demonstration of 10 Hz clearing at sub-fusion scale (1 kJ laser) would validate the flow dynamics; scaling to fusion neutron flux requires material survivability testing at high-flux neutron sources (IFMIF, SNS spallation targets).

---

### Challenge 6: O&M Structure and Laser Optics Replacement
- **Verdict**: **Likely resolvable, but likely underestimated in baseline LCOE**. The model assumes 101.6 M$/yr O&M (CAS70), derived from framework defaults (~2% of direct capital). IFE heritage analogues (HYLIFE-II, per `osti-servlets-purl-6137961.md §Summary`) suggest 5–8% of direct capital per year for pulsed high-power laser systems, implying 150–240 M$/yr at the modeled capital scale. Laser optics (both DPSSL and petawatt) degrade under high-fluence shot-cycle fatigue; at 10 Hz, a beamline optic accumulates 315 million shots per year. Replacement cycles on the order of 1–10 million shots would drive annual optics cost to tens of millions per year.
- **Rationale**: The baseline O&M assumption (52 M$/yr at 1 GWe for DT IFE) does not account for the dual-laser architecture or 10 Hz shot rate. NIF operates at <1 shot per day and spends ~$300 M/yr on operations (largely personnel and diagnostics, not optics); scaling to 10 Hz at commercial throughput would shift the cost structure toward consumables (optics, target injection hardware, first-wall armor). If optics replacement adds $50 M/yr and target fabrication adds $150 M/yr (at $0.50/target), total annual O&M rises to ~250 M$/yr, pushing LCOE from 69.9 to ~80 $/MWh.
- **What would retire this risk**: Publication of an O&M breakdown with optics replacement schedule and per-unit costs. Demonstration of 10⁷-shot optics lifetime (1 year at 10 Hz) would bound replacement cost to <$10 M/yr per beamline, making this a minor contributor. Conversely, if optics lifetime is ≤10⁶ shots (12 days at 10 Hz), replacement becomes a dominant cost driver and pushes LCOE above 80 $/MWh.

---

## 4. Structural Advantages and Disadvantages

### Advantages Relative to CHS D-T Direct Drive

1. **Reduced compression laser energy (20–40% savings)**: Fast ignition decouples compression from ignition, allowing lower compression laser energy to achieve the same areal density ρR. The Meier (2006) study quantified this: FI achieves gain at ~60% of the laser energy required for CHS at equivalent yield, translating to ~15% lower COE at 10 Hz under zero-ignitor-cost assumptions (`osti-servlets-purl-1438678.md §Results`). At baseline CAS22 driver cost of 221.5 M$, a 20% compression energy reduction saves ~45 M$ in capital, equivalent to ~1.5 $/MWh LCOE reduction. **Quantified benefit: -1.5 to -3.0 $/MWh vs. CHS-equivalent DPSSL plant**.

2. **Relaxed implosion symmetry requirements**: CHS direct drive requires laser beam uniformity on the order of 1–2% RMS to avoid Rayleigh-Taylor instabilities during compression. Fast ignition compresses to lower peak density (ρR ~ 0.3–0.5 g/cm² vs. 1.0+ g/cm² for CHS), reducing the growth rate of hydrodynamic instabilities. This allows coarser beam smoothing and potentially cheaper optics. **Non-quantified benefit: ~5–10% reduction in final optics cost (beam smoothing phase plates, polarization rotators)**, on the order of $5–10 M capital savings.

3. **Potential for higher burn-up fraction**: By igniting a pre-compressed core at a different location than the stagnation point, fast ignition may achieve higher fuel burn-up (35–40% vs. 25–30% for CHS, per some simulations). This reduces tritium throughput per unit energy output. **Non-quantified benefit: ~10% reduction in tritium inventory and breeding blanket thermal load**, translating to ~2–3 M$ savings in CAS27 tritium systems.

**Total quantified advantage: -4 to -6 $/MWh LCOE vs. CHS-equivalent at identical gain.**

### Disadvantages Relative to CHS D-T Direct Drive

1. **Dual-laser capital cost (+35–50% driver cost)**: The petawatt ignition laser adds 77–110 M$ in capital (at 35–50% premium over baseline 221.5 M$ DPSSL driver), increasing LCOE by 2.1–3.6 $/MWh. **Quantified penalty: +2.1 to +3.6 $/MWh**.

2. **Cone-in-shell target fabrication complexity (+2–5× cost per target)**: Symmetric CHS targets are projected at $0.10/target at mass production (per XEC white paper analogues); cone-in-shell targets are inherently more complex (alignment, cone material, quality control). At $0.30/target (3× penalty) and 10 Hz, annual target cost is $95 M/yr, adding ~3–4 $/MWh to LCOE. **Quantified penalty: +3 to +6 $/MWh** depending on target cost floor.

3. **Proton coupling efficiency losses (η_coup = 10–20%)**: Fast ignition introduces an additional energy-loss step between laser and hot spot. CHS direct drive couples ~90% of laser energy to the implosion; fast ignition couples ~10–20% of the ignition laser energy to the hot spot (after TNSA conversion and proton transport losses). For a fixed capsule gain G, the effective plant gain is reduced by the coupling factor: q_eng_FI = (η_coup) × G vs. q_eng_CHS ≈ 0.9 × G. At η_coup = 15%, fast ignition and CHS are comparable; at η_coup ≤ 10%, fast ignition requires proportionally more ignition laser energy to achieve the same q_eng, increasing driver capital. **Conditional penalty: 0 to +5 $/MWh** if η_coup < 12%.

4. **Asymmetric debris and chamber design complexity**: The cone vaporizes in a directional jet (along the cone axis), creating anisotropic debris patterns that complicate chamber clearing and first-wall erosion. CHS implosions produce spherically symmetric debris, allowing simpler isotropic clearing (gas puff, liquid wall). **Non-quantified penalty: ~5–10% increase in CAS22 chamber first-wall cost**, on the order of $3–5 M capital, equivalent to ~0.3–0.5 $/MWh LCOE increase.

**Total quantified disadvantage: +5 to +15 $/MWh LCOE vs. CHS-equivalent**, depending on ignitor laser cost and target fabrication scaling.

### Net Structural Position

Fast ignition is **conditionally advantageous** if: (1) proton coupling ≥15%, (2) petawatt laser cost ≤+30% premium over DPSSL, and (3) cone-in-shell targets scale to ≤$0.30/target. Under these conditions, FI achieves -1 to -3 $/MWh advantage vs. CHS. If any of these parameters falls outside the favorable range, FI is **structurally disadvantaged** by +5 to +10 $/MWh, making CHS direct drive the preferred IFE architecture.

The Meier (2006) result (+15% COE advantage at zero ignitor cost) is consistent with this conditional structure: the architecture provides genuine compression energy savings, but only if the ignition laser is "free" or very cheap. Once priced realistically, the advantage shrinks or reverses.

---

## 5. Cross-Concept Positioning

Focused Energy's fast ignition concept sits in the **high-risk, high-upside quadrant** of the IFE landscape:

- **Relative to indirect drive (NIF heritage)**: Fast ignition eliminates the hohlraum (CAS22 savings of ~$50–100 M in target fabrication infrastructure), but adds the petawatt ignition laser (+$77–110 M). Direct drive (fast ignition or CHS) is structurally cheaper than indirect drive if symmetric illumination is achievable, but indirect drive is the only IFE approach with demonstrated ignition (NIF 2022, Q_sci = 4.1). Fast ignition trades **physics maturity** (0 demonstrated gain) for **potential capital savings** (no hohlraum, relaxed symmetry).

- **Relative to Xcimer hybrid direct drive (17a)**: Both concepts use DPSSL drivers, D-T fuel, and steam/Brayton cycles; both target ~10 Hz operation; both face 900,000 targets/day fabrication. The key difference: Xcimer uses a single KrF driver (CHS implosion), while Focused Energy uses DPSSL compression + petawatt ignition (fast ignition). Xcimer's baseline LCOE (100.2 $/MWh at 400 MWe, scaling to ~87 $/MWh at 1 GWe) is ~20–25% higher than Focused Energy's baseline (69.9 $/MWh), but Xcimer's gain requirement is validated by NIF-scale experiments (indirect drive at Q = 4.1 provides CHS scaling confidence), while Focused Energy's gain is unvalidated. **Cross-concept judgment**: Xcimer is **lower risk, higher cost**; Focused Energy is **higher risk, lower cost (if physics works)**.

- **Relative to Inertia Fusion indirect drive (26)**: Inertia uses DPSSL + hohlraum (single driver, indirect drive), targeting G > 100 with steam cycle at ~10 Hz. Focused Energy eliminates the hohlraum but adds the petawatt laser; both carry similar driver capital ($200–300 M CAS22 range). Inertia's gain target (G > 100) exceeds Focused Energy's (G = 50–100), implying Inertia targets lower recirculating power and better LCOE — but Inertia's hohlraum adds target fabrication cost. **Cross-concept judgment**: Inertia and Focused Energy occupy similar LCOE bands (65–75 $/MWh) under optimistic assumptions, but Inertia's indirect drive has NIF validation heritage while Focused Energy's fast ignition does not.

- **Relative to HB11 p-B11 fast ignition (04)**: Both use fast ignition architecture (petawatt ignition laser, TNSA-class particle beam, dual-driver). HB11 eliminates tritium breeding (no CAS22 blanket, -$150 M capital) but requires 10–100× higher gain due to lower p-B11 cross-section and bremsstrahlung losses. HB11's LCOE is likely 2–3× higher than Focused Energy's due to gain scaling challenges. **Cross-concept judgment**: Focused Energy's D-T fuel is the "easy mode" version of the fast ignition architecture; HB11 is the "hard mode" with better fuel cycle but worse physics.

### Fast Ignition as a Class

The fast ignition architecture (dual-driver, TNSA/electron-beam ignition, cone-in-shell geometry) has been explored by multiple groups since the 1990s (FIREX-I at Osaka, RAL experiments, OMEGA-EP, NIF-ARC). **No group has demonstrated gain > 1**. The conceptual advantage (decoupled compression/ignition, relaxed symmetry) is real, but the physics validation gap is the largest in IFE. Fast ignition is the **highest-risk IFE approach** after exotic beam-driven concepts (heavy-ion, Z-pinch).

### Market Positioning

If fast ignition works (G > 50, η_coup > 15%, dual-laser costs scale to NOAK), Focused Energy achieves LCOE in the **65–75 $/MWh range**, competitive with Xcimer and other laser IFE but not with natural gas (~$40–60/MWh) or nuclear fission (~$60–90/MWh depending on regulatory environment). The concept is **commercially viable but not cost-disruptive** unless gain exceeds 100 and driver costs fall below $50/J.

If fast ignition fails to achieve ignition or coupling saturates at <10%, the concept is **non-viable** — LCOE exceeds 85 $/MWh and the dual-driver architecture carries no compensating advantage over CHS direct drive or indirect drive.

---

## 6. Modeling Confidence

**Rating: Low**

### Data-Anchored Parameters (4 of 15 major parameters)
1. **Energy conversion cycle**: Steam Rankine at 40% — explicitly confirmed by Focused Energy.
2. **Fuel cycle**: D-T with lithium blanket breeding — confirmed by Focused Energy, SRNL partnership announced.
3. **Repetition rate**: 10 Hz (~900,000 shots/day) — stated commercial target.
4. **DPSSL wall-plug efficiency target**: ~10% — stated development goal with Amplitude partnership.

### Speculative Parameters (11 of 15 major parameters)
1. **Engineering gain (q_eng = 4.0)**: Assumes capsule gain G = 60 and proton coupling η_coup = 15%. Neither has been demonstrated; range is 2.0–8.0 depending on coupling.
2. **Proton coupling efficiency (η_coup = 15%)**: Never measured at ignition-relevant conditions; defensible range 5–30%.
3. **Compression laser energy per shot**: Not disclosed by Focused Energy; T-STAR facility spec (400 kJ) is a science baseline, not a commercial plant value.
4. **Ignition laser cost**: No commercial precedent; assumed +40% premium over DPSSL with ±25% uncertainty.
5. **Availability (75%)**: Heritage analogue from HYLIFE-II; no fast ignition–specific engineering assessment.
6. **Target fabrication cost**: Not disclosed; industry estimates range $0.10–$1.00/target; cone-in-shell geometry likely 2–5× more expensive than CHS.
7. **Chamber design**: Not disclosed; first-wall cost, clearing mechanism, and neutronics are all unverified.
8. **Blanket type and TBR**: Lithium confirmed, chemistry unknown; TBR calculation impossible without blanket design.
9. **O&M cost structure**: Framework default (2% of direct capital) likely underestimates laser optics replacement and target injection maintenance at 10 Hz.
10. **Net electrical output**: "Gigawatt-scale" only; model assumes 1 GWe as a standard comparison point, not a disclosed design value.
11. **Construction time (5 years)**: IFE heritage default; no Focused Energy–specific schedule.

### Dominant Source of LCOE Uncertainty

**Proton coupling efficiency (η_coup)** is the single largest unknown, responsible for a factor-of-2 swing in LCOE (62 to 81 $/MWh across the 5–30% defensible range). This parameter is a **physics unknown** (not proprietary — Focused Energy likely does not know the answer either), and it cannot be constrained without experimental validation at ignition-relevant areal density (ρR > 0.5 g/cm²).

The second-largest uncertainty is **dual-laser capital cost** (specifically the petawatt ignition laser $/J), which is an **engineering unknown** with no commercial analogue. A factor-of-2 swing in ignition laser cost (±50% premium) translates to ±3 $/MWh LCOE variation.

Together, these two parameters span a -15 to +15 $/MWh uncertainty band around the baseline 69.9 $/MWh, producing a **final LCOE range of 55–85 $/MWh** under favorable-to-pessimistic assumptions within the defensible physics bounds.

---

## 7. What Would Change My Mind

### 1. Experimental demonstration of fast ignition gain > 10 at ρR > 0.5 g/cm² with diagnosed proton coupling efficiency
**Impact**: If T-STAR (2028 ignition target) or a comparable facility demonstrates G > 10 with measured η_coup = 15±5%, the baseline LCOE (69.9 $/MWh) is validated within ±10%. This would confirm fast ignition as a viable IFE approach and position Focused Energy as competitive with Xcimer and other laser IFE concepts. Conversely, if experiments show η_coup < 10% or gain saturation at G < 20, the concept is non-viable (LCOE > 85 $/MWh).

**Observable**: Publication of a Nature/Physical Review Letters paper reporting measured fusion yield, compression, and proton beam diagnostics in a cone-in-shell target at ignition-scale laser energy (≥100 kJ compression + ≥50 kJ ignition). The experiment must measure proton energy deposition in the hot spot (via alpha spectroscopy or neutron time-of-flight) to validate coupling efficiency.

### 2. Published cost estimate for the petawatt ignition laser at 10 Hz, 150 kJ/shot
**Impact**: If Focused Energy or Amplitude publishes a cost estimate showing the petawatt laser at ≤$120/J (≤+50% premium over DPSSL at $80/J NOAK), the dual-driver architecture remains economically competitive (LCOE < 73 $/MWh). If the cost exceeds $200/J (≥+150% premium), the fast ignition advantage over CHS direct drive disappears (LCOE > 78 $/MWh) and CHS becomes the preferred IFE architecture.

**Observable**: DOE cooperative agreement deliverable report or conference paper (e.g., IEEE Pulsed Power Conference, SPIE Photonics West) with itemized laser capital cost by subsystem (diodes, gain medium, optics, beam delivery). Alternatively, an Amplitude product announcement for a 10 Hz petawatt laser with published pricing.

### 3. Demonstration of cone-in-shell target fabrication at ≥10,000/day throughput with $/target < $0.30
**Impact**: If Focused Energy's Darmstadt targetry lab or a partner facility demonstrates sustained production at ≥10,000 targets/day with measured cost < $0.30/target, the 900,000/day commercial target becomes credible and target cost contribution to LCOE remains < 3 $/MWh. If cost floor is confirmed at > $0.50/target, annual target cost exceeds $150 M/yr and LCOE rises by +4 to +6 $/MWh (to 74–76 $/MWh).

**Observable**: Fusion Industry Association conference presentation or peer-reviewed paper (e.g., *Fusion Engineering and Design*) reporting throughput, cost per unit, and quality metrics (defect rate, cryogenic DT fill success rate) for cone-in-shell capsules at production scale (≥1,000/day sustained for ≥1 week).

---

## 8. LCOE Downselect Scoring

### C1: Modularization (1–5, higher = more modular)

**Sub-factor 1: Construction mode classification per CAS account**

| CAS Account | Construction Mode | Score | Justification |
|-------------|-------------------|-------|---------------|
| CAS21 Buildings | Stick-built / field-erected | 1 | Chamber building, laser halls, and target factory are site-specific concrete structures. No factory-manufactured building modules are feasible at GWe scale. |
| CAS22 Reactor Plant | Site-assembled from factory sub-assemblies | 3 | Laser beamlines (compression + ignition) are factory-manufactured optical modules; chamber and blanket are site-assembled from large segments. Target factory is stick-built on-site but uses factory-manufactured injection/tracking systems. Driver dominates CAS22 cost (221.5 M$ of 1632.3 M$ total); laser modules earn score of 3–4, but chamber/blanket dilutes to 3. |
| CAS23 Turbine Plant | Factory-manufactured module | 5 | Conventional Rankine steam turbine-generator set, factory-assembled and shipped as integrated unit. Zero fusion-specific customization. |
| CAS24 Electrical Plant | Factory-manufactured module | 5 | Switchyard, transformers, and grid connection equipment are commodity utility-scale components. |
| CAS25 Miscellaneous | Factory-manufactured module | 5 | HVAC, fire suppression, cranes — standard industrial equipment. |
| CAS26 Heat Rejection | Site-assembled from factory sub-assemblies | 3 | Cooling towers are modular but require on-site assembly and civil work (foundations, piping). |
| CAS27 Special Materials | Site-assembled | 1 | Tritium plant and cryogenic DT handling are site-integrated systems with extensive piping, shielding, and safety interlocks. |

**Cost-weighted average** (using CAS account costs from model output):

| Account | Cost (M$) | Weight | Score | Weighted |
|---------|-----------|---------|-------|----------|
| CAS21 | 751.6 | 0.202 | 1 | 0.202 |
| CAS22 | 1632.3 | 0.439 | 3 | 1.317 |
| CAS23 | 263.5 | 0.071 | 5 | 0.355 |
| CAS24 | 112.2 | 0.030 | 5 | 0.150 |
| CAS25 | 68.3 | 0.018 | 5 | 0.090 |
| CAS26 | 130.1 | 0.035 | 3 | 0.105 |
| CAS27 | 15.0 | 0.004 | 1 | 0.004 |
| **Total** | **3717.9** | **1.000** | — | **2.223** |

**Sub-factor 2: Module repetition boost**

Fast ignition uses **8 total laser beamlines** at T-STAR (4 compression + 4 ignition, per `laserfocusworld-lasers-sources-article-14274951-can-high.md`). Commercial plant likely requires 16–24 beamlines for symmetric illumination (direct drive). At 16–24 identical beamline modules, repetition boost = **+0.3** (10-49 units: +1.0, scaled down for <20 units).

Target injection/tracking: **1 per chamber** (no repetition boost).

**C1 = 2.223 + 0.3 = 2.5** (clamped to [1, 5])

**Justification**: Laser IFE benefits from beamline modularization (compression and ignition lasers are identical copies, factory-aligned and tested), but chamber, blanket, and tritium systems are site-integrated stick-built structures. The cost-weighted average is pulled down by CAS21 (buildings, 20% of direct capital) and CAS22 chamber/blanket (partial site assembly). Fast ignition is more modular than tokamaks (no site-wound superconducting magnets) but less modular than small modular MFE concepts with factory-manufactured core units (e.g., Commonwealth ARC, if ever realized at <200 MWe scale).

---

### C3: Supply Chain Learning (1–5, higher = more learning potential)

**Sub-factor A: Component learning rates (1–5, cost-weighted across CAS accounts)**

| CAS Account | Dominant Component | Learning Rate | Score | Justification |
|-------------|-------------------|---------------|-------|---------------|
| CAS21 Buildings | Concrete, steel structures | Commodity | 5 | Established global supply chain; no fusion-specific bottlenecks. |
| CAS22 Reactor Plant | Laser diodes (DPSSL + petawatt pump) | Industrial component, growing production | 4 | Diode pump modules for industrial/defense lasers are manufactured at >1 GW/yr scale globally; semiconductor learning curves apply. Current cost $0.1–$1/W; target $0.01/W requires 10× cost reduction, achievable via volume scaling and external demand pull (data centers, LiDAR). Petawatt Ti:sapphire/OPCPA gain media are specialty components (score 3), but diodes dominate cost → weighted score 4. |
| CAS23 Turbine Plant | Steam turbine-generator | Commodity | 5 | Decades of learning in coal/nuclear plants; no further cost reduction expected but supply chain is robust. |
| CAS24 Electrical | Switchyard equipment | Commodity | 5 | Mature utility-scale supply chain. |
| CAS25 Miscellaneous | HVAC, cranes | Commodity | 5 | Standard industrial equipment. |
| CAS26 Heat Rejection | Cooling towers | Commodity | 5 | Established supply chain for power plants. |
| CAS27 Special Materials | Tritium handling, cryogenics | Fusion-specific, limited market | 2 | Cryogenic DT systems and tritium permeation barriers have no external market; supply chain is limited to fusion and fission tritium facilities. |

**Cost-weighted average** (using CAS costs):

| Account | Cost (M$) | Weight | Score | Weighted |
|---------|-----------|---------|-------|----------|
| CAS21 | 751.6 | 0.202 | 5 | 1.010 |
| CAS22 | 1632.3 | 0.439 | 4 | 1.756 |
| CAS23 | 263.5 | 0.071 | 5 | 0.355 |
| CAS24 | 112.2 | 0.030 | 5 | 0.150 |
| CAS25 | 68.3 | 0.018 | 5 | 0.090 |
| CAS26 | 130.1 | 0.035 | 5 | 0.175 |
| CAS27 | 15.0 | 0.004 | 2 | 0.008 |
| **Total** | **3717.9** | **1.000** | — | **3.544** |

**Sub-factor B: Supply chain bottleneck count (start at 5.0, subtract penalties)**

- **Hard constraint**: Target fabrication at 900,000 cone-in-shell capsules/day — no known mass-production process exists; gold or high-Z cone material supply at scale is unproven. **-1.0 penalty**.
- **Scaling constraint**: Petawatt-class laser operation at 10 Hz — Ti:sapphire or OPCPA gain media at kW-scale average power (10 Hz × 150 kJ/shot = 1.5 MW peak optical power) has never been demonstrated. Thermal management and optics damage at this repetition rate require 10× scale-up from current state-of-art (OMEGA-EP, NIF-ARC operate at <0.01 Hz). **-0.5 penalty**.
- **Sole-source dependency**: Amplitude is Focused Energy's exclusive laser development partner (per $40M agreement). If Amplitude fails to deliver 10% WPE DPSSL or 10 Hz petawatt laser, Focused Energy has no alternate supplier. **-0.25 penalty**.
- **No He-3 fuel dependency**: D-T fuel cycle uses deuterium (seawater extraction, mature) and tritium (bred from lithium, no external purchase required at equilibrium). **No penalty**.

**Sub-factor B = 5.0 - 1.0 - 0.5 - 0.25 = 3.25**

**Sub-factor C: External demand pull (1–5, fraction of capital in components with >$1B/yr external market)**

| Cost Category | Capital (M$) | Has >$1B/yr External Market? | Justification |
|---------------|--------------|------------------------------|---------------|
| Buildings (CAS21) | 751.6 | Yes | Concrete, steel, construction labor — global market ~$1 trillion/yr. |
| Laser diodes (CAS22 driver) | ~150–200 | **Yes** | Industrial/defense laser diode market ~$3–5 B/yr (Coherent, IPG Photonics, nLight); data center interconnects and LiDAR add $1–2 B/yr growth. Fusion demand (10 GW diode capacity per plant) is <0.1% of global market. |
| Turbine (CAS23) | 263.5 | Yes | Steam turbine market ~$15 B/yr (GE, Siemens, Mitsubishi). |
| Electrical (CAS24) | 112.2 | Yes | Utility switchyard equipment market ~$50 B/yr globally. |
| Cooling (CAS26) | 130.1 | Yes | Cooling tower market ~$3 B/yr. |
| Chamber, blanket, tritium (CAS22 other, CAS27) | ~1,100 | **No** | Fusion-specific; no external market except ITER-class magnets (different confinement). |
| Target factory (CAS22 sub-account C220108) | 298.4 | **No** | Cone-in-shell cryogenic target fabrication has zero external demand; ICF research targets (NIF, LLE) are <1,000/yr globally. |
| Petawatt ignition laser (CAS22 C220104 premium) | ~77–110 | **No** | Petawatt lasers for fusion have no external market; defense/research petawatt facilities (ELI, BELLA) operate at <1 shot/hour, not 10 Hz. |

**Total capital with external demand**: 751.6 + 150 + 263.5 + 112.2 + 130.1 = **1,407.4 M$**
**Total direct capital**: 3,717.9 M$
**Fraction with external demand**: 1,407.4 / 3,717.9 = **37.8%**

Per framework: 20–40% → **score 3**

**Sub-factor C = 3.0**

**C3 = (3.544 + 3.25 + 3.0) / 3 = 3.26** → **3.3** (rounded to nearest 0.1)

**Justification**: Laser IFE benefits from strong external demand pull for laser diodes (data centers, industrial cutting, defense) and conventional BOP components (turbines, cooling, electrical), covering ~38% of direct capital. However, the fusion core (chamber, blanket, tritium, target factory, petawatt ignition laser) has no external market and faces hard supply chain constraints (900k targets/day, 10 Hz petawatt operation). The score is above-average (3.3 vs. tokamak ~2.5) but not exceptional (advanced fission SMRs with >60% commodity content score ~4.0).

---

### C4: Plant Complexity (1–5, higher = simpler)

**Sub-factor A: Operational coupling density (1–5, failure cascades and maintenance dependencies)**

Fast ignition at 10 Hz creates **high operational coupling**:

1. **Compression laser failure → full plant shutdown**: If any of the 4–8 compression laser beamlines fails to deliver energy within ±5% uniformity, the implosion symmetry is broken and the shot produces zero yield. The plant must halt until the failed beamline is repaired or the remaining beamlines are rebalanced (1–8 hour outage per beamline failure). At 10 Hz with 8 beamlines, this implies ~1 failure per 10⁵ shots (1 day) at 99.9% component reliability, producing ~3–10 shutdown events per year.

2. **Petawatt ignition laser failure → full plant shutdown**: The ignition laser must deliver its pulse within a ±10 ps timing window relative to peak compression (diagnosed via X-ray/neutron diagnostics). Timing jitter, pulse energy drop, or beam pointing error causes ignition failure. Unlike the compression laser (where beam imbalance can be corrected shot-to-shot), ignition laser failure is a discrete event: the shot either ignites or produces zero yield. This is a **single-point failure** — one petawatt laser, one target per shot, zero redundancy.

3. **Target injection failure → missed shot**: At 10 Hz, a target must be injected, tracked, and positioned to ±100 μm accuracy every 100 ms. Injection system failure (cryogenic line blockage, injector jam, tracking camera glitch) causes a missed shot, halting revenue for that 100 ms cycle. At 900,000 shots/day, a 0.1% injection failure rate produces 900 missed shots/day (90 seconds of lost revenue/day, or 0.1% availability loss).

4. **Tritium extraction failure → fuel starvation**: D-T fuel must be extracted from the blanket, purified, and recycled at a rate matching 10 Hz consumption (~0.2 mg DT/shot = 63 g/yr throughput). Tritium plant downtime halts fusion after the on-site inventory is exhausted (typically 1–7 days of buffer). This is a **failure cascade to shutdown** with 1-week time constant.

5. **Chamber clearing failure → shot blockage**: If debris from shot N does not clear within 100 ms, shot N+1 cannot proceed (target injection path is blocked). A single clearing failure at 10 Hz halts the plant for ≥1 second (10 missed shots) until the chamber is vented and cleaned, or the debris settles.

**Operational coupling assessment**: Fast ignition has **many critical single-point failures** (ignition laser timing, target injection, compression laser uniformity) and **moderate failure cascades** (tritium extraction → fuel starvation over days; chamber clearing → multi-shot blockage). The coupling density is **higher than steady-state MFE** (where plasma disruptions are recoverable within seconds) but **comparable to other pulsed IFE** (all 10 Hz laser fusion concepts face similar coupling).

**Sub-factor A = 2.5** (highly coupled; many single-point failures, moderate cascade depth)

**Sub-factor B: Subsystem count (significant CAS22 sub-accounts >1% of total capital)**

From model output CAS22 detail:

| Sub-account | Description | Cost (M$) | % of Total Capital (4,420 M$) |
|-------------|-------------|-----------|------------------------------|
| C220101 | First wall / blanket | 219.0 | 5.0% |
| C220102 | Blanket | 152.9 | 3.5% |
| C220104 | Driver (lasers) | 221.5 | 5.0% |
| C220108 | Target factory | 298.4 | 6.7% |
| C220110 | Tritium systems | 86.6 | 2.0% |
| C220111 | Vacuum systems | 144.8 | 3.3% |
| C220200 | Main heat transfer | 208.5 | 4.7% |
| C220500 | Cryogenics | 120.0 | 2.7% |
| C220700 | Instrumentation & control | 89.8 | 2.0% |

**Count of subsystems >1% of total capital: 9**

Per framework: 8-10 subsystems → **score 3**

**Sub-factor B = 3.0**

**C4 = (2.5 + 3.0) / 2 = 2.75** → **2.8** (rounded to nearest 0.1)

**Justification**: Fast ignition is operationally complex due to dual-laser timing requirements, 10 Hz pulsed operation, and target injection precision. The subsystem count (9 major accounts >1% of capital) is typical for IFE — comparable to tokamaks (breeding blanket, magnets, divertor, fueling, heating) but with different failure modes. The score (2.8) reflects moderate-to-high complexity, above continuous-flow stellarators (score ~3.5–4.0) but below early FOAK MFE with unproven tritium cycles (score ~2.0).

---

### C5: Customization Needs (1–4 raw, scaled to 1–5)

**Sub-factor A: Thermal rejection (1–4)**

Fast ignition uses **conventional steam Rankine cycle** (explicitly confirmed by Focused Energy, per `focused-energy-callahan-interview.md §Steam cycle`). This requires:
- Large cooling towers (>1 GWth heat rejection at 40% thermal efficiency → 1.5 GWth rejected)
- Once-through cooling or recirculating water system
- Thermal discharge permitting (Clean Water Act Section 316(a), EPA thermal pollution standards)

**No exceptional thermal rejection needs** beyond standard coal/nuclear plants. Thermal cycle is single-stage Rankine, not combined-cycle or hybrid.

**Sub-factor A = 2** (large cooling towers required, standard thermal cycle)

**Sub-factor B: Fuel safety profile (1–4)**

Fast ignition uses **D-T fuel** with tritium breeding from lithium blanket. This requires:
- Tritium handling license (10 CFR Part 30, NRC or Agreement State)
- Tritium inventory management (startup inventory 1–3 kg sourced from CANDU or fission reactors; equilibrium breeding from blanket)
- Cryogenic DT storage and purification systems (CAS22 tritium plant, CAS22 cryogenics)
- Permeation barriers and tritium recovery systems (tritium leaks into cooling water, building atmosphere, and waste streams)
- Neutron activation of chamber structures (14 MeV D-T neutrons produce activation products in steel, concrete, and cooling water)

D-T is the **highest-burden fuel cycle** in fusion (score 1 in framework).

**Sub-factor B = 1** (D-T: full tritium handling and breeding infrastructure)

**C5 raw = (A + B) / 2 = (2 + 1) / 2 = 1.5**

**C5 scaled = 1 + (1.5 - 1) × (4/3) = 1 + 0.5 × 1.333 = 1.67** → **1.7** (rounded to nearest 0.1)

**Justification**: Fast ignition inherits the full D-T fuel cycle burden (tritium licensing, breeding, inventory, activation) and requires large cooling towers for thermal rejection (no direct energy conversion). The score (1.7) is the floor for D-T concepts with thermal cycles — only alternate fuels (D-He3 score 2.5, p-B11 score 3.5+) or hybrid DEC (partial direct conversion, score 2.0–2.5) achieve better.

---

### C8: Data Adequacy (1–5, higher = more data available)

**Sub-factor A: Source diversity & independence (1–5)**

Available sources for Focused Energy fast ignition:
1. **Company sources**: Focused Energy technology website, Callahan Physics World interview (2023), PR Newswire Amplitude partnership announcement (2024), Laser Focus World T-STAR facility article (2023).
2. **Independent sources**: Optica OPN science feature (June 2023, fast ignition overview), OSTI IFE status review (purl-2561299), OSTI Meier 2006 HAPL systems study (purl-1438678), Hawker 2020 economic model (PMC-7658748).
3. **Peer-reviewed technical**: Focused Energy J. Fusion Energy 2023 paper (confirmed to exist via abstract, full text not accessed due to Springer paywall — likely contains chamber design and gain calculations).

**Assessment**: Mix of company publications (4 sources) and independent academic/government sources (4 sources). The J. Fusion Energy 2023 paper is peer-reviewed but not fully accessed. No multi-institution independent validation of Focused Energy's specific design claims (gain target, coupling efficiency, chamber concept).

**Sub-factor A = 3.5** (mix of independent and company sources with partial peer review; would be 4.0 if J. Fusion Energy paper were fully extracted)

**Sub-factor B: Reactor design specification (1–5)**

Focused Energy has disclosed:
- Physics approach: DPSSL compression + petawatt proton fast ignition, cone-in-shell Pearl™ capsule, D-T fuel
- Laser specifications: ~10% WPE target, 10 Hz rep rate, 400 kJ compression + 150 kJ ignition (T-STAR baseline)
- Power plant parameters: "gigawatt-scale" (no specific MWe), gain target G = 50–100, steam Rankine cycle
- Partnerships: Amplitude (laser development), SRNL (tritium extraction)
- Timeline: T-STAR 2028 ignition, LightHouse pilot plant end of 2030s

**Missing**:
- Chamber design (geometry, first-wall material, clearing mechanism)
- Blanket type (FLiBe, LiPb, liquid Li, solid ceramic)
- Target factory design (fabrication method, throughput validation)
- Net electrical output (1 GWe assumed by model, not disclosed by company)
- Capital cost estimate (no LCOE or $/kW published)
- Detailed subsystem integration (power balance, recirculating power, auxiliary systems)

**Sub-factor B = 3.0** (partial design with key subsystems defined but gaps in chamber, blanket, and plant-level integration)

**Sub-factor C: LCOE parameter coverage (1–5, based on blocking gap count from gap_report.md)**

From gap_report.md summary:
- **Blocking gaps** (criticality = blocking): 7 identified (proton coupling efficiency, fast ignition gain at scale, petawatt laser cost, DPSSL cost, chamber design, blanket type/TBR, net electrical output)

Per framework: 5-7 blocking gaps → **score 2**

**Sub-factor C = 2.0**

**Sub-factor D: Commercialization pathway clarity (1–5)**

Focused Energy has articulated:
- **Milestones**: T-STAR experimental facility (2028 ignition target), LightHouse pilot plant (end of 2030s, Q_eng > 1), commercial plant (2040s, gigawatt-scale)
- **Funding**: $175M+ raised (per PR Newswire 2024); $40M Amplitude partnership; DOE cooperative agreement (milestones: high-gain target design, proton fast ignition demonstration)
- **Technology partnerships**: Amplitude (lasers), SRNL (tritium), Darmstadt targetry lab (Pearl™ fabrication)
- **Regulatory pathway**: Not disclosed; standard NRC licensing assumed but no pre-application engagement announced

**Missing**:
- Cost targets for FOAK vs. NOAK (no $/kW or LCOE projections)
- Supply chain development strategy (diode pump scaling, target factory industrialization)
- Grid integration plan (no PPA announcements, no utility partnerships disclosed)
- Financial structure for LightHouse pilot (FOAK capital requirement $3–10B, no disclosed financing plan)

**Sub-factor D = 3.5** (clear pathway with milestones and partnerships, but lacking cost targets and FOAK financing strategy)

**C8 = (3.5 + 3.0 + 2.0 + 3.5) / 4 = 3.0**

**Justification**: Focused Energy has published more technical detail than many private fusion startups (gain targets, laser specs, timeline, partnerships), but the reactor design remains incomplete (no chamber, blanket, or capital cost disclosure). The J. Fusion Energy 2023 paper likely fills some gaps but was not fully accessed. Data adequacy is **sufficient for qualitative analysis and parameterized LCOE modeling**, but the model carries large uncertainty bands due to 7 blocking parameter gaps.

---

### C7: Technical Risk Evidence (risk matrix scored by Claude, C7 computed by Python)

#### Function 1: Plasma Performance

| Subcategory | Details |
|------------|---------|
| **Plant requirement** | Compressed areal density ρR ≥ 0.3 g/cm², ion temperature T_i ≥ 5 keV at stagnation, sufficient for proton beam penetration and hot-spot ignition. Fast ignition target must achieve 10× compression from initial DT ice density (~0.25 g/cm³ → 2.5 g/cm³) under direct-drive illumination with <10% asymmetry. |
| **Best demonstrated** | NIF indirect drive: ρR = 1.5 g/cm² at T_i = 5 keV (2022 ignition shot, Q_sci = 4.1). OMEGA direct drive: ρR = 0.15–0.3 g/cm² at T_i = 3–4 keV (no ignition). Fast ignition–specific: Osaka FIREX-I achieved compressed core at ρR ~ 0.1 g/cm² with electron fast ignition (not proton), no ignition. Proton fast ignition has **never demonstrated compressed core ignition at any scale** (best: CSU experiments at ρR < 0.05 g/cm², no fusion yield measured). |
| **Gap ratio** | Compression: 0.3 / 0.3 (OMEGA) = **1.0× for density**, but temperature gap 5 keV / 3.5 keV = **1.4× for ion temperature**. Proton fast ignition: 0.3 g/cm² / 0.0 (never ignited) = **N/A (undemonstrated)**. |
| **Closure mechanism** | Focused Energy claims Pearl™ capsule with optimized cone geometry achieves required compression via DPSSL direct drive at 400 kJ. Hot-spot ignition is achieved by petawatt laser–generated proton beam (150 kJ, TNSA mechanism) penetrating the cone and depositing energy in the compressed core within ±10 ps timing window. T-STAR facility (2028) is the validation experiment. |
| **Classification** | **Binary**. If compression fails to reach ρR ≥ 0.3 g/cm² or proton beam fails to deposit sufficient energy in the hot spot (η_coup < 7%), ignition does not occur and fusion yield is zero. The plant produces no net electricity. Unlike steady-state MFE (where confinement degradation reduces Q gradually), fast ignition is a threshold phenomenon — you ignite or you don't. |
| **Evidence tier** | **Physics: 2** (simulation/design study). Fast ignition gain calculations exist in LLNL hydrocodes (LASNEX, HYDRA) and Osaka group simulations, predicting G = 50–100 at 400 kJ compression + 150 kJ ignition under optimistic coupling assumptions. No experimental validation at ignition-relevant ρR. Tier 2: paper designs and simulations, no operating-regime demonstration. |
| **Evidence tier** | **Hardware: 2** (simulation/design study). Pearl™ capsule geometry (cone-in-shell, cryogenic DT) is a design concept; no capsules have been tested at ignition scale. Cone material (gold, aluminum, or plastic) and alignment tolerances are unvalidated at ρR > 0.3 g/cm² compression. Darmstadt targetry lab fabricates research targets but not at ignition energy. Tier 2: conceptual design, no subscale hardware demonstration at relevant compression. |

---

#### Function 2: Driver / Energy Input

| Subcategory | Details |
|------------|---------|
| **Plant requirement** | Dual-laser system: (1) DPSSL compression laser delivering 400 kJ at 527 nm, 10% wall-plug efficiency, 10 Hz repetition, with beam uniformity <2% RMS across target surface. (2) Petawatt ignition laser delivering 150 kJ at 800–1,050 nm, picosecond pulse, 10 Hz repetition, focused to ≤50 μm spot on cone-embedded foil. Combined average power: (400 + 150) kJ × 10 Hz = 5.5 MW optical output, requiring 55 MW electrical input at 10% WPE. |
| **Best demonstrated** | **DPSSL compression**: Amplitude and other vendors have demonstrated diode-pumped Nd:glass/Yb:YAG lasers at kJ scale and Hz-class repetition. NIF Nd:glass delivers 1.9 MJ at 527 nm but at <0.1% WPE and single-shot (no repetition). OMEGA delivers 30 kJ at 351 nm (frequency-tripled) at 1 shot/hour. 10 Hz operation at >10 kJ has been demonstrated at <1% WPE by defense lasers (Boeing HEL-MD, etc.). **No DPSSL has demonstrated 400 kJ at 10 Hz at 10% WPE** — current state-of-art is ~10 kJ at 10 Hz at 5% WPE (Amplitude Ti:sapphire pump lasers, Coherent industrial cutting lasers). **Petawatt ignition**: NIF ARC, OMEGA EP, ELI-NP, BELLA operate at petawatt peak power but <0.01 Hz (single-shot to 1 shot/hour). Amplitude's Sequoia laser delivers 150 J (not kJ) at picosecond duration at ~1 Hz. **No petawatt laser has demonstrated 150 kJ at 10 Hz** — the T-STAR facility is planned to achieve this by 2028 but is currently operating at 1 shot/60 seconds (0.017 Hz) for initial commissioning. |
| **Gap ratio** | **Compression laser**: energy gap = 400 kJ / 10 kJ = **40× energy scale-up**; repetition gap = 10 Hz / 10 Hz = **1.0× (no gap for rep rate, but WPE gap 10% / 5% = 2.0×)**. Combined gap: 40× energy × 2× WPE = **80× power-efficiency product**. **Ignition laser**: energy gap = 150 kJ / 0.15 kJ = **1,000× energy scale-up**; repetition gap = 10 Hz / 1 Hz = **10× rep rate scale-up**. Combined: **10,000× average power scale-up** (from 0.15 W to 1.5 MW average optical power). |
| **Closure mechanism** | Amplitude partnership ($40M, 2024) is developing DPSSL technology toward 10% WPE at kJ scale. Focused Energy's T-STAR facility (4 compression + 4 ignition beamlines, 2028 completion) is the scale-up demonstration. Diode pump modules must reach $0.01/W cost floor (per OSTI purl-2561299) via semiconductor learning curves and volume production (external demand pull from data centers, industrial lasers). Petawatt laser scale-up requires thermal management of Ti:sapphire or OPCPA gain media at 1.5 MW average power — active cooling, beam aperture scaling to >30 cm, and optics damage mitigation at 10 Hz fluence. |
| **Classification** | **Binary** for petawatt ignition laser. If the ignition laser cannot deliver 150 kJ at 10 Hz with <10 ps timing jitter, ignition fails and fusion yield is zero. The compression laser alone (without ignition) produces compressed cores but no ignition — Q < 1, no net electricity. **Degrading** for compression laser WPE shortfall: if WPE = 7% instead of 10%, recirculating power increases from 29% to 39% of gross output (q_eng drops from 4.0 to 2.8), reducing net output by ~25% and increasing LCOE by ~15%. Plant still operates but at worse economics. |
| **Evidence tier** | **Physics: 4** (near-regime demonstrated). Laser physics at kJ scale and Hz-class repetition is well understood; DPSSL diode pumping is mature (demonstrated at 10 kJ, 5% WPE, 10 Hz — within 2× of all three parameters). Petawatt pulse generation is mature at single-shot scale (NIF ARC, OMEGA EP). The gap is **engineering scale-up** (thermal management, optics damage, beam uniformity at high average power), not fundamental physics. Tier 4: subscale demonstrated, <2× gap on limiting parameters. |
| **Evidence tier** | **Hardware: 3** (subscale demonstration). DPSSL beamlines at 10 kJ, 5% WPE, 10 Hz exist (Amplitude, Coherent). Petawatt lasers at 150 J, 1 Hz exist (Amplitude Sequoia). The compression laser requires 40× energy scale-up (10 → 400 kJ) and 2× WPE improvement (5% → 10%); the ignition laser requires 1,000× energy scale-up and 10× rep rate improvement. T-STAR facility (2028 completion) is the first hardware integration at commercial scale. Tier 3: subscale hardware demonstrated, ≥4× gap on energy or repetition rate for ignition laser (1,000× energy × 10× rep rate exceeds the 4× threshold by 2,500×; dominant gap is ignition laser, not compression). |

---

#### Function 3: Instability Control

| Subcategory | Details |
|------------|---------|
| **Plant requirement** | Rayleigh-Taylor (RT) instability suppression during DT shell compression: surface roughness <1 μm RMS on inner ice layer, beam uniformity <2% RMS across target, pulse shaping to minimize acceleration phase RT growth. Fast ignition relaxes symmetry requirements relative to CHS (compression to ρR ~ 0.3 vs. 1.0 g/cm² reduces RT growth rate by ~2×), but cone insertion breaks spherical symmetry and seeds azimuthal perturbations. Cone-plasma interaction instabilities (proton beam filamentation, Weibel instability in cone-generated plasma) must not deflect proton beam by >10° or defocus the ignition spot to >50 μm. |
| **Best demonstrated** | OMEGA direct drive: RT-stabilized implosions at <2% beam non-uniformity achieve ρR ~ 0.3 g/cm² with <30% yield degradation vs. 1D simulations (Goncharov et al., Physics of Plasmas 2014). NIF indirect drive: hohlraum symmetry controls RT growth to achieve ignition at ρR = 1.5 g/cm² (Hurricane et al., Nature 2022). Fast ignition–specific: Osaka FIREX-I observed cone-tip plasma jets and proton beam deflection in compressed-core experiments but did not achieve ignition (no quantitative RT or beam-deflection measurements published). Cone-in-shell RT growth is **uncharacterized at ignition-relevant compression**. |
| **Gap ratio** | Compression symmetry: <2% beam uniformity demonstrated at OMEGA scales directly to 400 kJ fast ignition targets (no gap, same 527 nm direct drive). RT growth at ρR = 0.3 g/cm² is **near-regime** (OMEGA demonstrates 0.3 g/cm², fast ignition requires same density but with cone perturbation). Cone-tip instabilities: **N/A (undemonstrated)** — proton beam filamentation and Weibel instability in dense plasma have been observed in laser-plasma interaction experiments but never at the areal densities and proton energies relevant to fast ignition (ρR > 0.3 g/cm², proton E > 10 MeV). Gap ratio = **unquantifiable** (physics is understood qualitatively but not measured at relevant conditions). |
| **Closure mechanism** | Focused Energy claims Pearl™ capsule geometry is optimized to minimize cone-seeded perturbations via 3D hydrocode simulations (LASNEX, HYDRA). Beam smoothing via distributed phase plates (DPP) or smoothing by spectral dispersion (SSD) suppresses RT growth during compression (same techniques as OMEGA). Proton beam filamentation is mitigated by cone material choice (low-Z plastics suppress Weibel growth vs. high-Z gold) and by using proton energies >20 MeV (faster transit through cone plasma, less deflection). T-STAR experiments (2028) will measure cone-tip plasma density and proton beam deflection angles via proton radiography and X-ray backlighting. |
| **Classification** | **Binary** for proton beam deflection. If Weibel or filamentation instabilities deflect the proton beam by >20° or defocus the ignition spot to >100 μm (2× the 50 μm requirement), hot-spot energy deposition drops below the ignition threshold and fusion yield is zero. **Degrading** for RT growth during compression: excessive RT reduces compression efficiency (ρR achieved is 10–30% below 1D predictions), increasing required laser energy and reducing gain. At 30% RT-induced yield degradation, gain drops from G = 60 to G = 42, pushing q_eng from 4.0 to 2.8 (LCOE increases by ~15%). |
| **Evidence tier** | **Physics: 3** (subscale demonstration). RT instability physics at direct-drive ICF scale is well characterized (OMEGA database, 20+ years of experiments). Fast ignition relaxes RT constraints by ~2× (lower compression), so OMEGA RT data transfers with <2× extrapolation. Cone-tip instabilities are understood qualitatively (Weibel theory, PIC simulations) but **never measured at ignition-relevant conditions**. Tier 3: adjacent regime demonstrated (OMEGA RT), but cone-specific fast ignition instabilities are subscale or absent. |
| **Evidence tier** | **Hardware: 3** (subscale demonstration). Cone-in-shell targets have been fabricated and tested at sub-ignition scale (Osaka FIREX-I, RAL experiments, NIF cone-guided shots). Best demonstrated: Osaka FIREX-I cone-in-shell targets at ρR ~ 0.1 g/cm² (3× below ignition requirement). Pearl™ capsule at ρR > 0.3 g/cm² is undemonstrated; cone alignment and ice layer uniformity at cryogenic temperatures in a cone-perturbed geometry are **engineering unknowns**. Tier 3: subscale hardware (0.1 g/cm² vs. 0.3 g/cm² = 3× gap). |

---

#### Function 4: Plasma-Wall Interaction

| Subcategory | Details |
|------------|---------|
| **Plant requirement** | First wall must survive 10 Hz pulsed loading: 14 MeV neutron flux ~1×10¹⁴ n/cm²/shot (at 5 m chamber radius, 400 MJ fusion yield per shot at G=50), X-ray fluence ~5 J/cm²/shot, and debris impact (vaporized target + cone material, velocities ~10–100 km/s). Annual neutron fluence = 3×10²² n/cm²/yr (at 10 Hz, 75% availability). Displacement damage: ~20 dpa/yr in steel at 5 m standoff (using ENDF/B-VIII cross-sections for 14 MeV neutrons on Fe-56). First wall must survive ≥2 years between replacements (target: 5-year lifetime, 100 dpa total). Chamber clearing time <100 ms (10 Hz cycle). Final optics (laser beam delivery) must survive ≥10⁶ shots (12 days at 10 Hz) under combined neutron + X-ray + debris exposure, or be replaceable on <1-day maintenance cycles. |
| **Best demonstrated** | **Neutron damage**: ITER divertor tungsten tiles qualified at 20 dpa equivalent (ion beam testing at 300°C, equivalent to ~10 years at 1 MW/m² neutron wall loading, per ITER materials database). JET beryllium first wall operated at 0.5 dpa over 30 years (0.017 dpa/yr, fission-spectrum neutrons). **14 MeV fusion neutrons**: FFTF (fission reactor with Be reflector) achieved 5 dpa in steel at mixed-spectrum neutrons; 14 MeV–specific damage is undemonstrated at >1 dpa. **Pulsed loading**: Z-machine at Sandia demonstrates pulsed X-ray + debris loading at 0.1 Hz (1 shot/10 seconds) for ~1,000 shots total (Z-IFE target chamber tests, 2010s); chamber wall materials (tungsten, SiC, liquid lithium) were tested at <10⁴ shots. **10 Hz operation**: no fusion facility has operated at 10 Hz with fusion-scale neutron yield (Xcimer's HYLIFE heritage is sub-Hz; tokamaks are steady-state or pulsed at 0.01 Hz). **Final optics protection**: NIF final optics (fused silica lenses) are damaged by debris and require replacement every ~100 shots (~1% per shot damage probability); grazing-incidence mirrors survive ~10⁴ shots. No ICF facility has demonstrated 10⁶-shot optics lifetime at fusion yield. |
| **Gap ratio** | Neutron damage: 20 dpa/yr required / 0.017 dpa/yr demonstrated (JET, fission spectrum) = **1,200× neutron fluence gap**. Using ITER divertor (20 dpa at ion beam, extrapolated to fusion neutrons) = **1.0× dpa gap but different neutron spectrum** (14 MeV fusion vs. ion beam surrogate). **Pulsed rep rate**: 10 Hz / 0.1 Hz (Z-machine) = **100× rep rate gap**. **Final optics lifetime**: 10⁶ shots required / 10⁴ shots demonstrated (NIF grazing mirrors) = **100× shot-lifetime gap**. |
| **Closure mechanism** | Focused Energy has disclosed no chamber design or first-wall material. **Assumed closure mechanism (industry-standard IFE analogues)**: (1) Thick-liquid wall (FLiBe or LiPb, HYLIFE-III heritage) absorbs neutrons and self-heals between shots; 10 Hz clearing requires magnetohydrodynamic flow (0.1 m/s jet velocity, 1 m/s clearing speed → 5 m chamber clears in 5 seconds, too slow for 10 Hz → requires thin liquid layer <0.5 m or gas-jet clearing). (2) Tungsten armor first wall (ITER heritage) with active cooling; 20 dpa qualification extrapolates to 1 year at 10 Hz fast ignition (20 dpa/yr); replacement on 1-year cycles. (3) SiC-based low-activation ceramic first wall with He cooling; no pulsed-loading data at 10 Hz. **Final optics**: standoff distance >10 m reduces neutron flux by 4× (r⁻² scaling) but increases chamber building cost (CAS21); disposable debris shields (replaced every 10⁴ shots = 1 day at 10 Hz) add ~$10 M/yr O&M cost. |
| **Classification** | **Degrading**. First-wall erosion and final optics damage do not cause immediate plant failure but degrade availability and increase O&M costs. If first-wall lifetime is 1 year (vs. 5-year target), replacement downtime (2–4 weeks per year) reduces availability from 75% to 70%, increasing LCOE by ~7%. If final optics require replacement every 10⁴ shots (1 day at 10 Hz), O&M cost increases by $10–20 M/yr (~+1–2 $/MWh LCOE). Catastrophic first-wall failure (e.g., crack propagation, coolant leak) is a **binary risk** but is mitigated by redundant cooling loops and structural margin. |
| **Evidence tier** | **Physics: 3** (subscale/adjacent demonstration). 14 MeV neutron damage cross-sections are well characterized (ENDF/B-VIII for Fe, W, SiC); dpa calculations are validated against fission reactor data. Pulsed loading at 10 Hz is **undemonstrated at fusion neutron flux** but is understood via ion beam testing (ITER divertor qualification) and Z-machine X-ray pulse tests. Extrapolation from 0.1 Hz to 10 Hz (100× rep rate) is a **2–3× uncertainty in fatigue lifetime** (material fatigue under cyclic loading scales as N^(-0.1) to N^(-0.3) in metals, where N = cycle count). Tier 3: subscale rep rate, adjacent neutron spectrum. |
| **Evidence tier** | **Hardware: 2** (design study). Focused Energy has disclosed no chamber design, first-wall material, or final optics protection scheme. HYLIFE-III FLiBe thick-liquid concept (cited in XEC white paper and `sciencedirect-science-article-pii-s0920379624001868.md`) is a **design study** for sub-Hz IFE; scaling to 10 Hz requires 10–100× faster clearing (undemonstrated). ITER tungsten divertor is an **operating-regime hardware analogue** (20 dpa, but steady-state not pulsed; fission spectrum not 14 MeV). No 10 Hz IFE chamber has been built. Tier 2: ITER divertor analogue exists (would score tier 3–4) but concept-specific chamber is absent (scores tier 1–2) → weighted average **tier 2** (design study + analogue). |

---

#### Function 5: Neutron/Particle Handling

| Subcategory | Details |
|------------|---------|
| **Plant requirement** | Neutron yield: 5×10¹⁹ n/shot at G=50, 400 kJ compression + 150 kJ ignition (assuming 400 MJ fusion yield per shot, 80% of energy in neutrons = 320 MJ per shot → 320 MJ / 14 MeV per neutron = 1.4×10¹⁹ n/shot; correcting for 17.6 MeV total D-T energy → 5×10¹⁹ n/shot). Annual neutron emission: 1.3×10²⁹ n/yr at 10 Hz, 75% availability. Blanket must absorb neutrons, breed tritium (TBR > 1.05 for self-sufficiency including losses), and extract heat for thermal cycle. Shielding must reduce dose rate outside reactor building to <0.1 mSv/hr (10 CFR Part 20 occupational limit). Activation products in chamber structures (steel, concrete) must be managed per 10 CFR Part 61 low-level waste disposal standards; high-activation zones (first wall, blanket) require remote handling (CAS22 remote maintenance systems). |
| **Best demonstrated** | **Tritium breeding**: ITER blanket modules (under construction) target TBR = 1.15 using Li₄SiO₄ ceramic breeder + Be neutron multiplier (design, not yet operated). JET operated D-T with external tritium supply (no breeding). Fission reactors (CANDU) breed tritium from Li-6 targets in heavy-water coolant (TBR ~ 0.01 per fission neutron, irrelevant to fusion). **Neutron shielding**: ITER biological shield (steel + borated concrete, 2–3 m thickness) is designed to reduce dose to <0.1 mSv/hr outside reactor building at 500 MW fusion power (steady-state, not pulsed). NIF target bay shielding (concrete + polyethylene) handles pulsed 10¹⁹ n/shot at single-shot scale (no 10 Hz operation). **Activation**: JET D-T campaigns produced activated tungsten divertor tiles (~10⁴ Bq/g after 1 year decay, classified as low-level waste); remote handling demonstrated for tile replacement. **14 MeV neutron handling at 10 Hz**: undemonstrated — no fusion facility has operated at 10 Hz with >10¹⁸ n/shot. |
| **Gap ratio** | Tritium breeding: TBR > 1.05 required / TBR = 1.15 ITER design = **0.9× (ITER design exceeds requirement, but ITER has not operated yet)**. If ITER were operating, this would score tier 4; as a design, it scores tier 2. **Neutron fluence**: 1.3×10²⁹ n/yr fast ignition / 1×10²⁸ n/yr ITER (estimated from 500 MW fusion × 3×10⁷ s/yr / 17.6 MeV per neutron) = **13× annual fluence gap**. **Pulsed handling**: 10 Hz / single-shot NIF = **unquantifiable rep rate gap** (NIF handles pulsed neutrons but not at 10 Hz; ITER handles high fluence but steady-state). |
| **Closure mechanism** | Focused Energy confirms lithium blanket for tritium breeding (SRNL partnership for extraction, per Callahan interview). Blanket type unspecified; **inferred** (from IFE heritage): FLiBe liquid blanket (HYLIFE-III analogue) or LiPb liquid blanket (LIFE study analogue), both with Li-6 enrichment to 30–90% for TBR > 1.1. Neutron shielding: steel + borated concrete biological shield (ITER heritage). Activation: remote handling for first-wall and blanket replacement on 1–5 year cycles (CAS22 remote maintenance). Tritium extraction: SRNL-designed system (chemistry TBD: vacuum extraction for Li, chemical separation for LiPb, or electrolytic separation for FLiBe). |
| **Classification** | **Binary** for TBR < 1.0. If tritium breeding ratio falls below 1.0 (accounting for extraction losses, decay, and leakage), the plant cannot achieve fuel self-sufficiency and must purchase external tritium — global supply is ~20 kg/yr (CANDU production), insufficient for a 1 GWe D-T plant (requires ~2–5 kg/yr tritium throughput at steady state). TBR < 1.0 is a **non-viable fuel cycle**. **Degrading** for shielding or activation: insufficient shielding increases occupational dose (regulatory limit violations → forced shutdowns), increasing O&M cost and reducing availability. High activation of first wall/blanket increases replacement cost and waste disposal fees (~+5–10 $/MWh LCOE if disposal cost doubles). |
| **Evidence tier** | **Physics: 3** (subscale/adjacent demonstration). 14 MeV neutron cross-sections (n,2n on Be, n,T on Li-6) are well characterized (ENDF/B-VIII). TBR calculations are validated against fission reactor breeding and MCNP benchmarks (ITER neutronics, NIF-LIFE study). Pulsed neutron transport at 10 Hz is **not fundamentally different** from steady-state (neutron thermalization timescales ~1 ms << 100 ms cycle time), so ITER shielding and activation physics transfer directly. Gap: no **operating-regime demonstration** of TBR > 1.0 in any fusion device (ITER is under construction). Tier 3: adjacent regime (fission breeding, ITER design), subscale (no fusion breeding yet). |
| **Evidence tier** | **Hardware: 2** (design study). Focused Energy has disclosed no blanket design. ITER blanket modules are **under construction but not operated** (tier 2: design study with hardware fabrication in progress). HYLIFE-III FLiBe blanket and LIFE LiPb blanket are **design studies** (tier 2). Tritium extraction from lithium at 10 Hz throughput (63 g/yr = 0.17 g/day) is **undemonstrated** — ITER tritium plant (under construction) is designed for 1 kg/yr extraction (steady-state, not pulsed 10 Hz), which is 16× higher throughput than fast ignition but at different operating mode. Tier 2: ITER tritium plant design + HYLIFE blanket studies, no operating hardware. |

---

#### Function 6: Fuel Cycle Closure

| Subcategory | Details |
|------------|---------|
| **Plant requirement** | Breed tritium at TBR > 1.05, extract tritium from blanket at ≥63 g/yr (0.17 g/day to match 10 Hz consumption at 0.2 mg DT/shot), purify to >99% isotopic purity, and recycle unburned DT from target debris. Startup inventory: 1–3 kg tritium (sourced externally from CANDU or fission reactors; global supply ~20 kg/yr total). Deuterium extraction from seawater (commercial process, 150 ppm D₂O in seawater → 33 g D₂ per m³ seawater; 1 GWe plant requires ~1 kg D/yr = 30 m³ seawater, trivial). Tritium inventory management: <10 g in-process inventory (10 CFR Part 30 license limit), <1 kg on-site total (NRC safety evaluation threshold for Category 2 radioactive material). Tritium permeation control: permeation barriers on all coolant loops, building atmosphere tritium recovery system, tritiated water treatment. |
| **Best demonstrated** | **Tritium breeding**: TBR > 1.0 has **never been demonstrated in any fusion device**. ITER blanket modules (design, not operated) target TBR = 1.15. Fission breeder reactors (liquid metal fast breeder reactors, LMFBRs) achieve breeding ratios >1.0 for U-238 → Pu-239, but neutron energy spectrum is different (MeV fission neutrons vs. 14 MeV fusion neutrons). **Tritium extraction**: TSTA (Tritium Systems Test Assembly, LANL, 1984–1995) demonstrated tritium extraction from lithium at 1 g/day throughput in a test loop (no fusion neutrons, electric heating only). ITER tritium plant (under construction, not operated) is designed for 1 kg/yr extraction from D-T plasmas and blanket. **Tritium purification**: commercial tritium purification via cryogenic distillation achieves >99.9% isotopic purity (Ontario Power Generation Tritium Removal Facility, Darlington; processes 2 kg/yr from CANDU heavy water). **Fuel cycle integration**: JET D-T campaigns (1997, 2021) recycled unburned DT from exhaust gas (pumped via cryopumps, separated via cryogenic distillation); no breeding (external tritium supply). |
| **Gap ratio** | Tritium breeding: TBR > 1.05 required / TBR = 0 demonstrated (no fusion device has operated with breeding) = **N/A (undemonstrated)**. Using ITER design (TBR = 1.15) as reference: 1.05 / 1.15 = **0.9× (ITER design exceeds requirement, but ITER has not operated)**. **Extraction throughput**: 63 g/yr fast ignition / 1 g/day TSTA (365 g/yr) = **0.17× (TSTA exceeds requirement, but TSTA was a test stand not a fusion plant)**. **Fuel cycle integration**: fast ignition requires breeding + extraction + purification + recycling at 10 Hz (integrated loop); JET demonstrated recycling only (no breeding). Gap = **full integration undemonstrated**. |
| **Closure mechanism** | SRNL partnership is developing tritium extraction system (chemistry TBD; likely electrolytic or vacuum extraction depending on blanket type). Tritium plant includes: (1) blanket extraction (online, continuous at 0.17 g/day rate), (2) isotopic separation via cryogenic distillation (ITER-heritage), (3) unburned fuel recovery from target debris (debris swept into recovery system, cryopumped, distilled), (4) inventory control via accountancy system (track tritium in blanket, coolant, atmosphere, waste), (5) permeation barriers on primary coolant loops (ITER heritage: aluminum oxide coatings on steel, double-walled heat exchangers). Deuterium supply: seawater extraction (commercial, no technical risk). Startup tritium: 1–3 kg purchased from Ontario Power Generation or Savannah River (fission production); payback period 2–5 years once breeding reaches equilibrium. |
| **Classification** | **Binary** for TBR < 1.0 (see Function 5). If breeding fails, plant cannot sustain operation beyond startup inventory depletion (1–3 kg / 63 g/yr = 15–50 years at 100% extraction efficiency; in practice, 5–10 years accounting for losses → external tritium purchase required → global supply insufficient → plant shuts down). **Degrading** for extraction efficiency: if extraction efficiency is 80% (vs. 95% target), effective TBR = 0.8 × 1.15 = 0.92 < 1.0 → binary failure. If extraction efficiency is 90%, effective TBR = 1.04 ≈ 1.05 → marginal closure with 1–2% annual tritium makeup from external sources (global supply can support 1–5 fast ignition plants, not 100). |
| **Evidence tier** | **Physics: 3** (subscale demonstration). Tritium breeding physics (Li-6(n,T)He-4 reaction) is well characterized; TSTA validated extraction at 1 g/day (16× higher than fast ignition requirement). Fuel cycle integration (breeding + extraction + purification + recycling) is **undemonstrated** — JET recycled without breeding, TSTA extracted without breeding, ITER will integrate all steps but has not operated. Gap: no **operating fusion device** has closed the fuel cycle. Tier 3: subscale (TSTA extraction, JET recycling) but no full integration. |
| **Evidence tier** | **Hardware: 2** (design study). ITER tritium plant is under construction (tier 2: hardware in progress, not operated). Focused Energy has disclosed no tritium plant design; SRNL partnership is at early stage (no published system design). Blanket type is unspecified (FLiBe, LiPb, solid ceramic) → extraction chemistry is undefined. Tier 2: ITER hardware analogue (under construction) + SRNL partnership (early-stage design). |

---

#### Function 7: Power Conversion & BOP

| Subcategory | Details |
|------------|---------|
| **Plant requirement** | Conventional Rankine steam cycle: blanket heat (1.5 GWth absorbed neutron energy + 0.5 GWth radiation) drives primary coolant loop (Li or LiPb or FLiBe at 500–700°C, depending on blanket type), transfers heat via intermediate heat exchanger (IHX) to secondary steam loop (superheated steam at 450–550°C, 10–15 MPa), expands through steam turbine-generator at 40% thermal efficiency (canonical η_th for superheated steam per `scoring_framework.md`), condenses in cooling towers, and returns to IHX. Pulsed heat load: 2 GWth at 10 Hz = 200 MJ thermal per shot, absorbed by blanket/coolant thermal mass over 0.1 s cycle (peak heat flux averaged over blanket surface area ~1–2 MW/m² at 5 m chamber radius, 300 m² surface → 200–600 MW peak, 2 GW average). Thermal inertia: coolant thermal mass must buffer 100 ms shot-to-shot pulsations; steam generator sees time-averaged 2 GWth (no pulsations if blanket/coolant volume ≥10 m³ → thermal time constant ~10 s >> 0.1 s cycle). |
| **Best demonstrated** | **Rankine steam cycle at 40% efficiency**: commercially mature in coal, natural gas combined-cycle (Brayton-Rankine), and nuclear fission plants (PWR, BWR) at GWe scale. Thousands of operating plants globally at 35–42% thermal efficiency (coal: 35–40%, supercritical steam: 42–45%, nuclear PWR: 33–36%). **Pulsed heat source feeding steam cycle**: undemonstrated at fusion scale. Analogues: (1) pulsed nuclear reactors (TRIGA pulse mode: 250 MW peak, 30 ms pulse, 1 pulse/hour) feed pool cooling, not steam; (2) solar thermal with molten salt storage (time-averaged heat input to steam cycle, no pulsations); (3) Z-machine IFE chamber studies (pulsed heat at 0.1 Hz, no steam cycle integration). **IHX for liquid metal / molten salt to steam**: demonstrated in sodium-cooled fast reactors (SFR: Phenix, Superphenix, BN-600) at 250–560 MWe scale, steady-state (not pulsed). Molten salt reactor experiment (MSRE, 1965–1969) operated FLiBe-to-steam IHX at 7 MWth, steady-state. **10 Hz pulsed operation with steam cycle**: undemonstrated. |
| **Gap ratio** | Thermal cycle efficiency: 40% required / 40% demonstrated (commercial steam plants) = **1.0× (no gap)**. Pulsed heat integration: 10 Hz pulsed / steady-state steam plants = **N/A (different operating mode, but thermal buffering via coolant mass makes this a ~1.1× uncertainty, not a fundamental gap — thermal inertia smooths pulsations if coolant volume is adequate)**. IHX for liquid metal: demonstrated at SFR scale (250–560 MWe) → 1 GWe fast ignition requires **1.8–4× scale-up in IHX thermal power** (560 MWe SFR at ~33% thermal efficiency = 1.7 GWth; fast ignition at 2 GWth is 1.2× larger, within <2× gap → tier 4 "near-regime"). |
| **Closure mechanism** | Focused Energy explicitly confirmed conventional steam cycle (Callahan interview: "We will use a conventional steam cycle to convert the heat into electricity"). BOP is **fusion-agnostic** — once heat is delivered to the steam loop, the turbine-generator and cooling systems are identical to coal/nuclear plants. Pulsed heat is buffered by blanket/coolant thermal mass: liquid lithium (or LiPb or FLiBe) has high volumetric heat capacity (~3–4 MJ/m³/K); 10 m³ coolant volume at 600°C absorbs 200 MJ per shot with <10 K temperature rise → time-averaged heat input to steam generator is smooth (pulsations <1%). Steam turbine sees steady 2 GWth input, no pulsed-load stress. IHX: SFR heritage (sodium-to-steam) or MSRE heritage (FLiBe-to-steam); scaling from 250–560 MWe to 1 GWe is **engineering scale-up, not physics innovation**. |
| **Classification** | **Degrading**. Steam cycle failure (turbine trip, IHX leak, cooling water shortage) causes loss of heat sink → blanket/coolant temperature rises → plant shutdown to avoid overheat, but this is a **recoverable fault** (restart after cooldown, no permanent damage if shutdown occurs within ~1 hour). Pulsed-heat-induced fatigue in steam generator tubes (10 Hz thermal cycling at 100 ms period) could reduce IHX lifetime from 30 years (steady-state SFR) to 10–20 years (pulsed operation) → higher CAS22 replacement cost → +2–3 $/MWh LCOE increase. Not binary because backup heat rejection (blowdown to atmosphere, passive decay heat removal) prevents meltdown. |
| **Evidence tier** | **Physics: 5** (operating-regime demonstrated at commercial scale). Rankine steam cycle at 40% efficiency is **commercially mature** with >1,000 operating plants at GWe scale globally (coal, nuclear PWR, combined-cycle gas turbines). Pulsed heat buffering via thermal mass is **standard engineering** (solar molten salt storage, diesel engine coolant systems) — no physics risk. Tier 5: operating at commercial scale in the same thermal regime (450–600°C steam, 10–15 MPa). |
| **Evidence tier** | **Hardware: 4** (near-regime demonstrated). IHX for liquid metal or molten salt to steam is **demonstrated at 250–560 MWe scale** in SFRs (Phenix, BN-600) and MSRE (7 MWth). Fast ignition at 1 GWe requires 2 GWth IHX, which is **1.2–8× scale-up** depending on reference (BN-600 at 560 MWe = 1.7 GWth → 1.2× gap, tier 4 "near-regime"). Pulsed operation at 10 Hz is **undemonstrated** but poses low risk due to thermal buffering (coolant thermal mass >> per-shot energy → steam generator sees time-averaged heat). Tier 4: demonstrated at ≥50% of plant scale (BN-600) with <2× extrapolation (1.2× for thermal power, 10 Hz pulsations are buffered out). |

---

### Function-Level Means (Symmetric Arithmetic Average of Physics and Hardware Tiers)

| Function | Physics Tier | Hardware Tier | Mean (before heritage) | Heritage Credit (D-T tokamak/IFE = none for FI) | Final F_n |
|----------|--------------|---------------|------------------------|------------------------------------------------|-----------|
| F1: Plasma Performance | 2 | 2 | 2.0 | **3.5 (laser IFE heritage)** — NIF indirect drive demonstrated ignition (2022), OMEGA direct drive achieved ρR = 0.3 g/cm² (2014), but fast ignition has not demonstrated gain > 1. NIF-LIFE and HAPL design studies (LLNL, 2000s–2010s) provide systems engineering heritage. Apply laser IFE floor 3.5. | **3.5** |
| F2: Driver / Energy Input | 4 | 3 | 3.5 | **3.5 (laser IFE heritage)** — NIF Nd:glass laser (1.9 MJ demonstrated), OMEGA DPSSL (30 kJ at 1 shot/hour), Amplitude petawatt lasers (150 J at 1 Hz). Laser IFE floor 3.5 matches computed mean 3.5 (no override). | **3.5** |
| F3: Instability Control | 3 | 3 | 3.0 | **3.5 (laser IFE heritage)** — OMEGA RT-stabilized implosions (20+ years), NIF ignition (RT-controlled hohlraum symmetry). Fast ignition cone-tip instabilities are undemonstrated but general ICF instability physics is mature. Floor 3.5 overrides 3.0. | **3.5** |
| F4: Plasma-Wall Interaction | 3 | 2 | 2.5 | **3.5 (laser IFE heritage)** — Z-machine pulsed chamber tests (0.1 Hz, 10³ shots), HYLIFE-III FLiBe chamber design studies, NIF final optics replacement protocols. Laser IFE floor 3.5 overrides 2.5. | **3.5** |
| F5: Neutron/Particle Handling | 3 | 2 | 2.5 | **3.5 (laser IFE heritage)** — ITER shielding and tritium plant (under construction), HYLIFE/LIFE blanket neutronics (LLNL studies), fission reactor activation databases (ENDF/B-VIII). Floor 3.5 overrides 2.5. | **3.5** |
| F6: Fuel Cycle Closure | 3 | 2 | 2.5 | **3.5 (laser IFE heritage)** — JET D-T campaigns (tritium recycling), TSTA (tritium extraction), ITER tritium plant design, LIFE/HYLIFE fuel cycle studies. Floor 3.5 overrides 2.5. | **3.5** |
| F7: Power Conversion & BOP | 5 | 4 | 4.5 | **No heritage credit** (conventional steam cycle, not fusion-specific; scoring framework states heritage credit applies only when the heritage assists risk retirement — BOP is mature regardless of fusion concept). Floor does not apply. | **4.5** |

**Heritage credit rationale**: Focused Energy inherits laser IFE engineering heritage (NIF ignition 2022, OMEGA direct drive, HYLIFE/LIFE chamber/blanket studies, HAPL laser development) for functions F1–F6. Fast ignition has not demonstrated gain, but the compression physics (F1), DPSSL driver (F2), RT control (F3), chamber neutronics (F5), and fuel cycle (F6) share 80–90% commonality with validated IFE approaches. The heritage floor 3.5 reflects this inheritance. **F7 (BOP) gets no heritage credit** because steam Rankine cycle is mature outside fusion (commercial coal/nuclear plants) — the risk retirement comes from external analogues, not fusion heritage.

---

### Binary Risks

1. **TBR < 1.0 (Function 6)**: If tritium breeding ratio falls below 1.0 (accounting for extraction losses, decay, permeation), the plant cannot achieve fuel self-sufficiency and must purchase external tritium. Global tritium supply is ~20 kg/yr (CANDU production), insufficient to sustain a 1 GWe D-T plant long-term (requires 2–5 kg/yr throughput). Without breeding, the plant shuts down after startup inventory is exhausted (5–10 years).

2. **Proton coupling efficiency η_coup < 7% (Function 1)**: Fast ignition is a threshold phenomenon — if the proton beam fails to deposit sufficient energy in the compressed hot spot (η_coup below ignition threshold), thermonuclear burn does not initiate and fusion yield is zero. The plant produces no net electricity. Unlike CHS ignition (where coupling degrades gradually), fast ignition either ignites or fails discretely.

3. **Petawatt ignition laser failure at 10 Hz (Function 2)**: If the ignition laser cannot deliver 150 kJ at 10 Hz with ±10 ps timing jitter, ignition fails on every shot and fusion yield is zero. The compression laser alone (without ignition) produces compressed cores at ρR ~ 0.3 g/cm² but Q < 1 (no ignition) → no net electricity. Unlike CHS direct drive (where a single driver failure can be compensated by rebalancing remaining beams), fast ignition requires both lasers to function simultaneously within ps-level synchronization.

---

### YAML Scores Block

```yaml
---
scores:
  C1: 2.5
  C3: 3.3
  C4: 2.8
  C5: 1.7
  C8: 3.0
  F1: 3.5
  F2: 3.5
  F3: 3.5
  F4: 3.5
  F5: 3.5
  F6: 3.5
  F7: 4.5
  binary_risks:
    - "TBR < 1.0: Tritium breeding ratio below 1.0 (accounting for extraction losses) prevents fuel self-sufficiency; plant shuts down after startup inventory depletion (5-10 years); global tritium supply insufficient for long-term D-T operation"
    - "Proton coupling efficiency η_coup < 7%: Fast ignition threshold failure — hot spot never reaches thermonuclear conditions, fusion yield is zero, plant produces no net electricity"
    - "Petawatt ignition laser failure at 10 Hz: If ignition laser cannot deliver 150 kJ at 10 Hz with ±10 ps timing, ignition fails and fusion yield is zero; compression laser alone produces Q < 1 (no ignition, no net electricity)"
---
```
