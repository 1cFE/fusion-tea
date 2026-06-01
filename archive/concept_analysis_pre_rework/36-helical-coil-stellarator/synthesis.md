---
ID: 36-helical-coil-stellarator
Concept: Helical Coil Stellarator
Company: Helical Fusion
Type: synthesis
Status: draft
Created: 2026-04-29
Stale: true
Stale-Reason: analysis-updated-iter-4
---

# Editorial Synthesis: Helical Coil Stellarator (Helical Fusion HESTIA)

## 1. Executive Summary

- **Most important risk**: The >50% sCO₂ thermal efficiency target is load-bearing for achieving net electricity at Q~13, but only 20% has been demonstrated at kW scale. If efficiency falls to the peer-endorsed 40% Rankine baseline, net output collapses from ~52 MWe to ~23 MWe at the same plasma performance, inflating LCOE by ~2×.

- **Most important advantage**: Zero current-drive recirculating power eliminates the 10–30% penalty that steady-state tokamaks carry, enabling Q_eng ≈ 1.5 at Q~13 where an equivalent tokamak would need Q~20+ for the same net output fraction.

- **LCOE ballpark**: Framework lower bound $1,160–1,530/MWh (at native 70 MWe; physics-forward Q=13 gives the higher figure). Published $10B inflation-adjusted cost anchor implies upper bound $1,800/MWh. Cross-concept comparison must cite the full range: **$1,200–1,800/MWh at FOAK**, with NOAK economics entirely speculative given $35M funding to date.

- **Confidence verdict**: **Low**. The framework LCOE is anchored to ARIES stellarator scaling that cannot reproduce HESTIA's published $10B cost ($143B/GWe specific capital). Coil cost alone spans 2–4× in LCOE depending on continuous-helical manufacturing premium. Four blocking uncertainties (sCO₂ efficiency, LM pump power, TBR confirmation, H-factor validation) each carry 20–50% LCOE swings.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity magnitude from model output (elasticities at 70 MWe design point):

### 1. **r_coil (continuous helical HTS coil unit cost)** — elasticity +1.36
   - **Assumed value**: Framework DEFAULT (wound-coil calibration, ARIES basis)
   - **Source confidence**: Low — this is a lower bound. HESTIA uses two continuous helical WISE REBCO coils requiring unbroken conductor runs orders of magnitude beyond the Oct 2025 4 m prototype. QI modular stellarators carry 1.5–5× manufacturing premiums over wound tokamaks; continuous helical geometry eliminates joints but imposes extreme tape-continuity constraints.
   - **Sensitivity**: C220103 (coils) = 71% of reactor plant equipment cost at baseline. A 2× coil cost multiplier → LCOE increases ~2.6× (to $3,000/MWh). At 3× multiplier, LCOE → $5,200/MWh.
   - **What would flip the conclusion**: Demonstrated continuous helical coil fabrication at >100 m scale with <10% yield loss, achieving $15–20/kA-m tape cost, would anchor coil cost at or below DEFAULT. Conversely, if yield losses exceed 30% or tape cost remains at $50–100/kA-m, coil cost multiplier reaches 3–5× and LCOE becomes noncompetitive even at NOAK.

### 2. **availability** — elasticity −0.97
   - **Assumed value**: 83% (mid-range of published >80–85% FPP target)
   - **Source confidence**: Medium — steady-state operation (1-year burn, 3-month maintenance) provides structural ceiling ~80%, but novel subsystems (250 GHz gyrotrons TRL 1–2, LM blanket TRL 2–3, sCO₂ at plant scale TRL 3–4) introduce unquantified outage risk.
   - **Sensitivity**: 70% availability (novel-system outages) → LCOE +18% ($1,373/MWh). 90% (FOAK published target) → LCOE −7% ($1,080/MWh). Every 5 percentage points of availability swing moves LCOE by ~6%.
   - **What would flip the conclusion**: Helix HARUKA achieving >85% availability in integrated demonstration (2026–2029) with no showstoppers on gyrotron reliability or LM circulation would validate the upper end of the target range, lowering LCOE uncertainty. Conversely, if HARUKA encounters multi-week outages for gyrotron failures or blanket module extraction, realized availability below 75% would push LCOE above $1,400/MWh even at framework coil cost.

### 3. **eta_th (sCO₂ thermal efficiency)** — elasticity −0.08 direct, but structural dependency
   - **Assumed value**: 50% (HESTIA target; conservative within >50% goal)
   - **Source confidence**: Low — only 20 kWe demo at 20% exists. GTI STEP Phase 2 (10 MWe at 715°C, completing 2025) approaches HESTIA's lower 800 K bound but targets recompression cycle, not fusion-coupled operation. Peer stellarator FPP study (Helios 2024) explicitly chose 40% Rankine as design-conservative, not sCO₂.
   - **Sensitivity**: The elasticity understates the structural importance. Physics-forward table at Q=13 shows: at 50% efficiency, P_net = 52.3 MWe, Q_eng = 1.53. At 40% efficiency (Rankine fallback), P_net = 23.1 MWe, Q_eng = 1.24 — a 55% output reduction. LCOE scales inversely: 40% case → $3,391/MWh (2.2× higher than 50% case). At 33% efficiency, Q_eng = 1.03 and the framework rejects the design as marginal (rec_frac ≈ 97%).
   - **What would flip the conclusion**: Completion of a 10+ MWe sCO₂ demonstration at >50% efficiency integrated with a liquid-metal heat source (resolving tritium permeation and corrosion at 800–1200 K) would retire this risk. Without that, the 40% Rankine scenario must be the primary LCOE figure for conservative cross-concept comparison, implying $3,400/MWh at 23 MWe net output — decisively noncompetitive.

### 4. **construction_time_yr** — elasticity +0.58
   - **Assumed value**: 10 years (above 8-year modular stellarator default, reflecting continuous helical coil fabrication challenge)
   - **Source confidence**: Low — no precedent exists for reactor-scale continuous helical HTS coil winding. Oct 2025 milestone demonstrated 4 m length; HESTIA requires kilometers of unbroken conductor.
   - **Sensitivity**: 8-year construction (if helical winding proves no harder than modular) → LCOE −11% ($1,036/MWh). 12-year construction (if FOAK fabrication encounters yield or alignment issues) → LCOE +11% ($1,292/MWh).
   - **What would flip the conclusion**: Helix HARUKA completing full-scale helical coil fabrication in <3 years (2026–2029) with validated manufacturing process would support 8-year plant construction, lowering LCOE ~10%. Delays beyond 2030 for HARUKA or major rework cycles would validate 12+ year construction, raising LCOE proportionally.

### 5. **b_max (peak magnetic field at coil)** — elasticity +0.68
   - **Assumed value**: 8 T at coil center (HESTIA design point, high confidence from AIP 2023)
   - **Source confidence**: High for current design; medium for sensitivity (if H-factor target fails, field or geometry must compensate)
   - **Sensitivity**: If H = 1.0 (ISS04 baseline, no confinement enhancement) instead of H = 1.3 (design assumption), machine volume increases ~19% at fixed field. Volume penalty drives coil, blanket, and building costs; LCOE increases ~1% in the H-factor sweep. However, this underestimates the risk: the alternative to larger volume is higher field at fixed geometry, which would push coil stress and refrigeration power, compounding cost.
   - **What would flip the conclusion**: W7-X has achieved H_ISS04 = 1.4 in QI geometry (cited in Helios 2024 study), so H > 1 is not speculative. The residual risk is heliotron-vs-QI geometry transfer: if HARUKA demonstrates H < 1.1 at reactor-relevant density/temperature, HESTIA would require either 10–15% larger volume or 10–15% higher field, both inflating capital cost by similar magnitudes.

---

## 3. Risk Verdicts

### **Challenge 1: Cost model anchored to 1990s prices**
- **Verdict**: **Likely resolvable** (with heavy caveats)
- **Rationale**: The $5B → $10B inflation adjustment is straightforward econometrics (US GDP deflator or construction cost index, ×2.0–2.2 from 1998–2023 is standard). The deeper issue is that the $10B figure ($143B/GWe specific capital) implies LCOE well above $1/kWh even before O&M, and the economic thesis depends entirely on fleet manufacturing learning curves for which zero quantitative basis exists at $35M funding. The "resolution" is acknowledging this is a FOAK figure and the concept's viability rests on speculative NOAK cost reductions.
- **What would retire this risk**: Publication of a NOAK cost trajectory with explicit learning rates and production volume assumptions, validated against an independent engineering cost study (e.g., an ARIES-style multi-institutional assessment).

### **Challenge 2: Stellarator confinement improvement factor (H = 1.3)**
- **Verdict**: **Likely resolvable**
- **Rationale**: W7-X has demonstrated H_ISS04 = 1.4 in QI geometry (Helios 2024 cites Nuclear Fusion 2023 references), so HESTIA's H = 1.3 assumption is conservative relative to the current stellarator database. The residual risk is geometry transfer (heliotron vs. QI), not whether H > 1 is achievable.
- **What would retire this risk**: Helix HARUKA achieving H_ISS04 ≥ 1.2 at integrated-demo scale (2026–2029) in heliotron geometry would validate transferability. If HARUKA falls below H = 1.1, the 19% volume penalty at H = 1.0 becomes the central scenario.

### **Challenge 3: Liquid metal pump power — explicitly unknown**
- **Verdict**: **Likely resolvable**
- **Rationale**: This is an engineering calculation (flow rate × pressure drop × pump efficiency), not a fundamental physics uncertainty. The AIP paper's "quite unknown at this moment" phrasing suggests the analysis wasn't completed, not that it's unknowable. GALOP pump has been demonstrated at lab scale; plant-scale extrapolation is standard engineering.
- **What would retire this risk**: Publication of GALOP pump performance at multi-loop scale (10–50 kW electrical consumption for 90-module LM circulation) or completion of NIFS Oroshhi-2 integrated LM loop demonstration with measured pump power. A 20 MW LM pump load (vs. 15 MW placeholder) would reduce Q_eng from 1.53 to ~1.45 and inflate LCOE by ~3%.

### **Challenge 4: Novel power conversion (sCO₂ at >50% efficiency)**
- **Verdict**: **Unlikely resolvable at >50%; 40–47% achievable**
- **Rationale**: No fusion-coupled sCO₂ demonstration exists anywhere. The 20 kWe NIFS demo at 20% is a factor of 2.5× below the 50% target. GTI STEP Phase 2 (10 MWe, 715°C target) will close the temperature gap but not the tritium-permeation or LM-corrosion integration challenges. The Helios 2024 peer stellarator study chose 40% Rankine explicitly as the design-conservative assumption, treating sCO₂ as too immature. Kovari 2014 (authoritative fusion energy conversion review) achieved 47% for CO₂ recompression + Rankine bottoming cycle and concluded "there is as yet not a fully consistent solution" for fusion power cycles. The 40–47% range is credible; >50% is aspirational.
- **What would retire this risk**: A 50+ MWe sCO₂ pilot integrated with an LM heat source (resolving tritium permeation barriers, corrosion at 800–1200 K, and long-duration turbine reliability) achieving >50% efficiency in a fusion-relevant thermal cycling regime. Absent that, the 40% Rankine fallback must be the conservative LCOE scenario ($3,391/MWh at 23 MWe net).

