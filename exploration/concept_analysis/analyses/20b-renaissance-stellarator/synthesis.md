---
ID: 20b-renaissance-stellarator
Concept: Compact Liquid-Wall HTS Stellarator
Company: Renaissance Fusion
Type: synthesis
Status: draft
Created: 2026-04-29
---

# Synthesis: Compact Liquid-Wall HTS Stellarator (Renaissance Fusion)

## 1. Executive Summary

- **Most important risk**: The ignition target (Q=∞) is ~11× below the Lawson threshold according to ISS04 confinement scaling extrapolated to this geometry — this is a binary risk that determines whether the plant produces net electricity.
- **Most important advantage**: The liquid metal wall eliminates discrete first-wall replacement cycles while achieving 25 MW/m² wall loading (5× higher than solid blanket concepts), potentially reducing both capital cost and maintenance downtime.
- **LCOE ballpark**: 129 $/MWh at baseline assumptions, with a 99–517 $/MWh range driven primarily by laser-patterned magnet cost uncertainty (factor 3–10×). The ignition shortfall is not reflected in this estimate.
- **Confidence verdict**: Low — three compounding uncertainties (magnet manufacturing cost has no analogue, ignition physics is undemonstrated in stellarators, and liquid metal wall has no fusion-relevant demonstration) each independently create order-of-magnitude LCOE uncertainty.

---

## 2. What Matters Most for LCOE

Ranked by elasticity from model sensitivity analysis:

### 1. Plant availability (elasticity: −0.94)
- **Assumed value**: 92% (steady-state stellarator with no disruptions, no pulse cycling)
- **Source**: Inferred from "near-100% duty cycle" company statement; maintenance intervals for liquid metal pumps and heat exchangers are uncharacterized
- **Sensitivity magnitude**: A 10-percentage-point reduction (92% → 82%) increases LCOE by ~9%
- **What would flip the conclusion**: If liquid metal system maintenance requires >1 month/year downtime (reducing availability to ~90% or lower), the LCOE advantage vs. solid-blanket stellarators narrows substantially. Below 85% availability, LCOE exceeds 150 $/MWh even at optimistic magnet cost.

### 2. Coil cost multiplier (r_coil elasticity: +0.76)
- **Assumed value**: Baseline model uses tape-winding cost structure, which does NOT apply to laser-patterned REBCO film
- **Source**: No manufacturing cost data exists for this process. Model scenarios: 0.3× (film cheaper than winding, 99 $/MWh), 1× (placeholder, 129 $/MWh), 10× (first-of-kind premium, 517 $/MWh)
- **Sensitivity magnitude**: Factor-of-10 uncertainty produces 418 $/MWh swing — larger than any other single parameter
- **What would flip the conclusion**: If film deposition scales to industrial throughput at <30% of wound-tape cost, LCOE drops below 100 $/MWh (competitive with advanced fission). If manufacturing yields or rework rates drive cost >5× tape winding, LCOE exceeds 350 $/MWh (uncompetitive even if physics works).

### 3. Construction time (elasticity: +0.54)
- **Assumed value**: 10 years (first-of-kind with novel magnet and liquid metal wall integration)
- **Source**: Engineering judgment; framework default is 8 years
- **Sensitivity magnitude**: Each additional year of construction adds ~5% to LCOE via interest-during-construction
- **What would flip the conclusion**: If laser-patterning manufacturing proves faster than 3D coil winding (construction drops to 6–7 years), LCOE improves by ~15%. If first-plant experience pushes construction beyond 12 years, LCOE exceeds 160 $/MWh at baseline magnet cost.

### 4. Peak coil field (b_max elasticity: +0.38)
- **Assumed value**: 15 T (baseline design target); 20–40 T upper envelope in published paper
- **Source**: Nuclear Fusion 64 (2024) 026007; REBCO Jc degrades sharply above ~20 T at 20 K
- **Sensitivity magnitude**: 15 T → 40 T increases LCOE by 64% (129 → 211 $/MWh) due to larger coil cross-section needed at reduced Jc
- **What would flip the conclusion**: If QI optimization at compact A≈4 geometry requires >25 T peak field to achieve acceptable confinement, LCOE rises above 180 $/MWh. If 15 T proves sufficient, this risk is non-binding.

### 5. Thermal cycle efficiency (eta_th elasticity: −0.11)
- **Assumed value**: 50% (midpoint of 49–51% sCO₂ Brayton-Rankine combined cycle)
- **Source**: Energy Conversion and Management 276 (2023) 116572; genetic algorithm optimization
- **Sensitivity magnitude**: 15-percentage-point premium vs. steam Rankine (~35%), but elasticity is only −0.11 — a 5-point degradation (50% → 45%) increases LCOE by just ~5%
- **What would flip the conclusion**: Even if sCO₂ cycle fails and the plant falls back to steam Rankine (35% efficiency), LCOE increases by ~17 $/MWh to ~146 $/MWh at baseline magnet cost. This is a significant penalty but does not dominate the uncertainty range. The sCO₂ cycle is a favorable feature, not a load-bearing assumption.

---

## 3. Risk Verdicts

### Laser-patterned HTS film manufacturing cost
- **Verdict**: Genuinely uncertain
- **Rationale**: A 6 T Helmholtz demonstration validates the physics, but no production-scale cost data exists for thin-film REBCO deposition on 1 m cylinders at nuclear-grade quality.
- **What would retire this risk**: Public disclosure of film deposition throughput (m²/day), yield rates, and rework protocols from Renaissance Fusion's manufacturing scale-up program; or independent cost benchmarking from semiconductor/photovoltaic CVD industry with fusion-specific quality adjustments.

### Ignition (Q=∞) at compact stellarator geometry
- **Verdict**: Unlikely resolvable without intermediate experimental validation
- **Rationale**: ISS04 confinement scaling predicts n·τ_E ~11× below Lawson ignition threshold at the published 10 keV, R=4 m, A=4, B=10 T design point. The design likely requires either (a) higher operating temperature (20–30 keV), (b) confinement improvement beyond ISS04 from high-field QI optimization, or (c) larger plasma volume than the 200 m³ estimate. None of these assumptions have experimental support in compact stellarators.
- **What would retire this risk**: Demonstration of n·τ_E ≥ 3×10²⁰ m⁻³·s in a compact (A≤5) stellarator at fusion-relevant temperature (>5 keV), or validated physics-based design code showing QI confinement enhancement sufficient to close the 11× gap. Without this, the concept carries binary technical risk.

