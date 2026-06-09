---
ID: 36-helical-coil-stellarator
Concept: Helical-Coil Stellarator (HESTIA)
Company: Helical Fusion
Type: synthesis
Status: draft
Created: 2026-06-08
---

## 1. Executive Summary

- **Single most important risk**: Confinement enhancement factor H = 1.3 is unvalidated — if it doesn't materialize, the plant may not reach net electricity at the stated scale. The AIP paper explicitly warns "there is almost no experimental backup" for this assumption.
- **Single most important advantage**: Eliminates divertor entirely ($36.6M capital savings at native scale) by using an integrated liquid-metal free-surface first wall. No other concept achieves this.
- **LCOE ballpark**: 915 $/MWh at 1 GWe NOAK (1025 $/MWh at native 70.4 MWe scale). Non-competitive with fission or renewables, but in the middle of the stellarator pack.
- **Confidence verdict**: **Low**. The cost model rests on a single 1990s-era lump-sum estimate ($5B, requiring 2× inflation adjustment), zero per-account grounding, unvalidated confinement physics, and proprietary HTS conductor pricing.

---

## 2. What Matters Most for LCOE

### 2.1 HTS Magnet Cost (C220103: $3.08B absolute, dominates capital)

**Assumed value**: Library default REBCO pricing (~$40–50/kA-m, planar winding basis), scaled to 7.8 m major radius continuous helical coils at 9 T on-axis field.

**Sensitivity magnitude**: Magnets represent **47% of direct capital** at native scale. A 50% increase in WISE conductor cost (e.g., $75/kA-m due to 3D winding complexity) would raise overnight capital by ~$1.5B and LCOE by ~140 $/MWh at 1 GWe scale.

**What would flip the conclusion**: If WISE conductor achieves $20/kA-m through mass production (2.5× cost reduction vs. library default), LCOE drops to ~750 $/MWh — still non-competitive but within striking distance of coal + CCS. Conversely, if continuous helical winding carries a 2× manufacturing premium vs. modular coils, LCOE exceeds 1100 $/MWh and the concept is economically retired.

---

### 2.2 Thermal Conversion Efficiency (η_th: 50% assumed, 20% demonstrated)

**Assumed value**: 50% thermal efficiency via supercritical CO2 Brayton cycle at 800–1200 K (Helical Fusion target). The Oroshhi-2 demonstration targets 20 kWe at **20% efficiency** — a 2.5× gap.

**Sensitivity magnitude**: If η_th = 40% (closer to conventional Rankine), P_gross drops from 139 MWe to ~100 MWe. With 125 MW recirculating power (from Q_eng = 2.0), **the plant does not reach net electricity**. At 50%, P_net = 70 MWe. This is a binary viability threshold, not a marginal LCOE shift.

**What would flip the conclusion**: Demonstrating η_th ≥ 45% at MW-scale with tritium-compatible heat exchangers would validate the design point. Below 42%, the plant must either increase fusion power (larger machine, higher field, or validated confinement enhancement) or accept sub-net operation as a technology demonstrator.

---

### 2.3 Confinement Enhancement Factor H = 1.3 (unvalidated)

**Assumed value**: H = 1.3 relative to ISS04 stellarator scaling, plus γ_CEPI = 1.18 center-peaked heating effect, for a combined ~1.5× confinement improvement over baseline heliotron scaling.

**Sensitivity magnitude**: If H = 1.0 (baseline LHD-class heliotron, no optimization), the plasma must run at higher density to maintain P_fus = 250 MW. The design already operates near the Sudo density limit; exceeding it risks confinement degradation or requires off-axis ECRH mitigation (untested). This directly affects whether Q ~ 13 and Q_eng = 2.0 are achievable.

**What would flip the conclusion**: The $480M HESTIA-Primary prototype (1990s dollars, ~$1B current-year) is proposed specifically to validate this confinement enhancement. If HESTIA-Primary achieves H ≥ 1.2 with steady-state burn, the full HESTIA design is credible. If H < 1.1, the concept requires re-engineering (larger machine, higher field, or lower power target).

---

### 2.4 Liquid Metal Blanket Corrosion Rate (drives replacement frequency)

**Assumed value**: Library default blanket lifetime (~5–10 years between module replacements). The AIP paper warns that "tin is highly corrosive to steel" and that corrosion protection "requires careful consideration."

**Sensitivity magnitude**: If corrosion forces blanket module replacement every 2 years instead of 5+, O&M costs (CAS70) double, and availability drops due to extended maintenance outages. The 3-month maintenance interval claim assumes infrequent blanket replacement; annual replacement would violate the >80% availability target.