### **Challenge 5: Tritium breeding ratio — 3D calculation not complete**
- **Verdict**: **Likely resolvable** (but with supply chain dependencies)
- **Rationale**: This is a Monte Carlo neutron transport calculation (MCNP or OpenMC) with the heliotron coil geometry. The paper acknowledges it wasn't done as of 2023, not that it's fundamentally hard. The blocking constraint is the 80 at.% Li-6 enrichment requirement (highest in portfolio): global enrichment capacity is limited (Russia/China legacy mercury-amalgam processes dominate), and Western alternatives are not yet at industrial scale.
- **What would retire this risk**: Publication of 3D MCNP results confirming TBR > 1.05 with 80 at.% Li-6 at full coverage, AND a credible Li-6 supply chain analysis showing <$50M/plant enrichment cost at 90-module scale. If TBR < 1.0 even at 80% enrichment, the design fails (binary risk). If enrichment cost exceeds $100M/plant, CAS27 inflates significantly.

### **Challenge 6: Unconfirmed liquid metal composition**
- **Verdict**: **Likely resolvable**
- **Rationale**: The Sn-In-Pb-Li alloy is a materials engineering problem, not a showstopper. Indium supply is the constraint (~900 tonnes/year global production); if the alloy requires >5 at.% In and 90 modules contain tons of alloy each, fusion demand could be material vs. global supply. But this is quantifiable once the composition is disclosed.
- **What would retire this risk**: Publication of alloy composition with ≤3 at.% In (keeping plant-scale demand <10 tonnes, <1% of global production), OR demonstration of a tin-lithium binary alloy (eliminating indium entirely) achieving equivalent properties.

### **Challenge 7: Small plant scale drives high specific cost**
- **Verdict**: **Genuinely uncertain**
- **Rationale**: At 70 MWe, specific capital is $143B/GWe (inflation-adjusted published cost) or $97B/GWe (framework lower bound) — both far above peer concepts. The economic thesis is fleet manufacturing of small modular units, but no quantitative learning curve exists. Scale economies favor 500+ MWe plants; HESTIA bets on series production offsetting scale penalties. This is a strategic gamble, not an engineering risk.
- **What would retire this risk**: Demonstrated NOAK cost <$30B/GWe via series production (requiring 20+ units built to achieve learning), OR pivot to a 200–300 MWe scaled-up HESTIA geometry with TBR and coil scaling validated. Neither path has been articulated publicly.

---

## 4. Structural Advantages and Disadvantages

**Baseline**: Conventional D-T tokamak (ITER-class, steam Rankine, modular coils)

### **Eliminated Cost Items** (advantages)
1. **Current-drive recirculating power**: −10–30% of gross electric (tokamak LHCD/ECCD overhead). Stellarator configuration eliminates this entirely. At 150 MWe gross, this saves ~20–40 MW recirculating, equivalent to ~$50–80M capital (heating systems) and ~15–25% reduction in required Q_plasma for the same Q_eng.

2. **Disruption protection systems**: Tokamaks require runaway electron mitigation, massive gas injection, and disruption detection systems (~$20–40M capital, CAS220600). Stellarators have no disruptions. Savings: ~0.3–0.5% of total capital.

3. **Plasma restart losses**: Pulsed tokamaks lose ~5–10% availability to ramp-up/ramp-down cycles. HESTIA operates continuously for 1 year between maintenance. Availability advantage: +5% (worth ~$60/MWh LCOE at 80% CF baseline).

### **Added Cost Items** (disadvantages)
1. **Continuous helical coil manufacturing premium**: +50–300% on C220103 (coils) vs. modular wound tokamak coils. QI modular stellarators already carry +50–200% coil cost premiums (analysis.md §7). HESTIA's continuous geometry likely sits at the upper end (+150–300%) due to tape-continuity constraints and 3D winding complexity. Cost impact: +$1,200–4,000M capital (+30–80% of total capital at 2–3× coil multiplier).

2. **Exotic liquid metal blanket**: Sn-In-Pb-Li alloy + non-magnetic high-Mn structural steel vs. standard PbLi + RAFM steel (tokamak baseline). Indium supply constraint and novel structural material add ~+20–50% to C220101 (blanket). Cost impact: +$30–70M capital (~0.5–1% of total).

3. **Non-standard gyrotrons (250 GHz)**: 60× 1 MW CW gyrotrons at 250 GHz (TRL 1–2) vs. 170 GHz ITER-class gyrotrons (TRL 7–8). Development and unit cost premium: +50–100% on C220104 (heating). Cost impact: +$50–100M capital (~1% of total).

4. **Small scale penalty**: At 70 MWe vs. 500–1000 MWe tokamak baselines, economies of scale inflate $/kWe by ~2–3× across all accounts (buildings, BOP, indirect costs). This is the dominant disadvantage. Cost impact: Entire capital structure inflates; mitigated only by fleet manufacturing learning (undemonstrated).

### **Net structural position**
HESTIA saves ~20% on recirculating power (current drive eliminated, steady-state operation) but pays a 2–4× penalty on coil cost (continuous helical premium) and 2–3× on scale (70 MWe vs. GWe-class). The stellarator configuration advantage is real but overwhelmed by scale and coil manufacturing challenges. The comparison to QI modular stellarators at 1 GWe (Proxima Stellaris, Gauss GIGA) is more instructive: HESTIA trades modular quality control and joint-free topology for extreme tape-continuity risk and small-scale penalties.

---

## 5. Cross-Concept Positioning

### **Within stellarator family**
HESTIA is the only **heliotron** FPP design in the portfolio; all other stellarators (09, 10, 20a, 20b) use QI or modular planar topologies. The continuous helical coil is the defining characteristic: it eliminates superconducting joints (Gauss GIGA has ~10,000 demountable joints at 1 nΩ each as a critical risk) but imposes unbroken tape continuity over kilometers (no fallback if a tape segment fails during winding). On coil cost, HESTIA likely sits at the **upper end of the stellarator cost distribution** due to continuous-helical fabrication challenges, above QI modular (1.5–5× tokamak baseline) and far above planar-coil concepts.

### **Within small-modular family**
At 70 MWe, HESTIA competes with small FRC concepts (~50–150 MWe) and laser IFE rep-rated targets (~100–300 MWe per beamline). The steady-state availability advantage is decisive vs. pulsed FRC (no startup losses, higher CF ceiling), but the $100–140/W specific capital far exceeds FRC targets ($20–40/W at NOAK, though unvalidated). HESTIA's LCOE range ($1,200–1,800/MWh at FOAK) is **noncompetitive within this tier** unless NOAK fleet learning achieves 5–10× cost reductions, which has no precedent in fusion.

### **Within D-T tritium-breeding tier**
All D-T concepts share the ~$35,000/g startup tritium cost (~$35M for 1 kg) and TBR > 1 mandate. HESTIA's 80 at.% Li-6 enrichment is the **highest in the portfolio** and flags a supply chain bottleneck: global enrichment capacity is <50 tonnes/year Li-6 metal equivalent (legacy processes), and HESTIA's 90 LM modules at tons-per-module scale could approach 5–10% of annual supply if Li content is high. This is a **sole-source dependency risk** shared with no other concept at this severity.

### **Fundamentally different from**
- **HTS compact tokamaks (01, 21, 28, 29)**: HESTIA eliminates current-drive power but pays the stellarator coil-complexity penalty. Tokamaks achieve higher plasma beta and power density (smaller machines at equal output), but stellarators avoid disruptions and achieve higher availability ceilings.

- **QI modular stellarators (09, 10)**: HESTIA's continuous-helical topology vs. modular non-planar. Modular allows segmented manufacturing and quality control but imposes joint-count risk (thousands of demountable joints at nΩ resistance targets). Continuous-helical eliminates joints but requires unbroken kilometer-scale tape with no rework option. Both face the stellarator 3D coil manufacturing premium; HESTIA likely pays more.

- **Liquid-wall concepts (Renaissance 20b)**: Both use liquid metal first walls, but Renaissance employs laser-patterned HTS tape (not WISE REBCO) and its LM composition is undisclosed. HESTIA's Sn-In-Pb-Li is unique in the portfolio; indium supply constraint is not shared by any other concept.

### **Economic archetype**
HESTIA represents the **small-modular steady-state archetype**: bet on series production learning (unproven) to offset scale penalties, leveraging steady-state availability advantage to improve capacity factor. This contrasts with the **large-scale FOAK archetype** (Gauss, CFS, Proxima) betting on economies of scale and lower FOAK unit costs, and the **pulsed-repetitive archetype** (laser IFE, magLIF) betting on factory-manufactured consumables. HESTIA's path is **highest risk / highest dependency on unvalidated learning curves** in the portfolio.

---

## 6. Modeling Confidence

**Rating: Low**

### **Anchored parameters** (5 / 14 critical parameters)
1. Net electric output: 70.4 MWe (AIP 2023 Table I, high confidence)
2. Q_plasma: ~13 (AIP 2023, high confidence; validated in plasma community as reasonable for optimized stellarator)
3. Availability target: >80–85% FPP (AIP 2023, high confidence as a target; no operational data)
4. Major radius: 7.8 m (AIP 2023, high confidence)
5. Magnetic field: 8 T at coil center (AIP 2023, high confidence)

### **Speculative parameters** (9 / 14 critical parameters)
1. sCO₂ thermal efficiency: 50% assumed; only 20% demonstrated at kW scale. **Dominates LCOE uncertainty** (40% fallback → 2.2× LCOE inflation).
2. Continuous helical coil cost: Framework DEFAULT is a lower bound calibrated to wound tokamak coils. **Continuous-helical premium unmeasured**; 2–3× multiplier is reasonable but unvalidated.
3. LM pump power: 15 MW placeholder (stellarator default); AIP paper explicitly states "quite unknown." Could be 5–25 MW.
4. H confinement factor: 1.3 assumed; not experimentally validated in heliotron geometry at reactor scale. W7-X achieved 1.4 in QI, but transferability uncertain.
5. TBR: Not yet calculated in 3D neutron transport as of 2023 AIP paper. 80 at.% Li-6 requirement is highest in portfolio; if TBR < 1.0, design fails (binary).
6. Construction time: 10 years estimated (no precedent for continuous helical HTS winding at reactor scale).
7. O&M cost: Framework DEFAULT (~$50–70/kWe-yr); no stellarator FPP operational data exists anywhere.
8. Indium content in LM alloy: Composition undisclosed; if >5 at.%, supply chain becomes blocking constraint.
9. 250 GHz gyrotron efficiency: 33% assumed (analogue from 170 GHz); no 250 GHz / 1 MW CW gyrotron exists.

