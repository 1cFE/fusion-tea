---
ID: 26-heavy-ion-beam-icf
Concept: Heavy Ion Beam ICF (D-T)
Company: Intensity Energy
Type: synthesis
Status: draft
Created: 2026-05-14
---

# Synthesis: Heavy Ion Beam ICF (D-T)

## 1. Executive Summary

- **Single most important risk**: No commercial HIF driver exists — the entire induction linac at 5-15 Hz rep rate and mA-class beam current is extrapolation from lab-scale demonstrations, with no learning-curve validation of the claimed modular manufacturing cost advantage. Driver capital dominates LCOE and spans $0.7-2.5B.
- **Single most important advantage**: 30-40% driver efficiency versus 1-15% for laser ICF eliminates approximately 10-15 percentage points of recirculating power, reducing gross generation requirements by ~10-15% and dropping target gain requirements from 100-200 (laser) to 50-70 (HIF) for energy breakeven.
- **LCOE ballpark**: $94/MWh at 940 MWe (HYLIFE-II baseline), ranging $80-115/MWh across driver capital scenarios ($0.7-2.5B). This is approximately 43% below the CPI-inflated historical HYLIFE-II reference ($162/MWh from 6.5¢/kWh 1990s), likely because civil works are undercosted (km-scale accelerator tunnel not captured in tokamak-derived framework).
- **Confidence verdict**: Low — all cost data is 30-40 years old, no private company exists, driver-scale hardware has never been built, and target fabrication at ~189M targets/year is uncharacterized. The model LCOE should be read as a lower bound; the inflated historical figure as an upper bound.

## 2. What Matters Most for LCOE

**Ranked by sensitivity elasticity from model output:**

### 2.1 Availability (elasticity: -0.96)
- **Assumed value**: 80% (no published HYLIFE-II target; analogized from accelerator uptime ~85-95% derated for IFE chamber)
- **Source**: Analysis §S5 [analogue, low confidence]; no HIF plant has ever operated
- **Sensitivity magnitude**: Each 1 percentage point drop in availability raises LCOE by ~1%. A 10-point swing (70% → 80%) changes LCOE by approximately $13/MWh ($107/MWh → $94/MWh).
- **What would flip the conclusion**: If rep-rated chamber clearing, target injection, or driver availability falls below 75%, LCOE crosses $100/MWh and commercial competitiveness becomes doubtful. Conversely, if HIF achieves 85-90% availability (plausible given modular driver architecture and no blanket replacement), LCOE drops to $84-89/MWh — potentially competitive with advanced nuclear.