### Liquid Li-LiH wall at 25 MW/m² and 10 T
- **Verdict**: Likely resolvable with targeted R&D
- **Rationale**: Liquid lithium walls have been tested at small scale (NSTX, DIII-D LiMIT) and Pb-17Li MHD is well-characterized from EU-DEMO blanket programs. The specific Li-LiH mixture and 25 MW/m² loading are undemonstrated, but the underlying MHD and tritium extraction physics are tractable.
- **What would retire this risk**: Engineering demonstration of Li-LiH flow stability at 10 MW/m² wall loading and 5+ Tesla field in a curved-surface test facility; validated MHD pressure drop correlations showing pump power <500 MW at design conditions; tritium extraction from Li-LiH at kg/day rates with <1% holdup.

### sCO₂ Brayton-Rankine combined cycle at 49–51% efficiency
- **Verdict**: Likely resolvable
- **Rationale**: sCO₂ Brayton cycles are demonstrated at 10 MW scale (Sandia, Echogen) and the Brayton-Rankine combined architecture is established in gas turbine plants. GW-scale fusion integration is unproven, but this is primarily a commercial engineering challenge, not fundamental physics uncertainty.
- **What would retire this risk**: Demonstration of sCO₂ Brayton at 100+ MW scale with liquid metal heat source achieving >47% cycle efficiency; or publication of detailed turbomachinery cost estimates from industrial sCO₂ vendors (GE, Siemens, Echogen) for fusion BOP applications.

### Tritium breeding ratio (TBR = 1.60 claimed)
- **Verdict**: Likely resolvable (analytically verified, needs experimental confirmation)
- **Rationale**: JNM 599 (2024) §Case study reports TBR = 1.60 for the optimized 10 cm Pb + 22 cm Li-LiH configuration from neutron transport calculations, with 39% margin above the 1.15 design requirement. This is analytically sound but undemonstrated at fusion-relevant neutron flux.
- **What would retire this risk**: Prototypical blanket mock-up irradiation in a 14 MeV neutron source (e.g., IFMIF-DONES) confirming TBR within ±10% of prediction; or validated neutronics code benchmarking against experimental tritium production data from Pb-17Li test blanket modules in ITER.

---

## 4. Structural Advantages and Disadvantages

Comparison against conventional D-T tokamak baseline (e.g., SPARC/ARC-class):

### Eliminated cost items (advantages):
- **Central solenoid (CS) and current drive system**: Stellarators have no CS and require no current drive at steady state. Eliminates ~5–8% of tokamak reactor plant equipment cost (CAS220104 and associated power supplies). Estimated savings: ~$200–400M at 1 GWe scale.
- **Disruption mitigation and protection systems**: No plasma disruptions in stellarators. Eliminates disruption detection, mitigation coils, and structural reinforcement. Estimated savings: ~$50–150M.
- **Discrete first-wall replacement cycles**: Liquid metal wall is self-renewing. Eliminates remote handling for segmented first-wall module replacement (though pumps and heat exchangers still require maintenance). Estimated O&M savings: ~1–2 percentage points of availability (worth ~$10–20M/year in revenue at 1 GWe).

**Quantified capital cost advantage**: ~$250–550M (5–10% of overnight cost) relative to a tokamak of equivalent fusion power.

### Added cost items (disadvantages):
- **3D non-planar stellarator coil geometry**: Modular stellarator coils are more complex to manufacture than axisymmetric tokamak TF coils. However, Renaissance Fusion's laser-patterned cylinder approach may REVERSE this penalty if film deposition proves cheaper than winding complex 3D shapes. Cost impact: uncertain (could be +$500M to −$500M depending on manufacturing realization).
- **Liquid metal circulation system at 25 MW/m²**: LM pumps, heat exchangers, tritium extraction, and MHD-conditioning piping replace solid blanket cooling loops. The model assumes $400M for this system (Na-cooled fast reactor analogy), but uncertainty is factor 2–3×. Cost impact: +$200–800M vs. solid HCPB blanket baseline (~$200M for ARIES-CS).
- **Large recirculating power (471 MW estimated)**: Net efficiency is only 34% despite 50% thermal cycle efficiency. Liquid metal pumps consume ~380 MW (inferred; not disclosed), driving up turbine plant sizing requirements. Cost impact: +$100–200M in gross electrical capacity.

**Net structural position**: Potentially favorable if laser-patterning proves cost-effective (net −$200M) or unfavorable if magnet and LM wall costs compound (net +$700M). The uncertainty range spans both sides of zero.

---

## 5. Cross-Concept Positioning

Renaissance Fusion occupies a unique position in the stellarator landscape:

- **Compact high-field stellarators**: Proxima Fusion (09-qi-stellarator-hts) and Type One Energy (20a-type-one-stellarator) also pursue HTS stellarators, but use wound REBCO tape in 3D coils and target burning plasma (Q ~ 5–10) rather than ignition. Renaissance Fusion's ignition target eliminates steady-state heating cost but introduces binary physics risk. The laser-patterning approach is entirely unique.

- **Liquid metal blanket concepts**: Multiple tokamak and mirror concepts explore liquid Pb-17Li or Li blankets (Helical Fusion, some FRC variants), but Renaissance Fusion's flowing plasma-facing wall at 25 MW/m² is the most aggressive implementation. The consolidation of first wall + breeder + coolant into a single fluid circuit is architecturally distinct.

- **Advanced power cycles**: The sCO₂ Brayton-Rankine combined cycle (50% efficiency) is shared with Helical Fusion (36) and several advanced fission concepts. This puts Renaissance Fusion in the upper efficiency tier but does not uniquely differentiate it — thermal cycle efficiency has low LCOE elasticity (−0.11).

**Differentiation summary**: Renaissance Fusion combines the highest number of novel elements in a single concept (laser-patterned magnets, flowing liquid wall, ignition target, sCO₂ cycle) among all stellarators in this survey. This creates potential for compounding cost savings if all innovations succeed, or compounding risk if any fail. No other concept has this high a ratio of novel-to-borrowed subsystems.

**Economic positioning**: At optimistic magnet cost (0.3× tape-winding analogue) and demonstrated ignition, LCOE could reach 99 $/MWh — competitive with Proxima Fusion's best case and below most tokamak projections. At pessimistic magnet cost (10×) or ignition failure, LCOE exceeds 500 $/MWh or the plant produces zero net electricity. The range is the widest in the stellarator family.

---

## 6. Modeling Confidence

**Rating: Low**

### Data-anchored parameters (10 of 28 LCOE-critical inputs):
- Net electrical output (1 GWe)
- Thermal cycle efficiency (50%)
- Net plant efficiency (34%)
- Major radius (≤4 m)
- Toroidal field (10 T nominal)
- Wall loading (25 MW/m²)
- Radial build dimensions
- Operation mode (steady-state)
- Startup heating approach (NNBI)
- Magnet operating temperature (20 K)