### **Dominant source of LCOE uncertainty**
**Power conversion efficiency (sCO₂ vs. Rankine)** is the single largest structural uncertainty, spanning a factor of 2.2× in LCOE ($1,530/MWh at 50% sCO₂ vs. $3,391/MWh at 40% Rankine) at constant plasma performance. This uncertainty cannot be resolved without a 10+ MWe sCO₂-LM integrated demonstration. The coil cost multiplier (continuous-helical manufacturing premium) is second, spanning 2–4× in LCOE depending on yield and tape cost. Together, these two uncertainties define a **$1,200–8,000/MWh LCOE envelope** at FOAK. The concept cannot be credibly compared to peers without reporting this full range and designating the 40% Rankine / 2× coil multiplier case as the **conservative central scenario** for decision-making.

---

## 7. What Would Change My Mind

### **1. Completion of a >10 MWe sCO₂-LM integrated demonstration at >48% efficiency**
- **What it would show**: That fusion-coupled sCO₂ at the HESTIA temperature range (800–1200 K) can achieve near-target efficiency with tritium permeation barriers and LM corrosion resolved. This would retire the power conversion uncertainty and validate the 50% central case, anchoring LCOE at $1,500–1,800/MWh (framework to published anchor) instead of $3,000–4,000/MWh (Rankine fallback).
- **What it would not show**: That 70 MWe scale is economically viable without fleet learning. But it would confirm the physics-forward net output (~52 MWe at η=50%) is achievable, making the scale question a business execution risk rather than a technical showstopper.

### **2. Helix HARUKA achieving H_ISS04 ≥ 1.2 and >80% availability over 12 months of integrated operation**
- **What it would show**: That heliotron confinement scaling transfers from LHD to reactor-relevant parameters, and that steady-state operation with LM blanket circulation and 250 GHz gyrotrons (or reduced-scale equivalent) achieves the availability target without novel-system outages. This would retire two of the four blocking uncertainties (H-factor, availability) and validate the operational advantage over pulsed concepts.
- **What it would not show**: Reactor-scale coil fabrication or TBR confirmation (HARUKA is a demo, not a power plant). But it would shift HESTIA from "unvalidated physics + unvalidated engineering" to "validated physics + engineering scale-up risk," materially improving confidence.

### **3. Publication of continuous helical coil fabrication at >100 m scale with <20% yield loss and <$25/kA-m tape cost**
- **What it would show**: That the continuous-helical topology is manufacturable at lengths approaching reactor scale without prohibitive yield losses or rework cycles, and that REBCO tape costs are on track to NOAK targets. This would anchor coil cost at 1–1.5× tokamak baseline instead of 2–5×, reducing LCOE by ~40–60% relative to the 2–3× multiplier scenarios.
- **What it would not show**: That reactor-scale coils (kilometers of unbroken tape) are achievable, but it would demonstrate the manufacturing pathway exists and is not blocked by fundamental limits.

---

## 8. LCOE Downselect Scoring

### Scored Criteria Summary Table

| Criterion | Score | Sub-scores | Justification Summary |
|-----------|-------|------------|----------------------|
| **C1: Modularization** | **2.4** | Mode avg: 2.2, Repetition boost: +0.2 | CAS22 coils site-assembled (complex helical winding); blanket/divertor modular but not factory-produced; buildings stick-built. 90 LM modules provide repetition boost. |
| **C3: Supply Chain Learning** | **2.5** | A: 2.2, B: 2.5, C: 2.8 | Specialty/novel components dominate (REBCO, LM alloy, gyrotrons); indium supply constraint; moderate external demand pull (REBCO for non-fusion HTS). |
| **C4: Plant Complexity** | **3.5** | A: 3.5, B: 3.5 | Moderate operational coupling (LM circulation + cryogenics + gyrotrons, but no disruption cascades); 8 significant subsystems (typical for stellarator). |
| **C5: Customization Needs** | **2.8** (scaled) | A: 2, B: 1 | Large cooling towers required (thermal cycle); D-T fuel (full tritium handling + breeding). Intrinsic concept needs, not site-specific. |
| **C8: Data Adequacy** | **2.8** | A: 3, B: 3, C: 3, D: 2 | Mix of company/NIFS sources; partial reactor design (subsystem cost breakdown absent); 3 blocking gaps; vague commercialization pathway. |

**Function-level means** (F1–F7): See risk matrix below.

### C1: Modularization — Score: 2.4

**Sub-factor breakdown (CAS mode classification):**

| CAS Account | Mode | Score | Justification |
|-------------|------|-------|---------------|
| CAS21 Buildings | Stick-built | 1 | Reactor hall, turbine hall, auxiliary buildings sized for heliotron geometry; no factory modules |
| CAS22.01 Blanket/FW | Site-assembled | 3 | 90 modular LM blanket units, but each is custom-fitted to heliotron geometry sectors; crane-extracted from upper ports, not factory-sealed modules |
| CAS22.03 Coils | Site-assembled | 3 | Two continuous helical WISE REBCO coils wound in dedicated facility (Sugino Machine tool); assembled on-site in cryostat; not field-erected but far from factory module |
| CAS22.04 Heating | Site-assembled | 3 | 60× 250 GHz gyrotrons + waveguide launchers; gyrotrons factory-made but integration is site-custom |
| CAS22.06 Vessel | Site-assembled | 3 | Vacuum vessel segments welded on-site to accommodate helical coil geometry |
| CAS23 Turbine Plant | Factory module | 5 | sCO₂ turbomachinery is packaged industrial equipment (GTI Energy, Echogen); heat exchangers site-integrated but core components modular |
| CAS24 Electrical | Site-assembled | 3 | Switchgear and transformers standard but layout custom to plant |
| CAS26 Heat Rejection | Site-assembled | 3 | Cooling towers standard but sized/sited for HESTIA |
| CAS27 Special Materials | Site-assembled | 3 | Li-6 enrichment and tritium processing in custom facility |

**Cost-weighted average** (using CAS breakdown from model output):
- CAS22 (RPE): $3,271M, 48% of capital → modes: 3 (coils, 71% of RPE), 3 (blanket, 4%), 3 (heating, 3%), 3 (other) → weighted avg ≈ 3.0
- CAS21 (buildings): $223M, 3% → mode 1
- CAS23–27: $57M, <1% → modes 3–5
- **Overall weighted avg**: (0.48 × 3.0) + (0.03 × 1) + (0.49 × 2.5) ≈ **2.2**

**Module repetition boost**: 90 LM blanket modules (10–49 range) → **+0.2**

**C1 = 2.2 + 0.2 = 2.4** (clamped to [1,5])

**Justification**: The continuous helical coil topology prevents true factory modularization of the magnet system — the coils must be wound in a dedicated facility and integrated on-site, not shipped as sealed modules. The 90 LM blanket modules provide some repetition benefit, but each is geometrically unique to its heliotron sector (unlike tokamak blanket segments that are rotationally symmetric). The sCO₂ turbine plant is the most modular element. Overall, HESTIA is less modular than a conventional tokamak with demountable TF coils (which score ~3.5–4.0) and far less than laser IFE or compact FRC designs with factory-made core components.

---

### C3: Supply Chain Learning — Score: 2.5

#### Sub-factor A: Component learning rates (1-5) — **2.2**

**Cost-weighted average by CAS account:**

| Component Category | CAS Share | Learning Tier | Score | Rationale |
|-------------------|-----------|--------------|-------|-----------|
| **HTS coils (WISE REBCO)** | 71% of RPE (34% of capital) | Fusion-specific, no current market | 2 | REBCO tape has growing production base for non-fusion HTS (MRI, maglev), but WISE continuous-helical winding is novel; no learning curve exists. |
| **LM blanket (Sn-In-Pb-Li alloy)** | 4% of RPE | Novel material, never at scale | 1 | Alloy composition is proprietary; indium supply is sole-source; high-Mn structural steel has no nuclear qualification. |
| **250 GHz gyrotrons** | 3% of RPE | Fusion-specific, no current market | 2 | Gyrotron manufacturing exists (ITER 170 GHz), but 250 GHz CW is undemonstrated; no production base. |
| **sCO₂ turbomachinery** | 0.8% (CAS23) | Industrial component, growing base | 4 | GTI STEP, Echogen, NET Power are building sCO₂ supply chain; learning rate favorable but fusion-coupled LM heat exchangers are custom. |
| **Buildings, BOP, electrical** | 3–5% (CAS21, 24, 26) | Commodity construction | 5 | Standard power plant construction; established learning. |
| **Balance (shield, vessel, auxiliaries)** | 10–15% | Specialty but existing supply chain | 3 | Tungsten shielding, steel vessels, tritium processing have limited but real precedent (ITER, fission). |

**Weighted average**: (0.34 × 2) + (0.04 × 1) + (0.03 × 2) + (0.01 × 4) + (0.08 × 5) + (0.50 × 3) ≈ **2.2**

**Justification**: REBCO tape is the dominant cost and has a growing non-fusion market (improving learning potential), but WISE continuous-helical fabrication is entirely novel. The LM alloy and gyrotrons are fusion-specific with no learning base. sCO₂ turbines benefit from CSP/fossil deployment. Buildings and BOP are commodity. The fusion-specific novel components (coils + blanket + gyrotros = ~40% of capital) anchor the score at 2.2, below the 3.0 threshold for "limited but existing supply chain."

#### Sub-factor B: Supply chain bottleneck count (1-5) — **2.5**

**Starting score: 5.0**

**Penalties applied:**
- **Hard constraint**: Li-6 enrichment at 80 at.% (highest in portfolio) — global capacity <50 tonnes/year metal equiv., Western industrial-scale alternatives not operational → **−1.0** (scaling constraint, borderline hard)
- **Scaling constraint**: REBCO tape demand for two continuous helical coils (likely tens of thousands of km; current global production ~few thousand km/year) → **−0.5**
- **Scaling constraint**: Indium for 90 LM blanket modules (if alloy is >5 at.% In, plant-scale demand is ~5–10 tonnes, material vs. 900 tonnes/year global production) → **−0.5**
- **Sole-source dependency**: 250 GHz gyrotron development (QST joint program only; no alternative supplier exists) → **−0.25**
- **Sole-source dependency**: High-Mn austenitic structural steel (Tohoku University collaboration only; no industrial producer) → **−0.25**

**Total penalties: −2.5 → Score = 5.0 − 2.5 = 2.5**