### 2.2 Q_eng (engineering gain, elasticity: -0.32)
- **Assumed value**: 6.5 (derived from HIBALL's published 15% recirculating power fraction)
- **Source**: hif-technology-overview.md §HIBALL; HYLIFE-II recirculating fraction unpublished
- **Sensitivity magnitude**: 1% improvement in q_eng → 0.32% reduction in LCOE. A 20% q_eng improvement (6.5 → 7.8, via higher driver efficiency or lower parasitic loads) drops LCOE by ~6%.
- **What would flip the conclusion**: If driver efficiency degrades from 35% to 25% (below published HIF range), q_eng falls to ~4.6 and LCOE rises to ~$97/MWh — eroding the advantage over laser ICF. This parameter encodes HIF's core structural advantage; degradation beyond the 30-40% efficiency range undermines the entire concept economics.

### 2.3 Driver Capital Cost (C220104, manual scenario analysis)
- **Assumed value**: $1,400M (HYLIFE-II $570M 1990s × 2.5 CPI)
- **Source**: hif-technology-overview.md §HYLIFE-II; only published HIF driver bottom-up cost
- **Sensitivity magnitude**: Driver cost scenarios span $0.7-2.5B, yielding LCOE $80-115/MWh. A $700M reduction (modular NOAK manufacturing) drops LCOE by $14/MWh; a $1,100M increase (no-learning pessimistic) raises LCOE by $21/MWh.
- **What would flip the conclusion**: If modular induction cell manufacturing achieves the claimed learning-curve cost reduction and driver capital falls below $1.0B, LCOE drops to ~$86/MWh and HIF becomes cost-competitive with tokamaks. If driver costs rise above $2.0B (scientific-instrument procurement with no learning), LCOE crosses $105/MWh and the concept is uncompetitive unless availability exceeds 85%.

### 2.4 Thermal Efficiency (eta_th, elasticity: -0.23)
- **Assumed value**: 35% (canonical steam Rankine per scoring framework; HYLIFE-II used steam but did not specify efficiency)
- **Source**: Analysis §S5 [analogue, low confidence]; 1990s-era steam plant
- **Sensitivity magnitude**: 1% improvement in eta_th → 0.23% LCOE reduction. Moving from 35% (steam Rankine) to 48% (sCO₂ Brayton, GT-MHR-class) would reduce LCOE by approximately 8.5%, or ~$8/MWh.
- **What would flip the conclusion**: No HIF study has evaluated sCO₂ Brayton. If FLiBe → sCO₂ heat exchange proves viable, LCOE drops to ~$86/MWh. This is a meaningful lever but not dominant — driver capital and availability matter more.

### 2.5 Construction Time (elasticity: +0.37)
- **Assumed value**: 7 years (extended for km-scale accelerator complex)
- **Source**: Model assumption; HIBALL/HYLIFE-II construction schedules not published
- **Sensitivity magnitude**: Each 1-year extension raises LCOE by ~5.3% (~$5/MWh) via interest during construction. Reducing construction to 5 years (aggressive modular accelerator factory pre-assembly) drops LCOE by ~$10/MWh.
- **What would flip the conclusion**: If first-of-kind HIF construction extends to 10+ years (comparable to ITER's timeline), LCOE rises above $110/MWh even with optimistic driver capital. Conversely, modular driver factory assembly could credibly achieve 5-6 year construction, but this requires validating the modular architecture claim.

## 3. Risk Verdicts

### 3.1 Driver capital cost uncertainty ($0.7-2.5B range, 30-40 year old estimate)
- **Verdict**: Genuinely uncertain
- **Rationale**: The $1.4B figure is the only published driver cost, from 1990s HYLIFE-II, inflated by CPI. Modular induction cell manufacturing could plausibly halve this via learning curves, or costs could double if scientific-instrument procurement persists.
- **What would retire this risk**: A modern bottom-up driver cost estimate using current component costs (pulsed power, induction cores, beam transport magnets) with a credible learning-curve model for mass-produced cells. Alternatively, building a prototype multi-cell induction linac at 1/10 scale and validating costs.

### 3.2 Target fabrication at commercial scale (~189M targets/year, uncharacterized cost)
- **Verdict**: Likely resolvable
- **Rationale**: HIF direct-drive targets are geometrically simpler than NIF hohlraums (spherical, no laser entrance holes, no hohlraum liner). The Goodin et al. criterion (<10% of electricity value per target) implies ~$3/target (1990s dollars). At 189M targets/year, this is ~$570M/year OPEX — manageable if geometry simplification delivers cost savings.
- **What would retire this risk**: A detailed target fabrication process design (DT ice layering, tamper/pusher assembly, QC at 10 Hz throughput) with bottom-up cost estimate. Demonstration of continuous cryogenic target production at 1-10 Hz for >1000 shots would validate the manufacturing pathway.

### 3.3 Chamber clearing and liquid wall reformation at 6-15 Hz (undemonstrated at scale)
- **Verdict**: Likely resolvable
- **Rationale**: HYLIFE-II analyzed FLiBe jet hydrodynamics in detail and concluded jets reform within 167 ms (6 Hz cycle). Water-surrogate experiments validated jet dynamics at lower intensities. The physics is tractable — the gap is demonstration at fusion yield (350 MJ/shot) and 30-year integrated lifetime.
- **What would retire this risk**: A rep-rated fusion chamber test facility (Z-pinch or laser IFE at 5+ Hz with liquid walls) demonstrating clearing, vapor re-condensation, and jet reformation over 10,000+ shots. Alternatively, high-fidelity simulation validated against HYLIFE-II geometry.

### 3.4 Rep-rated induction linac driver at mA-class beam current (never built)
- **Verdict**: Unlikely resolvable without large-scale demonstration
- **Rationale**: Individual induction cells are mature (TRL 5-6), but a full driver at HYLIFE-II spec (5 MJ, 6 Hz, mA beam, 10⁹ shots over 30 years) is 4-5 orders of magnitude beyond current demonstrations (NDCX-II: µA-class, single-shot or low rep rate). Beam quality preservation, emittance control, and component lifetime at commercial duty cycle are entirely extrapolative.
- **What would retire this risk**: Build a multi-stage induction linac demonstration at 1/10 beam current and 1 Hz for 1 year continuous operation (~3×10⁷ shots). Validate beam transport, final focus, and on-target accuracy. This is a $100M+ demonstration facility — no pathway to this without renewed national lab commitment.

### 3.5 Final focus optics and beam-on-target accuracy at 10-15 Hz (design-stage only)
- **Verdict**: Genuinely uncertain
- **Rationale**: Heavy ion beams must focus to mm-scale spots on moving cryogenic targets at 5-10 Hz. Superconducting quadrupole final focus magnets must survive neutron exposure over 30 years and 10⁹ shots. No prototype exists; the LBNL HIF program ended before building a driver-scale final focus system.
- **What would retire this risk**: Build a final focus magnet test stand with prototypical geometry and irradiate to 10-20 dpa with neutrons. Demonstrate beam-on-target accuracy <1 mm RMS at 5 Hz for 10,000 shots. This requires restarting the HIF program — no commercial actor will fund this scale of R&D.

### 3.6 Li-6 enrichment supply chain (no active production facility, 53× price premium)
- **Verdict**: Unlikely resolvable on commercial timelines
- **Rationale**: All D-T breeding concepts face this constraint. At 2019 market prices (€53k/kg), a 2 GW plant's Li-6 inventory costs ~€2.5-3B — comparable to total plant capital. The ICOMAX production restart timeline is ~20 years from 2019 baseline (readiness late 2030s). This is a structural gating constraint for all D-T fusion.
- **What would retire this risk**: Commission an Li-6 production facility at pilot scale (10+ tonnes/year enriched Li-6) and validate production-cost pricing below €5k/kg. This requires government-led investment (analogous to tritium production at CANDU) — no private fusion company can solve this alone. Timeline: 15-25 years.

### 3.7 Target physics: gain 50-70 achieved at relevant driver energies (simulation only)
- **Verdict**: Genuinely uncertain
- **Rationale**: HIF target gain requirements (50-70) are lower than laser ICF (100-200) due to higher driver efficiency, but no HIF target has been driven to ignition. HYLIFE-II's gain = 70 at 5 MJ is a simulation result. NIF's path to ignition took 13 years of iterative campaigns after achieving multi-MJ driver delivery — HIF has no analogous iterative platform.
- **What would retire this risk**: Drive an HIF target with a multi-MJ heavy ion beam (Bi²⁺ or Cs⁺ at 5-10 GeV) to ignition and measure fusion yield. Validate gain ≥ 50 with shot-to-shot reproducibility. This requires building the driver first — a circular dependency. Alternatively, validate target physics on NIF/Z-machine with ion-beam-heated indirect-drive surrogates.

## 4. Structural Advantages and Disadvantages

**Comparison baseline**: D-T tokamak (spherical tokamak HTS, concept 21)

### Advantages (cost items eliminated or reduced):

1. **No plasma-confining magnets (−$300-600M)**: HIF requires no toroidal field coils, no poloidal field coils, no HTS tape supply chain bottleneck, and no cryogenic plant for km-scale magnet systems. Accelerator quadrupoles use conventional LTS or modest HTS in small quantities. This eliminates the largest single capital cost item in tokamak designs (~15-25% of total capital).

2. **No blanket replacement schedule (−$50-100M NPV over 30 years)**: HYLIFE-II's FLiBe thick liquid wall self-renews every shot, claiming 30-year chamber lifetime with no first wall replacement. Tokamaks replace blanket modules every 2-6 years at $50-100M per cycle. If validated, this is a major availability and CAPEX advantage.

3. **Lower target gain requirement (G = 50-70 vs. G = 5-10 for tokamaks, Q_eng = 6.5 vs. ~1.2 break-even)**: HIF's 30-40% driver efficiency means the "physics problem" is easier — target gain of 50-70 achieves commercial Q_eng, versus tokamak's need for Q_plasma ≈ 10-30 to overcome resistive/turbulent losses. This maps to lower fusion power density requirements and potentially more forgiving plasma conditions.

4. **Modular driver architecture enables factory manufacturing**: If validated, mass-produced induction cells could achieve cost learning curves analogous to semiconductor or automotive manufacturing. Tokamak central solenoids and HTS magnets are one-off fabrications with limited learning potential.

5. **Low in-system tritium inventory (140 g structural + 0.5 g FLiBe vs. kg-scale in tokamaks)**: The FLiBe liquid wall minimizes tritium holdup in structural materials. Tokamak blankets accumulate tritium in beryllium multipliers and structural penetrations, complicating maintenance and safety case.

### Disadvantages (cost items added or increased):

1. **Driver capital dominates LCOE (+$1.4B at baseline, 40-60% of total capital)**: The induction linac driver is the largest single capital item and has no tokamak analog. Tokamak CAS22 is dominated by magnets ($300-600M) and vacuum vessel; HIF CAS22 is dominated by the driver ($1.4B baseline). Driver cost uncertainty is the single largest LCOE uncertainty.

2. **Per-shot consumable costs (target fabrication OPEX, uncharacterized but plausibly $500M+/year)**: At ~$3/target × 189M targets/year, target OPEX is comparable to tokamak fuel cycle costs but with no demonstrated manufacturing pathway. Tokamaks have steady-state fueling (mg/s injection) with no consumable hardware per shot.

3. **Civil works for km-scale accelerator infrastructure (+$200-400M estimated undercosting)**: HIBALL used a ~3 km single-pass linac; HYLIFE-II used a recirculating architecture with storage ring. Either requires tunnel boring, shielding, and beam transport infrastructure qualitatively different from tokamak building geometry. Framework CAS21 ($652M) likely underestimates this by $200-400M, explaining part of the model/historical LCOE gap.

4. **No operating heritage (TRL 2-3 at system level vs. TRL 5-6 for tokamaks)**: Tokamaks have 70+ years of experimental progression (ZETA → JET → ITER → SPARC). HIF has NDCX-II (subscale) and ended national programs. The risk of unforeseen integration challenges is higher for HIF.

5. **Target ignition physics unproven (vs. tokamak Q > 1 demonstrated at JET)**: NIF achieved ignition after 13 years of iterative campaigns. HIF has no ignition platform and lower gain requirements do not eliminate the need to cross the ignition threshold experimentally.

### Net structural assessment:
HIF trades tokamak's magnet capital cost and blanket replacement cycle for driver capital cost and per-shot consumable costs. If driver manufacturing learning is real and chamber lifetime is validated, HIF's LCOE structure is potentially superior (no scheduled blanket CAPEX, higher availability uptime). If driver costs remain at scientific-instrument levels and target fabrication scales poorly, HIF is structurally disadvantaged.

## 5. Cross-Concept Positioning

Heavy ion beam ICF occupies a unique position in the IFE landscape as the only driver architecture with 30-40% wall-plug efficiency. This is its sole claim to economic superiority over laser ICF.

**Within IFE:**
- **Laser ICF (concepts 03, 04, 17a, 17b, 26, 30, 31)**: HIF's efficiency advantage (30-40% vs. 1-15%) translates to ~10-15 percentage points lower recirculating power and 50-70 vs. 100-200 target gain requirements. However, laser ICF has demonstrated ignition (NIF 2022) and multi-GW private-sector development (Commonwealth Fusion, Focused Energy). HIF has no private actors and no ignition platform. **HIF is economically superior on paper but 10-15 years behind in experimental validation.**
- **Projectile ICF (concept 22, First Light Fusion)**: Shares the "no optics in chamber" advantage and potentially high driver efficiency (railgun/gas gun). Both eliminate laser optics neutron damage. Projectile ICF operates at <1 Hz (limited by mechanical cycling); HIF targets 5-15 Hz. **HIF has higher throughput potential but projectile ICF is closer to commercial demonstration.**
- **MagLIF (concept 07, Sandia Z-machine)**: Pulsed-power driver with moderate efficiency (~15-30%). MagLIF achieves high gain with magnetic compression at <1 Hz. **HIF has higher rep rate and efficiency; MagLIF has active national lab platform (Z-machine).**

**Relative to MFE:**
- **Tokamaks (concepts 01, 21, 28, 29, 33, 34)**: HIF eliminates magnets ($300-600M) and blanket replacement ($50-100M NPV) but adds driver capital ($1.4B) and per-shot consumables ($500M/year OPEX). Tokamaks have 70 years of experimental heritage; HIF has lab-scale demos. **HIF is economically competitive only if driver manufacturing learning is validated.**
- **Stellarators (concepts 05, 09, 10, 20a, 20b, 36)**: Stellarator magnets are more complex than tokamaks ($500M-1B+). HIF's no-magnet advantage is even larger vs. stellarators. However, stellarators claim steady-state operation with no disruptions — HIF's pulsed operation is fundamentally different. **HIF eliminates stellarator's hardest engineering problem (3D magnet coils) but introduces new ones (rep-rated driver, target factory).**
- **Mirrors (concepts 06, 11)**: Mirrors also eliminate toroidal confinement magnets (using simpler axial mirror coils). Like HIF, mirrors trade confinement magnets for other capital (in mirror's case, plasma guns/beam injectors). **Mirrors and HIF both avoid toroidal complexity but have lower TRL than tokamaks.**

**Key differentiator**: HIF is the only fusion concept where **driver efficiency** is the primary economic claim. All MFE concepts have auxiliary heating (NBI, ECRH, ICRH) at 30-60% efficiency, but this is a small fraction of recirculating power. All laser IFE concepts have driver efficiency <15%. HIF's 30-40% efficiency is structurally unique and, if validated, justifies lower target gain requirements and higher plant availability.

**Positioning verdict**: HIF is the economically rational IFE architecture if you believe (a) target gain 50-70 is achievable, (b) modular driver manufacturing delivers cost learning, and (c) 5-15 Hz rep-rated chamber clearing is tractable. None of these are proven. Laser ICF has momentum (NIF ignition, private capital); HIF has better physics-on-paper but no demonstration pathway.

## 6. Modeling Confidence

**Rating: Low**

### Data-anchored parameters (5 of 15 key inputs):
1. Driver efficiency (30-40%): high confidence, cross-confirmed across multiple sources
2. Target gain requirement (50-70): high confidence, derived from driver efficiency and power balance
3. Repetition rate (6 Hz HYLIFE-II, 5 Hz HIBALL): high confidence, design specifications
4. Fuel type (D-T): high confidence, both major designs
5. Energy conversion type (steam Rankine): medium-high confidence, both designs baselined steam

### Speculative parameters (10 of 15 key inputs):
1. **Driver capital cost ($1.4B)**: 1990s estimate inflated by CPI, no modern validation, spans $0.7-2.5B in scenarios
2. **Q_eng (6.5)**: derived from HIBALL 15% recirculation; HYLIFE-II value unpublished
3. **eta_th (35%)**: canonical steam Rankine assumption; HYLIFE-II did not specify efficiency
4. **Availability (80%)**: no published HIF target; analogized from accelerator uptime with IFE chamber derate
5. **Target fabrication cost**: uncharacterized; Goodin criterion (<10% electricity value) implies ~$3/target but no manufacturing cost exists
6. **Chamber lifetime (30 years no replacement)**: HYLIFE-II analytical conclusion, never demonstrated
7. **Final focus magnet lifetime**: no irradiation database, no rep-rated demonstration
8. **Civil works cost (CAS21 $652M)**: tokamak-derived scaling, likely undercosted for km-scale accelerator by $200-400M
9. **Construction time (7 years)**: model assumption, no published HIBALL/HYLIFE-II schedule
10. **FLiBe inventory cost**: 1994 dollars only, no modern beryllium/Li-6 supply chain costing

### Dominant source of LCOE uncertainty:
**Driver capital cost** dominates at 40-60% of total capital ($1.4B baseline, plausible range $0.7-2.5B). Each $100M driver cost change moves LCOE by ~$1/MWh. The $1.8B uncertainty range ($0.7B optimistic to $2.5B pessimistic) spans $35/MWh LCOE range — larger than the entire sensitivity contribution of all other engineering levers combined.

Second-order uncertainty is **availability** (elasticity -0.96), where a 10-point swing (70% to 80%) is worth $13/MWh. Availability is uncharacterized because no HIF plant has operated; the 80% base case is an analogy with 20+ percentage points of uncertainty.

**Model reliability assessment**: The model LCOE ($94/MWh at 940 MWe) is 43% below the CPI-inflated historical HYLIFE-II reference ($162/MWh from 6.5¢/kWh 1990s). This gap is too large to attribute solely to NOAK vs. FOAK or inflation methodology. The likely explanation is **civil works undercosting** (km-scale accelerator tunnel not captured in tokamak framework) and possibly **target factory OPEX underestimation** (framework default does not scale with 189M targets/year consumable cost). The model LCOE should be read as a **lower bound**; the inflated historical figure as an **upper bound**. True LCOE is plausibly $110-140/MWh for a first commercial plant, narrowing to $90-110/MWh at NOAK with driver learning.

## 7. What Would Change My Mind

### Developments that would lower LCOE estimate (make HIF more attractive):

1. **Modular driver demonstration with validated costs**: Build a 10-cell induction linac demonstration with factory-manufactured cells and validate per-cell cost below $5M (vs. ~$10-15M implied by scientific-instrument procurement). If mass production achieves 40-60% cost reduction, driver capital drops from $1.4B to $0.7-1.0B and LCOE falls to $80-86/MWh — potentially competitive with advanced nuclear. **This is the single most impactful data release.**

2. **Rep-rated liquid wall chamber demonstration**: Demonstrate FLiBe jet clearing and reformation at 5+ Hz for 10,000+ shots with simulated fusion yields (using Z-pinch or laser surrogate). If validated, this confirms 30-year chamber lifetime with no blanket replacement and justifies 85-90% availability projections (LCOE $84-89/MWh).

3. **Simplified target fabrication at <$1/target**: Demonstrate continuous production of HIF direct-drive targets (DT ice + tamper) at 1-10 Hz with validated cost below $1/target (vs. $3/target Goodin criterion). At 189M targets/year, this saves ~$380M/year OPEX and drops LCOE by ~$6-8/MWh.

### Developments that would raise LCOE estimate (make HIF less attractive):

1. **Driver-scale final focus failure**: If beam-on-target accuracy at commercial geometry cannot achieve <1 mm RMS at 5+ Hz (due to space-charge effects, emittance growth, or ion-optical aberrations), driver energy must increase by 50-100% to compensate for target miss fraction. This raises driver capital to $2.0-2.5B and LCOE to $105-115/MWh — uncompetitive.

2. **Target gain shortfall**: If HIF target simulations prove optimistic and ignition requires gain > 100 (comparable to laser ICF), the driver efficiency advantage is neutralized. Q_eng drops from 6.5 to 3-4 and LCOE rises to $110-120/MWh. NIF's 13-year path to ignition suggests target physics is harder than initial simulations predict — HIF could face the same gap.

3. **Li-6 enrichment bottleneck persists past 2040**: If no Li-6 production facility achieves pilot-scale operation by 2040, all D-T breeding concepts (including HIF) face €2.5-3B inventory cost at current prices (€53k/kg). This adds $10-15/MWh to LCOE and delays commercial deployment by 10-20 years. This is not HIF-specific but affects all D-T concepts equally.

## 8. LCOE Downselect Scoring

### C1: Modularization (scored by Claude)

| CAS Account | Construction Mode | Score | Share of Capital | Weighted Score |
|-------------|------------------|-------|------------------|----------------|
| CAS21 (Buildings) | Site-assembled (accelerator tunnel, chamber building) | 3 | 10.2% | 0.31 |
| CAS22.01 (Blanket/FW) | Factory module (FLiBe manifold modules) | 5 | 2.9% | 0.15 |
| CAS22.02 (Shield) | Factory module (modular shield panels) | 5 | 2.0% | 0.10 |
| CAS22.04 (Induction Linac Driver) | Factory module (identical induction cells) | 5 | 20.8% | 1.04 |
| CAS22.08 (Vacuum) | Site-assembled (chamber vessel, beam pipes) | 3 | 3.9% | 0.12 |
| CAS22.10 (Primary Coolant) | Site-assembled (FLiBe loops, HX) | 3 | 1.2% | 0.04 |
| CAS22.11 (Tritium) | Factory module (extraction skids) | 5 | 2.6% | 0.13 |
| CAS22.20 (Final Focus Magnets) | Factory module (SC quadrupoles) | 5 | 2.9% | 0.15 |
| CAS22.50 (Target Factory) | Factory module (automated production line) | 5 | 1.7% | 0.09 |
| CAS23 (Turbine Plant) | Factory module (steam turbine) | 5 | 3.3% | 0.16 |
| CAS24 (Electrical) | Factory module (switchgear, transformers) | 5 | 1.4% | 0.07 |
| CAS26 (Heat Rejection) | Factory module (cooling towers) | 5 | 1.6% | 0.08 |

**Weighted average**: (0.31 + 0.15 + 0.10 + 1.04 + 0.12 + 0.04 + 0.13 + 0.15 + 0.09 + 0.16 + 0.07 + 0.08) / (0.102 + 0.029 + 0.020 + 0.208 + 0.039 + 0.012 + 0.026 + 0.029 + 0.017 + 0.033 + 0.014 + 0.016) = 2.44 / 0.545 = **4.48**

**Module repetition boost**: Induction linac driver (C220104) requires hundreds of identical cells — exact count depends on gradient per cell, but HIBALL (~3 km linac at 10 GeV) implies 300-600 cells. This qualifies for the 10-49 identical modules repetition boost: +1.0.

**C1 score**: 4.48 + 1.0 = **5.0** (clamped at maximum)

**Justification**: The induction linac driver is inherently modular — hundreds of identical induction cells, beam transport quadrupoles, and pulsed power units are factory-manufactured and site-assembled. This is HIF's principal claimed advantage over one-off scientific instruments. The FLiBe blanket is also modular (manifold sections, shield panels). CAS21 buildings and chamber integration are site-assembled, but these are minority contributors (10-15% combined). The driver dominates at ~21% of capital and is fully modular. Module count (300-600 cells) justifies the +1.0 repetition boost, yielding maximum score.

---

### C3: Supply Chain Learning (scored by Claude)

#### Sub-factor A: Component learning rates (1-5)
Cost-weighted average across CAS accounts:

| Component | Learning Rate | Justification | Share | Weighted |
|-----------|--------------|---------------|-------|----------|
| Induction cells (C220104) | 3 | Fusion-specific pulsed magnetics; limited production base but scalable | 20.8% | 0.62 |
| SC beam transport magnets (C220200) | 4 | Industrial SC magnets (NbTi/Nb3Sn); HEP accelerator supply chain exists | 2.9% | 0.12 |
| FLiBe/LiPb coolant (C220111) | 2 | Fusion-specific with limited supply (Be scarcity, Li-6 enrichment) | 2.6% | 0.05 |
| Chamber/vessel (C220108) | 3 | Specialty fusion components; stainless/ferritic steel fabrication exists but not at fusion spec | 3.9% | 0.12 |
| Tritium systems (C220111) | 2 | Fusion-specific with no current market (extraction from FLiBe/LiPb at scale) | 2.6% | 0.05 |
| Buildings/tunnels (CAS21) | 5 | Commodity civil construction; tunnel boring is mature | 10.2% | 0.51 |
| Turbine plant (CAS23) | 5 | Commodity industrial equipment; mature steam turbine market | 3.3% | 0.16 |
| Electrical (CAS24) | 5 | Commodity electrical switchgear | 1.4% | 0.07 |
| Heat rejection (CAS26) | 5 | Commodity cooling towers | 1.6% | 0.08 |
| Balance (other CAS22) | 3 | Mix of specialty fusion and industrial components | 50.7% | 1.52 |

**Weighted average**: (0.62 + 0.12 + 0.05 + 0.12 + 0.05 + 0.51 + 0.16 + 0.07 + 0.08 + 1.52) / 1.00 = **3.30**

**Sub-factor A score**: 3.3

#### Sub-factor B: Supply chain bottleneck count (1-5)
Start at 5.0, subtract penalties:

- **Hard constraint (no known path)**: None identified — Li-6 enrichment has a path (ICOMAX), just long timeline
- **Scaling constraint (exists but must scale 10×+)**:
  - Li-6 enrichment capacity (−0.5): current stockpile is finite; new production facility required
  - Beryllium production for FLiBe (−0.5): global production ~300 t/yr; HYLIFE-II requires large inventory
  - Induction cell manufacturing at 300-600 unit scale (−0.5): current production is one-off scientific instruments
- **Sole-source dependency**:
  - Beryllium (Materion Corp. dominates, −0.25)
  - Li-6 enrichment (no active producer, future sole-source, −0.25)

**Sub-factor B score**: 5.0 − 0.5 − 0.5 − 0.5 − 0.25 − 0.25 = **3.0**

#### Sub-factor C: External demand pull (1-5)
Fraction of capital cost in components with >$1B/yr external market:

| Component | External Market | Share of Capital |
|-----------|----------------|------------------|
| Buildings/civil (CAS21) | Tunnel boring, civil construction (>$10B/yr global) | 10.2% |
| Turbine plant (CAS23) | Steam turbines (>$10B/yr industrial market) | 3.3% |
| Electrical (CAS24) | Switchgear, transformers (>$50B/yr global) | 1.4% |
| Heat rejection (CAS26) | Cooling towers (>$5B/yr) | 1.6% |
| SC magnets (C220200) | HEP/MRI magnets (~$2B/yr) | 2.9% |
| **Total with external demand** | | **19.4%** |

**Sub-factor C score**: 19.4% falls in the 10-20% bucket → **2**

#### C3 Calculation
C3 = (3.3 + 3.0 + 2.0) / 3 = **2.8**

**Justification**: The induction linac driver (21% of capital) is fusion-specific with limited learning rate (scored 3). FLiBe/tritium systems are also fusion-specific (scored 2). However, ~19% of capital is in commodity components with large external markets (buildings, turbines, electrical, cooling). The supply chain bottlenecks (Li-6, Be, induction cell scale-up) are resolvable but require dedicated effort. Overall, HIF is moderately disadvantaged vs. concepts with higher commodity content but better than exotic materials (He-3, advanced ceramics).

---

### C4: Plant Complexity (scored by Claude)

#### Sub-factor A: Operational coupling density (1-5)

The operational coupling question for HIF: if subsystem X fails during operation, what else stops working?

**Independent subsystems**:
- Target factory → can buffer 1-2 hours of targets; production halt does not immediately stop shots
- Turbine plant → chamber can fire into dump load for short periods; electricity generation is decoupled from driver
- Cooling towers → thermal inertia provides 10-30 minute buffer

**Moderate coupling**:
- FLiBe coolant loops → failure stops chamber clearing and breeding, but driver can idle; not instant cascade
- Tritium extraction → can operate at reduced TBR for days-weeks using reserve; not immediate shutdown
- Beam transport magnets → quench in one sector stops driver, but no plasma disruption analog; recovery is <hours

**High coupling**:
- Induction linac driver → cell failure propagates to entire accelerator; beam quality loss cascades to target miss → lost shot, but no chamber damage from missed shot (unlike tokamak disruption)
- Final focus magnets → misalignment stops on-target delivery; shots are lost until realignment (<hours downtime)

**Failure cascade count**: 2 high-coupling subsystems (driver, final focus) but neither causes chamber damage or extended outage. Tokamak disruptions can damage first wall and force weeks-months outage; HIF missed shots waste driver energy but don't damage hardware. Moderate coupling in coolant/tritium (buffer capacity exists).

**Sub-factor A score**: **4** — Mostly decoupled; driver and final focus failures cascade to lost shots but not to full plant shutdown or hardware damage. FLiBe loop and tritium systems have operational buffers.

#### Sub-factor B: Subsystem count (1-5)

CAS22 sub-accounts representing >1% of total capital:

1. C220104 — Induction linac driver (20.8%)
2. C220101 — Blanket/first wall (FLiBe manifolds) (2.9%)
3. C220102 — Shield (2.0%)
4. C220108 — Vacuum/chamber (3.9%)
5. C220111 — Tritium extraction (2.6%)
6. C220110 — Primary coolant (FLiBe loops) (1.2%)
7. C220200 — Final focus magnets (2.9%)
8. C220500 — Target factory (1.7%)

**Count**: 8 significant subsystems

**Sub-factor B score**: **3** — 8-10 significant subsystems (per framework)

#### C4 Calculation
C4 = (4 + 3) / 2 = **3.5**

**Justification**: HIF has moderate plant complexity. The driver is large and modular but failure-tolerant (individual cell faults don't cascade to chamber damage). The liquid wall architecture decouples plasma-facing components from structural lifetime (unlike solid first walls). However, the target factory, cryogenic supply, and final focus all must coordinate at 6 Hz for successful shots — this is higher operational tempo than steady-state MFE. The "magic wand" test: if target physics were proven tomorrow, the plant would still be operationally complex (6 Hz coordination of multiple subsystems) but not extreme (no single-point failure cascades to months-long outage).

---

### C5: Customization Needs (scored by Claude)

#### Sub-factor A: Thermal rejection (1-4)

HYLIFE-II uses steam Rankine cycle with FLiBe primary coolant. Gross thermal power is ~2,650 MW thermal (from 940 MWe net at ~35% eta_th). Waste heat rejection requires large cooling towers (~1,700 MW thermal to environment).

**Score**: **2** — Large cooling towers required (standard thermal cycle)

#### Sub-factor B: Fuel safety profile (1-4)

D-T fuel with tritium breeding (either LiPb or FLiBe blanket). Requires:
- Tritium breeding blanket (TBR ~1.2)
- Tritium extraction from FLiBe or LiPb
- Tritium fuel processing and purification
- Tritium inventory management (~140 g in-system per HYLIFE-II)
- Startup tritium procurement (~1 kg at $35,000/g)

Full tritium handling and breeding infrastructure.

**Score**: **1** — D-T (full tritium handling and breeding infrastructure)

#### C5 Calculation (raw)
Raw = (2 + 1) / 2 = **1.5**

Scale to [1, 5]: C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.67 = **1.7**

**Justification**: HIF requires standard site customization for large thermal plant (cooling towers, water supply, discharge permitting). The D-T fuel cycle is the dominant customization driver — tritium breeding, extraction, and handling require specialized facilities and regulatory approval. No site-specific advantages are claimed (HYLIFE-II is a generic design, not tied to a specific location). The FLiBe chemistry (corrosive, toxic Be content) adds modest additional site requirements but is second-order to the tritium handling constraint.

---

### C8: Data Adequacy (scored by Claude)

#### Sub-factor A: Source diversity & independence (1-5)

**Available sources**:
- HIBALL (KfK-3202, 1985): Joint German-US national lab study (independent, government-funded)
- HYLIFE-II (OSTI 7021072, ~1994): LLNL national lab study (independent, government-funded)
- arXiv 2005.07520 (2020): Academic review paper (independent)
- LBNL HIF program technical reports (1980s-2000s): National lab publications (government-funded)
- GSI/HIDIF program reports (1990s-2000s): European national lab (government-funded)

**No company publications exist** — "Intensity Energy" is unverified as a company. All sources are public-domain national lab or academic.

**Score**: **5** — Multiple independent public-domain sources (national lab studies, academic papers, no commercial bias)

#### Sub-factor B: Reactor design specification (1-5)

HYLIFE-II provides:
- Complete power plant design with engineering layouts
- Subsystem specifications (driver, chamber, blanket, energy conversion)
- Cost breakdown by major subsystem (driver $570M, chamber, tritium systems, turbine plant)
- Energy balance (fusion power, driver energy, recirculating power, net electric)
- Tritium inventory and breeding calculations
- Chamber hydrodynamics and clearing analysis

HIBALL provides:
- Multi-chamber plant design (3.8 GWe)
- Driver specifications (10 GeV Bi²⁺, ~3 km linac)
- LiPb blanket with TBR = 1.195
- Recirculating power fraction (15%)

**Gaps**: No modern design (post-2000), no sCO₂ evaluation, no final focus optics detail, no target factory manufacturing process.

**Score**: **4** — Comprehensive conceptual design with major subsystems specified (HYLIFE-II and HIBALL are full conceptual designs, but 30-40 years old and with some subsystem gaps)

#### Sub-factor C: LCOE parameter coverage (1-5)

**Blocking gaps from gap report**:
1. Modern CAPEX estimate in current dollars
2. Target fabrication cost at commercial volume
3. Driver component replacement schedule and cost
4. Capacity factor target and maintenance model

**Count**: 4 blocking gaps

**Score**: **3** — 3-4 blocking gaps (per framework)

#### Sub-factor D: Commercialization pathway clarity (1-5)

**Commercialization status**:
- No private company exists ("Intensity Energy" is unverified)
- No ARPA-E or DOE fusion program funding for HIF post-2010
- LBNL HIF program ended (date unclear, but NDCX-II is the only active facility and is for research, not commercialization)
- No published commercialization roadmap, timeline, or funding plan
- No regulatory engagement, no licensing pathway scoped
- No private capital investment, no venture funding, no SPAC/IPO pathway

**Score**: **1** — No commercialization pathway articulated (no company, no program, no funding, no timeline)

#### C8 Calculation
C8 = (5 + 4 + 3 + 1) / 4 = **3.2**

**Justification**: Data quality is high (multiple independent national lab studies with full conceptual designs), but data currency is poor (30-40 years old) and commercialization pathway is absent (no company exists). The technical data adequacy is good; the commercial viability data adequacy is near-zero.

---

### C7: Technical Risk Evidence (7 functions × 2 subcategories = 14 cells)

#### Function 1: Plasma Performance

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | Target gain G ≥ 50-70 at 5-8 MJ driver energy for 1 GWe plant (arxiv 2005.07520) | DT ice layer uniformity <1% RMS, tamper/pusher concentricity <5 µm, target positioning accuracy <0.5 mm at 6 Hz throughput |
| **Best demonstrated** | No HIF target driven to ignition. NIF achieved ignition with laser drive (2022) at G ~ 1.5 (Lawson). HIF target simulations project G = 70-130 but unvalidated. | NIF produces DT ice targets at ~10-50/year with <1% ice layer uniformity (single-shot cadence). No HIF target production demonstrated at any scale. |
| **Gap ratio** | G = 50 required / G = 0 demonstrated = undefined (no HIF ignition) | 189M targets/year required / ~50 targets/year NIF demonstrated = **3.8 million × throughput gap** |
| **Closure mechanism** | Drive HIF target with multi-MJ heavy ion beam; validate gain via radiation-hydrodynamics simulations (LASNEX, HYDRA) then experimental ignition campaign. | Scale cryogenic DT layering process to continuous production; automate tamper/pusher assembly; demonstrate 6 Hz injection with <0.5 mm positioning accuracy. |
| **Classification** | **Binary** — if target gain < 30, Q_eng < 3 and plant cannot achieve net electricity | **Degrading** — target cost >$10/target (Goodin criterion violated) raises OPEX by $1B+/year and makes LCOE uncompetitive, but plant still operates |
| **Evidence tier** | **Tier 2** — Simulation (LASNEX/HYDRA target codes) with no HIF driver-scale ignition platform. NIF ignition with laser drive is adjacent but different coupling physics (X-ray vs. ion deposition). | **Tier 2** — NIF target production is subscale (50/year vs. 189M/year) and different geometry (hohlraum vs. direct-drive). No manufacturing process design exists for HIF. |

**Function 1 mean**: (2 + 2) / 2 = **2.0**

---

#### Function 2: Driver / Energy Input

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | Beam energy 5-8 MJ per shot at 6 Hz, beam current 100-200 mA, ion energy 5-10 GeV (Bi²⁺ or Cs⁺), emittance preservation through ~3 km linac, final focus spot size <5 mm FWHM at 5-10 m standoff (HYLIFE-II, HIBALL specs) | Induction cell components (magnetic cores, pulsed power switches) survive 10⁹ shots over 30 years at 6 Hz; ion source produces 100-200 mA at >99.5% availability; beam transport SC magnets survive neutron exposure (~0.1-1 dpa/year at final focus location) |
| **Best demonstrated** | NDCX-II (LBNL): ~1 MeV Li⁺ beams at µA-class current, single-shot or low rep rate (<<1 Hz sustained). FAIR/SIS100 (GSI): high-intensity ion pulses but synchrotron architecture (not linac) and nuclear physics mission (not fusion). | Individual induction cells operational at NDCX-II; LTS SC quadrupoles for beam transport operational in HEP accelerators (SNS, CERN) at 1-10 Hz; no 100-200 mA ion source at 6 Hz demonstrated. |
| **Gap ratio** | 5 MJ / 0.001 MJ (NDCX-II) = **5,000× beam energy gap**; 100 mA / 0.1 mA (NDCX-II) = **1,000× beam current gap** | 10⁹ shots / 10⁴ shots (NDCX-II est.) = **100,000× shot count gap**; 6 Hz / 0.01 Hz (NDCX-II sustained) = **600× rep rate gap** |
| **Closure mechanism** | Build multi-stage induction linac with 300-600 cells (HIBALL scale); demonstrate beam emittance control via SC quadrupole lattice; validate final focus via plasma lens or chromatic correction. | Qualify induction core materials (ferrite, metglas) for 10⁹ cycle lifetime; demonstrate pulsed power switches at 6 Hz for 10⁶+ cycles; validate SC magnet quench recovery at rep rate. |
| **Classification** | **Binary** — if beam cannot deliver 5-8 MJ to target with <5 mm spot size, target gain collapses and plant fails | **Degrading** — driver component replacement accelerates OPEX; ion source availability <95% drops plant availability and raises LCOE proportionally (elasticity -0.96) |
| **Evidence tier** | **Tier 2** — Subscale demonstration (NDCX-II at µA, <<1 Hz). Physics of induction linac beam transport is understood (LBNL publications), but driver-scale integration is paper design. | **Tier 2** — Individual components (induction cells, SC quads) are TRL 5-6 in accelerator context, but no rep-rated fusion-relevant integration. Component lifetime at 10⁹ shots is extrapolation. |

**Function 2 mean**: (2 + 2) / 2 = **2.0**

---

#### Function 3: Instability Control

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | Target compression symmetry >95% (required for ignition); suppress Rayleigh-Taylor instabilities during implosion; avoid beam-target coupling asymmetries from non-uniform beam illumination or target misalignment >0.5 mm | Final focus magnet system delivers symmetric beam illumination (quadrupole symmetry or multiple beam ports); target injection system achieves <0.5 mm positioning repeatability at 6 Hz; no beam jitter >0.1 mm during pulse |
| **Best demonstrated** | NIF indirect-drive laser ICF achieved ignition with Rayleigh-Taylor control via hohlraum symmetry (2022). HIF direct-drive symmetry requirements are stricter (no hohlraum to smooth asymmetries). Ion beam stopping power and deposition uniformity calculated but never validated experimentally at ignition-relevant intensities. | NIF target injection: ~0.1 mm positioning accuracy at single-shot cadence. No demonstration of cryogenic target injection at 6 Hz or target tracking during beam-on. |
| **Gap ratio** | Symmetry requirement 95% / no HIF direct-drive symmetry demonstrated = undefined | 6 Hz target injection at 0.5 mm / NIF single-shot at 0.1 mm = **~40× throughput gap** (Hz) with relaxed accuracy |
| **Closure mechanism** | Validate ion beam deposition uniformity via integrated target shots on a driver-scale platform (analogous to NIF's iterative ignition campaign 2010-2022). Simulate via 3D radiation-hydrodynamics codes. | Develop automated cryogenic target delivery system with optical tracking and piezo-actuated alignment; demonstrate 6 Hz throughput with <0.5 mm RMS error for 1,000+ shots. |
| **Classification** | **Binary** — asymmetry >5% prevents ignition; target gain collapses below 30 and plant fails to achieve net power | **Degrading** — target positioning accuracy 0.5-1.0 mm reduces gain by 10-30% (estimated); raises driver energy requirement and LCOE proportionally |
| **Evidence tier** | **Tier 2** — Simulation (LASNEX/HYDRA) with no direct-drive HIF ignition demonstration. NIF is adjacent (ignition achieved, but indirect-drive laser, not direct-drive ion beam). | **Tier 2** — NIF target injection is subscale throughput and not integrated with ion beam final focus. Concept design exists (HYLIFE-II) but no prototype. |

**Function 3 mean**: (2 + 2) / 2 = **2.0**

---

#### Function 4: Plasma-Wall Interaction

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | FLiBe liquid jet system clears chamber debris (vaporized FLiBe, ablated target material, fusion ash) and reforms thick liquid wall (30-50 cm) within 167 ms (6 Hz cycle time); wall vapor pressure <1 mTorr for beam transport; no jet breakup or FLiBe contamination of final focus magnets over 10⁹ shots | FLiBe manifold nozzles survive 10⁹ thermal/mechanical cycles at 6 Hz with corrosive molten salt (FLiBe at 500-650°C); chamber first wall (behind FLiBe jets) survives 350 MJ/shot blast loading and 1-2 MW/m² neutron wall loading for 30 years with no structural replacement (HYLIFE-II claim) |
| **Best demonstrated** | HYLIFE-II hydrodynamic analysis concluded FLiBe jets reform within 167 ms cycle time (CFD + analytic models). Water-surrogate jet experiments validated jet formation at lower intensities. No demonstration with fusion-relevant yields (350 MJ/shot) or FLiBe at temperature and 6 Hz. | MSRE (Molten Salt Reactor Experiment, 1960s) operated FLiBe primary coolant loop at 650°C for ~2 years, but static loop (not pulsed jets) and fission neutron spectrum. No rep-rated FLiBe jet nozzle system demonstrated. Chamber first wall exposure: no analog. |
| **Gap ratio** | 6 Hz sustained for 30 years (10⁹ shots) / 0 Hz fusion-relevant demonstration = undefined | 10⁹ thermal cycles / 0 cycles at fusion conditions = undefined; 30-year no-replacement claim / MSRE 2-year static loop = **15× lifetime extrapolation** |
| **Closure mechanism** | Build a rep-rated liquid wall test facility (laser or Z-pinch driver at 1-5 Hz with FLiBe jets) and demonstrate clearing, reformation, and vapor pressure control for 10,000+ shots. Validate chamber first wall lifetime via neutron irradiation testing to 10-20 dpa. | Develop corrosion-resistant FLiBe manifold materials (Hastelloy-N or advanced alloys); test nozzle lifetime at 6 Hz thermal cycling in FLiBe for 10⁶ cycles; demonstrate tritium extraction from flowing FLiBe at power-plant throughput. |
| **Classification** | **Binary** — if FLiBe jets fail to reform or vapor pressure rises above beam transport threshold, shots stop and plant shuts down | **Degrading** — if chamber first wall requires replacement before 30 years (HYLIFE-II 30-year claim fails), blanket replacement CAPEX ($50-100M every 5-10 years) and availability loss erode LCOE advantage |
| **Evidence tier** | **Tier 2** — Analytical (HYLIFE-II CFD + hydrodynamic models) with water-surrogate partial validation. No fusion-yield demonstration. Adjacent: fission MSR FLiBe operation (static loop, not jets). | **Tier 2** — MSRE FLiBe loop is adjacent (fission neutrons, static flow, 2-year duration). No rep-rated jet nozzle demonstration. Chamber lifetime claim is paper design with no analog. |

**Function 4 mean**: (2 + 2) / 2 = **2.0**

---

#### Function 5: Neutron/Particle Handling

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | Shield final focus magnets to <0.1-1 dpa over 30 years (10⁹ shots at 350 MJ yield, 80% in 14 MeV neutrons); shield accelerator components to <0.01 dpa; bulk shield provides 10⁵-10⁶ attenuation of 14 MeV neutron flux to meet site boundary dose limits | Final focus SC magnet insulation survives 0.1-1 dpa cumulative displacement damage without degradation; accelerator beam pipes and quadrupoles survive scattered neutron exposure; biological shield (concrete + steel) provides dose attenuation with no streaming through beam ports |
| **Best demonstrated** | Neutron transport modeling (MCNP, Serpent) for IFE chamber geometry. HYLIFE-II and HIBALL include shield designs with calculated attenuation. No experimental validation of bulk shield performance at HIF geometry (large beam ports for final focus, scattered neutron flux). | Fission reactor pressure vessel steel: ~40 dpa over 40-year PWR lifetime (~1 dpa/year). HTS magnets for tokamaks: radiation tolerance demonstrated to ~0.1 dpa (ITER TF coil irradiation tests). LTS SC magnets: similar radiation tolerance (0.1-1 dpa before quench). |
| **Gap ratio** | Calculated attenuation 10⁵-10⁶ / no HIF-geometry validation = N/A (calculation only) | 0.1-1 dpa required / 0.1 dpa HTS magnet irradiation tests = **1-10× extrapolation** |
| **Closure mechanism** | Validate neutron transport models via mock-up experiments (ion beam or laser surrogate in prototypical HIF geometry with dosimetry); demonstrate final focus magnet shielding achieves <0.1 dpa at standoff distance. | Irradiate final focus SC magnet mock-ups (NbTi or Nb₃Sn) to 0.5-1 dpa with 14 MeV neutrons and measure quench performance; demonstrate no degradation. Use fission reactor PWV steel analogue for bulk shield. |
| **Classification** | **Degrading** — if final focus magnets degrade before 30 years, accelerated replacement schedule raises OPEX and availability loss; but plant can continue operating with more frequent magnet replacement | **Degrading** — magnet replacement cost (estimated $10-50M per replacement cycle for final focus array) and 1-2 week outage per replacement erode availability and LCOE |
| **Evidence tier** | **Tier 2** — Neutron transport simulation (MCNP) with no HIF-geometry validation. Fission reactor shielding is adjacent but different geometry (no beam ports). | **Tier 3** — Fission PWV steel at ~1 dpa/year for decades (direct analog for bulk structural steel); HTS/LTS magnet irradiation tests to 0.1 dpa (subscale for final focus requirement of 0.1-1 dpa). **Cite**: ITER TF coil irradiation qualification to 0.1 dpa; fission PWR vessel steel to 40 dpa over 40 years. |

**Function 5 mean**: (2 + 3) / 2 = **2.5**

---

#### Function 6: Fuel Cycle Closure

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | TBR ≥ 1.05-1.10 (breeding ratio with margin for losses and startup inventory accumulation) for FLiBe (HYLIFE-II) or LiPb (HIBALL) blanket; tritium extraction efficiency ≥99% from flowing FLiBe or LiPb at power-plant throughput (~200 g/day bred tritium for 1 GWe plant); tritium inventory in system ≤500 g (safety/regulatory limit) | FLiBe or LiPb coolant loop operates at 500-650°C for 30 years with corrosion <1 mm/year; tritium extraction system (vacuum sieve tray, molten salt distillation, or equivalent) processes ~200 g/day tritium; permeation barriers on heat exchangers prevent tritium loss to steam cycle (<1 Ci/day); startup tritium procurement (~1 kg at $35,000/g from CANDU or DOE stockpile) |
| **Best demonstrated** | HYLIFE-II neutronics: TBR = 1.05-1.15 (MCNP calculation, FLiBe blanket with Li-6 enrichment). HIBALL neutronics: TBR = 1.195 (LiPb blanket, MCNP). MSRE demonstrated tritium extraction from FLiBe at 99.7% efficiency (static loop, fission-bred tritium at ~1 g/day scale). | MSRE operated FLiBe primary loop at 650°C for ~2 years with Hastelloy-N piping (corrosion acceptable). EU-DEMO PbLi blanket program: ongoing engineering development. TSTA (Tritium Systems Test Assembly, LANL 1980s): demonstrated tritium processing at ~100 g/day scale (fueling test, not breeding extraction). |
| **Gap ratio** | Calculated TBR 1.05-1.195 / MSRE demonstrated 99.7% extraction at 1 g/day = **~200× throughput scale-up** for extraction | 30-year FLiBe loop lifetime / 2-year MSRE static loop = **15× lifetime extrapolation**; ~200 g/day extraction required / TSTA 100 g/day (fueling) = **2× scale-up** |
| **Closure mechanism** | Validate TBR via neutronics mock-ups (D-T neutron generator or fission-fusion hybrid blanket test); build tritium extraction pilot loop (flowing FLiBe or LiPb at 10-50 L/min) and demonstrate >99% extraction at 10-50 g/day for 1+ year. | Develop advanced corrosion-resistant alloys for FLiBe (improved Hastelloy-N or Mo-based alloys); test at 650°C for 5-10 years with flowing salt. Develop tritium permeation barriers for FLiBe-to-steam HX (ceramic coatings, double-wall HX with He sweep). Secure startup tritium from CANDU production or DOE reserve (1 kg = $35M). |
| **Classification** | **Binary** — if TBR < 1.0 (after extraction losses and inventory holdup), plant cannot sustain tritium self-sufficiency and must purchase external tritium (not available at scale); plant shuts down | **Degrading** — if FLiBe corrosion requires loop replacement every 10-15 years (vs. HYLIFE-II 30-year claim), replacement CAPEX ($50-100M) and availability loss degrade LCOE; if tritium permeation to steam exceeds regulatory limits, additional cleanup systems add OPEX |
| **Evidence tier** | **Tier 3** — MSRE demonstrated tritium extraction from FLiBe at small scale (1 g/day, 99.7%) in fission-bred environment (adjacent: similar chemistry, different scale). Neutronics calculations (TBR 1.05-1.2) are Tier 2 (simulation with no fusion blanket validation). **Cite**: MSRE 1965-1969 operations (Haubenreich & Engel, Nucl. Appl. Tech. 1970); HYLIFE-II TBR calculation (Moir 1994, OSTI 7021072). | **Tier 3** — MSRE FLiBe loop (2-year operation at 650°C, subscale); TSTA tritium processing (100 g/day scale, different chemistry — gas fueling not FLiBe extraction). EU-DEMO PbLi program is Tier 2 (design + component tests, no full blanket loop). **Cite**: MSRE final report (ORNL-4548, 1969); TSTA operations summary (LANL LA-UR-88-3739). |

**Function 6 mean**: (3 + 3) / 2 = **3.0**

---

#### Function 7: Power Conversion & BOP

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | Steam Rankine cycle (HYLIFE-II baseline): thermal efficiency ~35-38% at 500-550°C steam conditions; pulse smoothing of 6 Hz pulsed heat input (350 MJ/shot = 2.1 GW pulsed thermal at 6 Hz) via FLiBe thermal inertia; load-following capability for grid integration | FLiBe-to-steam heat exchanger (HX) operates at 500-650°C FLiBe primary / 500-550°C steam secondary for 30 years; tritium permeation barriers prevent T₂ contamination of steam (<1 Ci/day to environment); steam turbine operates with pulsed thermal input (frequency content smoothed by FLiBe thermal mass, but temporal variations in steam conditions may stress turbine blades) |
| **Best demonstrated** | Conventional steam Rankine cycle: mature commercial technology deployed at coal, nuclear (PWR/BWR), and CSP plants at 33-42% efficiency (500-600°C steam). MSR/FHR heat transport: MSRE operated FLiBe → air HX (not steam) at 650°C (1960s). | Fission reactor steam generators: stainless steel tube bundles with FLiBe or NaK on primary side (MSR, sodium fast reactors) operating for decades. Tritium permeation barriers: under development for fusion (ceramic coatings, double-wall HX with He sweep) but not deployed at power-plant scale. Steam turbines: operate with constant steam conditions (no pulsed input analog). |
| **Gap ratio** | N/A — steam Rankine physics is mature | FLiBe-to-steam HX with tritium barriers: 30-year lifetime required / 2-year MSRE (FLiBe-to-air, no steam, no tritium) = **15× lifetime extrapolation**; pulsed thermal input: 6 Hz power variations / steady-state turbines = undefined (novel operating regime) |
| **Closure mechanism** | Validate FLiBe-to-steam HX with tritium permeation barriers via pilot-scale loop (10-50 MWth) operating for 2-5 years; measure tritium permeation <1 Ci/day. Validate pulse smoothing via FLiBe thermal inertia modeling (thermal mass of primary loop smooths 6 Hz to <1% steam pressure variation). Turbine vendor (GE, Siemens) evaluates compatibility with smoothed pulsed input. | Develop and test ceramic permeation barrier coatings (Al₂O₃, Er₂O₃, or equivalent) on HX tubes at 600-650°C; irradiate to 1-5 dpa and measure permeation rates. Demonstrate double-wall HX with He sweep at 50 MWth scale. Commission turbine with thermal input variation <1% (equivalent to smoothed 6 Hz after FLiBe buffering). |
| **Classification** | **Degrading** — if FLiBe-to-steam HX efficiency is lower than conventional (due to added permeation barrier resistance), eta_th drops from 35% to 30-32% and LCOE rises by ~8-10% (elasticity -0.23); if tritium permeation exceeds limits, additional cleanup systems add OPEX | **Degrading** — HX replacement every 10-15 years (if corrosion or permeation barrier degradation) adds $20-50M CAPEX per cycle and 2-4 week outage (availability loss); steam turbine fatigue from pulsed input (if smoothing insufficient) shortens blade lifetime and raises O&M |
| **Evidence tier** | **Tier 4** — Steam Rankine cycle is operating-regime demonstrated at commercial scale (GW-class coal/nuclear plants at 500-600°C steam, 33-42% efficiency). **Cite**: conventional PWR steam generators (Westinghouse, Framatome) at 500-550°C, 33-35% cycle efficiency; supercritical coal plants at 600°C, 40-42% efficiency. | **Tier 3** — Fission reactor FLiBe HX is adjacent (MSRE FLiBe-to-air, 2-year operation, no steam, no tritium barriers). Tritium permeation barriers are Tier 2 (lab-scale development, no power-plant deployment). Pulsed thermal input is Tier 2 (HYLIFE-II analytical model with no experimental validation). **Cite**: MSRE HX operations (ORNL-4548, 1969); tritium permeation R&D for fusion (ongoing EU-DEMO program, not yet demonstrated at scale). |

**Function 7 mean**: (4 + 3) / 2 = **3.5**

---

### Function-level means summary (before heritage credit):

| Function | F_n | Justification |
|----------|-----|---------------|
| F1 (Plasma Performance) | 2.0 | No HIF ignition demonstrated; target gain and fabrication are simulations + subscale demos |
| F2 (Driver / Energy Input) | 2.0 | Driver-scale induction linac is 1,000-5,000× extrapolation from NDCX-II; components are TRL 5-6 but integration is paper |
| F3 (Instability Control) | 2.0 | Direct-drive symmetry requirements unvalidated; target injection at 6 Hz is subscale from NIF |
| F4 (Plasma-Wall Interaction) | 2.0 | FLiBe liquid wall clearing at 6 Hz is analytical + water surrogates; no fusion-yield demonstration |
| F5 (Neutron/Particle Handling) | 2.5 | Bulk shielding is simulation (Tier 2); final focus magnet irradiation is subscale (Tier 3, PWR steel analog) |
| F6 (Fuel Cycle Closure) | 3.0 | MSRE demonstrated tritium extraction from FLiBe at subscale (Tier 3); TBR calculations are Tier 2 but MSRE provides adjacent validation |
| F7 (Power Conversion & BOP) | 3.5 | Steam Rankine is commercial (Tier 4); FLiBe-to-steam HX is adjacent from MSRE (Tier 3); tritium barriers are Tier 2 (dev stage) |

### Heritage credit (D-T fuel):

HIF has **no heritage floor** — not in the heritage lineage table. HIF is a novel IFE approach with no predecessor public fusion experiments at ignition-relevant scale. NDCX-II is a research platform, not a reactor prototype. The heavy ion accelerator heritage (LBNL HIF program, GSI heavy ion physics) is for scientific instruments, not fusion drivers. Therefore, **no heritage credit applies** — F1-F7 remain as computed.

---

### Binary risks identified:

From the 14-cell risk matrix, the following risks are classified as **binary** (zero net electricity if unmitigated):

1. **F1 Physics (Target gain < 30)**: If HIF target gain falls below ~30, Q_eng < 3 and plant cannot achieve net electricity
2. **F1 Hardware (Target fabrication failure)**: If target throughput cannot achieve 6 Hz or quality control fails, shots stop and plant shuts down
3. **F2 Physics (Beam delivery failure)**: If beam cannot deliver 5-8 MJ to target with <5 mm spot size, target gain collapses
4. **F2 Hardware (Driver availability <80%)**: If driver component failures drop availability below ~75%, plant LCOE exceeds $100/MWh and commercial viability fails (not "zero net electricity" but "uncompetitive" — reclassify as Degrading)
5. **F3 Physics (Compression asymmetry >5%)**: Prevents ignition; target gain collapses below 30 and plant fails
6. **F4 Physics (FLiBe jet reformation failure)**: If jets fail to reform or vapor pressure rises above beam transport threshold, shots stop
7. **F6 Physics (TBR < 1.0)**: Plant cannot sustain tritium self-sufficiency; must shut down (no external tritium available at scale)

**Correction**: F2 Hardware (driver availability) is reclassified as **Degrading** — driver availability <80% raises LCOE via the -0.96 elasticity, but plant still operates (just uneconomically). Not a zero-net-electricity failure.

**Final binary risks** (6 total):
1. F1 Physics: Target gain < 30
2. F2 Physics: Beam delivery failure (cannot achieve 5 MJ at <5 mm spot)
3. F3 Physics: Compression asymmetry >5%
4. F4 Physics: FLiBe jet reformation failure or vapor pressure exceeds beam transport threshold
5. F6 Physics: TBR < 1.0 (tritium self-sufficiency failure)
6. F1 Hardware: Target fabrication throughput failure (cannot sustain 6 Hz with quality control)

---

## YAML Scores Block

```yaml
---
scores:
  C1: 5.0
  C3: 2.8
  C4: 3.5
  C5: 1.7
  C8: 3.2
  F1: 2.0
  F2: 2.0
  F3: 2.0
  F4: 2.0
  F5: 2.5
  F6: 3.0
  F7: 3.5
  binary_risks:
    - "F1 Physics: Target gain < 30 prevents net electricity (Q_eng < 3)"
    - "F2 Physics: Beam delivery failure (cannot achieve 5-8 MJ at <5 mm spot size) collapses target gain"
    - "F3 Physics: Compression asymmetry >5% prevents ignition"
    - "F4 Physics: FLiBe jet reformation failure or vapor pressure exceeds beam transport threshold stops shots"
    - "F6 Physics: TBR < 1.0 prevents tritium self-sufficiency; no external supply at scale"
    - "F1 Hardware: Target fabrication throughput failure (cannot sustain 6 Hz with quality control) stops plant operation"
---
```