### Speculative or weakly-anchored parameters (18 of 28):
- Magnet system capital cost (no analogue; factor 3–10× uncertainty)
- Liquid metal wall system cost (Na-cooled fast reactor analogy; factor 2–3× uncertainty)
- Plasma confinement time (ISS04 scaling predicts ignition shortfall; unverified at this geometry)
- Recirculating power breakdown (p_pump = 380 MW inferred, not disclosed)
- Availability / maintenance intervals (92% assumed; liquid metal system MTBF unknown)
- Component replacement schedules
- O&M costs
- Divertor design (not addressed in any source)
- Plasma density and bootstrap fraction (not published)
- Construction time (10 years estimated; first-of-kind uncertainty)
- TBR (1.60 analytically verified but not demonstrated)
- Tritium extraction rates from Li-LiH
- sCO₂ turbomachinery cost at GW scale
- Cryogenic refrigeration power at 20 K
- Li-6 enrichment requirements (baseline uses non-enriched, but optimization unclear)
- REBCO film Jc at peak fields 20–40 T
- MHD pressure drop in Li-LiH flow
- Long-term Li-LiH corrosion of RAFM steels

### Dominant source of LCOE uncertainty:
**Laser-patterned HTS film manufacturing cost.** With elasticity +0.76, the magnet cost multiplier produces a 418 $/MWh swing across the 0.3–10× scenario range — three times larger than the next-largest lever (construction time, 61 $/MWh swing across 6–12 years). The ignition shortfall is a separate binary risk: if the plasma does not ignite, LCOE is undefined (zero net electricity). These two uncertainties compound: even if magnet cost lands at the optimistic 0.3× scenario, an ignition shortfall makes the 99 $/MWh estimate meaningless.

**Secondary uncertainty**: Liquid metal wall system cost and maintenance. Factor 2–3× cost uncertainty (~±$200–400M) and uncharacterized availability impact create ~±20 $/MWh LCOE uncertainty independent of the magnet cost.

**Modeling approach limitation**: The baseline model (129 $/MWh) assumes ignition is achieved. The ISS04 confinement analysis shows this assumption is not supported by stellarator scaling laws extrapolated to this geometry. A risk-weighted LCOE (probability-weighted over ignition success/failure scenarios) would be substantially higher, but estimating the probability of ignition success requires physics expertise beyond the scope of this economic synthesis.

---

## 7. What Would Change My Mind

### In the optimistic direction (toward LCOE <100 $/MWh):

1. **Renaissance Fusion publishes film deposition cost data showing <$10M per stellarator field period at production scale.** If laser patterning proves 3–5× cheaper than winding complex 3D coils (rather than 3–10× more expensive), the magnet cost advantage alone would reduce LCOE to ~90 $/MWh even if other parameters remain at baseline.

2. **Independent stellarator confinement modeling validates n·τ_E ≥ 3×10²⁰ m⁻³·s at the published geometry via QI optimization at 10 T.** If a credible physics design code (STELLOPT, VMEC, or equivalent) demonstrates ignition closure without requiring >25 T peak field or >30 keV operating temperature, the binary physics risk is retired and the economic case depends primarily on manufacturing execution.

3. **Liquid metal wall demonstration at 10 MW/m² and 5 T with pump power <200 MW confirms MHD pressure drop models.** If the inferred 380 MW pump power proves conservative and actual circulation requires <200 MW, net efficiency improves to ~38%, reducing required thermal capacity and lowering LCOE by ~10 $/MWh.

### In the pessimistic direction (toward LCOE >200 $/MWh or technical infeasibility):

1. **Film deposition at 1 m cylinder scale shows <50% yield or requires extensive rework.** If manufacturing quality control drives effective film cost >5× the tape-winding analogue, LCOE exceeds 350 $/MWh even at optimistic availability. Above 10× tape cost, LCOE approaches 500 $/MWh and the concept is economically uncompetitive regardless of physics success.

2. **Compact stellarator experimental program (e.g., a next-generation A<5 device) demonstrates confinement degradation at high field.** If empirical data shows ISS04 scaling breaks down unfavorably in the compact high-field regime, the 11× ignition shortfall widens further and the concept requires either unaffordable machine growth (R → 6–8 m, cost +50–100%) or abandonment of the ignition target (adding 50–100 MW steady-state heating, reducing Q_eng and increasing LCOE by 15–25 $/MWh).

3. **Li-LiH corrosion or tritium permeation rates prove incompatible with RAFM steels at operating temperature.** If the liquid metal wall requires exotic refractory alloys (e.g., W-based) or double-wall heat exchangers with permeation barriers, capital cost increases by $300–500M and LCOE rises by 25–40 $/MWh.

---

## 8. LCOE Downselect Scoring

### C1: Modularization

Renaissance Fusion's approach creates a sharp divergence: the liquid metal wall and laser-patterned magnets are intrinsically modular manufacturing processes, but stellarator geometry complexity and first-of-kind integration reduce site-level modularity.

**Sub-factor breakdown by CAS account:**

| CAS Account | Construction Mode | Score | Justification |
|-------------|------------------|-------|---------------|
| CAS21 (Buildings) | Stick-built | 1 | Stellarator reactor building is geometrically complex due to non-planar coil envelope; no factory prefabrication |
| CAS220101 (First Wall / Blanket) | Factory-manufactured module | 5 | Liquid metal wall system components (pumps, heat exchangers, piping) are industrial equipment manufacturable in factories; tritium extraction modules are skid-mounted |
| CAS220102 (Shield) | Site-assembled from factory sub-assemblies | 3 | VH₂ + concrete bioshield is site-poured; VH₂ vessels may be prefabricated |
| CAS220103 (Magnets) | Factory-manufactured module | 5 | Laser-patterned HTS cylinders are deposited in a controlled factory environment; each cylinder is a standalone module transported to site |
| CAS220104 (Current Drive) | N/A | 5 | Stellarator has no current drive system |
| CAS220105 (NNBI - startup only) | Factory-manufactured module | 5 | NNBI systems are factory-assembled (ITER precedent); startup-only duty cycle reduces complexity |
| CAS220200 (Divertor) | Site-assembled | 3 | No divertor design published; stellarator island divertors are typically site-installed |
| CAS220300 (Vacuum Vessel) | Site-assembled | 3 | Complex 3D stellarator vacuum vessel geometry requires site assembly |
| CAS22040X (Thermal Shields) | Factory-manufactured module | 5 | Cryogenic shields are modular; 20 K HTS reduces shield count vs. 4 K LTS |
| CAS22050X (Cryogenics) | Factory-manufactured module | 5 | Helium refrigeration plants are industrial equipment; standard commercial units |
| CAS220600 (Power Supplies) | Factory-manufactured module | 5 | DC power supplies for HTS are commercial equipment |
| CAS23 (Turbine Plant) | Factory-manufactured module | 5 | sCO₂ turbomachinery will be factory-manufactured (emerging industrial product) |
| CAS24 (Electrical) | Factory-manufactured module | 5 | Standard industrial electrical equipment |
| CAS26 (Heat Rejection) | Factory-manufactured module | 5 | Cooling towers and auxiliary cooling are commercial products |