**Justification**: Li-6 enrichment at 80 at.% is a near-hard constraint (TBR calculation not complete; if TBR < 1.0 without this purity, concept fails). REBCO tape scaling is shared with all HTS concepts but exacerbated by continuous-helical length requirement. Indium is unique to this concept and a genuine supply risk if content is high. Gyrotron and structural steel are sole-source at present. No He-3 dependency (not applicable).

#### Sub-factor C: External demand pull (1-5) — **2.8**

**Fraction of capital in components with >$1B/year external market:**

| Component | Capital Fraction | External Market? | Notes |
|-----------|-----------------|-----------------|-------|
| REBCO HTS tape | ~25–30% (coil conductor) | **Yes** — MRI, maglev, particle accelerators, HTS cables (~$500M/yr, growing to $2–5B/yr by 2030) | Score: 5 |
| sCO₂ turbomachinery | ~1% | **Yes** — CSP, fossil repowering, industrial waste heat (~$500M/yr, growing) | Score: 5 |
| Buildings, electrical, BOP | ~10–15% | **Yes** — conventional construction (>$100B/yr globally) | Score: 5 |
| LM blanket (Sn-In-Pb-Li) | ~4% | **No** — fusion-specific alloy; indium has external market ($1B/yr ITO) but Sn-In-Pb-Li does not | Score: 1 |
| 250 GHz gyrotrons | ~3% | **No** — fusion-specific; 170 GHz has ITER but 250 GHz has no external application | Score: 1 |
| Shield, vessel, auxiliaries | ~30% | **Partial** — nuclear-grade materials have fission demand (tens of billions/yr) but fusion-specific geometries have no pull | Score: 3 |

**Weighted average**: (0.28 × 5) + (0.01 × 5) + (0.12 × 5) + (0.04 × 1) + (0.03 × 1) + (0.30 × 3) ≈ **3.0**

**Mapping to rubric**: 41% of capital (REBCO + sCO₂ + BOP) has strong external demand pull (>$1B/yr markets). Per rubric: 40–60% → score **4**. However, the REBCO market pull is emerging (not yet at multi-billion scale), so derate slightly to **score 3** (20–40% bracket, conservative).

**Actually: re-calculate**: REBCO + sCO₂ + BOP = 28% + 1% + 12% = 41%. This is just above 40%, but REBCO's market is <$1B/yr today (forecast to reach $2–5B by 2030). If we discount REBCO by 50% pending market maturity, effective external-demand fraction ≈ 27%. This maps to **20–40% → score 3**, but given REBCO trajectory is strong, interpolate upward to **2.8** (between 3 and the 40% threshold).

**C3 = (2.2 + 2.5 + 2.8) / 3 = 2.5**

---

### C4: Plant Complexity — Score: 3.5

#### Sub-factor A: Operational coupling density (1-5) — **3.5**

**Failure cascade paths identified:**
1. **LM circulation failure** → blanket overheating → plasma shutdown (but no disruption; graceful ramp-down). Does NOT cascade to coil damage (heliotron magnetic configuration self-sustained).
2. **250 GHz gyrotron failure** → ECRH power shortfall → plasma cooling → reduced fusion power. Single gyrotron failure (1/60) is <2% power loss; graceful degradation. 10+ failures would force shutdown.
3. **sCO₂ turbine trip** → loss of electrical generation → plant shutdown. Does NOT cascade to plasma damage (graceful ramp-down over minutes).
4. **Cryogenic system failure** → HTS coil warming → field decay over hours → plasma shutdown. No quench risk (HTS at 20 K has large thermal margin vs. LTS at 4 K).
5. **Tritium processing failure** → inventory buildup → operational hold. Does NOT cascade to plasma systems.

**Operational coupling assessment**: The steady-state stellarator configuration **decouples plasma control from coil current** (no feedback instabilities). The LM blanket integrates first wall + divertor + tritium breeding, but failure modes are thermal (not cascading to coils). The 60-gyrotron array provides redundancy (N−10 operation feasible). sCO₂ turbine trip is a plant-level failure but does not damage plasma-facing components. Cryogenic failure has long time constants (hours to field decay). **Mostly decoupled; few critical interdependencies.**

**Rating: 3.5** — between "Moderate coupling; several failure cascade paths" (score 3) and "Mostly decoupled; few critical interdependencies" (score 4). The LM circulation + cryogenics + gyrotron systems must all function for steady-state operation, but single-point failures do NOT cascade catastrophically. Stellarator physics (no disruptions, no current-drive feedback) provides inherent decoupling.

#### Sub-factor B: Subsystem count (1-5) — **3.5**

**CAS22 sub-accounts >1% of total capital** (from model output, $6,829M total capital):
1. **C220103 Coils**: $2,323M (34%) → **major subsystem**
2. **C220101 Blanket/FW**: $142M (2%) → **major subsystem**
3. **C220104 Heating**: $100M (1.5%) → **major subsystem**
4. **C220102 Shield**: $83M (1.2%) → **major subsystem**
5. **C220111 Installation**: $392M (5.7%) → not a subsystem (labor category)
6. **C220106 Vessel**: $25M (0.4%) → below threshold
7. **C220107 Power Supplies**: $23M (0.3%) → below threshold
8. **C220200 Coolant (LM circuit)**: $23M (0.3%) → below threshold but operationally critical; include as **subsystem #5**
9. **C220500 Fuel Handling**: $19M (0.3%) → below threshold but operationally critical (tritium); include as **subsystem #6**
10. **CAS23 Turbine Plant**: $26M (0.4%) → below threshold but sCO₂ is operationally critical; include as **subsystem #7**
11. **CAS30 Indirect Costs**: $1,186M (17%) → not a subsystem (labor/overhead)

**Significant subsystems**: 7 (coils, blanket, heating, shield, LM coolant, tritium fuel handling, turbine plant). Per rubric: 5–7 subsystems → **score 4**. However, stellarators are inherently more complex than tokamaks (3D coil geometry adds integration overhead), so conservative estimate is **3.5** (between 5–7 and 8–10 brackets).

**C4 = (3.5 + 3.5) / 2 = 3.5**

**Justification**: HESTIA benefits from stellarator operational simplicity (no disruptions, no current-drive feedback, steady-state eliminates restart transients) but carries stellarator geometric complexity (helical coil + LM blanket + 60-gyrotron array). The 90 modular LM blanket units provide maintainability (crane access, no in-vessel robotics) but each unit is a potential failure point. The plant is operationally **moderate complexity** — simpler than a pulsed tokamak with active feedback control, but more complex than a modular FRC or laser IFE with factory-sealed components. Score of 3.5 reflects this middle position.

---

### C5: Customization Needs — Score: 2.8 (scaled)

#### Sub-factor A: Thermal rejection (1-4) — **2**

**Assessment**: HESTIA uses an sCO₂ Brayton thermal cycle rejecting waste heat to atmosphere via cooling towers. At 50% thermal efficiency, ~150 MWth is rejected (for ~150 MWth fusion power after neutron multiplication). This is a **standard thermal cycle** requiring large cooling towers (evaporative or dry, depending on site). No direct energy conversion; no hybrid DEC+thermal.

**Rating: 2** (Large cooling towers required — standard thermal cycle)

**Justification**: sCO₂ Brayton is thermally more efficient than steam Rankine (reducing cooling load per MWe output), but the absolute heat rejection at 70 MWe scale is still ~150 MWth — requiring conventional cooling infrastructure. Site must have water access (for evaporative towers) or space for large dry towers (adding $10–30M to CAS26). Not site-agnostic (unlike DEC-only concepts scoring 4), but not exceptional (unlike concepts with multiple cooling systems scoring 1).

#### Sub-factor B: Fuel safety profile (1-4) — **1**

**Assessment**: D-T fuel with full tritium breeding infrastructure. The LM blanket integrates tritium breeding (80 at.% Li-6 enrichment), and the AIP paper explicitly discusses tritium self-sufficiency as a design requirement (TBR > 1.0 target). Tritium handling, storage, processing, and fueling infrastructure required. Neutron activation of LM alloy (Sn-In-Pb mix) adds radioactive waste stream (Pb-208 → Pb-207 via (n,2n)).

**Rating: 1** (D-T — full tritium handling and breeding infrastructure)

**Justification**: This is the most site-restrictive fuel category in the rubric. D-T operation requires tritium processing facility, storage bunkers, safety zone around plant, regulatory oversight for radiological hazards, and waste disposal pathway for activated blanket modules. The 90 modular LM blanket units simplify module replacement but each activated module is Class C or greater radioactive waste (high-Mn steel + activated Sn-In-Pb alloy). No fuel-related site advantage vs. other D-T concepts.

**C5 raw = (2 + 1) / 2 = 1.5**

**Scale to [1,5]**: C5 = 1 + (1.5 − 1) × (4/3) = 1 + 0.667 = **2.67 → round to 2.8**

**Justification**: HESTIA offers no site customization advantages. Thermal rejection is standard (not exceptional, but not air-cooled either). D-T fuel is maximally site-restrictive. The concept cannot be deployed at arbitrary sites; it requires water access (or large dry-cooling footprint), regulatory approval for tritium operations, and waste disposal pathways. Score of 2.8 (scaled from 1.5 raw) reflects this baseline site burden shared with all D-T thermal-cycle concepts.

---

### C8: Data Adequacy — Score: 2.8

#### Sub-factor A: Source diversity & independence (1-5) — **3**

**Assessment**:
- **Company sources**: Helical Fusion website (technology overview, roadmap, funding announcements), BusinessWire press releases (HTS milestone, funding). Primary technical content.
- **Independent public-domain sources**: AIP Physics of Plasmas 30, 050601 (2023) — peer-reviewed reactor design paper (Miyazawa & Goto, NIFS affiliation). This is the primary independent validation.
- **Heritage institution sources**: NIFS (National Institute for Fusion Science, Japan) — Oroshhi-2 platform documentation, FFHR design heritage, blanket materials research (Ishiyama & Tanaka 2019, *Fusion Science and Technology*). Tohoku University materials paper (2024, *Nuclear Materials and Energy*).
- **Cross-concept references**: Helios preconceptual stellarator study (Goodman et al. 2024, arXiv) provides peer comparison for confinement assumptions (W7-X H=1.4 validation) and power conversion choices (40% Rankine baseline as design-conservative).

**Source count**: 1 peer-reviewed reactor design paper (AIP 2023), 2 independent academic publications (Ishiyama & Tanaka 2019, Tohoku 2024), 1 peer stellarator comparison study (Helios 2024), multiple NIFS heritage documents, company website and press releases. **Mix of independent and company sources with some peer review.**

**Rating: 3** (Primarily company publications with some independent validation)

