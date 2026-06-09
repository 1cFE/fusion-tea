---
ID: 35-polomac-magnetic-confinement
Concept: Polomac Magnetic Confinement (Deutelio)
Company: Deutelio
Type: synthesis
Status: draft
Created: 2026-06-08
---

# Editorial Synthesis: Polomac Magnetic Confinement (Deutelio)

## 1. Executive Summary

- **Most important risk**: The magnetic tunnel concept has never been experimentally demonstrated. The claimed 2-3× lower magnetic field advantage depends entirely on unquantified particle losses through field-line "breaches" that may render the concept non-viable.

- **Most important advantage**: If the physics works, steady-state operation at 2-3 T field (vs 5+ T for tokamaks or 12-20 T for HTS compact tokamaks) could dramatically reduce magnet capital costs without disruption risk.

- **LCOE ballpark**: No credible estimate possible. The speculative corridor model yields 130 ¢/kWh at ~84 MWe assuming invented parameters (P_fus=400 MW, Q_sci=10), but this number is meaningless without experimental validation. The concept has no design point, no disclosed power target, and no power balance analysis.

- **Confidence verdict**: **Low** — All cost-relevant parameters are either unknown (fusion power, Q_eng, heating method, reactor geometry) or unvalidated (magnetic field advantage, confinement time, particle loss rates). The 81× temperature gap between the planned 100 eV prototype and 8.1 keV D-T reactor requirements makes extrapolation extremely speculative.

## 2. What Matters Most for LCOE

### Ranked by sensitivity (high to extreme uncertainty):

**1. Q_eng and Power Balance** (BLOCKING)
- **Assumed value**: Q_eng ~ 5.5 (derived from speculative P_fus=400 MW, Q_sci=10)
- **Sensitivity**: At Q_sci=5, LCOE → 245 ¢/kWh. At Q_sci=20, LCOE → 105 ¢/kWh. Below Q_sci ~ 3.5, plant becomes energy sink.
- **Source**: Pure speculation — no heating method disclosed, no recirculating power analysis exists
- **What would flip the conclusion**: The 2014 design had 700 MW coil power consumption (excessive for steady state). If superconducting transition fails to reduce this below ~50 MW, Q_eng collapses below unity and LCOE becomes infinite. Conversely, if tunnel losses are negligible and Q_sci reaches 15+, LCOE could approach 110 ¢/kWh.

**2. Fusion Power Scale** (BLOCKING)
- **Assumed value**: 400 MW fusion power yielding ~84 MWe net
- **Sensitivity**: LCOE ∝ 1/P_fus approximately. At 200 MW: 238 ¢/kWh. At 800 MW: 100 ¢/kWh.
- **Source**: Invented for corridor purposes — no company-disclosed power target exists
- **What would flip the conclusion**: The 1300 m³ plasma volume (2014 design) is enormous compared to compact tokamaks. If Deutelio pursues a small-scale demonstration plant (<100 MWe), LCOE will be poor due to economy-of-scale penalties. A commercial-scale plant (400+ MWe) would require demonstrating the physics at lab scale first — a multi-decade pathway.

**3. Magnetic Tunnel Particle Losses** (PHYSICS UNDEMONSTRATED)
- **Assumed value**: Losses acceptable, confinement time τ_E = 4-5 s comparable to ITER
- **Sensitivity**: Not directly modeled, but if tunnel losses degrade confinement by 2×, fusion power requirement doubles for same net output, shifting LCOE from 130 → 200+ ¢/kWh.
- **Source**: 2024 JTSP paper notes particles at 100 eV "cannot be deviated and hit the vault" along tunnel symmetry planes, and 10 eV particles "could accumulate drifts or get aligned with the field and escape." Extent of loss unquantified.
- **What would flip the conclusion**: If PSI particle-path analysis (contracted, unpublished) shows >30% of plasma energy is lost through tunnels, the concept is non-viable — confinement advantage disappears, negating the lower-field benefit. If losses are <10%, the 2-3 T field advantage is real and LCOE could beat conventional tokamaks.

**4. Magnet Capital Cost** (HIGH UNCERTAINTY)
- **Assumed value**: $180M for 2.5 T superconducting system
- **Sensitivity**: $100M → 127 ¢/kWh; $400M → 137 ¢/kWh (8% LCOE swing across range)
- **Source**: Assumed from lower-field advantage, but no magnet design disclosed
- **What would flip the conclusion**: Magnetic tunnel geometry creates discontinuous azimuthal structure. If coil integration requires expensive custom support structures or neutron shielding penetrations compromise field quality, magnet cost could exceed tokamak values despite lower field. The 2.5 T advantage is only economic if tunnel-penetrated geometry doesn't add structural cost.