**Cost-weighted average (using baseline CAS values from model output):**
- CAS21 (1 × $660M) = 660
- CAS220101 (5 × $400M) = 2000
- CAS220102 (3 × $184M) = 552
- CAS220103 (5 × $2262M) = 11310
- CAS220104 (5 × $0M) = 0
- CAS220105 (5 × $9M) = 45
- CAS220200 (3 × $203M) = 609
- CAS220300 (3 × $226M) = 678
- CAS22040X (5 × $6M) = 30
- CAS22050X (5 × $120M) = 600
- CAS220600 (5 × $12M) = 60
- CAS23 (5 × $232M) = 1160
- CAS24 (5 × $126M) = 630
- CAS26 (5 × $66M) = 330

**Total weighted**: 18664 / **Total cost**: 4897 M$ → **Base score**: 3.81

**Module repetition boost**: The liquid metal wall circuit has ~50–100 identical pump modules, heat exchanger modules, and tritium extraction skids (estimated from system scale). The HTS cylinders number ~20–40 (stellarator field period count × coil types; not published but typical for modular stellarators). Applying +1.0 boost for 10–49 identical modules per subsystem:

**C1 = 3.81 + 1.0 = 4.81, clamped to [1, 5] → 4.8**

**Justification**: The laser-patterned magnet cylinders and liquid metal system components are intrinsically factory-manufacturable, and the stellarator's steady-state operation eliminates pulsed power equipment. However, the 3D vacuum vessel and reactor building are site-constructed. The module repetition boost reflects the high count of identical LM wall components. This score is higher than conventional wound-coil stellarators (which score ~3.0–3.5 due to unique 3D coil geometries) but lower than fully modular mirror or FRC concepts (which can achieve 4.5–5.0).

---

### C3: Supply Chain Learning

**Sub-factor A: Component learning rates (cost-weighted average across CAS)**

| CAS Account | Learning Category | Score | Weight (M$) | Justification |
|-------------|------------------|-------|-------------|---------------|
| CAS21 | Specialty (limited existing supply chain) | 3 | 660 | Fusion reactor buildings are specialty construction but draw on nuclear/industrial precedent |
| CAS220101 | Fusion-specific (no current market) | 2 | 400 | Flowing liquid Li-LiH wall at 25 MW/m² has no commercial or research analogue at scale |
| CAS220102 | Specialty | 3 | 184 | VH₂ + concrete shielding uses established materials; VH₂ production is limited but growing (hydrogen economy) |
| CAS220103 | Fusion-specific | 2 | 2262 | Laser-patterned REBCO film on 1 m cylinders has never been manufactured beyond lab scale; deposition equipment is specialty |
| CAS220105 | Industrial (growing production base) | 4 | 9 | NNBI systems leverage ITER development; negative ion sources are specialty but established |
| CAS220200 | Fusion-specific | 2 | 203 | Stellarator divertors are research-phase; no commercial manufacturing |
| CAS220300 | Specialty | 3 | 226 | Complex 3D vacuum vessels are specialty but draw on pressure vessel industry |
| CAS22040X | Industrial | 4 | 6 | Cryogenic thermal shields are commercial products for LNG, aerospace |
| CAS22050X | Industrial | 4 | 120 | Helium refrigeration plants are commercial (though 20 K scale-up required) |
| CAS220600 | Commodity | 5 | 12 | DC power supplies are industrial products |
| CAS23 | Industrial (emerging) | 4 | 232 | sCO₂ turbomachinery is pre-commercial but industrial development is active (GE, Siemens, Echogen) |
| CAS24 | Commodity | 5 | 126 | Standard electrical plant equipment |
| CAS26 | Commodity | 5 | 66 | Cooling towers are commodity infrastructure |

**Weighted average**: (3×660 + 2×400 + 3×184 + 2×2262 + 4×9 + 2×203 + 3×226 + 4×6 + 4×120 + 5×12 + 4×232 + 5×126 + 5×66) / 4906 = **2.72**

**Sub-factor B: Supply chain bottleneck count**

Starting at 5.0:
- **Hard constraint (no known path to required quantity)**: None identified
- **Scaling constraint (exists but must scale 10×+)**:
  - REBCO film deposition equipment capacity (−0.5): Current global REBCO film production is research-scale; GW-scale fusion deployment requires 100–1000× throughput increase
  - Li-6 enrichment capacity (−0.5): Global capacity is ~100 kg/year (legacy Russian + Chinese); a fleet of 10 plants at 1 GWe each requires ~500–1000 kg/year Li-6 (estimated from blanket inventory + makeup). However, baseline design uses NON-ENRICHED Li-LiH and achieves TBR = 1.60, so enrichment is optional — downgrading this to −0.25
  - sCO₂ turbomachinery at GW scale (−0.25): Currently demonstrated at 10 MW; 100× scale-up required
- **Sole-source dependency**: None (liquid metal and Pb are globally sourced; REBCO deposition equipment is specialty but not sole-source)
- **He-3 fuel dependency**: Not applicable (D-T fuel)

**Sub-factor B = 5.0 − 0.5 − 0.25 − 0.25 = 4.0**

**Sub-factor C: External demand pull**

Estimating capital cost fraction with >$1B/year external market:
- Buildings (13.5%): General construction — YES
- Liquid metal wall ($400M, 8%): Industrial pumps and heat exchangers — PARTIAL (50% of component cost has external market in chemical processing; Li-LiH-specific elements do not) → 4% counts
- Shield (3.8%): Concrete, VH₂ vessels — PARTIAL (concrete yes, VH₂ emerging) → 2% counts
- Magnets (46%): REBCO film deposition — NO (fusion-specific at this scale)
- Divertor (4%): Fusion-specific — NO
- Vacuum vessel (5%): Pressure vessel industry — PARTIAL (complex geometry is specialty) → 2% counts
- Thermal shields (0.1%): Cryogenic equipment — YES
- Cryogenics (2.4%): Helium refrigeration — YES
- Power supplies (0.2%): Industrial equipment — YES
- Turbine plant (4.7%): sCO₂ turbomachinery — EMERGING (not yet >$1B/year but industrial development active; count 50%) → 2.4% counts
- Electrical plant (2.6%): Industrial equipment — YES
- Heat rejection (1.3%): Cooling towers — YES

**Total with external demand**: 13.5% + 4% + 2% + 0.1% + 2.4% + 0.2% + 2.4% + 2.6% + 1.3% = **28.5%**