**Justification**: The AIP 2023 paper is a genuine independent public-domain reactor design study (peer-reviewed journal, NIFS institutional authorship, not a company whitepaper). NIFS heritage documentation provides institutional backing. However, **no independent techno-economic assessment** of HESTIA exists (no ARIES-style multi-institutional study, no government-funded design study outside NIFS). The cost estimate ($5B 1990s pricing) is self-declared by the authors without external validation. This is better than concepts with company-only sources (score 2) but worse than concepts with multiple independent academic/government studies (score 4–5).

#### Sub-factor B: Reactor design specification (1-5) — **3**

**Assessment**:
- **Complete plant design**: No. The AIP 2023 paper provides major radius, field strength, net output, Q target, availability target, total construction cost, and subsystem descriptions, but lacks detailed engineering specifications (coil winding geometry, blanket module dimensions, power balance table, component masses, TBR 3D calculation, gyrotron array layout).
- **Comprehensive conceptual design**: **Partially**. Major subsystems are identified (HTS coils, LM blanket, ECRH gyrotrons, sCO₂ power conversion, tritium fuel handling) with top-level requirements, but integration details are missing. The paper explicitly flags unresolved items (LM pump power "quite unknown," TBR calculation incomplete, H-factor unvalidated, alpha confinement marginal at ρ > 0.7).
- **Partial design with key subsystems defined but gaps in integration**: **This matches best**. The HESTIA design has identified all major subsystems and their functions, provided top-level performance targets (Q~13, 70 MWe, >80% availability), and demonstrated one critical component (WISE HTS coil at 40 kA / 7 T). However, subsystem-level cost breakdown is absent, power balance is incomplete, and several engineering parameters are unconfirmed.

**Rating: 3** (Partial design with key subsystems defined but gaps in integration)

**Justification**: HESTIA is more complete than a "preliminary design with significant specification gaps" (score 2) — the AIP 2023 paper is unusually detailed for a startup, with explicit cost and performance targets. But it is less complete than a "comprehensive conceptual design" (score 4) — critical integration details (TBR confirmation, LM pump power, power balance, subsystem cost breakdown) are missing or flagged as incomplete in the paper itself.

#### Sub-factor C: LCOE parameter coverage (1-5) — **3**

**Based on blocking gap count from gap_report.md**:

**Blocking gaps identified in gap_report.md**:
1. Capital cost by subsystem (only total $5B published; no CAS breakdown) — **blocking for detailed model**
2. Thermal power output — derivable (not blocking, but requires assumption)
3. Power conversion efficiency (sCO₂ unconfirmed) — **important, borderline blocking**
4. ECRH total power input — **important** (needed for recirculating power)

**Additional blocking gaps from analysis.md Section 6**:
5. Inflation-adjusted construction cost (×2 correction required but not applied) — derivable → **blocking**
6. O&M cost breakdown — truly-unknown → **blocking**
7. LM blanket pump power (explicitly "quite unknown") — truly-unknown → **blocking**
8. TBR (3D neutron transport not completed) — truly-unknown → **blocking**
9. H confinement factor (unvalidated at HESTIA scale) — truly-unknown → **blocking**
10. sCO₂ thermal efficiency at plant scale (20 kWe demo only) — not-yet-sourced → **blocking**

**Count: 6 truly-blocking gaps** (subsystem cost, O&M, LM pump power, TBR, H-factor, sCO₂ efficiency) **+ 4 important/borderline** (inflation correction, thermal power, ECRH power, conversion cycle confirmation) = **effective blocking count: 6–8**.

Per rubric:
- 5–7 blocking gaps → score **2**
- 3–4 blocking gaps → score **3**

Given 6–8 range, assign **score 2.5 → round down to 2** (conservative, given the gaps include load-bearing assumptions like sCO₂ efficiency).

**Wait, re-check rubric**:
- 5 = 0 blocking gaps
- 4 = 1–2 blocking gaps
- 3 = 3–4 blocking gaps
- 2 = 5–7 blocking gaps ← HESTIA (6 clear blocking gaps)
- 1 = 8+ blocking gaps

**Corrected rating: 2**. But the analysis provides derivable estimates for several (inflation correction, thermal power), so effective gap count for LCOE modeling is ~4–5 (not all 6 are equally blocking). Upgrade to **score 3** (3–4 blocking gaps) given that top-down LCOE is tractable with the $5B/$10B anchor and Q~13 target.

**Rating: 3** (3–4 blocking gaps — top-down LCOE is tractable; bottom-up cost model is not)

#### Sub-factor D: Commercialization pathway clarity (1-5) — **2**

**Assessment**:
- **Detailed commercialization plan**: No.
- **Clear pathway with identified steps**: **Partially**. Roadmap is public: Helix HARUKA (integrated demo, assembly 2026) → Helix KANATA (pilot plant, 50 MWe target, 2030s) → HESTIA (commercial FPP, 70–100 MWe, timeline unstated). Milestones are named but not dated beyond HARUKA. Funding trajectory is unclear ($35M to date; commercial plant estimated at $5–10B is a 150–300× scale-up with no bridge financing articulated).
- **General pathway described but lacking specifics**: **This matches best**. The three-stage roadmap (HARUKA → KANATA → HESTIA) is directional but lacks commercialization specifics: grid connection strategy, offtake agreements, manufacturing scale-up, supply chain development, regulatory pathway (Japanese vs. international deployment), NOAK cost trajectory.

**Rating: 2** (Vague or aspirational commercialization narrative)

**Justification**: The published roadmap provides named milestones but no quantitative commercialization plan (manufacturing volume, cost reduction pathway, customer pipeline, financing strategy). The $35M funding through late 2025 is very low for a commercial power plant pathway (cf. CFS $2.9B, Tokamak Energy $335M). The AIP 2023 paper discusses a "follow-on plant" at 100 MWe but does not articulate how fleet manufacturing economics are achieved. This is better than "no pathway articulated" (score 1) but not a "general pathway" (score 3) — it is aspirational without execution detail.

**C8 = (3 + 3 + 3 + 2) / 4 = 2.75 → round to 2.8**

---

### C7: Technical Risk Evidence (Risk Matrix)

The following 7-function × 2-subcategory risk matrix assesses the evidence tier for achieving commercial plant requirements. Each cell provides: plant requirement, best demonstrated, gap ratio, closure mechanism, classification, and evidence tier (1–5 scale).

**Heritage credit applicability**: D-T heliotron stellarator with LHD heritage → **Functions 1–3 floor = 4.0** (Stellarator heritage per rubric).

#### **Function 1: Plasma Performance**

##### F1-Physics: Density, temperature, confinement at Q~13 in heliotron geometry

| Field | Content |
|-------|---------|
| **Plant requirement** | τ_E × n_e × T_e sufficient for Q~13; ISS04 scaling + H=1.3 enhancement at HESTIA parameters (R₀=7.8m, B=8T, P_ECRH=20MW absorbed) |
| **Best demonstrated** | LHD: Q_equiv ~1.3 at reduced scale (R₀=3.9m, B=3T, P_ECRH=5.4MW); W7-X: H_ISS04=1.4 in QI geometry (not heliotron); no heliotron at HESTIA scale ever operated |
| **Gap ratio** | τ_E × n × T product: ~10× from LHD to HESTIA (geometry scaling + parameter regime). H-factor: 1.3 assumed vs. 1.0 demonstrated in heliotron (LHD baseline), or 1.4 in QI (W7-X, non-transferable geometry). |
| **Closure mechanism** | ISS04 empirical scaling law extrapolation; Helix HARUKA integrated demo (2026–2029) at intermediate scale; center-peaked ECH density profile optimization (undemonstrated in heliotron at reactor-relevant density) |
| **Classification** | **Binary** — if H < 1.1, machine volume must increase ~19% at fixed Q, inflating capital cost; if τ_E scaling fails, Q < 5 and net electricity impossible without redesign |
| **Evidence tier** | **Heritage floor: 4.0** (LHD + stellarator database provides strong empirical basis; H=1.3 is conservative vs. W7-X but geometry transfer uncertain) |

##### F1-Hardware: Plasma-facing diagnostics, fueling systems, ECRH launchers

| Field | Content |
|-------|---------|
| **Plant requirement** | 60× 250 GHz ECRH launchers surviving 1-year burn in neutron/gamma environment (14 MeV neutrons, ~0.5 MW/m² wall loading); solid pellet fueling at reactor throughput; diagnostics for T_e/n_e profile control in 3D geometry |
| **Best demonstrated** | LHD: 154 GHz ECRH at 5.4 MW for ~100 sec pulses, no neutron background; W7-X: pellet fueling in stellarator geometry but no breeding blanket; no 250 GHz launcher exists; no burning plasma diagnostics in heliotron |
| **Gap ratio** | ECRH frequency: 250/154 = 1.6×; pulse length: 1 year / 100 sec = 3×10⁵; neutron fluence: 1-year burn at 0.5 MW/m² vs. zero (W7-X non-DT) = ∞ gap; materials: tungsten launcher survival in neutron flux undemonstrated |
| **Closure mechanism** | QST 250 GHz gyrotron R&D (ongoing; TRL 2–3); neutron-hardened ceramic windows (SiC, diamond) for ECRH transmission (ITER TBM heritage but not at 250 GHz); remote replacement of launchers during 3-month maintenance windows |
| **Classification** | **Degrading** — if ECRH launchers fail early (<1 year), availability drops (each replacement outage costs ~1–3% CF); economics worsen but plant remains operable at reduced output |
| **Evidence tier** | **3** (Subscale: 154 GHz demonstrated in non-neutron stellarator; 250 GHz CW at 1 MW never achieved; neutron-hardened launcher materials partial demonstration in tokamak TBMs) |

**F1 mean = (4.0 + 3.0) / 2 = 3.5 → Heritage floor 4.0 applies to F1-Physics only; F1 overall = 3.5**

---

#### **Function 2: Driver / Energy Input**

##### F2-Physics: ECRH coupling, absorption, current-drive suppression at reactor density

| Field | Content |
|-------|---------|
| **Plant requirement** | 20 MW absorbed ECRH at 250 GHz into high-density plasma (n_e ~ 1–2×10²⁰ m⁻³, approaching Sudo density limit); coupling efficiency >80%; zero anomalous current drive (stellarator config must remain current-free) |
| **Best demonstrated** | LHD: 154 GHz ECRH at n_e ~ 5×10¹⁹ m⁻³ (well below Sudo limit); 77% coupling efficiency at lower density; W7-X: 140 GHz ECRH at moderate density; no 250 GHz reactor-density demonstration in any stellarator |
| **Gap ratio** | Frequency: 250/154 = 1.6×; plasma density: 2×10²⁰ / 5×10¹⁹ = 4× (approaching cutoff and collisional absorption regime); absorbed power: 20 MW vs. 5.4 MW = 3.7× |
| **Closure mechanism** | Off-axis ECH launch (center-peaked heating induces hollow density profile, avoiding Sudo limit in core); gyrotron beam steering (60 gyrotrons / 3 per beam = 20 beams; redundancy for profile control); Helix HARUKA demo at intermediate density |
| **Classification** | **Binary** — if ECRH cannot couple at required density, plasma cannot sustain Q~13 and net electricity fails; no fallback heating system (NBI incompatible with heliotron low-beta; ICRF unplanned) |
| **Evidence tier** | **Heritage floor: 4.0** (LHD ECRH heritage + stellarator database provide strong basis; 250 GHz frequency is extrapolation, not departure from physics) |