**5. Thermal Conversion Efficiency** (MODERATE UNCERTAINTY)
- **Assumed value**: 35% (Rankine cycle at 350°C target)
- **Sensitivity**: 30% → 175 ¢/kWh; 45% → 87 ¢/kWh
- **Source**: 2024 JTSP roadmap mentions "350°C for electricity generation" but no power cycle specified
- **What would flip the conclusion**: The initial development target is 150-200°C heat generation (industrial use), which would yield <20% thermal efficiency — economically uncompetitive for electricity. If blanket design allows sCO2 cycle at 500-600°C (45% efficiency), LCOE could drop to ~90 ¢/kWh, but D-T blanket at this temperature is a major engineering challenge.

## 3. Risk Verdicts

### **Magnetic Tunnel Physics** → **Genuinely uncertain**
**Rationale**: The concept has never been tested. Past poloidal confinement experiments failed due to support-wire contamination; magnetic tunnels eliminate wires but introduce field-line breaches. Whether particle losses through tunnels are acceptable is unknown.

**What would retire this risk**: Small prototype operation (100 eV, 0.2-0.3 T) demonstrating (1) shaped magnetic tunnels exist as designed, (2) particle loss rates through tunnels are measurable, and (3) confinement time scales favorably compared to simple dipole. Timeline: prototype construction in ~1 year (claimed), experimental campaign 2-3 years. Results by ~2027 earliest.

### **81× Temperature Scaling (100 eV → 8.1 keV)** → **Unlikely resolvable in near term**
**Rationale**: This is not a small extrapolation. The prototype operates at sub-ionization energies; the reactor requires D-T fusion temperatures. Heating method for reactor scale is not disclosed. MHD stability at fusion-relevant beta and temperature is unanalyzed.

**What would retire this risk**: Intermediate-scale experiment (1-10 keV, ~1 T field, D-D conditions) with validated heating method and measured confinement. This would require funding and infrastructure comparable to a mid-scale tokamak program — likely a 10-15 year pathway from prototype to keV-scale demonstration.

### **700 MW Coil Power Consumption (2014 Design)** → **Likely resolvable**
**Rationale**: The 2014 design used copper coils. Transition to superconducting magnets (mentioned in roadmap) would reduce steady-state power consumption to cryogenic loads (~10-20 MW). This is engineering risk, not physics risk.

**What would retire this risk**: Superconducting magnet design study showing <30 MW recirculating power for reactor-scale field. LTS magnets at 2-3 T are well-established technology (ITER-class). HTS would be overkill at this field. Risk is low if physics works; high if physics doesn't justify the investment.

### **D-D Fuel Pathway (142× Lawson Criterion vs D-T)** → **Unlikely resolvable**
**Rationale**: D-D operation at 100-200 keV with 20-40 s confinement time is dramatically more challenging than D-T. No fusion concept has achieved these conditions. The stated goal of avoiding tritium breeding blankets is laudable, but the performance requirement is prohibitive.

**What would retire this risk**: Demonstration of D-D breakeven in any magnetic confinement concept. This would be a field-wide breakthrough, not Polomac-specific. More realistic: abandon D-D aspirations, accept D-T blanket complexity, and target 8.1 keV D-T conditions (still undemonstrated for Polomac but at least tokamak-comparable).

### **Large Plasma Volume (1300 m³)** → **Genuinely uncertain**
**Rationale**: The 2014 conceptual design had 1300 m³ plasma volume — 20× larger than HTS compact tokamaks. This suggests a large device with correspondingly high capital costs (vessel, blanket, shield, building). The lower magnetic field advantage may be offset by size-driven cost increases.

**What would retire this risk**: Updated reactor-scale design study with plasma volume optimization. If high beta (20-30%) enables volume reduction to 300-500 m³ while maintaining power output, capital cost concerns are mitigated. If 1000+ m³ is intrinsic to the dipole geometry, the concept competes poorly with compact tokamaks on $/kWe.

## 4. Structural Advantages and Disadvantages

**vs. Conventional D-T Tokamak (ITER-class, 5.3 T, pulsed):**