This is in the 20–40% range → **Sub-factor C = 3**

**C3 = (2.72 + 4.0 + 3.0) / 3 = 3.24 → 3.2**

**Justification**: The magnet system (46% of capital) has no external market and requires novel manufacturing scale-up. The liquid metal wall (8%) is fusion-specific. However, the sCO₂ power cycle, cryogenics, and conventional BOP benefit from external industrial development. Supply chain scaling constraints are moderate (REBCO film deposition and sCO₂ turbomachinery are emerging technologies, not absent). Li-6 enrichment is optional for the baseline design. The score reflects significant fusion-specific manufacturing challenges but not insurmountable bottlenecks.

---

### C4: Plant Complexity

**Sub-factor A: Operational coupling density**

The liquid metal wall creates a tightly coupled thermal-hydraulic system, but stellarator steady-state operation eliminates pulse-cycle coupling:

- **Liquid metal circulation loop**: Pump failure stops wall cooling and forces plasma shutdown within minutes (tight coupling). However, the LM system has ~50+ parallel pump modules — partial failures degrade performance but do not cascade to full shutdown. Heat exchanger fouling degrades thermal performance gradually (graceful degradation, not cascade failure).

- **Cryogenic system**: HTS at 20 K can tolerate 5–10 K temperature excursions without quenching (unlike LTS at 4 K, which quenches on <1 K rise). Warm-up time constants are hours. Cryo failure forces magnet de-energization but does not cascade to vacuum vessel breach or structural damage.

- **Tritium extraction**: Failure increases Li circuit tritium inventory but does not immediately stop plasma operation. Allows controlled shutdown over days (not minutes).

- **Power conversion**: sCO₂ turbine trip dumps heat to bypass but does not cascade to plasma disruption (stellarators have no disruptions). Plasma can be maintained in low-power mode during turbine restart.

- **Vacuum vessel**: Stellarator vacuum vessel has no fast transients (no disruptions, no vertical displacement events). Leak detection and isolation are on hour-to-day timescales.

**Overall coupling assessment**: Moderate coupling density. LM pump failure is the tightest coupling (minutes to forced shutdown), but the parallel-module architecture limits cascade scope. The absence of disruptions, vertical control, and current-drive interdependencies significantly reduces coupling vs. tokamaks. Cryo system tolerance is higher than LTS concepts. Compared to IFE (which has highly decoupled driver + target + chamber systems), this is more coupled; compared to tokamaks (disruption mitigation + vertical control + current drive feedback), this is less coupled.

**Sub-factor A = 4** (mostly decoupled; few critical interdependencies)

**Sub-factor B: Subsystem count (CAS22 sub-accounts >1% of total capital)**

From model output, CAS22 sub-accounts >1% of total capital ($108.5M threshold at $10.85B total):
1. C220101 (Liquid metal wall): $400M (3.7%)
2. C220102 (Shield): $184M (1.7%)
3. C220103 (Magnets): $2262M (20.8%)
4. C220106 (Supplementary heating - NNBI): $34M (0.3%) — below threshold
5. C220107 (Primary structure): $106M (0.98%) — borderline; exclude
6. C220108 (Vacuum vessel): $104M (0.96%) — borderline; exclude
7. C220110 (Power supplies): $184M (1.7%)
8. C220111 (Divertor): $416M (3.8%)
9. C220200 (Assembly): $203M (1.9%)
10. C220300 (Maintenance): $226M (2.1%)
11. C220500 (Cryogenics): $120M (1.1%)

**Count**: 9 significant subsystems (above the strict >1% threshold; two borderline items excluded)

**Sub-factor B = 3** (8–10 significant subsystems)

**C4 = (4 + 3) / 2 = 3.5**

**Justification**: Stellarator steady-state operation and the liquid metal wall's parallel-module architecture reduce operational coupling compared to tokamaks. The "magic wand" test is decisive: if ignition were proven tomorrow, the plant has moderate complexity (9 major subsystems, LM pump coupling is tightest failure mode) but is operationally simpler than a tokamak (no disruptions, no current drive, no vertical control). The subsystem count is in the mid-range for MFE concepts.

---

### C5: Customization Needs

**Sub-factor A: Thermal rejection**

Renaissance Fusion uses a conventional sCO₂ Brayton-Rankine thermal cycle rejecting ~1.5 GWth waste heat (from 2.9 GWth fusion thermal at 50% cycle efficiency). This requires large cooling towers, comparable to any other thermal power plant.

**Sub-factor A = 2** (large cooling towers required; standard thermal cycle)

**Sub-factor B: Fuel safety profile**

D-T fuel with full tritium breeding infrastructure and handling.

**Sub-factor B = 1** (D-T: tritium handling and breeding)

**Raw C5 = (2 + 1) / 2 = 1.5**

**Scaled to [1, 5]: C5 = 1 + (1.5 − 1) × (4/3) = 1 + 0.67 = 1.67 → 1.7**

**Justification**: The concept has no site-specific advantages — it requires full D-T tritium infrastructure and conventional large-scale thermal rejection. The liquid metal wall does not reduce cooling tower size (the sCO₂ cycle still rejects 1.5 GWth). This score is identical to all D-T thermal fusion concepts and reflects the intrinsic fuel and thermal cycle constraints.

---

### C8: Data Adequacy

**Sub-factor A: Source diversity & independence**

- **Company publications**: 3 peer-reviewed papers (Nuclear Fusion 2024, JNM 2024, ECM 2023) covering design point, blanket, and power cycle
- **Independent validation**: No third-party stellarator cost study addresses laser-patterned magnets or liquid metal walls. ARIES-CS provides stellarator plant analogy but uses wound coils and solid blanket.
- **Public-domain architecture literature**: UC Berkeley seminar and MT29 abstract provide hardware validation (6 T Helmholtz demo). No independent academic analysis of Renaissance Fusion's specific design.

**Sub-factor A = 3** (Primarily company publications with peer review; no independent validation of the integrated concept)

**Sub-factor B: Reactor design specification**

From the three peer-reviewed papers:
- **Geometry and plasma**: R≤4 m, A~4, B=10 T, D-T at 10 keV, Q=∞ — specified
- **Magnets**: Laser-patterned HTS at 20 K, 15 T peak (baseline) to 40 T (upper envelope) — specified but manufacturing details absent
- **Blanket**: 15 cm Pb + 18 cm Li-LiH radial build, 25 MW/m² wall loading, TBR=1.60, mn=1.07 — specified
- **Power cycle**: sCO₂ Brayton-Rankine, 49–51% efficiency, 34% net — specified
- **Gaps**: No divertor design, no vacuum vessel design, no maintenance system design, no remote handling architecture, no specific pump/heat exchanger sizing, no cryogenic system specification