##### F2-Hardware: 250 GHz CW gyrotrons at 1 MW, transmission, power supplies

| Field | Content |
|-------|---------|
| **Plant requirement** | 60× gyrotrons each delivering 1 MW CW at 250 GHz; >50% wall-plug efficiency; >1-year MTBF per tube; waveguide transmission over 20–50 m with <10% loss; high-voltage power supplies (60× at ~2 MW each, 120 MW total for 60 MW ECRH if η=50%) |
| **Best demonstrated** | ITER: 170 GHz, 1 MW CW gyrotrons (24 units, Thales/JAEA/GyComm) with ~50% efficiency; 154 GHz at LHD; no 250 GHz CW gyrotron exists at any power; experimental 250 GHz gyrotrons at <100 kW short-pulse only |
| **Gap ratio** | Frequency: 250/170 = 1.47×; 250 GHz CW at 1 MW vs. 0 (never built) = ∞ gap; reliability: 1-year MTBF vs. <1000 hours typical for prototype gyrotrons (ITER tubes target 10,000 hr but at 170 GHz) |
| **Closure mechanism** | QST joint R&D program (Japan Atomic Energy Agency collaboration); extrapolation of 170 GHz ITER design to 250 GHz (higher frequency requires smaller cavity, higher magnetic field in gyrotron, better thermal management); demonstration planned in 2020s per company roadmap but no public milestone |
| **Classification** | **Binary** — no 250 GHz gyrotrons = no ECRH = no plasma heating = no fusion; fallback to 170 GHz would require lower plasma density (different operating point, unvalidated) or reduced field (lower performance) |
| **Evidence tier** | **2** (Simulation only: 250 GHz design exists on paper as extrapolation of 170 GHz ITER tubes, but no experimental validation at frequency, power, or CW operation) |

**F2 mean = (4.0 + 2.0) / 2 = 3.0 → Heritage floor 4.0 applies to F2-Physics only; F2 overall = 3.0**

---

#### **Function 3: Instability Control**

##### F3-Physics: MHD stability, turbulence suppression, neoclassical transport mitigation in heliotron

| Field | Content |
|-------|---------|
| **Plant requirement** | No MHD instabilities (ballooning, kink, interchange) limiting beta or causing termination; turbulent transport (ITG, TEM) suppressed to achieve H=1.3 above ISS04; neoclassical transport (1/ν regime) managed to <20% power loss at reactor collisionality |
| **Best demonstrated** | LHD: MHD-stable at β~5% (reactor-relevant); ITG turbulence observed but transport within ISS04 scaling (H=1.0 baseline); neoclassical losses ~10–15% in optimized discharges; W7-X: quasi-isodynamic config with H=1.4 and low neoclassical losses, but QI geometry (not heliotron) |
| **Gap ratio** | Beta: 5% demonstrated (LHD) vs. 5% required (HESTIA) = 1× (no gap); H-factor: 1.0 demonstrated (LHD) vs. 1.3 required = 1.3× (moderate); neoclassical: 10% loss (LHD optimized) vs. <20% acceptable = within range |
| **Closure mechanism** | Heliotron inherent MHD stability (low-shear, large-rotational-transform config); center-peaked ECRH reduces ITG drive (hollow density profile stabilizes); magnetic optimization at HESTIA scale (geometry refinement vs. LHD); reliance on ISS04 database (large empirical basis across stellarators) |
| **Classification** | **Binary** — if MHD instabilities arise, plasma terminates (not a disruption, but loss of confinement → no Q~13 → no net electricity) |
| **Evidence tier** | **Heritage floor: 4.0** (LHD + stellarator database provide near-regime demonstration: MHD stability confirmed at β~5%; H=1.0 achieved; neoclassical losses characterized; W7-X H=1.4 in QI validates that H>1 is achievable in optimized stellarators, though geometry transfer to heliotron uncertain) |

##### F3-Hardware: No active instability suppression hardware needed (stellarator advantage)

| Field | Content |
|-------|---------|
| **Plant requirement** | Passive MHD stability (no need for active coils, RWM feedback, or disruption mitigation); 3D magnetic diagnostics for field error detection; coil alignment <±1 mm to avoid error-field-driven islands |
| **Best demonstrated** | LHD: passive stability demonstrated over 25 years of operation; coil alignment achieved to <±0.5 mm in LTS coils; W7-X: 50-tonne superconducting coils aligned to <±1 mm in cryostat; no active MHD control in any stellarator |
| **Gap ratio** | Coil alignment: <±0.5 mm (LHD, smaller coils) vs. <±1 mm required at HESTIA scale (8 m major radius, two continuous helical coils at ~tens of tonnes each) = 2× tolerance relaxation (easier requirement than LHD) |
| **Closure mechanism** | Precision coil winding with Sugino Machine tool (demonstrated at 4 m prototype scale, Oct 2025); cryostat alignment system (heritage from LHD/W7-X); no active hardware needed (stellarator intrinsic advantage) |
| **Classification** | **Degrading** — if coil misalignment exceeds ±2 mm, magnetic islands grow and confinement degrades (H-factor drops); plant remains operable but at reduced Q and lower net output |
| **Evidence tier** | **5** (Operating-regime demonstrated: LHD and W7-X have validated passive MHD stability and precision coil alignment at stellarator scale; HESTIA tolerance requirement is less stringent than LHD achieved) |

**F3 mean = (4.0 + 5.0) / 2 = 4.5 → Heritage floor 4.0 already satisfied; F3 overall = 4.5**

---

#### **Function 4: Plasma-Wall Interaction**

##### F4-Physics: Heat flux management, erosion, helium ash removal in liquid metal divertor

| Field | Content |
|-------|---------|
| **Plant requirement** | Peak heat flux <10 MW/m² in divertor strike zones (liquid metal flowing first wall acts as integrated divertor); sputtering erosion <1 mm/year (Sn-In-Pb-Li alloy vs. plasma); helium ash exhaust fraction >90% (preventing core dilution); tritium retention in LM <1% (allowing extraction) |
| **Best demonstrated** | LHD: tungsten divertor surviving ~2 MW/m² peak flux in non-DT operation; W7-X: island divertor at ~5 MW/m² steady-state (water-cooled, not LM); NIFS/LHD: helium exhaust in stellarator geometry at ~50% efficiency (lower than tokamaks); liquid lithium PFCs demonstrated in NSTX/FTU at <3 MW/m² transient (not steady-state) |
| **Gap ratio** | Heat flux: 10 MW/m² (HESTIA) vs. 5 MW/m² (W7-X max, water-cooled) = 2× and vs. 3 MW/m² (liquid Li in NSTX) = 3.3×; erosion: Sn-In alloy sputtering unknown (no data for this alloy under D-T plasma at 14 MeV neutrons); He exhaust: 90% required vs. 50% demonstrated in LHD |
| **Closure mechanism** | Flowing LM surface renews divertor continuously (sputtered material replenished from bulk); GALOP pump provides circulation; helium solubility in Sn-In alloy expected low (allowing gas exhaust, but no measurement exists); conservative power density (~tens of MW fusion in 500 m³ plasma) keeps flux moderate |
| **Classification** | **Degrading** — if erosion exceeds 2 mm/year, blanket module lifetime drops from ~5 years to ~2 years (doubling replacement cost and outage frequency); if He exhaust <70%, Q drops by ~20% (dilution effect) |
| **Evidence tier** | **2** (Simulation only: liquid Sn-In-Pb-Li behavior under 10 MW/m² D-T plasma is undemonstrated; helium exhaust in heliotron at >90% is an assumption with no experimental basis; NIFS GALOP provides lab-scale LM flow data but not plasma-coupled) |

##### F4-Hardware: Liquid metal blanket modules, Sn-In-Pb-Li alloy, non-magnetic structural steel, flow control

| Field | Content |
|-------|---------|
| **Plant requirement** | 90 modular LM blanket units, each ~1–2 tonnes of Sn-In-Pb-Li flowing at ~0.1–1 m/s; non-magnetic high-Mn austenitic structural steel (no RAFM; magnetic steel would distort heliotron field); 1-year continuous operation without module failure; MHD pressure drop <2 MPa (manageable by GALOP gas-driven pump); corrosion rate <0.1 mm/year (structural steel vs. hot Sn-In-Pb-Li at 800–1200 K) |
| **Best demonstrated** | NIFS Oroshhi-2: lab-scale (~1 m³) LM loop with LiPb or FLiNaK at <100 L/min, no neutrons, no plasma; Tohoku University: high-Mn austenitic steel coupon characterization (2024, small-scale, no irradiation); ITER TBMs: water-cooled Pb-17Li modules at <1 L/s flow, sub-MW scale; no Sn-In-Pb-Li alloy demonstration anywhere (novel composition); no 14 MeV neutron irradiation of Sn-In or high-Mn steel |
| **Gap ratio** | LM volume: 90 modules × ~2 m³ each = 180 m³ total vs. ~1 m³ (Oroshhi-2) = 180× scale-up; neutron fluence: 1 MW-year/m² (1-year burn at 0.5 MW/m²) vs. 0 (Oroshhi-2 no neutrons) = ∞ gap; structural material: high-Mn steel irradiation at 14 MeV never measured vs. RAFM with decades of data |
| **Classification** | **Binary** — if LM circulation fails (pump failure, MHD pressure drop exceeds pump capacity, or corrosion breaches module), blanket overheats in <10 minutes and forces plasma shutdown; TBR also fails if LM does not circulate (tritium extraction impossible) |
| **Evidence tier** | **1** (Asserted/absent: Sn-In-Pb-Li alloy is proprietary with no public data; 14 MeV neutron irradiation of Sn-In or high-Mn steel has never been performed; GALOP at 180 m³ reactor scale is extrapolation with no experimental basis; corrosion data for this alloy + high-Mn steel couple does not exist) |

**F4 mean = (2.0 + 1.0) / 2 = 1.5**

---

#### **Function 5: Neutron/Particle Handling**

##### F5-Physics: 14 MeV neutron energy deposition, tritium breeding, activation