### Advantages (if physics works):
- **Lower magnetic field** (2-3 T vs 5.3 T): Eliminates ~40% of magnet stored energy, potentially reducing CAS22-C220103 by $200-400M for equivalent thermal output. Estimated savings: ~15% of reactor plant capital.
- **Steady-state by design**: No disruption risk, no cyclic thermal/mechanical fatigue, no current-drive requirement beyond startup. Reduces CAS27 (maintenance) by ~10-20% relative to pulsed tokamak.
- **High beta (20-30%)**: Enables higher plasma pressure at lower field. Could reduce required plasma volume by 2-3× for given fusion power, offsetting size concerns.

### Disadvantages (or neutral):
- **Particle losses through magnetic tunnels**: Creates an energy loss channel not present in closed-flux-surface tokamaks. Unquantified. Could increase fusion power requirement by 1.5-3× for same net output, increasing CAS22-C220101 (blanket) and CAS22-C220104 (heating) by 30-50%.
- **Large plasma volume** (1300 m³ from 2014 design): 20× larger than SPARC-class compact tokamaks. Increases CAS21 (reactor building), CAS22-C220101/102/105/106 (blanket, shield, structure, vessel) by estimated 50-100% for equivalent net power. The lower-field magnet savings may be entirely offset by size penalties.
- **Magnetic tunnel structural complexity**: Discontinuous azimuthal geometry with field-line penetrations. Increases CAS22-C220105 (primary structure) by estimated 20-40% relative to continuous toroidal structure due to non-standard loading paths and neutron streaming concerns.
- **Unknown heating system**: No disclosed method for 8.1 keV D-T (or 100-200 keV D-D). CAS22-C220104 (heating) is pure speculation. If D-D is pursued, heating costs could be 2-5× tokamak values due to extreme temperature requirement.

### Net Cost Position:
**Indeterminate.** The lower-field advantage ($100-200M savings) competes against size penalty ($200-400M increase) and tunnel complexity ($50-100M increase). If tunnel losses are severe, heating requirements dominate and LCOE exceeds tokamaks. If tunnel losses are negligible and plasma volume can be reduced via high beta, LCOE could undercut conventional tokamaks by 20-30%. Current data does not support a confident prediction.

## 5. Cross-Concept Positioning

**Polomac occupies a unique niche: poloidal dipole confinement with mechanical support via magnetic field shaping.**

### Closest relatives:
- **Levitated Dipole (LDX, MIT)**: Same closed-field-line dipole physics, but avoided support-wire contamination via superconducting levitation coil. LDX achieved plasma confinement but required cryogenic levitation system and operated at sub-keV temperatures. Polomac eliminates levitation complexity by mechanically supporting the dipole through field-free "tunnels," but reintroduces plasma-structure interaction losses at tunnel locations. **Trade**: simpler engineering, uncertain plasma impact.

- **Magnetic Mirrors (Realta, Terra Fusion)**: Open-ended field lines with axial loss cone. Mirrors accept particle losses by design and optimize end-plugs. Polomac has closed field lines except at tunnel locations — conceptually lower losses than mirrors, but tunnel loss rate is unknown. **Trade**: potentially better confinement, undemonstrated.

- **Conventional Tokamaks**: Closed flux surfaces, high field (5-12 T), pulsed or near-steady-state. Polomac claims 2-3× lower field via high beta — if validated, this is a major cost advantage. **Trade**: lower field and simpler geometry vs. 40 years of validated tokamak physics.

### Cost landscape position (speculative):
- **Above tokamaks** if tunnel losses are severe (130-250 ¢/kWh range)
- **Comparable to tokamaks** if tunnel losses are moderate and superconducting transition succeeds (100-130 ¢/kWh)
- **Below tokamaks** if tunnel losses are negligible and high beta enables compact design (70-100 ¢/kWh) — optimistic scenario

**The concept is not clearly "better" or "worse" than tokamaks — it's a high-variance bet on undemonstrated physics.** If magnetic tunnel confinement works as hoped, Polomac could be a simpler, cheaper tokamak alternative. If tunnel losses are high, it's a dead end.

## 6. Modeling Confidence

**Rating: Low**

### Parameters data-anchored:
- Magnetic field target (2-3 T): literature-stated, medium confidence
- Plasma volume (1300 m³): from 2014 paper, low confidence (may be outdated)
- Beta (20-30%): from past poloidal experiments, medium confidence (but at much lower temperature)
- Fuel costs (D-D or D-T): well-established, high confidence