**Sub-factor B = 3** (Partial design with key subsystems defined but gaps in integration — divertor, maintenance, and detailed engineering missing)

**Sub-factor C: LCOE parameter coverage (based on blocking gap count from gap_report.md)**

From gap_report.md, blocking gaps:
1. Capital cost by subsystem (truly-unknown)
2. Magnet system capital cost (truly-unknown)
3. Liquid metal wall system cost (truly-unknown)
4. Liquid metal circulation pump power (proprietary / truly-unknown)
5. Total plant overnight cost (proprietary)
6. Laser-patterned HTS for 3D stellarator field (proprietary)
7. REBCO film deposition capacity (truly-unknown)

**Blocking gap count: 7**

Per framework: 5–7 blocking gaps → **Sub-factor C = 2**

**Sub-factor D: Commercialization pathway clarity**

Renaissance Fusion has disclosed:
- Hardware milestones: 6 T Helmholtz demo completed (2024)
- Public target: 1 GWe pilot plant by 2030s (from company website; timeline not detailed)
- Funding: Undisclosed (private company)
- Intermediate steps: No published roadmap for compact stellarator demonstration device between Helmholtz demo and pilot plant

**Sub-factor D = 2** (Vague commercialization narrative — pilot plant target stated but no detailed pathway, milestones, or intermediate experimental program)

**C8 = (3 + 3 + 2 + 2) / 4 = 2.5**

**Justification**: The three peer-reviewed papers provide unusually strong technical documentation for a private fusion company, but economic data is entirely absent (zero published cost estimates, despite "economically optimized design point" paper title). The 7 blocking gaps reflect the unanchored capital cost model. Commercialization pathway lacks detail beyond the pilot plant target. The score reflects good physics/engineering disclosure but poor economic and programmatic transparency.

---

### C7: Technical Risk Evidence (Risk Matrix)

The risk matrix below assesses 7 functions × 2 subcategories (physics and hardware) = 14 cells.

#### **Function 1: Plasma Performance**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | n·τ_E ≥ 3.1×10²⁰ m⁻³·s at T=10 keV for ignition (Lawson criterion); compact QI stellarator at A=4, B=10 T must achieve confinement quality sufficient for Q=∞ | W7-X: n·τ_E ~ 10¹⁹ m⁻³·s at T ~ 3 keV, A=10, B=2.5 T (not fusion-relevant); ISS04 scaling extrapolated to Renaissance geometry predicts n·τ_E ~ 2.7×10¹⁹ m⁻³·s — 11× below Lawson threshold | 11× gap (confinement time shortfall) | QI optimization at high field (10 T) and compact aspect ratio (A=4) claimed to exceed ISS04 scaling; alpha heating self-organization may improve confinement; or higher operating temperature (20–30 keV) where <σv> peaks | **Binary** | **2** (Simulation only — QI optimization codes exist but no experimental validation at compact A=4 high-field conditions) |
| **Hardware** | Plasma-facing liquid Li-LiH wall must maintain stable free surface or confined film at 25 MW/m² wall loading under 10 T stellarator field without degrading confinement via MHD-driven flow perturbations or impurity contamination | NSTX LiMIT limiter: liquid Li at <1 MW/m² in tokamak geometry; DIII-D: flowing Li divertor at <5 MW/m² | 5–25× wall loading gap; 3–10× field strength gap | MHD flow conditioning (shaping flow velocity profile to minimize plasma interaction); LiH additive stabilizes Li chemistry and raises melting point; neutron heating drives natural convection assisting flow | **Binary** | **2** (No fusion-relevant demonstration; MHD modeling exists but experimental validation at 10 MW/m² + 5 T scale is absent) |

**Function 1 mean (before heritage)**: (2 + 2) / 2 = **2.0**

---

#### **Function 2: Driver / Energy Input**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | NNBI at 60% neutralization efficiency sufficient for plasma ramp-up to ignition; startup-only duty cycle (not continuous) | ITER NNBI program: 1 MeV D⁻ beams at 50–60% neutralization efficiency demonstrated in test facilities (ELISE, SPIDER) | ~1× (ITER NNBI target matches requirement) | ITER-class NNBI adapted to stellarator beam port geometry; startup-only operation reduces lifetime fluence vs. continuous heating | **Degrading** | **4** (Near-regime demonstrated — ITER NNBI at 1 MeV and 60% neutralization is validated in test facilities; stellarator geometry adaptation is incremental) |
| **Hardware** | NNBI injectors, power supplies, and neutralizer must survive startup thermal/mechanical cycling over 30-year plant life; beam port access in compact A=4 stellarator geometry | ITER NNBI injectors are in late engineering (not yet operated at full spec in ITER); JT-60SA positive NBI operated at multi-MW scale | N/A (incremental development from ITER program) | ITER NNBI hardware adapted for startup-only duty cycle (reduced fluence, intermittent operation may reduce degradation vs. continuous heating) | **Degrading** | **4** (ITER NNBI hardware is late-stage development; startup-only operation is lower risk than continuous; stellarator beam port access is design challenge but not fundamental barrier) |

**Function 2 mean (before heritage)**: (4 + 4) / 2 = **4.0**

---

#### **Function 3: Instability Control**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | Compact QI stellarator at A=4 must maintain quasi-isodynamic field optimization to suppress neoclassical transport and avoid MHD instabilities at β ~ 1.4% (design point); ignited plasma must be alpha-particle-stable | W7-X: QI optimization validated at A=10, β <1%, non-burning plasma; no stellarator has operated with significant alpha heating | ~2× aspect ratio extrapolation; no alpha-heating validation | 3D MHD equilibrium codes (VMEC, STELLOPT) predict QI stability at compact geometry; compact A=4 has less geometric flexibility for QI optimization than W7-X A=10, but higher field (10 T vs. 2.5 T) provides stabilization margin | **Binary** | **3** (Subscale demonstration — W7-X proves QI works at A=10 but compact A=4 extrapolation is unvalidated; alpha stability has no experimental basis in any stellarator) |
| **Hardware** | 3D magnetic field coils (laser-patterned HTS cylinders) must maintain field precision <1 mm RMS to preserve QI confinement quality; manufacturing tolerances and thermal/mechanical deformation under neutron irradiation must not degrade field | MT29 Helmholtz demo: 6 T peak field at 1.2 m diameter validates laser patterning works; no demonstration of 3D stellarator field accuracy or neutron environment performance | N/A (Helmholtz is proof-of-principle, not stellarator field) | Laser patterning claimed to achieve <100 μm current path precision; cylinder substrate dimensional stability under cryogenic cycling and neutron displacement damage (RAFM or composite substrates) | **Binary** | **3** (Partial demonstration — Helmholtz validates laser patterning physics; stellarator 3D field accuracy and neutron-induced distortion are undemonstrated) |