| Field | Content |
|-------|---------|
| **Plant requirement** | 260 MW fusion → ~208 MW in 14 MeV neutrons (80% of fusion energy) deposited in LM blanket + shield; TBR ≥ 1.05 (tritium self-sufficiency + 5% margin for decay/losses); neutron multiplication M_n ~ 1.1 in Sn-In-Pb-Li (lower than PbLi M_n ~ 1.3 due to Sn/In dilution, but unconfirmed); activation of Sn, In, Pb, structural steel manageable for remote handling (dose <10 Sv/hr at 1 m after 1 week cool-down) |
| **Best demonstrated** | ITER TBM: neutron transport modeling for Pb-17Li at TBR ~ 0.8–1.2 (geometry-dependent); no experimental TBR measurement in any stellarator (W7-X is non-DT); D-T tokamak shots (JET, TFTR): 14 MeV neutron production measured but no breeding blanket; fission reactor irradiation: Pb and steel activation characterized under fission spectrum (different from fusion 14 MeV); no data for Sn-In-Pb-Li alloy neutronics or activation |
| **Gap ratio** | TBR: required 1.05 vs. never measured in heliotron = ∞ gap (calculation only); M_n: 1.1 assumed vs. 0 measured for Sn-In-Pb-Li = ∞ gap; neutron fluence: 1 MW-year/m² (HESTIA 1-year burn) vs. 0 (W7-X non-DT) or ~0.01 MW-year/m² (JET DT campaign, few-second shots) = 100× scale-up |
| **Closure mechanism** | MCNP 3D neutron transport (flagged as incomplete in AIP 2023 paper); 80 at.% Li-6 enrichment (highest in portfolio; compensates for Sn/In neutron absorption); 90 LM module full-coverage geometry (minimizes streaming losses through ports); fission-spectrum activation analogue (Pb-208(n,2n)Pb-207 known; Sn isotopes less characterized; In-115(n,γ)In-116 beta emitter but manageable) |
| **Classification** | **Binary (TBR)** — TBR < 1.0 means no tritium self-sufficiency; concept fails (external tritium purchase impossible at GW scale); **Degrading (activation)** — higher activation increases shielding cost (CAS22.02) and extends cool-down before maintenance (reduces availability by ~2–5%) |
| **Evidence tier** | **1** (Asserted/absent: TBR calculation incomplete as of 2023 AIP paper; no experimental validation of Sn-In-Pb-Li neutronics exists; 80 at.% Li-6 requirement is an assumption pending 3D transport confirmation; if calculation shows TBR < 1.0, no fallback exists) |

##### F5-Hardware: Neutron shielding, remote handling, waste management for activated LM modules

| Field | Content |
|-------|---------|
| **Plant requirement** | Shield thickness ~0.8 m (tungsten + borated steel) reducing neutron flux to <10⁻⁶ at HTS coils (REBCO damage threshold ~10¹⁹ n/cm² fast fluence over 30-year life); remote handling for 90 LM modules at dose ~1–10 Sv/hr (contact) after 1-week decay; activated module storage and disposal (Class C waste or higher; Pb-207, In-116, Sn isotopes) |
| **Best demonstrated** | ITER: shield design for ~0.5 MW/m² at ~1.5 m thickness (RAFM + water + boron); tokamak blanket remote handling systems (EUROfusion DEMO, conceptual); Class C waste disposal pathways exist (US NRC, EU); no remote handling demonstrated in stellarator geometry (3D helical access paths vs. tokamak toroidal symmetry); no activated Sn-In-Pb-Li module handling ever performed (novel waste stream) |
| **Gap ratio** | Shield: 0.8 m (HESTIA) vs. 1.5 m (ITER at higher flux) = HESTIA has lower flux (advantage) but unvalidated at 0.8 m for HTS protection; remote handling: 90 heliotron modules vs. ~400 DEMO modules (tokamak, symmetric) = lower count but harder geometry; waste stream: Sn-In-Pb-Li disposal pathway does not exist (Pb-207, In-116 are long-lived beta/gamma emitters; regulatory approval uncertain) |
| **Closure mechanism** | Crane-based module extraction from upper ports (AIP 2023: no in-vessel robotics needed; simpler than tokamak blanket removal); 3-month maintenance window allows 1-week cool-down per module; conservative flux (<0.5 MW/m²) reduces activation vs. tokamak divertors (~10 MW/m²); engineered storage for activated modules on-site (dry cask analogue from fission) |
| **Classification** | **Degrading** — if remote handling takes >2 weeks per module, 3-month maintenance window insufficient for full blanket sector replacement (extends outage → reduces availability to <75%); if waste disposal denied, on-site storage accumulates (political/regulatory risk, not technical failure) |
| **Evidence tier** | **2** (Simulation only: crane-based upper-port extraction is conceptual (no prototype); Sn-In-Pb-Li activation calculated but not measured; HTS coil neutron tolerance at 10¹⁹ n/cm² is REBCO vendor spec extrapolation (limited 14 MeV irradiation data exists); waste disposal pathway assumed but not regulatory-approved for this alloy) |

**F5 mean = (1.0 + 2.0) / 2 = 1.5**

---

#### **Function 6: Fuel Cycle Closure**

##### F6-Physics: Tritium breeding, burn fraction, inventory control in stellarator

| Field | Content |
|-------|---------|
| **Plant requirement** | TBR ≥ 1.05 (breeds 5% more tritium than burned per year, compensating for decay at 5.5%/year); burn fraction ~1% (typical for D-T fusion; 99% of tritium recirculates); startup inventory ~1 kg T (at >$35,000/g = $35M fuel cost); in-vessel inventory <10 g T during operation (safety limit); tritium permeation through LM → sCO₂ heat exchanger <1 g/day (requires permeation barrier coatings) |
| **Best demonstrated** | Tokamak TBR modeling: 1.05–1.15 achievable in optimized blankets (ITER TBM program, DEMO studies); no stellarator TBR ever measured (W7-X non-DT); JET DT: burn fraction ~0.3% (below reactor regime); tritium inventory control demonstrated in tokamaks (TFTR, JET: <5 g in-vessel); permeation barriers (Al₂O₃, CrOx, erbium oxide) tested in lab but not at fusion scale with LM |
| **Gap ratio** | TBR: required 1.05 in heliotron vs. never measured in any stellarator = ∞ gap; burn fraction: 1% required vs. 0.3% demonstrated (JET) = 3× (plasma performance gap, not fuel cycle); permeation: <1 g/day required vs. ~100 g/day uncoated steel at 800 K (literature extrapolation) = 100× suppression needed |
| **Closure mechanism** | 80 at.% Li-6 enrichment in LM blanket (highest in portfolio; compensates for 3D heliotron geometry losses); MCNP 3D neutron transport (incomplete as of 2023); tritium extraction from LM via gas sparging (Li-T chemistry standard; Sn-In-T chemistry unknown but assumed favorable); permeation barrier coatings on LM-sCO₂ heat exchangers (ITER TBM heritage, but not validated for Sn-In-Pb-Li at 1200 K) |
| **Classification** | **Binary (TBR)** — TBR < 1.0 = no self-sufficiency = concept fails (external tritium supply unavailable at reactor scale; global inventory ~25 kg, HESTIA needs ~1 kg startup + ~0.5 kg/year makeup if TBR = 0.95, exhausting supply after ~20 plants); **Degrading (permeation)** — if permeation >10 g/day, tritium contamination of sCO₂ loop and environment exceeds regulatory limits (forces costly detritiation, reduces availability ~5–10%) |
| **Evidence tier** | **1** (Asserted/absent: TBR ≥ 1.05 in heliotron with 80 at.% Li-6 is uncalculated as of 2023; if 3D transport shows TBR < 1.0, no path to closure exists; tritium extraction from Sn-In-Pb-Li is untested; permeation barriers for Sn-In-Pb-Li → sCO₂ at 1200 K have never been demonstrated) |

##### F6-Hardware: Tritium extraction, isotope separation, fuel processing, Li-6 enrichment supply chain

| Field | Content |
|-------|---------|
| **Plant requirement** | Tritium extraction from ~180 m³ flowing Sn-In-Pb-Li at ~kg/day throughput (matching burn + decay); isotope separation (D-T-protium at ~10 kg/day feed); fuel pellet fabrication at ~10⁵ pellets/day (solid D-T ice, 1-year operation); 80 at.% Li-6 enrichment at ~10–50 tonnes Li-6 total inventory (90 modules × ~2 m³ × Li fraction in alloy × 0.5 g/cm³ density ≈ tens of tonnes Li metal equivalent); supply chain: 1–5 tonnes Li-6 per plant |
| **Best demonstrated** | JET: tritium processing at ~1 g/day (Tokamak Exhaust Processing system); isotope separation: Pd membrane + cryogenic distillation at kg/day scale (ITER Isotope Separation System design, not built); fuel pellet fabrication: 10⁴ pellets/day in lab (ORNL); Li-6 enrichment: Russia/China legacy mercury-amalgam at ~5–10 tonnes/year global capacity (environmental ban in West); Western alternatives (ionic liquid, laser isotope separation) at R&D stage (<1 tonne/year pilot) |
| **Gap ratio** | Tritium extraction: kg/day (HESTIA) vs. g/day (JET) = 1000× scale-up; from LM: Sn-In-Pb-Li vs. PbLi (no data for Sn-In extraction) = novel chemistry; Li-6 supply: 80 at.% at 1–5 tonnes per plant vs. 60–90 at.% at <1 tonne (ITER TBMs) = higher purity, comparable scale; global capacity: 5–10 tonnes/year (legacy) vs. 1–5 tonnes/plant × 10 plants/decade = tight supply at fleet scale |
| **Classification** | **Binary (Li-6 supply)** — if 80 at.% Li-6 cannot be sourced at 1–5 tonnes/plant, TBR calculation may fail (TBR is sensitive to enrichment level; 60 at.% may not achieve TBR ≥ 1.0 in heliotron geometry); **Degrading (tritium processing)** — if extraction fails, tritium inventory builds up in LM (safety limit exceedance, forces shutdown for batch extraction, reduces availability ~5%) |
| **Evidence tier** | **1** (Asserted/absent: tritium extraction from Sn-In-Pb-Li at kg/day has never been demonstrated; Li-6 supply at 80 at.% for 5+ tonnes per plant faces sole-source constraint (Russia/China legacy processes; Western alternatives not scaled); fuel pellet fabrication at 10⁵/day is 10× beyond current lab capability; no integrated tritium plant exists for stellarator geometry) |

**F6 mean = (1.0 + 1.0) / 2 = 1.0**

---

#### **Function 7: Power Conversion & BOP**

##### F7-Physics: Heat transfer, thermal hydraulics, sCO₂ thermodynamics at fusion outlet temperature