**What would flip the conclusion**: GALOP test results showing <0.1 mm/year corrosion rate under prototypical liquid metal flow + neutron flux would validate long module lifetimes. Conversely, if corrosion exceeds 1 mm/year, the high-manganese steel first wall degrades faster than acceptable, and the integrated blanket/divertor advantage evaporates (savings from eliminating C220108 are offset by increased C220101 replacement costs).

---

### 2.5 250 GHz Gyrotron Unit Cost (C220104: $100M at native scale, 60 units)

**Assumed value**: Library default based on ITER 170 GHz gyrotron cost (~$2–3M each). HESTIA requires 60× 250 GHz, 1 MW CW units, which **do not yet exist**.

**Sensitivity magnitude**: If 250 GHz gyrotrons carry a 2× development premium ($5M each), C220104 rises from $100M to $300M, adding ~30 $/MWh to LCOE at 1 GWe scale. If mass production drives unit cost below $1M (optimistic), LCOE drops by ~15 $/MWh.

**What would flip the conclusion**: A vendor quote (CPI, Thales, Toshiba) for 250 GHz, 1 MW CW gyrotrons at <$2M/unit would validate library defaults. Above $6M/unit, ECRH becomes a critical cost driver and the concept should pivot to alternative heating (e.g., NBI, but this violates HESTIA's "no NBI" design philosophy).

---

## 3. Risk Verdicts

### 3.1 Confinement Enhancement H = 1.3 Not Validated

**Verdict**: **Genuinely uncertain**

**Rationale**: LHD has 25 years of heliotron data at H ~ 1.0; the optimized configuration is untested.

**What would retire this risk**: HESTIA-Primary prototype achieving H ≥ 1.2 with steady-state burn over multi-hour discharges. Alternatively, scaled LHD experiments with magnetic field optimization demonstrating confinement improvement in the heliotron configuration.

---

### 3.2 Supercritical CO2 Efficiency Gap (20% demonstrated, 50% required)

**Verdict**: **Unlikely resolvable at stated timeline without major redesign**

**Rationale**: The 2.5× efficiency gap between Oroshhi-2 demo (20%) and commercial target (50%) is large. Fission sCO2 programs (DOE-funded) target 45–48% efficiency and are still TRL 5–6 after years of development.

**What would retire this risk**: Oroshhi-2 or a follow-on demonstration achieving ≥45% efficiency at MW-scale thermal input with tritium-compatible heat exchangers. If this milestone is not met by the time HESTIA-Primary is operational, the design should revert to conventional Rankine (33–36% efficiency) and accept higher P_gross requirement (likely pushing the plant to 100+ MWe native scale to maintain net electricity).

---

### 3.3 Tin Corrosion of High-Manganese Steel First Wall

**Verdict**: **Likely resolvable** (but requires validation)

**Rationale**: High-manganese austenitic steel with silicon addition (Tohoku University collaboration) is specifically engineered for liquid metal compatibility. Corrosion-resistant oxide coatings and porous titanium layers are design features, not afterthoughts.

**What would retire this risk**: GALOP test results showing <0.2 mm/year corrosion rate over 1000+ hour campaigns with prototypical tin-indium-lithium alloy flow. If validated, blanket module lifetimes of 5+ years are plausible, and the integrated blanket/divertor architecture is a genuine cost advantage.

---

### 3.4 WISE Conductor Manufacturing Yield at Multi-Kilometer Scale

**Verdict**: **Likely resolvable**

**Rationale**: The October 2025 demonstration validated 40 kA at 7 T in a >4 m coil with 30-layer REBCO stacking and impregnation. Scaling to multi-hundred-meter continuous helical coils is an engineering challenge (yield, joint elimination, winding precision) but not a physics barrier.

**What would retire this risk**: Helix HARUKA (integrated demonstration device, planned 2026 assembly) successfully winding a full-length helical coil at reactor geometry. If the Sugino Machine custom winding equipment achieves <1 defect per 100 m of continuous winding, WISE conductor cost will track library defaults (REBCO tape + impregnation markup is manageable).

---

### 3.5 Liquid Metal Pump Power Consumption (currently "quite unknown")

**Verdict**: **Genuinely uncertain**

**Rationale**: The AIP paper explicitly states that pump power requirements are unknown. Liquid metal circulation power feeds directly into recirculating power fraction and therefore Q_eng. If MHD-driven pump inefficiency adds 10+ MW wall-plug, Q_eng drops below 2.0 and net electricity margin collapses.

**What would retire this risk**: GALOP test results extrapolated to reactor scale via validated CFD simulations, showing pump power <5 MW for the required blanket flow rate (sufficient for tritium breeding and heat removal). Above 15 MW, the design becomes unviable without re-engineering the blanket flow architecture.

---

## 4. Structural Advantages and Disadvantages

### Advantages vs. Conventional D-T Tokamak

1. **Eliminates divertor system entirely**: $36.6M capital savings at native scale (~4% of direct capital). Liquid metal free-surface first wall integrates divertor function. This is unique among fusion concepts.

2. **No disruption mitigation systems**: Stellarators have no plasma current, therefore no disruptions. Eliminates massive gas injection, vertical stability coils, and runaway electron suppression systems. Saves ~$20–30M in C220105 (structure) and C220110 (remote handling) by reducing design margins.

3. **True steady-state operation, no current drive**: Tokamaks need NBI, ECRH, or LHCD to sustain plasma current in steady-state (tens of MW wall-plug). HESTIA achieves steady-state with ECRH for heating only, not current drive. Saves ~30–50 MW of recirculating power vs. steady-state tokamaks.

4. **No central solenoid**: Frees the central bore, reducing C220103 (magnets) and C220105 (structure). Tokamak solenoids cost $100–300M in CFS-class designs.

5. **Higher capacity factor**: >80% availability target is plausible for stellarators (LHD has demonstrated multi-hour steady-state discharges; scaling to year-long campaigns is engineering, not physics). Pulsed tokamaks achieve 30–50%; quasi-steady advanced tokamaks target 60–70%.

**Quantified advantage**: Summing divertor elimination + disruption margin reduction + solenoid savings yields ~$150–200M capital cost reduction vs. a tokamak of equivalent fusion power. However, this is **more than offset** by the 3D coil complexity premium (see Disadvantages below).

---

### Disadvantages vs. Conventional D-T Tokamak

1. **3D coil complexity drives magnet cost premium**: HESTIA's continuous helical coils require flexible REBCO conductor and specialized winding equipment. Tokamaks use simple toroidal field coils (planar, stackable) and poloidal field coils (circular or D-shaped). The library's stellarator magnet cost is ~2× higher per Tesla-meter than tokamak magnets due to 3D geometry. At HESTIA's 9 T / 7.8 m scale, this adds **~$1.5–2B** to C220103 vs. an equivalent-field tokamak.

2. **Lower power density → larger machine for same P_fus**: HESTIA achieves 70.4 MWe at 7.8 m major radius. Compact tokamaks (CFS SPARC, Tokamak Energy ST80) target 100+ MWe at <2.5 m major radius via 12–20 T fields and higher beta. Larger size increases C220105 (structure), C220106 (vacuum vessel), CAS21 (buildings), and site footprint. At 1 GWe scaling, the stellarator's building cost (CAS21: $968M) is ~3× the compact tokamak equivalent.

3. **Unvalidated high-performance confinement assumptions**: HESTIA assumes H = 1.3 confinement enhancement with "almost no experimental backup." Advanced tokamaks (ITER H-mode baseline H98 = 1.0; SPARC targets H98 ~ 0.7–0.8 with demonstrated I-mode) operate closer to validated scaling. If HESTIA's H = 1.0 (baseline), the plasma must run hotter or denser, risking density limit violations.

4. **sCO2 thermal efficiency undemonstrated at fusion scale**: Conventional tokamaks use Rankine steam cycles at 33–36% efficiency (TRL 8–9 for fusion). HESTIA's 50% sCO2 target is aspirational; current demonstrations achieve 20%. If forced to revert to Rankine, thermal efficiency drops by 30–40%, and the plant requires higher P_fus to maintain P_net.

**Quantified penalty**: The 3D coil premium (~$1.5–2B) and larger building footprint (~$600M excess at 1 GWe scale) add ~$2–2.5B to capital cost vs. a compact tokamak, **exceeding** the savings from eliminated subsystems. The net structural disadvantage is ~$2B capital or ~200 $/MWh LCOE penalty at 1 GWe scale.

---

## 5. Cross-Concept Positioning

### Within the Stellarator Family

HESTIA occupies the **"manufacturing-optimized heliotron"** niche within the stellarator landscape:

- **vs. Planar-Coil Stellarators (Thea Energy, Type One)**: HESTIA trades coil simplicity for better plasma confinement. Planar coils are easier to manufacture but require more coils or larger machine size for equivalent fusion power. HESTIA's continuous helical coils are the opposite bet: harder to wind, but fewer coils and smaller machine if confinement enhancement is validated.

- **vs. Quasi-Isodynamic/Helias Stellarators (Proxima Fusion, Gauss Fusion)**: QI and Helias stellarators achieve intrinsically better neoclassical transport (lower H enhancement required) but need modular 3D coils with complex shapes. HESTIA accepts higher neoclassical transport (mitigated via H = 1.3 enhancement assumption) to enable simpler continuous helical coils. If both concepts validate their physics assumptions, HESTIA has a **manufacturing cost advantage**. If neither does, QI/Helias are safer because their baseline confinement is better.

- **vs. Renaissance Fusion (laser-patterned HTS film)**: Renaissance bets on radically different HTS manufacturing (deposit REBCO film, laser-etch current paths). If successful, Renaissance achieves lowest $/kA-m via mass production. HESTIA's WISE conductor is intermediate risk/reward: more complex than planar winding, simpler than full 3D modular coils, but relies on impregnation process novelty.

**HESTIA's unique value proposition**: The **only** stellarator (and possibly the only fusion concept globally) to eliminate the divertor entirely via an integrated liquid-metal first wall. This is a $40–100M capital savings and removes a major technology risk (tungsten monoblock erosion, remote handling complexity). However, this advantage is offset by the 3D coil complexity premium unless WISE conductor achieves <$30/kA-m at scale.

---

### Broader Fusion Landscape

HESTIA sits in the **"steady-state MFE, medium power density, high technology risk"** cluster:

- **vs. Compact Tokamaks (CFS SPARC, Tokamak Energy)**: Compact tokamaks achieve higher power density (smaller machines, lower capital cost) but face disruption risk, current drive power requirements, and divertor heat flux challenges. HESTIA avoids these risks but pays a ~2× magnet cost premium and requires unvalidated confinement enhancement.

- **vs. Spherical Tokamaks (Tokamak Energy ST80, General Fusion MTF)**: Spherical tokamaks achieve very high beta (compact, low field) but struggle with neutron shielding for the central column and have limited divertor space. HESTIA avoids the central column problem (no solenoid, wide central bore) but has larger footprint.

- **vs. Field-Reversed Configuration (TAE)**: FRC is the only other concept claiming >80% availability via steady-state operation, but FRC lacks confinement validation at fusion-relevant parameters. HESTIA has 25 years of LHD heritage; FRC has <5 years of experimental data at sub-fusion densities.

**HESTIA's market positioning**: If confinement and thermal efficiency are validated, HESTIA becomes the **lowest-risk steady-state MFE concept** (stellarator disruption immunity + LHD heritage). If not validated, it becomes a **$5–10B science project** with non-competitive LCOE. The binary outcome hinges on the HESTIA-Primary prototype.

---

## 6. Modeling Confidence

**Rating: Low**

### Data-Anchored Parameters (4 of 15 major cost drivers)

1. **Geometry (R0, a, B)**: High confidence — AIP paper provides explicit values.
2. **Fusion power and plasma gain (P_fus, Q)**: Medium confidence — stated in paper, but contingent on H = 1.3 assumption.
3. **Net electric power (P_net)**: High confidence — design point value is explicit.
4. **Divertor elimination**: High confidence — paper explicitly states "no separate divertor systems."

### Speculative Parameters (11 of 15)

1. **HTS magnet cost (C220103: $3.08B)**: Library default; no WISE conductor unit cost published. **Uncertainty: ±50%** (could be $2B if REBCO tape production scales, or $5B if 3D winding carries 2× premium).
2. **Blanket cost (C220101: $154M)**: Library default; no per-module or liquid-metal-inventory cost breakdown. **Uncertainty: ±60%** (corrosion-resistant coatings and 3D-printed first walls are expensive; alternative is low-cost if tin-lithium alloy proves benign).
3. **Thermal efficiency (50%)**: Aspirational; demonstrated at 20%. **Binary risk**: below 42%, plant does not reach net electricity.
4. **Confinement enhancement (H = 1.3)**: Unvalidated. **Binary risk**: at H = 1.0, fusion power drops or density exceeds limits, violating design point.
5. **Gyrotron cost (C220104: $100M)**: Library default scaled from ITER 170 GHz; 250 GHz units do not exist. **Uncertainty: ±100%** (could be $50M if mass-produced, or $300M if development premium is high).
6. **Liquid metal pump power**: Stated as "quite unknown" in AIP paper. **Uncertainty: unbounded** (could be negligible <5 MW, or critical >15 MW, collapsing Q_eng).
7. **O&M costs (CAS70: $322M lifetime at 1 GWe)**: Library default; no staffing or maintenance schedule published. **Uncertainty: ±40%** (liquid metal systems may require specialized skills and frequent inspections, or may be low-touch if corrosion is managed).
8. **Blanket module replacement frequency**: Assumed 5+ years; corrosion rate is unvalidated. **Uncertainty: ±3× cost impact** (2-year lifetimes triple O&M; 10-year lifetimes halve it).
9. **sCO2 turbine cost (CAS23: $414M at 1 GWe)**: Library default; no HESTIA-specific quote. **Uncertainty: ±30%** (sCO2 turbines are similar cost to Rankine at scale, but tritium-compatible heat exchangers add unknown markup).
10. **Cryogenic system power (20 K cooling)**: Library default; neutron heating on HTS coils is flagged as a concern in the AIP paper. **Uncertainty: ±50%** (if neutron shielding is insufficient, refrigeration power doubles).
11. **Component lifetimes beyond 6.4 years**: Paper states 6.4-year reactor lifetime but does not specify blanket, gyrotron, or first wall replacement schedules. **Uncertainty: drives O&M, unbounded**.

### Dominant Source of LCOE Uncertainty

**HTS magnet cost (47% of direct capital) combined with confinement enhancement validation** is the dominant uncertainty. If WISE conductor costs $75/kA-m (50% above library default) **and** confinement enhancement is invalidated (requiring 20% larger machine to compensate), overnight capital rises from $86,567/kW (1 GWe NOAK) to ~$130,000/kW, and LCOE exceeds 1400 $/MWh — firmly non-competitive.

Conversely, if WISE conductor achieves $30/kA-m **and** H = 1.3 is validated (enabling 20% smaller machine at same P_fus), overnight capital drops to ~$60,000/kW and LCOE approaches 650 $/MWh — still expensive but within the range of early fission SMRs.

The **±300 $/MWh LCOE swing** from these two parameters alone exceeds the entire contribution of all other cost accounts combined.

---

## 7. What Would Change My Mind

### 7.1 HESTIA-Primary Prototype Achieves H ≥ 1.2 with Steady-State Burn (Change: LCOE estimate becomes credible)

**What to watch**: The AIP paper proposes a $480M (1990s dollars, ~$1B current-year) HESTIA-Primary prototype to validate the optimized heliotron confinement. If this device demonstrates:
- H ≥ 1.2 relative to ISS04 scaling,
- Steady-state burn (multi-hour discharges at fusion-relevant density and temperature),
- Alpha particle confinement ε_α ≥ 80%,

then the full HESTIA physics case is validated, and the LCOE estimate of 915 $/MWh (1 GWe NOAK) becomes **defensible**. Without this, the concept is speculative.

**Timeline**: Helical Fusion's roadmap shows Helix KANATA pilot plant (likely HESTIA-Primary) as a medium-term milestone; no public date. If prototype results are available by 2028–2030, the concept remains on track. Delay beyond 2032 suggests physics validation risk is higher than expected.

---

### 7.2 WISE Conductor Unit Cost Published at <$40/kA-m (Change: magnet cost uncertainty resolves favorably)

**What to watch**: A vendor partnership announcement (e.g., Helical Fusion + Shanghai Superconductor, CFS, or Faraday Factory Japan) quoting WISE conductor at <$40/kA-m for continuous helical winding would validate library defaults and confirm that 3D winding complexity does not carry a prohibitive premium. This would anchor the single largest capital cost item (C220103: $3.08B, 47% of direct capital) and remove the ±50% uncertainty band.

**Counter-signal**: If WISE conductor costs exceed $60/kA-m (50% above library default due to impregnation process complexity or low yield), LCOE rises to ~1100 $/MWh at 1 GWe NOAK, and the concept becomes economically non-viable without major redesign.

---

### 7.3 Oroshhi-2 or Follow-On Demonstrates ≥45% sCO2 Efficiency at MW-Scale (Change: thermal efficiency risk retires)

**What to watch**: NIFS Oroshhi-2 (or a DOE-funded sCO2 pilot project, e.g., Sandia National Labs, Southwest Research Institute) achieving ≥45% thermal efficiency at MW-scale thermal input with tritium-compatible heat exchangers (or a credible proxy). This would close the 2.5× efficiency gap between the current 20 kWe / 20% demonstration and the commercial 50% target.

**Counter-signal**: If Oroshhi-2 achieves only 30–35% efficiency at scale (closer to Rankine), HESTIA must either:
- Revert to conventional Rankine steam cycle (accepting 33–36% efficiency and higher P_gross requirement), or
- Increase P_fus by 30–40% (larger machine, higher field, or validated confinement enhancement),

both of which increase capital cost and LCOE. At 35% efficiency, P_gross = ~87 MWe (vs. 139 MWe at 50%), and with 125 MW recirculating power, **the plant does not reach net electricity** at the current design point.