**Function 3 mean (before heritage)**: (3 + 3) / 2 = **3.0**

---

#### **Function 4: Plasma-Wall Interaction**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | Plasma exhaust solution must handle 25 MW/m² steady-state heat flux without excessive impurity contamination; divertor or liquid wall must maintain Z_eff <2.0 for acceptable fusion reactivity | W7-X island divertor: ~10 MW/m² peak heat flux in short pulses; liquid Li walls (NSTX): demonstrated low recycling but impurity control at high flux is uncertain | 2.5× heat flux gap | No divertor design published; liquid Li-LiH wall may self-pump impurities (Li gettering) or may release Li/H impurities into plasma at high flux — mechanism uncertain | **Binary** | **2** (No published exhaust solution; liquid wall impurity physics at 25 MW/m² is simulation-only) |
| **Hardware** | RAFM steel structure in contact with flowing Li-LiH at elevated temperature must survive 14 MeV neutron irradiation at 25 MW/m² wall loading without excessive corrosion, embrittlement, or tritium permeation over 30-year life (target fluence ~50 dpa) | RAFM steels (EUROFER, F82H): irradiated to ~30 dpa in fission spectrum; Li corrosion data at <10 dpa; no combined 14 MeV neutron + Li-LiH exposure at fusion-relevant fluence | ~2× fluence gap; chemical compatibility undemonstrated | RAFM steel selection optimized for Li compatibility (EUROFER97 or F82H); LiH additive claimed to reduce corrosion vs. pure Li; neutron irradiation testing in IFMIF-DONES (when available) | **Degrading** | **3** (Partial demonstration — RAFM at 30 dpa in fission spectrum; extrapolation to 50 dpa in 14 MeV + Li-LiH is unvalidated but incremental) |

**Function 4 mean (before heritage)**: (2 + 3) / 2 = **2.5**

---

#### **Function 5: Neutron/Particle Handling**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | 99.99% neutron energy absorption in blanket + shield (15 cm Pb + 18 cm Li-LiH + 50 cm VH₂ + 1.3 m concrete) to limit activation of external structures and achieve shielding compliance | JNM 599 (2024): Monte Carlo neutron transport (MCNP or equivalent) predicts 99.99% absorption for the specified radial build | ~1× (analytically verified) | Pb pebble layer provides neutron multiplication and moderation; Li-LiH absorbs thermalized neutrons; VH₂ + concrete outer shield attenuates fast neutron and gamma leakage | **Degrading** | **3** (Simulation validated against experimental data from fission reactors and fusion neutron sources; full-system validation requires prototypical blanket mock-up irradiation) |
| **Hardware** | Flowing liquid Li-LiH blanket must maintain structural integrity and tritium containment under 14 MeV neutron displacement damage to RAFM structure + Pb pebble bed retention at 25 MW/m² for 30-year plant life | Pb-17Li blanket modules tested in fission reactors (IFMIF precursor experiments); no flowing Li-LiH at fusion fluence | ~5× fluence gap; Li-LiH chemistry undemonstrated | RAFM structure designed for 50 dpa lifetime; Pb pebble bed retained by flow baffles; Li-LiH chemistry managed via temperature and LiH fraction control | **Degrading** | **3** (Partial demonstration — Pb-Li blanket modules at <10 dpa; extrapolation to 50 dpa and Li-LiH mixture is engineering development, not fundamental barrier) |

**Function 5 mean (before heritage)**: (3 + 3) / 2 = **3.0**

---

#### **Function 6: Fuel Cycle Closure**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | TBR ≥ 1.15 (design requirement) to achieve tritium self-sufficiency; JNM 599 reports TBR = 1.60 for optimized 10 cm Pb + 22 cm Li-LiH blanket configuration | TBR = 1.60 analytically verified by neutron transport (Monte Carlo); no experimental validation at fusion-relevant neutron flux | ~1× (analytically confirmed with 39% margin above threshold) | Pb (n,2n) neutron multiplication + Li-6(n,α)T breeding in non-enriched Li-LiH; 39% TBR margin intended to cover port penetration losses and fuel cycle inefficiencies in 3D geometry | **Binary** (TBR <1.0 is unmitigated failure; TBR = 1.60 claim must be validated) | **3** (Simulation validated against experimental data from test blanket modules; full-system validation requires prototypical 3D geometry blanket irradiation in 14 MeV neutron source) |
| **Hardware** | Tritium extraction from flowing Li-LiH circuit at kg/day rates (estimated ~1.5 kg/day for 1 GWe D-T plant) with <1% inventory holdup; tritium permeation through Li-LiH-to-sCO₂ heat exchangers must be <1 Ci/day to prevent contamination of secondary circuit | EU DEMO Pb-17Li blanket program: tritium extraction demonstrated at <100 g/day in test loops; Li has ~100× higher T solubility than Pb-17Li, increasing extraction challenge; no demonstration with Li-LiH mixture | ~15× extraction rate gap; Li-LiH chemistry uncharacterized | Vacuum sieve tray or molten salt extraction adapted from fission breeder blanket R&D; LiH component may alter tritium solubility and extraction kinetics vs. pure Li; low-permeation heat exchanger (double-wall with He sweep or permeation barrier coatings) | **Binary** (tritium extraction failure prevents fuel cycle closure) | **2** (Simulation and small-scale experiments for Pb-17Li; extrapolation to kg/day from Li-LiH is unvalidated; heat exchanger permeation at operating temperature is undemonstrated) |

**Function 6 mean (before heritage)**: (3 + 2) / 2 = **2.5**

---

#### **Function 7: Power Conversion & BOP**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | sCO₂ Brayton-Rankine combined cycle must achieve 49–51% thermal efficiency at turbine inlet temperature enabled by liquid Li-LiH heat source (temperature not published, but high enough to enable 50% cycle efficiency) | sCO₂ Brayton cycle: 10 MW demonstrated at 45–47% efficiency (Sandia, Echogen); combined Brayton-Rankine: natural gas combined cycle achieves >60% efficiency; fusion-specific sCO₂ combined cycle at 50% is analytically optimized (ECM 2023 genetic algorithm) but undemonstrated | ~100× power scale gap; fusion heat source integration undemonstrated | Industrial sCO₂ turbomachinery development (GE, Siemens, Echogen targeting 100+ MW scale); Li-LiH-to-sCO₂ heat exchanger design with tritium permeation control | **Degrading** | **4** (Industrial sCO₂ Brayton at 10 MW scale with 45%+ efficiency; combined cycle architecture is established in gas turbines; fusion integration is engineering scale-up, not fundamental physics) |
| **Hardware** | sCO₂ turbomachinery (turbines, compressors, recuperators) at ~1.5 GWe gross output must achieve 30-year lifetime with <2 week/year maintenance downtime; tritium-compatible heat exchangers between Li-LiH primary and sCO₂ secondary | sCO₂ turbines demonstrated at 10 MW (Sandia 2021, Echogen); natural gas combined cycle turbines operate at GW scale with 95%+ availability; no fusion-specific sCO₂ BOP integration | ~150× power scale gap | Industrial sCO₂ turbomachinery vendors scaling to 100 MW (2025 target) and GW scale (2030s projection); tritium permeation barriers (Al₂O₃ or ceramic coatings) on heat exchanger surfaces; remote handling for heat exchanger replacement | **Degrading** | **4** (sCO₂ turbomachinery at 10 MW TRL 5–6; GW-scale is industrial engineering development; tritium compatibility is design challenge but solvable with coatings/barriers) |

