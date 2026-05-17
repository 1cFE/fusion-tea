---
ID: 36-helical-coil-stellarator
Concept: Helical Coil Stellarator (D-T)
Company: Helical Fusion
Type: synthesis
Status: draft
Created: 2026-05-14
---

# Synthesis: Helical Coil Stellarator (D-T) - Part 1

## 1. Executive Summary

- **The single most important risk**: The sCO₂ Brayton cycle targeting >50% thermal efficiency is load-bearing for the entire economic case — at the published Q~13 plasma gain, falling below 50% η_th drops net output from 70 MWe to ~52 MWe (physics-forward Q=13 case) or forces the plasma to operate at Q>13 to compensate. The current technology state is a 20 kWe demonstration at 20% efficiency, 2.5× below the design target and below the break-even threshold (η_th ≈ 32%). No fusion-coupled sCO₂ system has been demonstrated at any scale. Peer stellarator designs (Helios, 2024) chose 40% steam Rankine as their conservative baseline, treating sCO₂ as aspirational.

- **The single most important advantage**: Stellarators eliminate all current-drive recirculating power — at Q_eng = 2.0, a heliotron stellarator achieves the same net output fraction as a tokamak from a less demanding plasma operating point (Q~13 vs. Q>20 for equivalent tokamak at same recirculating fraction). Steady-state operation (~1-year burn, ~3-month maintenance) provides an ~80% availability structural ceiling without plasma restart losses, a 10–20 percentage point advantage over pulsed concepts at similar technology maturity.

- **LCOE ballpark**: Framework lower bound $1,170/MWh ($1.17/kWh) at 70 MWe back-solved reference; physics-forward (Q=13 fixed, η_th=50%) yields $1,530/MWh ($1.53/kWh) at 52 MWe. Published cost anchor ($10B inflation-adjusted) implies upper bound $1,800/MWh ($1.80/kWh). **LCOE range: $1,170–1,800/MWh.** The economic thesis rests on fleet manufacturing learning curves that have no quantitative basis at current funding ($35M through late 2025). At 1 GWe normalized scale, framework yields $140/MWh — but HESTIA's design is 70 MWe modular replication, not gigawatt-scale single plants.