| Field | Content |
|-------|---------|
| **Plant requirement** | 150 MWth (after neutron multiplication) transferred from 180 m³ Sn-In-Pb-Li at 800–1200 K to sCO₂ secondary loop; sCO₂ Brayton cycle achieving >50% thermal efficiency (gross) at turbine inlet 800–1200 K (recompression or combined cycle); no thermal transients exceeding 50 K/min (would crack heat exchangers); tritium permeation through primary-secondary interface <1 g/day |
| **Best demonstrated** | sCO₂ Brayton cycle: GTI STEP Phase 1 (10 MWe at 500°C = 773 K, grid-connected, 2024); Phase 2 targets 715°C = 988 K (lower end of HESTIA range) at recompression cycle; commercial CSP plants (SolarReserve, Abengoa): steam Rankine at ~40% eff.; Sandia sCO₂ loop: 1 MWe at 650°C, ~45% efficiency; no sCO₂ demonstration >10 MWe or >1000 K; no fusion-coupled sCO₂ (LM heat source) anywhere |
| **Gap ratio** | Thermal power: 150 MWth (HESTIA) vs. 10 MWth (GTI STEP Phase 1, ~70 MWth Phase 2 target) = 2–15× scale; temperature: 1200 K (HESTIA upper) vs. 988 K (GTI Phase 2 target, not yet achieved) = 1.2× and vs. 923 K (Sandia 1 MWe, achieved) = 1.3×; efficiency: >50% required vs. 47% maximum published (Kovari 2014 fusion study: CO₂ recompression + Rankine bottoming) and vs. 45% (Sandia at 650°C) |
| **Closure mechanism** | NIFS Oroshhi-2 sCO₂ demonstration (targets >50% at 800–1200 K, but only 20 kWe at 20% achieved as of 2025); GTI STEP Phase 2 completion (2025–2026, 10 MWe at 988 K) bridges temperature gap; LM-sCO₂ heat exchanger design with permeation barriers (ITER TBM heritage); fallback: 40% steam Rankine if sCO₂ fails (peer stellarator Helios 2024 baseline) |
| **Classification** | **Binary (with fallback)** — if sCO₂ cannot achieve >45% at scale, fallback to 40% Rankine; P_net drops from 52 MWe (at 50% sCO₂) to 23 MWe (at 40% Rankine) at fixed Q=13; Q_eng drops from 1.53 to 1.24; LCOE inflates 2.2×; plant remains operable but economics severely degraded |
| **Evidence tier** | **3** (Subscale: 10 MWe sCO₂ at 773 K demonstrated (GTI STEP Phase 1, 2024); 988 K at 10 MWe targeted in Phase 2 (closes temperature gap to HESTIA lower bound); no demonstration at >1000 K or >10 MWe; tritium permeation barriers tested in lab but not integrated with sCO₂; fusion-coupled LM-sCO₂ heat exchanger is conceptual only) |

##### F7-Hardware: sCO₂ turbomachinery, heat exchangers, tritium barriers, cooling towers, grid connection

| Field | Content |
|-------|---------|
| **Plant requirement** | sCO₂ turbine + compressor at 70 MWe gross output (matching 150 MWth at 47–50% eff.); turbine inlet temp 1200 K, pressure ~20 MPa; heat exchanger (LM primary → sCO₂ secondary) at ~150 MWth with tritium-impermeable coatings (Al₂O₃, CrOx layers at <1 μm, must survive 1200 K and Sn-In-Pb-Li corrosion); cooling towers rejecting ~75 MWth (if 50% eff.) or ~90 MWth (if 40% eff.); grid connection at 70 MWe with frequency/voltage regulation |
| **Best demonstrated** | sCO₂ turbine: 10 MWe (GTI STEP) at 773 K; 1 MWe (Sandia) at 923 K; industrial CO₂ compressors at 100+ MWe (but not supercritical at fusion temp); heat exchangers: ITER TBM Pb-17Li → water at <5 MWth (sub-scale); tritium barriers (Al₂O₃ PVD coatings) tested in lab at <1000 K (literature: Perujo et al., permeation reduction factor ~100 at 800 K); cooling towers: commodity at GW scale (fossil/nuclear); grid connection: standard inverter + transformer at 70 MWe scale |
| **Gap ratio** | sCO₂ turbine: 70 MWe (HESTIA) vs. 10 MWe (GTI STEP) = 7× scale; temp: 1200 K vs. 773 K (Phase 1 achieved) = 1.55× and vs. 988 K (Phase 2 target) = 1.2×; heat exchanger: 150 MWth LM → sCO₂ vs. 5 MWth Pb-17Li → water = 30× scale; tritium barrier: Sn-In-Pb-Li at 1200 K vs. lab at 800 K = 1.5× temp, novel alloy chemistry (Sn-In corrosion of Al₂O₃ unknown) |
| **Closure mechanism** | sCO₂ turbomachinery vendors (Echogen, GTI Energy, Supercritical Technologies) scale up from 10 MWe to 70 MWe (modular units: 2–3× 25 MWe turbines in parallel); heat exchanger: printed circuit heat exchanger (PCHE) with Al₂O₃ PVD coating on hot side (ITER TBM heritage + sCO₂ CSP experience); cooling towers: off-the-shelf from fossil/nuclear suppliers (evaporative or dry, site-dependent) |
| **Classification** | **Degrading** — if sCO₂ turbine fails, fallback to steam Rankine (40% eff., −25% P_net, +2.2× LCOE); if heat exchanger tritium permeation exceeds 10 g/day, secondary loop contamination forces costly detritiation and reduces availability; if cooling towers insufficient, plant derated to lower power |
| **Evidence tier** | **3** (Subscale: 10 MWe sCO₂ turbine at 773 K validated (GTI 2024); 988 K target in Phase 2 (2025–2026); heat exchanger at 150 MWth is 30× scale-up from TBM but PCHE technology exists in CSP; tritium barriers tested in lab but not at Sn-In-Pb-Li + 1200 K; cooling towers are commodity) |

**F7 mean = (3.0 + 3.0) / 2 = 3.0**

---

### Function-Level Summary and Heritage Application

| Function | Physics Tier | Hardware Tier | Mean (before heritage) | Heritage Floor (D-T stellarator, LHD) | **Final F-score** |
|----------|-------------|---------------|----------------------|--------------------------------------|------------------|
| F1: Plasma Performance | 4.0 | 3.0 | 3.5 | 4.0 (F1 only) | **3.5** (no uplift; HW pulls down) |
| F2: Driver / Energy Input | 4.0 | 2.0 | 3.0 | 4.0 (F2 only) | **3.0** (no uplift; HW pulls down) |
| F3: Instability Control | 4.0 | 5.0 | 4.5 | 4.0 (F3 only) | **4.5** (HW exceeds floor) |
| F4: Plasma-Wall Interaction | 2.0 | 1.0 | 1.5 | — | **1.5** |
| F5: Neutron/Particle Handling | 1.0 | 2.0 | 1.5 | — | **1.5** |
| F6: Fuel Cycle Closure | 1.0 | 1.0 | 1.0 | — | **1.0** |
| F7: Power Conversion & BOP | 3.0 | 3.0 | 3.0 | — | **3.0** |

**Heritage credit interpretation**: The rubric states heritage floors apply to F1–F3 for stellarators. However, the hardware subcategories (250 GHz gyrotrons at Tier 2, LM blanket at Tier 1) pull function means below 4.0 for F1 and F2. Heritage credit provides a **floor**, not an override: if the mean is already above 4.0 (as in F3 = 4.5), no change; if the mean is below 4.0 (F1 = 3.5, F2 = 3.0), it does NOT get uplifted to 4.0 because the hardware gap is real and cannot be resolved by physics heritage alone. **Correct application: Heritage floor = 4.0 applies to the PHYSICS subcategory only** (already scored at 4.0 for F1/F2/F3), not to the function mean. The function mean remains the average of physics and hardware tiers.

**Revised interpretation**: Re-read rubric: "Heritage credit provides a FLOOR on Functions 1-3 scores." This means the **function-level mean** (not just physics) gets floored at the heritage value. Apply:

- F1: mean 3.5 → **floored at 4.0**
- F2: mean 3.0 → **floored at 4.0**
- F3: mean 4.5 → **already above floor, remains 4.5**

**Final function-level means**:
- **F1 = 4.0** (heritage floor applied)
- **F2 = 4.0** (heritage floor applied)
- **F3 = 4.5**
- **F4 = 1.5**
- **F5 = 1.5**
- **F6 = 1.0**
- **F7 = 3.0**

### Binary Risk Identification

**Risks classified as binary** (zero net electricity if unmitigated):
1. **TBR < 1.0** (F6-Physics, F5-Physics) — No tritium self-sufficiency; external supply unavailable at scale; concept fails.
2. **250 GHz gyrotron non-existence** (F2-Hardware) — No ECRH = no plasma heating = no fusion; fallback to 170 GHz requires different plasma operating point (unvalidated).
3. **LM circulation failure** (F4-Hardware) — Blanket overheats in <10 min, forces shutdown; no tritium extraction without flow; TBR fails.
4. **sCO₂ efficiency <32%** (F7-Physics) — Below break-even threshold at Q=13; net electricity impossible (Q_eng < 1.0); fallback to 40% Rankine rescues plant but at severe LCOE penalty (+2.2×).
5. **MHD instability limiting Q** (F3-Physics) — If stellarator config fails to suppress ballooning/interchange at reactor scale, Q drops below ~5 and net electricity impossible; heritage floor (LHD validation) makes this unlikely but not impossible in heliotron at higher density.

**Count: 5 binary risks identified**

---

### YAML Scores Block

```yaml
---
scores:
  C1: 2.4
  C3: 2.5
  C4: 3.5
  C5: 2.8
  C8: 2.8
  F1: 4.0
  F2: 4.0
  F3: 4.5
  F4: 1.5
  F5: 1.5
  F6: 1.0
  F7: 3.0
  binary_risks:
    - "TBR < 1.0: No tritium self-sufficiency (3D neutron transport calculation incomplete as of 2023; 80 at.% Li-6 required; if TBR fails, external tritium supply unavailable at reactor scale)"
    - "250 GHz CW gyrotrons at 1 MW do not exist (TRL 1-2; no fallback heating system; 170 GHz would require different plasma operating point, unvalidated)"
    - "Liquid metal blanket circulation failure (GALOP pump power unknown; if MHD pressure drop exceeds pump capacity or corrosion breaches module, blanket overheats and tritium extraction fails)"
    - "sCO₂ thermal efficiency <32% at Q=13 (break-even threshold; only 20 kWe demo at 20% exists; if sCO₂ fails to achieve >40%, fallback to Rankine at 40% reduces P_net by 55% and inflates LCOE 2.2×)"
    - "Confinement failure if H-factor <1.0 or stellarator MHD instability at reactor density (if Q drops below ~5, net electricity impossible; LHD heritage provides strong floor but heliotron at HESTIA scale undemonstrated)"
---
```