**Function 7 mean (before heritage)**: (4 + 4) / 2 = **4.0**

---

### Heritage Credit Application

Renaissance Fusion uses **D-T fuel** and has **good traceability to W7-X stellarator** (QI optimization validated) and **ARIES-CS stellarator plant study** (modular stellarator architecture). Heritage floor for stellarator lineage: **4.0** applies to Functions 1–3 (Plasma Performance, Driver, Instability Control).

**Before heritage**:
- F1 = 2.0
- F2 = 4.0 (already above floor)
- F3 = 3.0

**After heritage**:
- F1 = max(2.0, 4.0) = **4.0** (heritage floor applied)
- F2 = **4.0** (unchanged)
- F3 = max(3.0, 4.0) = **4.0** (heritage floor applied)

**Function-level means (after heritage)**:
- F1 = 4.0
- F2 = 4.0
- F3 = 4.0
- F4 = 2.5
- F5 = 3.0
- F6 = 2.5
- F7 = 4.0

**Binary risks identified**:
1. Plasma Performance (Physics): Ignition (Q=∞) at compact stellarator geometry — 11× below Lawson threshold per ISS04 scaling
2. Plasma Performance (Hardware): Liquid Li-LiH wall stability at 25 MW/m² and 10 T without confinement degradation
3. Instability Control (Physics): Alpha-particle-driven instabilities at ignition (no stellarator precedent)
4. Instability Control (Hardware): 3D field precision maintenance under neutron irradiation
5. Plasma-Wall Interaction (Physics): Plasma exhaust solution at 25 MW/m² (no published divertor design)
6. Fuel Cycle Closure (Physics): TBR = 1.60 validation at fusion-relevant flux in 3D geometry
7. Fuel Cycle Closure (Hardware): Tritium extraction from Li-LiH at kg/day rates

**C7 computation (Python will perform, but for reference)**:
Mean of F1–F7 (after heritage) = (4.0 + 4.0 + 4.0 + 2.5 + 3.0 + 2.5 + 4.0) / 7 = **3.43**

Function-level cap check: F4 = 2.5 and F6 = 2.5 are both >1.5, so no cap applied.

**C7 ≈ 3.5** (rounded to nearest 0.5)

---

### Summary Table

| Criterion | Score | Justification Summary |
|-----------|-------|----------------------|
| **C1** | 4.8 | Laser-patterned HTS cylinders and liquid metal system components are factory-manufacturable; 50+ identical pump/HX modules; stellarator building is site-built |
| **C3** | 3.2 | Magnet film deposition (46% of capital) is fusion-specific with no current market; sCO₂ and cryogenics benefit from external industrial development; moderate supply chain scaling constraints (REBCO film equipment, sCO₂ turbomachinery) |
| **C4** | 3.5 | Stellarator steady-state operation reduces coupling vs. tokamaks; liquid metal pump failure is tightest coupling (minutes to shutdown) but parallel modules limit cascade; 9 major subsystems |
| **C5** | 1.7 | D-T fuel with full tritium breeding infrastructure; conventional thermal cycle with large cooling towers; no site-specific advantages |
| **C8** | 2.5 | Three peer-reviewed papers provide strong physics/engineering documentation; zero published economic data despite "economically optimized design point" paper title; 7 blocking gaps in LCOE parameters; vague commercialization pathway |
| **F1** | 4.0 | Plasma Performance: Heritage credit applied (stellarator lineage overrides ignition shortfall at Tier 2) |
| **F2** | 4.0 | Driver: ITER NNBI at 60% neutralization is near-regime; stellarator adaptation is incremental |
| **F3** | 4.0 | Instability Control: Heritage credit applied (W7-X QI validation + MHD codes) |
| **F4** | 2.5 | Plasma-Wall: No published exhaust solution (Tier 2 physics); RAFM + Li-LiH at 25 MW/m² is partial demonstration (Tier 3 hardware) |
| **F5** | 3.0 | Neutron Handling: 99.99% absorption is analytically verified (Tier 3 physics); RAFM + Pb-Li at <10 dpa extrapolates to 50 dpa (Tier 3 hardware) |
| **F6** | 2.5 | Fuel Cycle: TBR = 1.60 analytically verified with margin (Tier 3 physics); tritium extraction from Li-LiH at kg/day is simulation-only (Tier 2 hardware) |
| **F7** | 4.0 | Power Conversion: sCO₂ at 10 MW scale is near-regime (Tier 4 physics); GW-scale turbomachinery is industrial development (Tier 4 hardware) |

---

```yaml
---
scores:
  C1: 4.8
  C3: 3.2
  C4: 3.5
  C5: 1.7
  C8: 2.5
  F1: 4.0
  F2: 4.0
  F3: 4.0
  F4: 2.5
  F5: 3.0
  F6: 2.5
  F7: 4.0
  binary_risks:
    - "Ignition (Q=∞) at compact stellarator geometry: ISS04 scaling predicts n·τ_E ~11× below Lawson threshold at published design point"
    - "Liquid Li-LiH wall stability at 25 MW/m² plasma-facing heat flux and 10 T magnetic field without MHD-driven confinement degradation"
    - "Alpha-particle-driven instabilities at ignition conditions in compact QI stellarator (no experimental precedent in any stellarator)"
    - "3D stellarator magnetic field precision <1 mm RMS maintained under neutron irradiation and thermal cycling of laser-patterned HTS cylinders"
    - "Plasma exhaust solution at 25 MW/m² steady-state heat flux with Z_eff <2.0 (no divertor design published)"
    - "TBR = 1.60 validation at fusion-relevant 14 MeV neutron flux in 3D stellarator geometry with port penetrations"
    - "Tritium extraction from flowing Li-LiH circuit at kg/day rates with <1% inventory holdup and heat exchanger permeation <1 Ci/day"
---
```