### Parameters speculative or unknown:
- **Fusion power** (P_fus): Invented. No source value.
- **Scientific Q** (Q_sci): Assumed. No heating method disclosed.
- **Engineering Q** (Q_eng): Derived from speculative Q_sci and assumed recirculating power. 2014 design had Q_eng << 1 (700 MW coil power). Superconducting transition claimed but not analyzed.
- **Confinement time** (τ_E): Extrapolated from tokamak values. No experimental basis for magnetic tunnel geometry.
- **Particle loss rates through tunnels**: Unquantified. Acknowledged as unknown in 2024 JTSP paper.
- **Heating method and power**: Unknown for reactor scale. Small prototype uses 5-10 kW ECRH, not scalable.
- **Net electric output**: No design point disclosed. ~84 MWe in model is corridor invention.

### Dominant source of LCOE uncertainty:
**Q_eng and power balance.** The 2014 design was not a viable power plant (700 MW recirculating power). The 2024 report mentions superconducting magnets but provides no Q_eng or net power analysis. Until recirculating power fraction is quantified, all LCOE estimates are speculative.

The magnetic tunnel particle loss rate is the **dominant physics uncertainty**. If losses are <10%, the concept could be competitive. If losses are >30%, LCOE escalates rapidly due to increased fusion power requirement.

### Confidence breakdown:
- **Physics demonstration**: Zero experimental data. TRL 2-3.
- **Engineering design**: No reactor-scale design exists. 2014 paper is conceptual electromagnetics study.
- **Cost model**: Pure speculation. No capital cost, O&M, or capacity factor data from Deutelio.

**This is not a cost estimate — it's a speculative corridor illustrating where LCOE might land IF the physics works and IF superconducting magnets are successfully integrated.**

## 7. What Would Change My Mind

### In the direction of HIGHER confidence / LOWER LCOE:

**1. Small prototype experimental results (2027-2029 timeframe)**
- Demonstration that magnetic tunnels confine plasma at 100 eV with measurable particle loss rates <20% of total energy flow
- Measured confinement time scaling favorably with temperature (τ_E ∝ T^α where α ≥ 0.5)
- Validation of custom MHD code predictions against experimental equilibrium
- **Impact**: Would retire the absolute physics blocker and enable credible extrapolation to keV-scale. LCOE confidence → Medium. Would justify intermediate-scale experiment funding.

**2. Reactor-scale design study disclosure (post-2026)**
- Quantified power balance: P_fus, P_th, P_net with recirculating power breakdown
- Superconducting magnet specification (conductor type, field, stored energy, cryogenic load)
- Plasma volume optimization via high-beta scaling (target <500 m³ for 500+ MWe)
- **Impact**: Would replace speculative corridor with data-grounded estimate. LCOE confidence → Medium-High if design shows Q_eng > 5.

**3. Independent validation of magnetic tunnel confinement claims**
- PSI particle-path analysis publication showing <15% energy loss through tunnels
- Second lab (non-Deutelio) builds magnetic tunnel test article and confirms field shaping
- Plasma confinement community peer review endorsing the concept as plausible
- **Impact**: Would shift concept from "speculative" to "unproven but credible." LCOE confidence → Medium.

### In the direction of LOWER confidence / HIGHER LCOE (or non-viability):

**1. PSI particle-path analysis shows severe losses (>30%)**
- Magnetic tunnels act as large loss channels, degrading confinement by 2-3× relative to closed dipole
- Confinement time cannot reach tokamak-comparable values without impractical field increase
- **Impact**: Concept is non-viable. LCOE → infinite. Physics blocker becomes retirement trigger.

**2. Small prototype fails to confine plasma or shows uncontrolled instabilities**
- Custom MHD code predictions do not match experimental observations
- Plasma cannot be heated above 100 eV due to tunnel losses
- Stability issues prevent steady-state operation
- **Impact**: Development pathway stalls. LCOE confidence → Very Low (concept likely abandoned).

**3. Superconducting magnet integration shows high recirculating power (>50 MW for 400 MW fusion)**
- Cryogenic loads, power supplies, and control systems consume more power than anticipated
- Q_eng < 3, making net-positive electricity difficult at small scale
- **Impact**: LCOE → 200+ ¢/kWh due to poor power balance. Concept shifts to "thermal-only" niche (industrial heat, not electricity).

---

**In summary: This concept is a high-uncertainty, high-potential-payoff bet. The physics gap is absolute (no experimental validation), the power balance is unknown (no Q_eng analysis), and the cost structure depends entirely on undemonstrated advantages (lower field, acceptable tunnel losses). LCOE could range from 70 ¢/kWh (optimistic breakthrough) to infinite (physics doesn't work). Current best estimate if physics works: 100-150 ¢/kWh at small scale, potentially 70-100 ¢/kWh at NOAK commercial scale — but confidence is low until prototype demonstrates confinement.**