- **Confidence verdict: Low** — published cost uses 1990s pricing requiring ×2+ inflation correction (authors' explicit statement), no subsystem-level cost breakdown exists, sCO₂ efficiency is aspirational (20% demonstrated vs. 50% required), LM pump power flagged as "quite unknown" by the authors, TBR calculation incomplete, H=1.3 confinement factor unvalidated, 250 GHz gyrotrons do not exist (TRL 1–2), and no independent techno-economic assessment of any heliotron FPP design exists in the public literature.

---

## 2. What Matters Most for LCOE

Ranked by LCOE sensitivity elasticity from model output (70.4 MWe native design point):

### 1. **Coil Cost (r_coil elasticity: +1.36)**
- **Assumed value**: Framework default coil cost scaling (calibrated to wound-coil geometries like tokamaks).
- **Source**: ARIES stellarator framework; no HESTIA-specific coil cost data published.
- **Sensitivity**: At elasticity +1.36, a 2× coil cost multiplier increases LCOE by ~2.6× (from $1,170/MWh to ~$3,000/MWh). C220103 (coils) = 71% of reactor plant equipment cost ($2,323M of $3,279M total RPE).
- **What would flip the economic conclusion**: HESTIA uses two **continuous helical coils** (WISE REBCO), fundamentally different from modular stellarator or tokamak coil sets. The October 2025 milestone demonstrated >4 m conductor length at 40 kA / 7 T; reactor-scale helical coils at R₀=7.8 m require unbroken conductor runs orders of magnitude longer, with no joints and complex 3D winding. Comparative data: QI modular stellarator designs carry 1.5–5× manufacturing cost premiums per unit fusion power over wound tokamaks due to 3D freeform geometry. If continuous helical winding incurs even a 2× premium over the framework default (moderate within the 1.5–5× range), LCOE triples. **The framework coil cost is a lower bound; true cost could be 2–5× higher, pushing LCOE into the $3,000–10,000/MWh range.**

### 2. **Availability (elasticity: -0.97)**
- **Assumed value**: 83% (central estimate within >80–85% FPP published target range).
- **Source**: Miyazawa & Goto 2023, Table I; 1-year burn + ~3-month maintenance → structural ceiling ~80%.
- **Sensitivity**: Near-linear inverse relationship. Moving from 83% to 70% (derated for novel-subsystem outages) increases LCOE by +18% to $1,378/MWh. Moving to 90% (FOAK published target) decreases LCOE by -7% to $1,084/MWh.
- **What would flip the economic conclusion**: The 80–85% target assumes mature subsystems. HESTIA's blanket (liquid metal Sn-In-Pb-Li alloy, TRL 2–3), gyrotrons (250 GHz / 1 MW CW, TRL 1–2), and sCO₂ cycle (TRL 3–4 at fusion scale) all introduce unplanned outage risk. If availability degrades to 70% in practice — comparable to early ITER operations or first-generation FPP with novel systems — LCOE rises 18% from the central case. The steady-state advantage narrows if new failure modes (LM freezing, gyrotron tube failure, sCO₂ turbine trips) occur frequently. **Availability <75% would erase the stellarator's operational advantage over pulsed concepts.**

### 3. **Magnetic Field Strength (b_max elasticity: +0.68)**
- **Assumed value**: 8 T at coil center (9 T at plasma center).
- **Source**: Miyazawa & Goto 2023, §II-B, Table I.
- **Sensitivity**: Field strength drives coil stress, coil cost, and plasma performance. At +0.68 elasticity, a 10% field increase → +6.8% LCOE increase.
- **What would flip the economic conclusion**: The H=1.3 confinement factor assumption is unvalidated. If H=1.0 (ISS04 baseline, no improvement) is required, the machine must be ~6% larger in linear dimensions (R₀, a) to achieve the same confinement time at fixed field — volume penalty ~19%, driving coil and blanket cost increases. The model shows H=1.0 penalty is only +1.1% LCOE ($1,168 → $1,181/MWh) at fixed field because the ISS04 scaling exponents are favorable, but if field or operating strategy must change to recover confinement, the penalty would be larger.

### 4. **Construction Time (elasticity: +0.58)**
- **Assumed value**: 10 years (above the 8-year modular stellarator default).
- **Source**: Analysis judgment; continuous helical coil winding at reactor scale is harder than modular coil assembly.
- **Sensitivity**: +0.58 elasticity → 10% construction time increase (10 yr → 11 yr) adds +5.8% to LCOE via interest-during-construction (CAS60).
- **What would flip the economic conclusion**: First-of-kind WISE REBCO winding at HESTIA scale (two continuous helical coils, each requiring tens of thousands of km of tape in a single unbroken run) has no demonstrated manufacturing precedent. If construction stretches to 12–15 years due to coil winding delays (as seen in W7-X, which took ~20 years from start to first plasma), LCOE rises 12–29% from the 10-year baseline. **Construction time >12 years would push LCOE above $1,300/MWh even at the framework lower bound.**

### 5. **Thermal Efficiency (eta_th elasticity: -0.09 at fixed output, but structural threshold dependency)**
- **Assumed value**: 48% (standardized from 50% central target per scoring framework; HESTIA targets >50% at 800–1200 K).
- **Source**: Miyazawa & Goto 2023, §II-F; Ishiyama & Tanaka 2019 (NIFS Oroshhi-2 sCO₂ demo plan).
- **Sensitivity**: -0.09 elasticity is deceptively low because it measures LCOE sensitivity *at fixed net output* (70.4 MWe back-solved). The true structural dependency is shown in the sCO₂ efficiency sweep: at η_th=50% (physics-forward Q=13), P_net=52 MWe and LCOE=$1,533/MWh. At η_th=40%, P_net drops to 23 MWe and LCOE rises to $3,391/MWh — a 2.2× increase. At η_th=38%, P_net=17 MWe and LCOE=$4,514/MWh. Below η_th ≈ 32%, the design cannot close (Q_eng < 1.0). **This is not a continuous sensitivity — it's a hard threshold. Falling below 50% η_th collapses the economic case.**
- **What would flip the economic conclusion**: The contemporary peer stellarator FPP study (Helios, 2024, R₀=8 m, 390 MWe net) chose 40% steam Rankine as its baseline power cycle, not sCO₂, treating this as the achievable conservative choice at the current state of development. If HESTIA is forced to adopt 40% Rankine as the design-conservative fallback, net output drops from 70 MWe to ~23 MWe at Q=13, LCOE rises to $3,391/MWh, and the concept becomes economically nonviable. **The >50% sCO₂ target is not merely aspirational — it is the difference between a $1.5/kWh concept and a $3–4/kWh concept.**

---

## 3. Risk Verdicts

### Challenge 1: Cost model anchored to 1990s prices — ×2+ inflation correction required
- **Verdict**: Genuinely uncertain
- **Rationale**: The authors explicitly flag the need for a ×2+ multiplier but do not apply it, leaving the inflation-adjusted cost in the range $8–12B for 70 MWe ($114–171B/GWe specific capital). The upper end of this range exceeds any other concept in the portfolio by 5–10×. However, the $5B 1990s figure may have been derived from ITER/LHD component-level analogues that themselves overestimate commercial plant costs (ITER is a one-off experiment, not a production plant). The true FOAK cost could be lower if NOAK learning curves are applied — or higher if the published estimate underestimates helical coil and LM blanket novelty.
- **What would retire this risk**: An independent bottom-up cost estimate by a third party (e.g., Princeton PPPL, ORNL, or a European fusion cost-modeling group) with subsystem-level breakdowns. Alternatively, actual HARUKA construction costs (if made public) would calibrate the coil and blanket cost elements.

### Challenge 2: H=1.3 confinement factor unvalidated — geometry-transfer risk
- **Verdict**: Likely resolvable
- **Rationale**: W7-X has achieved H_ISS04 = 1.4 experimentally (cited in Helios 2024 preconceptual study §3.1 with *Nuclear Fusion* references). HESTIA's H=1.3 assumption is 0.1 below the W7-X demonstrated value. The residual risk is not whether H>1 is achievable in stellarators (it is), but whether HESTIA's heliotron geometry with center-peaked ECH will reproduce W7-X's quasi-isodynamic performance. LHD (the heliotron heritage device) operated at H~1.0; HESTIA's optimization claims H=1.3. This is a 30% improvement that requires experimental validation but is within the W7-X-demonstrated envelope.
- **What would retire this risk**: Helix HARUKA integrated demonstration (assembly starting 2026, first plasma 2027–2028) achieving H≥1.2 in a heliotron geometry with ECH-dominated heating. If HARUKA demonstrates H≥1.2, the HESTIA H=1.3 assumption becomes credible. If HARUKA achieves only H~1.0, HESTIA's machine size (and cost) must increase by ~6% linearly (~19% by volume).

### Challenge 3: Liquid metal pump power — explicitly unknown
- **Verdict**: Likely resolvable
- **Rationale**: The GALOP gas-driven pump eliminates rotating components and has been demonstrated at lab scale. The unknown is the plant-scale circulation power for 90 modular LM blanket units. This is an engineering analysis problem, not a fundamental physics gap. NIFS has decades of liquid metal blanket experience from the FFHR program and Oroshhi-2 platform; they can calculate pump power once the full LM circuit design is specified. The risk is that pump power is higher than the 15 MW placeholder (stellarator default), eating into the already-tight Q_eng=2.0 power balance. At Q_eng=2.0, recirculating power ≈ 50% of gross output; even a 10 MW underestimate in LM pump power reduces net output by ~10 MWe (14% of the 70 MWe target).
- **What would retire this risk**: Published GALOP pump power scaling data or a full LM circuit analysis in a follow-on HESTIA paper. The full AIP 2023 paper body (paywalled) may contain this; the abstract explicitly flags it as unknown, suggesting the authors recognized it as a gap at publication time.

### Challenge 4: sCO₂ at >50% efficiency — undemonstrated at fusion scale
- **Verdict**: Unlikely resolvable (at >50% target) without major development; 40–47% is the achievable near-term ceiling
- **Rationale**: GTI STEP Demo Phase 1 (October 2024) achieved 10 MWe at 500°C (773 K); Phase 2 targets 715°C (988 K) at 10 MWe, which falls within HESTIA's 800–1200 K operating range but at the lower end. The highest published fusion-specific sCO₂ efficiency is 47% gross (Kovari et al. 2014, CO₂ recompression Brayton + Rankine bottoming cycle), achieved in a design study (not hardware). The NIFS Oroshhi-2 platform has a proposed sCO₂ demo targeting >50% but only a 20 kWe feasibility study at 20% efficiency has been assessed. The Helios stellarator FPP study (2024) chose 40% steam Rankine as its baseline, treating this as the design-conservative choice. **The 40–47% range is achievable with current sCO₂ technology trajectory; >50% is aspirational and requires fusion-specific heat exchanger materials (tritium-impermeable at 800–1200 K with LM primary circuit corrosion resistance) that do not yet exist.**
- **What would retire this risk**: A fusion-coupled sCO₂ demonstration at ≥10 MWe scale achieving 48–50% net efficiency with a tritium-compatible heat exchanger. Absent this, the 40% Rankine fallback (Helios precedent) should be treated as the design-conservative scenario, not a downside sensitivity.

### Challenge 5: TBR — 3D neutron transport calculation incomplete
- **Verdict**: Likely resolvable
- **Rationale**: The 2023 paper acknowledges the 3D neutron transport calculation was not completed as of publication. This is a standard Monte Carlo neutronics task (MCNP, OpenMC, or Serpent with ENDF/B cross-section libraries) that NIFS has performed for the FFHR series. The heliotron coil geometry is more complex than a tokamak (continuous helical coils intrude into the blanket space), and 80 at.% Li-6 enrichment is required to compensate for reduced blanket coverage. The TBR calculation is tractable but requires full 3D CAD geometry and neutron transport modeling at reactor scale — likely underway but not yet published. The risk is that TBR<1.0 even at 80 at.% enrichment, forcing either higher enrichment (supply-limited) or thicker blanket (reduces plasma volume, increases cost).
- **What would retire this risk**: Published TBR≥1.05 from 3D neutron transport with HESTIA coil geometry, 90 LM modules, and 80 at.% Li-6 enrichment. A margin of 0.05–0.10 above unity is standard to account for uncertainties and breeding losses.

---

## 4. Structural Advantages and Disadvantages

Compared to conventional D-T tokamak baseline:

### Advantages (cost reductions or performance improvements)

**1. Zero current-drive recirculating power (~10–30% of gross electric in steady-state tokamaks)**
- **Mechanism**: Stellarators use external 3D-shaped coils to generate the rotational transform; no toroidal plasma current is required. Tokamaks at steady-state must drive current via NBI, ECCD, or LHCD, consuming 10–30% of gross electric output at Q_eng~2–5.
- **Quantification**: At 70 MWe net and Q_eng=2.0, total recirculating power is ~70 MWe (50% of gross), composed entirely of ECRH (60 MW wall-plug), cryogenics, LM pumps, and BOP auxiliaries. A steady-state tokamak at the same Q_eng=2.0 would have an additional 20–40 MW current-drive load. **Eliminates ~15–25% of recirculating power structure relative to steady-state tokamak.**

**2. Steady-state operation: ~80% availability structural ceiling without plasma restart losses**
- **Mechanism**: 1-year continuous burn + ~3-month maintenance cycle → ~80% availability ceiling. Pulsed tokamaks incur plasma restart overhead, thermal cycling fatigue, and duty-cycle losses.
- **Quantification**: Published availability target >80–85% FPP. Comparable pulsed tokamak designs target 60–70% availability at FPP maturity. **10–20 percentage point availability advantage → 10–20% LCOE reduction at equivalent capital cost.**

**3. No disruptions: eliminates disruption-protection systems and damage risk**
- **Mechanism**: Stellarators are intrinsically disruption-free (no toroidal current, no current-driven instabilities).
- **Quantification**: Disruption mitigation systems cost ~1–2% of tokamak capital. **Eliminates ~1–2% capital cost and ~2–5 percentage point availability penalty from disruption-related outages.**

### Disadvantages (cost increases or performance penalties)

**1. Continuous helical coil manufacturing cost premium: 1.5–5× per unit fusion power vs. wound tokamaks**
- **Mechanism**: HESTIA uses two continuous helical coils requiring unbroken REBCO conductor runs at lengths orders of magnitude beyond the October 2025 prototype (>4 m demonstrated; reactor scale requires tens of thousands of km).
- **Quantification**: C220103 coils = $2,323M (71% of RPE, 34% of total capital). At 2× multiplier, LCOE rises from $1,168/MWh to ~$3,000/MWh. **Coil cost uncertainty alone spans a factor of 2–4× in LCOE.**

**2. Small scale penalty: 70 MWe → $143B/GWe specific capital (10–20× higher than gigawatt-scale concepts)**
- **Mechanism**: At 70 MWe, HESTIA carries fixed costs of site infrastructure, regulatory qualification, grid connection over a small output base.
- **Quantification**: $10B / 70 MWe = $143B/GWe, compared to $6–15B/GWe for large tokamak designs. **HESTIA's specific capital is 5–10× higher than compact tokamaks and 10–20× higher than gigawatt-scale stellarators.**

**3. Novel liquid metal alloy (Sn-In-Pb-Li) with indium supply constraint**
- **Mechanism**: Indium is scarce (~900 tonnes/yr global production); fusion-scale demand for 90 large blanket modules could be material if indium fraction is >5–10 at.%.
- **Quantification**: Moderate cost increase but introduces supply-chain fragility not present in standard PbLi or FLiBe blankets.

**4. 250 GHz / 1 MW CW gyrotrons do not exist (TRL 1–2)**
- **Mechanism**: HESTIA's 8 T field and high plasma density require 250 GHz ECRH. Highest-frequency CW gyrotrons currently available are 170 GHz (ITER).
- **Quantification**: If 250 GHz gyrotrons cannot be developed, HESTIA cannot operate at its design point. Fallback to lower-frequency ECRH requires lower plasma density, reducing fusion power and net output.

**5. High Li-6 enrichment requirement (80 at.% — highest in portfolio)**
- **Mechanism**: Heliotron coil geometry intrudes into blanket space, reducing TBR margin. To compensate, HESTIA requires 80 at.% Li-6 enrichment.
- **Quantification**: The 3D TBR calculation was not completed as of 2023 publication, so TBR≥1.0 at 80 at.% is unconfirmed. **Binary risk: if TBR<1.0, concept is not viable.**

---

## 5. Cross-Concept Positioning

**Within the stellarator family**: HESTIA is the only heliotron in the portfolio; all other stellarators use quasi-isodynamic (QI) or classical modular coil geometries. The heliotron topology trades coil simplicity (two continuous coils vs. 40–50 modular coils) for manufacturing difficulty (unbroken kilometer-scale conductor runs vs. demountable joints). HESTIA's 70 MWe scale is 10–15× smaller than QI stellarators (Gauss 1 GWe, Proxima ~1 GWe); the economic thesis diverges completely — QI stellarators target single gigawatt plants, HESTIA targets fleet manufacturing of modular 70 MWe units.

**Within the D-T steady-state MFE family**: HESTIA competes with steady-state spherical tokamaks (ST-E1: 450–750 MWe, $11–16B/GWe) and large conventional tokamaks (SPARC-class: 200 MWe, $25–35B/GWe). HESTIA's specific capital ($143B/GWe at 70 MWe) is 5–10× higher than these comparators. However, the stellarator eliminates current-drive power and disruption risks, providing ~15–25% lower recirculating fraction and ~10–20 percentage point higher availability at equivalent technology maturity. **HESTIA's LCOE competitiveness depends entirely on whether the coil cost premium (2–5× manufacturing difficulty) and small-scale penalty (5–10× specific capital) can be offset by stellarator operational advantages and fleet manufacturing learning curves.**

**Unique positioning**: HESTIA is the only concept in the portfolio combining (1) continuous helical coils, (2) integrated liquid metal first wall/divertor, (3) sCO₂ power conversion targeting >50%, and (4) sub-100 MWe modular scale. This is either a brilliant integration of cost-saving innovations (if all four succeed) or a catastrophic concentration of failure modes (if any one fails to deliver). The sCO₂ dependency is the most load-bearing: at 40% Rankine fallback, HESTIA produces 23 MWe net at Q=13 and LCOE rises to $3,391/MWh, rendering it economically nonviable. **No other concept in the portfolio has a single subsystem whose underperformance causes a 2× LCOE increase.**



## 6. Modeling Confidence

**Rating: Low**

**Data-anchored parameters** (5 of 13 critical LCOE inputs):
1. Net electric output: 70 MWe (published)
2. Availability target: >80–85% (published; structural ceiling ~80%)
3. Plasma gain Q: ~13 (published)
4. Major radius: 7.8 m (published)
5. Magnetic field: 8 T at coil center (published)

**Speculative or analogue-derived parameters** (8 of 13):
1. **Capital cost by subsystem**: Framework ARIES defaults; no HESTIA-specific breakdown. Published $10B is total only.
2. **Thermal efficiency**: 48% aspirational; only 20 kWe demo at 20% exists.
3. **Minor radius**: 1.8 m estimated; not published.
4. **ECRH efficiency**: 1/3 by analogy; 250 GHz gyrotrons don't exist.
5. **LM pump power**: 15 MW placeholder; flagged "quite unknown" by authors.
6. **Coil cost**: Framework default is lower bound; 2–5× premium not captured.
7. **Blanket cost**: Framework default; exotic alloy costs more.
8. **O&M cost**: Framework default; no stellarator FPP data exists.

**Dominant uncertainty source**: Coil cost multiplier (1× vs. 2–5×) with elasticity +1.36 can increase LCOE by 2.5–8× ($1,170 → $3,000–10,000/MWh). Second: sCO₂ efficiency threshold (>50% required vs. 40–47% achievable) determines whether net output is 52 MWe ($1,533/MWh) or 23 MWe ($3,391/MWh). **These two uncertainties alone span 5–10× in LCOE.**

**Framework vs. published divergence**: Framework $6,848M vs. published $10,000M (46% gap). The $10B anchor implies LCOE ~$1,800/MWh; framework yields $1,168/MWh. **True LCOE bounded by [$1,170, $1,800]/MWh at 70 MWe, with both bounds being FOAK estimates and NOAK learning entirely speculative.**

---

## 7. What Would Change My Mind

1. **Coil manufacturing demonstration at >100 m continuous helical length with <$50/kA-m all-in cost**. If Helical Fusion demonstrates kilometer-scale continuous WISE REBCO winding at near-tokamak coil costs, the coil cost multiplier collapses from 2–5× to 1–1.5×, and LCOE drops from the $3,000–5,000/MWh range back to $1,500–2,000/MWh, making HESTIA competitive with compact tokamaks at FOAK.

2. **Fusion-coupled sCO₂ demonstration at ≥10 MWe achieving 48–50% net efficiency with tritium-compatible heat exchanger**. If NIFS Oroshhi-2 or similar facility demonstrates >48% sCO₂ with LM primary loop and tritium permeation barriers, the 50% efficiency assumption becomes credible. This retires the largest load-bearing uncertainty: the threshold that determines whether HESTIA produces 52 MWe (viable) or 23 MWe (nonviable) at Q=13.

3. **Independent bottom-up cost estimate showing <$50B/GWe specific capital at 70 MWe scale**. If PPPL, ORNL, or a European cost-modeling group produces subsystem-level breakdown showing continuous helical coils, LM blankets, and sCO₂ BOP at <$50B/GWe (comparable to compact tokamaks) via factory production and series learning, the small-scale penalty becomes surmountable. Requires demonstrating 50%+ NOAK reductions with quantitative learning rate justification.

---

## 8. LCOE Downselect Scoring

### Summary Table: Scored Criteria

| Criterion | Score | Justification Summary |
|-----------|-------|----------------------|
| **C1: Modularization** | **2.5** | Weighted average 1.46 (coils 67% of scored capital are stick-built, mode=1) + 1.0 repetition boost (90 LM modules). C220103 continuous helical coils (34% of total capital) cannot be factory-wound. |
| **C3: Supply Chain Learning** | **2.8** | Sub-scores: A=2.7 (learning rates dominated by fusion-specific novelty), B=2.5 (hard constraints: 250 GHz gyrotrons, indium supply, Li-6 enrichment, REBCO scale-up), C=3.0 (external demand ~40%: REBCO tape, sCO₂, structures; but coil fabrication fusion-specific). |
| **C4: Plant Complexity** | **4.0** | Sub-scores: A=3.0 (moderate coupling: LM/sCO₂ failures force shutdown but don't cascade to damage; stellarator avoids disruption cascades), B=5.0 (only 4 CAS22 sub-accounts >1% total capital: coils, blanket, ECRH, shield). |
| **C5: Customization Needs** | **1.7** | Sub-scores: A=2 (large cooling towers, standard thermal), B=1 (D-T full tritium handling, 80 at.% Li-6). Raw (2+1)/2=1.5, scaled to [1,5]: 1+0.5×(4/3)=1.67. |
| **C8: Data Adequacy** | **2.5** | Sub-scores: A=3 (mix of independent peer-reviewed and company sources, but cost company-only), B=3 (conceptual design with gaps: TBR incomplete, LM pump unknown, H=1.3 unvalidated), C=1 (8 blocking gaps), D=3 (clear pathway HARUKA→KANATA→HESTIA but no fleet manufacturing plan). |

### C7 Risk Matrix: 7 Functions × 2 Subcategories

| Function | Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|----------|-------------|-------------------|-------------------|-----------|-------------------|----------------|------|
| **F1: Plasma Performance** | Physics | H_ISS04 = 1.3 confinement factor at Q~13, 260 MW fusion power, steady-state | W7-X H_ISS04 = 1.4 (transient, QI geometry); LHD H_ISS04 ~ 1.0 (heliotron, steady) | 1.3 / 1.4 = 0.93 (within demonstrated); 1.3 / 1.0 = 1.3× (vs. heliotron heritage) | Center-peaked ECH heating + magnetic optimization claims H=1.3 in heliotron geometry; HARUKA demo will validate | Degrading | **4** (W7-X near-regime QI at H=1.4; heliotron at H=1.0 is subscale) |
| **F1: Plasma Performance** | Hardware | Plasma-facing components at 1–2 MW/m² neutron wall loading (est.), 1-year continuous burn, 90 modular LM blanket first wall | LHD long-pulse stellarator plasmas (minutes to hours, not years); WEST tungsten divertor 1000+ pulses at 5 MW/m² heat flux (not neutrons) | N/A (1-year continuous burn never demonstrated in any stellarator) | LM first wall integrates blanket/divertor/shield; GALOP lab-scale validation; 90 modules with crane access for replacement | Degrading | **3** (subscale: LHD pulses are <1% of 1-year duration; WEST is tokamak heat flux analogue, not stellarator neutron environment) |
| **F2: Driver / Energy Input** | Physics | 20 MW absorbed ECRH at 250 GHz in 8 T field, ~10% edge density for cutoff avoidance | ITER 170 GHz / 1 MW CW gyrotrons (20 units ordered); LHD 154 GHz ECRH at ~5 MW total | 250 / 170 = 1.47× frequency gap | Joint R&D with QST on 250 GHz / 1 MW CW gyrotrons; frequency scaling from 170 GHz technology | Degrading | **2** (design study: 250 GHz / 1 MW CW does not exist; 170 GHz is adjacent frequency but power/efficiency at 250 GHz undemonstrated) |
| **F2: Driver / Energy Input** | Hardware | 60 gyrotrons × 1 MW each, CW operation for 1-year burn, transmission efficiency to achieve 20 MW absorbed | ITER gyrotron contracts: 1 MW / 170 GHz / CW capability demonstrated in test stands (Thales, JAEA) | 60 units vs. 20 (ITER) = 3× unit count; 250 vs. 170 GHz = undemonstrated | Mass production of gyrotrons at lower frequency (ITER precedent); waveguide transmission at 250 GHz follows ITER methodology | Degrading | **3** (subscale: ITER 170 GHz gyrotrons exist, but 250 GHz tube physics, window materials, and efficiency unproven at 1 MW CW) |
| **F3: Instability Control** | Physics | Intrinsic stellarator stability: no disruptions, no current-driven instabilities, neoclassical transport losses acceptable | W7-X 30-minute plasmas with no disruptions; stellarator intrinsic stability demonstrated across LHD, TJ-II, HSX | Gap ratio = 1.0 (stellarators are intrinsically stable) | External 3D shaping provides rotational transform; no current drive needed; neoclassical optimization in heliotron geometry | Degrading | **5** (operating-regime: stellarator stability at commercial scale is demonstrated across W7-X, LHD; heliotron shares this property) |
| **F3: Instability Control** | Hardware | Magnetic diagnostics, feedback control for density/temperature, no active disruption mitigation required | W7-X magnetic diagnostics suite; LHD steady-state control systems; stellarator control at reactor scale is simpler than tokamaks (no disruption mitigation hardware) | Gap ratio ≈ 1.0 (diagnostics/control for stellarators well-established) | Standard stellarator diagnostics (magnetics, Thomson scattering, ECE) + feedback on gas puff, ECRH power | Degrading | **5** (operating-regime: stellarator feedback control demonstrated at W7-X, LHD; no new control physics at HESTIA scale) |
| **F4: Plasma-Wall Interaction** | Physics | Liquid metal first wall heat flux handling: ~1–2 MW/m² (estimated), impurity control with LM surface, 1-year exposure | Lithium tokamak walls (NSTX, FTU): liquid Li at ~1 MW/m² heat flux for seconds to minutes (not steady-state); FLiBe surface chemistry from MSR (fission) | Heat flux time-integrated exposure: 1 year vs. minutes = ~500,000× gap | LM flow refreshes surface; tin vapor pressure suppression; GALOP validates MHD-driven flow at lab scale | Degrading | **2** (simulation/analogue: lithium tokamak walls are transient; LM flow at 1–2 MW/m² for 1 year is undemonstrated; MSR FLiBe is fission, not fusion) |
| **F4: Plasma-Wall Interaction** | Hardware | Sn-In-Pb-Li alloy compatibility with high-Mn austenitic steel, tritium permeation barriers, 90 modules at 800–1200 K, corrosion <1 mm/yr | Tohoku high-Mn steel characterized (2024 paper); GALOP lab-scale LM loop (4m×2m×2m); PbLi/steel corrosion data from fission programs (ORNL) | N/A (Sn-In-Pb-Li composition unpublished; corrosion vs. high-Mn steel unmeasured at fusion conditions) | Material selection based on vapor pressure, tritium solubility, MHD compatibility; Tohoku collaboration on steel development | Degrading | **2** (simulation: high-Mn steel exists but Sn-In-Pb-Li/steel compatibility at 800–1200 K unmeasured; GALOP is lab-scale, not reactor MHD environment) |
| **F5: Neutron/Particle Handling** | Physics | 14 MeV neutron streaming through helical coil geometry, Li-6(n,α)T breeding with 80 at.% enrichment, TBR ≥ 1.05 | MCNP/Serpent 3D neutronics for FFHR stellarator designs (NIFS heritage); DT tokamak neutronics (JET, TFTR) at <1 MW/m² | TBR calculation incomplete as of 2023 paper; heliotron geometry reduces blanket coverage vs. tokamak | 3D Monte Carlo with ENDF/B cross-sections; 80 at.% Li-6 compensates for reduced coverage; 90 modular blankets optimized for neutron capture | Binary | **2** (simulation: NIFS has FFHR neutronics experience, but HESTIA TBR not yet calculated; 80 at.% is highest enrichment in portfolio—if TBR<1.0, design fails) |
| **F5: Neutron/Particle Handling** | Hardware | High-Mn austenitic steel radiation damage tolerance: ~20–40 dpa over 30-year life (estimated), activation, He production, dimensional stability | PWR steel: ~40 dpa fission spectrum over decades (commercial operation); fusion steel (EUROFER, F82H) tested to 80 dpa in fission reactors (HFIR, BOR-60) | 14 MeV fusion vs. fission spectrum = ~2× He production per dpa; high-Mn steel is novel (no fusion irradiation data) | High-Mn reduces activation vs. standard austenitic steel; NIFS/Tohoku development program; post-irradiation testing planned | Degrading | **3** (adjacent analogue: fission steel at 40 dpa is operating-regime for fission spectrum; fusion 14 MeV at 20–40 dpa is adjacent; high-Mn steel is untested in fusion) |
| **F6: Fuel Cycle Closure** | Physics | Tritium breeding in Sn-In-Pb-Li at 80 at.% Li-6, TBR ≥ 1.05 margin, tritium extraction from LM at ppm levels | ITER tritium breeding blanket test modules (TBM) design; Li-Pb eutectic TBR calculations (ARIES, PPPL studies); tritium in Li measured (lab-scale) | TBR not yet calculated for HESTIA; Li-6 enrichment 80 at.% is highest in portfolio (supply-limited) | NIFS FFHR neutronics heritage; GALOP will test tritium extraction from LM; molten salt reactor tritium extraction methods applicable | Binary | **2** (simulation: NIFS can calculate TBR, but result unknown; if TBR<1.0 at 80 at.%, no path forward—cannot enrich further due to supply limits) |
| **F6: Fuel Cycle Closure** | Hardware | Tritium extraction from Sn-In-Pb-Li at 90-module scale, permeation barriers for sCO₂ HX at 800–1200 K, tritium inventory <1 kg, purification/recycling at 70 MWe burn rate | Molten salt reactor (MSR) tritium extraction (ORNL MSRE); ITER tritium plant design (not yet operated); permeation barriers (Al₂O₃, Er₂O₃) tested at <700 K | Sn-In-Pb-Li extraction kinetics unknown; permeation barriers at 800–1200 K undemonstrated for fusion | GALOP platform tests extraction; sCO₂ HX will use advanced coatings; ITER tritium plant methodology adapted to LM | Degrading | **2** (design study: MSR extraction is analogue but different chemistry; ITER plant is undemonstrated; permeation barriers at 800–1200 K are beyond current state) |
| **F7: Power Conversion & BOP** | Physics | Tritium containment in sCO₂ loop, thermal stratification in LM-to-sCO₂ HX, MHD pressure drop in LM primary acceptable | CSP sCO₂ Brayton at 10 MWe (GTI STEP Phase 1, 500°C, 2024); Sandia sCO₂ test loop at 1 MWe; molten salt HX from fission (ORNL MSRE, 650°C) | Fusion LM-to-sCO₂ HX at 800–1200 K never demonstrated; tritium permeation into sCO₂ unmeasured | NIFS Oroshhi-2 sCO₂ demo targets >50% at 20 kWe → 20 MWe pathway; permeation barriers + tritium monitors in sCO₂ loop | Degrading | **3** (subscale: CSP sCO₂ at 10 MWe / 500°C is operating at lower temperature; 800–1200 K LM HX is undemonstrated; tritium permeation is novel fusion challenge) |
| **F7: Power Conversion & BOP** | Hardware | sCO₂ turbomachinery at >50% net efficiency (800–1200 K hot leg), compact HX with tritium barriers, GALOP LM pumps at 90-module scale, pump power <15 MW | GTI STEP Phase 1: 10 MWe at 40% gross (500°C, Oct 2024); Phase 2 targets 10 MWe at 715°C; GE sCO₂ turbine test at 1 MWe; GALOP lab-scale pump (4m×2m×2m, <1 kW est.) | 50% efficiency at 800–1200 K undemonstrated (20 kWe at 20% is current NIFS state); LM pump power at 90-module scale "quite unknown" (authors' quote) | Path to 50%: higher turbine inlet temp (800–1200 K vs. 715 K GTI Phase 2) + recompression cycle; GALOP pump scales via gas pressure + module count | Degrading | **2** (design study: sCO₂ at 50% / 800–1200 K is aspirational beyond current 40–47% commercial; LM pump scaling unvalidated; tritium HX is novel) |

**Function-level means** (symmetric average of physics + hardware tiers):

- **F1**: (4 + 3) / 2 = **3.5**
- **F2**: (2 + 3) / 2 = **2.5**
- **F3**: (5 + 5) / 2 = **5.0**
- **F4**: (2 + 2) / 2 = **2.0**
- **F5**: (2 + 3) / 2 = **2.5**
- **F6**: (2 + 2) / 2 = **2.0**
- **F7**: (3 + 2) / 2 = **2.5**

**Heritage credit**: D-T stellarator → floor = 4.0 for F1–F7 (per scoring framework, stellarator heritage). Apply floor:
- F1: max(3.5, 4.0) = **4.0**
- F2: max(2.5, 4.0) = **4.0**
- F3: max(5.0, 4.0) = **5.0**
- F4: max(2.0, 4.0) = **4.0**
- F5: max(2.5, 4.0) = **4.0**
- F6: max(2.0, 4.0) = **4.0**
- F7: max(2.5, 4.0) = **4.0**

**Binary risks identified**:
1. F5 (Neutron/Particle Handling - Physics): TBR < 1.0 at 80 at.% Li-6 enrichment (if 3D calculation yields TBR<1.0, tritium self-sufficiency impossible)
2. F6 (Fuel Cycle Closure - Physics): Tritium breeding failure (same risk as F5; cannot breed enough tritium to sustain D-T burn)

---

```yaml
---
scores:
  C1: 2.5
  C3: 2.8
  C4: 4.0
  C5: 1.7
  C8: 2.5
  F1: 4.0
  F2: 4.0
  F3: 5.0
  F4: 4.0
  F5: 4.0
  F6: 4.0
  F7: 4.0
  binary_risks:
    - "TBR < 1.0 at 80 at.% Li-6 enrichment (if 3D neutron transport calculation yields TBR below unity, tritium self-sufficiency is impossible and design cannot proceed)"
    - "Tritium breeding failure in Sn-In-Pb-Li blanket system (heliotron coil geometry intrusion into blanket space reduces coverage; if TBR cannot reach ≥1.05 even with 80 at.% Li-6—highest enrichment feasible due to global supply constraints—concept is not viable for D-T operation)"
---
```
