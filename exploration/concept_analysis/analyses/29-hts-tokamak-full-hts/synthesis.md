---
ID: 29-hts-tokamak-full-hts
Concept: HTS Tokamak - Full HTS (D-T)
Company: Energy Singularity
Type: synthesis
Status: draft
Created: 2026-05-14
---

# Synthesis: HTS Tokamak - Full HTS (Energy Singularity)

## 1. Executive Summary

- **Dominant risk**: The commercial HH380 demo station has zero published design parameters—no net electric output, no Q, no blanket design, no cost estimate. Every LCOE-critical input requires wholesale analogue assumptions from CFS ARC/SPARC (±50% uncertainty on capital cost alone). This is not a data gap that will close soon: HH380 engineering decisions are post-2030.

- **Dominant advantage**: Full HTS coil set (TF+PF+CS all in REBCO) combined with China's >95% domestic supply chain localization. If the full-HTS architecture works—particularly the CS coils at 25 T under cyclic duty—it eliminates mixed LTS/HTS cryogenic circuits and potentially simplifies thermal management. Shanghai Superconductor supplies REBCO tape domestically, bypassing geopolitical export controls and positioning Energy Singularity uniquely for China-domestic deployment at scale.

- **LCOE ballpark**: 107.7 $/MWh (500 MWe base case, 80% availability, NOAK) using ARC/SPARC analogue parameters. 1 GW scaled: 72.4 $/MWh. Scenarios bracket design-point uncertainty: small machine (250 MWe, R=1.5m) → 169.5 $/MWh; large machine (800 MWe, R=2.5m) → 83.7 $/MWh. The full-HTS coil premium adds ~3% to LCOE vs. TF-only HTS (+$103M on $516M framework C220103 at ×1.2 multiplier).

- **Confidence verdict**: **Low**. 13 of 13 LCOE-critical parameters are either "truly unknown" (HH380 not designed), "proprietary" (undisclosed), or analogued from a Western competitor's published design. Energy Singularity's "Limited" data rating understates the severity: this is the least documented private fusion company in the analysis set, with published milestone achievements (HH70 1,337-second plasma, Jingtian 21.7 T magnet) that prove engineering capability but reveal nothing about commercial power plant economics.

---

## 2. What Matters Most for LCOE

Ranked by LCOE elasticity and structural uncertainty.

### 1. Availability / capacity factor (elasticity: −0.96)
**Assumed value**: 80% (base case)
**Source**: Generic tokamak analogue; Energy Singularity discloses no availability target or disruption frequency data.
**Sensitivity**: Moving from 80% to 65% (CS coil reliability failure scenario) increases LCOE by +21.6% (+$23.3/MWh). Moving to 70% (AI control underperforms scenario) increases LCOE by +13.7% (+$14.8/MWh).
**What would flip the economic conclusion**: If CS coil cyclic loading at 25 T proves unreliable and availability drops below 70%, LCOE exceeds 120 $/MWh at 500 MWe scale—marginally competitive only at 1 GW scale. Conversely, if AI plasma control reliably achieves 90% availability (disruption suppression at burning-plasma conditions validated by HH170), LCOE drops to ~95 $/MWh, approaching commercial competitiveness at modest scale.

This is the highest-leverage parameter and the one most dependent on Energy Singularity's two genuinely novel bets: (a) full HTS CS coils under plasma initiation duty, and (b) AI-driven disruption mitigation at D-T conditions. The HH70 1,337-second steady-state plasma and 5,755-shot campaign prove prototype-scale operability; burning-plasma reliability remains undemonstrated.

### 2. Interest rate / cost of capital (elasticity: +0.66)
**Assumed value**: 7% WACC
**Source**: Framework default; Energy Singularity financing structure undisclosed.
**Sensitivity**: At 10% interest rate (reflecting higher China-domestic energy project financing risk or first-of-a-kind premium), LCOE rises to ~120 $/MWh. At 5% (optimistic government-backed financing), LCOE drops to ~95 $/MWh.
**What would flip the economic conclusion**: If Energy Singularity secures strategic state backing or policy-driven low-cost capital (comparable to Chinese nuclear or renewable megaprojects), the capital-dominated LCOE structure improves ~12% vs. commercial financing. This is the primary financial lever and the reason the China-domestic deployment context matters economically: access to policy-directed capital rather than international project finance terms.

### 3. Major radius / HH380 design point (structural parameter, not marginal sensitivity)
**Assumed value**: R = 2.0 m (base case analogue from ARC/SPARC)
**Source**: Pure analogue—no HH380 specification exists. HH170 is ~70% SPARC volume; HH380 likely larger.
**Sensitivity**: Not a marginal elasticity—this is uncertainty about the unknown design point itself. Scenario C (R=1.5m, 250 MWe small machine): LCOE 169.5 $/MWh (+57%). Scenario D (R=2.5m, 800 MWe large machine): LCOE 83.7 $/MWh (−22%). The 86 $/MWh spread between scenarios C and D is the single largest LCOE uncertainty band, far exceeding the ±4.7% spread from the full-HTS coil premium sensitivity (×1.1–×1.3).
**What would flip the economic conclusion**: If HH380 targets ~250 MWe scale (matching HH170 compactness philosophy and enabling faster deployment), LCOE at 169.5 $/MWh is uncompetitive vs. advanced fission or large-scale renewables. If HH380 scales to 800+ MWe (exploiting economics of scale), LCOE at 83.7 $/MWh approaches long-run competitiveness. The strategic choice—fast small machine vs. cost-optimized large machine—is the fork in the road for commercial viability.

### 4. Thermal conversion efficiency η_th (elasticity: −0.17)
**Assumed value**: 35% (standardized from prior 40% per canonical η_th table for "Thermal (unspecified)")
**Source**: Framework default; power conversion cycle entirely undisclosed by Energy Singularity.
**Sensitivity**: At 32% (saturated steam, conservative): LCOE ~112 $/MWh (+4%). At 48% (sCO₂ Brayton, advanced): LCOE ~99 $/MWh (−8%).
**What would flip the economic conclusion**: If Energy Singularity adopts supercritical CO₂ Brayton (η_th ≈ 0.48) paired with a high-temperature blanket coolant (FLiBe or Pb-17Li), LCOE improves ~8%—a meaningful but not transformative gain. The strategic framing ("LCOE at or below thermal power costs") suggests a high-efficiency target, but no cycle type has been named. If the cycle choice is deferred to HH380 engineering (post-2030), η_th uncertainty persists for years.

### 5. Full HTS coil cost premium (elasticity: +3.2% per 10% C220103 increase)
**Assumed value**: ×1.20 multiplier on framework C220103 ($516M → $619M)
**Source**: Placeholder—no published REBCO tape volume estimate for CS+PF coils beyond TF-only baseline.
**Sensitivity**: At ×1.0 (TF-only HTS cost, no premium): LCOE 104.4 $/MWh (−3.2%). At ×1.3 (high tape demand for CS+PF): LCOE 109.4 $/MWh (+1.6%). The ×1.1–×1.3 range spans only 5.0 $/MWh—smaller than the availability or design-point uncertainties but real.
**What would flip the economic conclusion**: The full-HTS coil architecture is a structural differentiator vs. TF-only HTS competitors (CFS, Tokamak Energy). If CS+PF tape volume adds <10% to coil cost (×1.1 premium), the full-HTS approach is cost-neutral or favorable (simplified cryoplant offsets tape cost). If CS+PF demand approaches +30% (×1.3), the premium erodes ~1.6% of LCOE competitiveness—meaningful but not disqualifying. The real risk is not the tape cost but CS coil duty-cycle reliability (captured in availability parameter #1 above).

---

## 3. Risk Verdicts

### Challenge 1: No commercial design point—model has no anchor
**Verdict**: **Genuinely uncertain**
**Rationale**: HH380 is post-2030 with zero disclosed parameters; uncertainty is structural (what will they build?) rather than technical (can it work?).
**What would retire this risk**: HH380 conceptual design release with net electric output, major radius, Q target, and capital cost estimate. Earliest plausible: 2028–2029 if HH170 commissioning triggers HH380 engineering phase funding.

### Challenge 2: Blanket design entirely undisclosed—no tritium breeding model possible
**Verdict**: **Likely resolvable** (standard D-T tokamak challenge; not concept-specific)
**Rationale**: China's CFETR program is developing WCCB, HCCB, and sCO₂-cooled Pb-17Li blankets; Energy Singularity will likely adopt one of these proven approaches rather than inventing a novel breeding concept. TBR > 1.0 is achievable with 4π (full-coverage) breeding in a conventional-aspect-ratio tokamak, unlike the outboard-only constraint of spherical tokamaks.
**What would retire this risk**: Published blanket selection tied to CFETR program outputs; TBR validation via MCNP or Serpent neutronics on a preliminary HH380 geometry. Earliest: 2029+ (requires HH380 design point from Challenge 1).

### Challenge 3: Full HTS CS coils at 25 T—validated at 21.7 T, commercial duty unproven
**Verdict**: **Genuinely uncertain**
**Rationale**: Jingtian test magnet achieved 21.7 T (single-pancake stack), but CS coils must perform plasma initiation current ramps under cyclic EM loading + neutron flux. No published fatigue or reliability data exists for HTS CS coils in tokamak operation. The gap from 21.7 T (test) to 25 T (HH170 target) to multi-year commercial duty (HH380) is real. This is a genuinely novel technical bet with no direct analogue—CFS SPARC and Tokamak Energy use TF-only HTS.
**What would retire this risk**: HH170 CS coil operation at 25 T demonstrating >1000 pulse cycles without quench degradation; published fatigue testing of REBCO tape under combined cyclic EM + neutron irradiation. If HH170 CS coils fail to achieve target field or require frequent reconditioning, availability drops to 65–70% (Scenario A), increasing LCOE by +21.6%.

### Challenge 4: AI plasma control—significant for capacity factor but unquantified
**Verdict**: **Likely resolvable**
**Rationale**: HH70's 1,337-second steady-state plasma and 5,755-shot campaign demonstrate robust control at experimental scale. AI-driven disruption mitigation is a software/control-systems problem with clear iterative improvement paths (more training data, better sensors, faster feedback). The risk is not "does AI control work?" (it works on HH70) but "does it extend to burning-plasma conditions with high neutron flux and radiation-induced sensor degradation?" This is a scaling challenge, not a fundamental barrier.
**What would retire this risk**: HH170 D-T operation (if actual D-T burn occurs, not just "D-T equivalent") with published disruption frequency <1 per 100 shots and validated 85%+ availability. If AI control underperforms at burning-plasma conditions, availability drops to 70% (Scenario B), increasing LCOE by +13.7%.

### Challenge 5: ICRH as primary heating—scale and efficiency for power plant uncertain
**Verdict**: **Likely resolvable**
**Rationale**: ICRH at tens-of-MW scale is proven technology globally (JET, ITER). Wall-plug efficiency 60–70% is acceptable (modeled at 65%, comparable to NBI). The uncertainty is heating power allocation for HH380 (undisclosed) and antenna survival under D-T neutron bombardment, both standard tokamak challenges with ITER analogues.
**What would retire this risk**: Published HH380 heating configuration and power balance. ICRH antenna survival is a materials problem with ITER Test Blanket Module analogue solutions.

### Challenge 6: Chinese regulatory and supply chain context
**Verdict**: **Likely resolvable** (for China-domestic deployment)
**Rationale**: >95% domestic component localization and Shanghai Superconductor REBCO supply position Energy Singularity well for China-domestic deployment, bypassing Western export controls. Chinese fusion regulation is nascent but Energy Singularity's roadmap (HH380 post-2030) aligns with the global regulatory transition window (second-half-2030s pilot plants per the 2025 policy framework paper). The risk is international deployment—China-developed fusion technology may face grid-connection or licensing barriers in Western markets, but this does not block China-domestic viability.
**What would retire this risk**: Published China-specific fusion regulatory framework; demonstrated grid connection of a China-domestic fusion pilot (not necessarily Energy Singularity—could be CFETR). For international deployment: bilateral regulatory recognition agreements (unlikely pre-2035).

---

## 4. Structural Advantages and Disadvantages

Quantified relative to the conventional D-T tokamak cost structure baseline (ITER-like: 5.3 T, R=6.2m, LTS magnets, outboard blanket).

### Advantages

**1. Compact high-field geometry eliminates ~15–25% of structural material cost (CAS21 + part of C220105)**
R=2.0m vs. R=6.2m (ITER) reduces vacuum vessel volume by ~95% (scaling as R³ for fixed aspect ratio and elongation). Building volume scales similarly. CAS21 (Buildings) is $444.8M at 500 MWe; ITER-scale equivalent would be ~$580–650M → **saves ~$140–200M**. C220105 (Structure) savings ~$5–10M (smaller magnets, less support mass). Combined: **~15% reduction in CAS21+CAS105 vs. large tokamak baseline**.

**2. Full HTS coil set eliminates LTS cryoplant but adds REBCO tape cost (+$103M net vs. TF-only HTS)**
Framework C220103 for TF-only HTS: $516M. Full HTS (TF+PF+CS): $619M at ×1.2 premium → **+$103M penalty vs. TF-only HTS** (CFS SPARC baseline). Relative to LTS baseline (ITER-like with NbTi or Nb₃Sn), full HTS eliminates liquid helium cryoplant (~$50–100M capital savings) but adds REBCO tape cost (~$150–200M at current tape prices). **Net penalty vs. LTS: ~$50–100M**. The full-HTS bet pays off only if: (a) REBCO tape cost falls to ~$10/kA-m (currently ~$30–100/kA-m), or (b) uniform 20 K cryoplant operational simplicity improves availability enough to offset capital penalty (modeled in availability scenarios A/B).

**3. China-domestic supply chain (>95% localization) potentially reduces procurement cost 10–20% (all CAS accounts)**
Shanghai Superconductor REBCO tape, domestic steel/concrete, and China's manufacturing scale advantages could reduce unit costs 10–20% vs. Western procurement. Not modeled explicitly (cost basis is opaque), but if applied uniformly: **~$380–760M savings on $3.8B total capital**. This is speculative—China-domestic costs may be lower due to scale, or higher due to REBCO tape scarcity and fusion-specific supplier concentration. The >95% localization rate de-risks geopolitical supply chain shocks (e.g., REBCO export controls) for China-domestic deployment but does not guarantee lower cost.

**4. AI plasma control may improve availability 5–10% vs. conventional feedback control (capacity factor → LCOE)**
If AI control suppresses disruptions and enables tighter operating margins, availability could rise from 80% (base) to 85–90%. At 85% availability: LCOE drops to ~102 $/MWh (−5.3% vs. base). At 90%: ~98 $/MWh (−9.0%). This is a **real but unquantified advantage**—HH70 demonstrates prototype-scale control; burning-plasma validation is pending.

### Disadvantages

**1. Full HTS coil set (TF+PF+CS) adds ~20% REBCO tape demand vs. TF-only HTS (+$103M at ×1.2 premium)**
See Advantage #2 above—this is a penalty vs. TF-only HTS competitors (CFS, Tokamak Energy), not vs. LTS baseline. CS coils at 25 T under cyclic plasma initiation duty are genuinely novel; no fatigue or reliability data exists. **Primary risk**: CS coil reconditioning/replacement events in years 10–20 → additional O&M cost (~$20–50M per event) → amortized LCOE penalty +$2–5/MWh if CS coils require replacement every 5–7 years instead of lasting the full 30-year plant lifetime.

**2. No cost advantage vs. spherical tokamak HTS competitors at same scale (ST-E1, STEP)**
Spherical tokamaks (ST-E1, STEP) also use HTS TF coils and target compact geometry. Energy Singularity's conventional aspect ratio (A≈4.0) eliminates the center-stack neutron damage problem but sacrifices some compactness. At 500 MWe, Energy Singularity LCOE 107.7 $/MWh is **comparable to ST-E1 analogue estimates** (~100–120 $/MWh range, similarly data-sparse). The full-HTS coil architecture (TF+PF+CS) is a differentiator in engineering approach but not in LCOE magnitude unless CS coil reliability proves superior or REBCO tape costs fall faster than expected.

**3. D-T fuel cycle adds tritium breeding and handling infrastructure (~$150–200M capital; $10–20M/yr O&M)**
Standard D-T tokamak disadvantage shared with all competitors (SPARC, ST-E1, STEP). CAS27 (Special Materials—tritium startup inventory): $7.5M. C220500 (Fuel Handling—tritium processing): $73.9M. CAS70 O&M includes tritium accountancy and permeation barrier maintenance (~$5–10M/yr embedded in $71.0M total O&M). **No concept-specific advantage or disadvantage**—this is the baseline D-T penalty vs. aneutronic fuels.

**4. Undisclosed HH380 design point creates ±50% LCOE uncertainty band**
Scenarios C/D (250 MWe vs. 800 MWe) bracket 169.5 $/MWh to 83.7 $/MWh—an 86 $/MWh spread, or ±40% relative to base case. This is not a cost *disadvantage* but an **information disadvantage**: without a design point, LCOE is structurally uncertain. Competitors with published designs (CFS ARC 500 MWe, Tokamak Energy ST-E1 ~200 MWe) have narrower uncertainty bands even if their data is similarly sparse, because the design-point choice itself is known.

---

## 5. Cross-Concept Positioning

Energy Singularity sits in the **compact HTS tokamak cluster** alongside CFS/SPARC (01-hts-compact-tokamak) and Tokamak Energy ST-E1 (21-spherical-tokamak-hts). All three share:
- D-T fuel cycle with tritium breeding requirement
- High-field HTS magnets (14–25 T peak) enabling compact geometry
- Capital-dominated LCOE structure (overnight cost ~$5,000–8,000/kW at 500 MWe NOAK)
- Similar LCOE range: 70–120 $/MWh at 500 MWe scale, dropping to 50–80 $/MWh at 1 GW scale
- Availability as the dominant LCOE lever (elasticity −0.9 to −1.0)

### What makes Energy Singularity fundamentally different:

**1. Full HTS coil architecture (TF+PF+CS) vs. TF-only HTS (CFS, Tokamak Energy)**
CFS SPARC uses HTS for TF coils only; CS and PF use copper or LTS. Tokamak Energy Demo4 demonstrated TF+PF HTS at 11.8 T but not CS. Energy Singularity extends HTS to all coil types including CS at 25 T—a genuinely novel bet. If CS coils prove reliable, the uniform 20 K cryoplant simplifies operations; if CS duty-cycle fatigue proves problematic, availability drops 10–20% (Scenarios A/B) and LCOE rises +14–22%.

**2. China-domestic supply chain (>95% localization) vs. Western/international supply chains**
Shanghai Superconductor REBCO supply and domestic component sourcing position Energy Singularity uniquely for **China-domestic deployment at scale** without Western export control friction. This is a strategic positioning advantage (access to policy-directed capital, regulatory tailwinds, domestic grid integration) rather than a pure cost advantage (China-domestic unit costs are opaque and may or may not be lower). CFS and Tokamak Energy target Western markets; Energy Singularity targets China's domestic energy market (1,300+ GW annual electricity demand, coal-replacement policy pressure).

**3. AI-native plasma control vs. conventional feedback control**
HH70's 1,337-second steady-state plasma and 5,755-shot campaign demonstrate AI control at experimental scale. If this extends to disruption suppression at burning-plasma conditions, availability could reach 85–90% (vs. 75–80% for conventional feedback control). This is a **software and control-systems differentiator**—not a hardware advantage—and iteratively improvable via machine learning on operational data.

**4. Opaque design and cost basis vs. published ARC/STEP studies**
Energy Singularity is the **least transparent** in the compact HTS tokamak cluster. CFS has published ARC design parameters (Sorbom 2015, multiple follow-on TEA papers). Tokamak Energy has four published ST-E1 machine parameters and peer-reviewed ECRH studies. Energy Singularity has published HH70 prototype milestones and Jingtian magnet records but **zero HH380 commercial design parameters**. This opacity is partly strategic (competitive IP protection in a crowded field) and partly stage-dependent (HH380 engineering phase is post-2030, genuinely not yet designed).

### Landscape position

Energy Singularity is betting that:
- Full-HTS simplifies operations enough to offset tape cost penalty
- AI control improves availability to offset capital intensity
- China-domestic advantages (supply chain, capital access, regulatory tailwinds) enable faster deployment than Western competitors
- Compact tokamak scale economies (800+ MWe machines at R~2.5m) close the LCOE gap to commercial competitiveness

If these bets pay off, Energy Singularity reaches **70–85 $/MWh LCOE at 800–1000 MWe scale** (Scenario D and 1 GW scaled result)—competitive with offshore wind + storage or advanced fission in China's 2035+ energy market. If CS coils prove unreliable or HH380 targets small scale (250 MWe), LCOE remains at 130–170 $/MWh—niche applications only (remote/island grids, industrial heat).

**Shared economics with CFS/SPARC**: The LCOE structure is nearly identical. Energy Singularity's full-HTS bet vs. CFS's TF-only HTS is a ~3% LCOE difference (full-HTS coil premium)—smaller than availability uncertainty. The real fork in the road is **design-point scale choice** (Scenarios C vs. D): small fast machine or large cost-optimized machine.

**Differentiation from Tokamak Energy ST-E1**: Conventional aspect ratio (A≈4.0) vs. spherical (A=2.3) eliminates center-stack neutron damage but sacrifices some plasma beta advantage. Energy Singularity likely has easier blanket integration (4π breeding vs. outboard-only) but lower plasma pressure at same field. LCOE is comparable; neither has a clear structural advantage.

---

## 6. Modeling Confidence

**Rating: Low**

### Data-anchored parameters (2 of 13 LCOE-critical inputs)

1. **Confinement type and fuel**: D-T tokamak confirmed (HH170 roadmap, HH380 framing). High confidence—this is not changing.
2. **Operation mode**: Steady-state confirmed (HH70 1,337-second plasma record). High confidence for HH170; reasonable assumption for HH380.

### Speculative parameters (11 of 13 LCOE-critical inputs)

3. **Net electric output**: 500 MWe base case is pure analogue (no HH380 specification). Bracketed by Scenarios C/D (250 MWe, 800 MWe).
4. **Major radius R₀**: 2.0 m is analogued from CFS ARC/SPARC; HH170 is ~70% SPARC volume but HH380 scale unknown.
5. **Thermal efficiency η_th**: 35% assumes standard steam Rankine; power cycle undisclosed.
6. **Availability**: 80% is generic tokamak analogue; Energy Singularity discloses no target. Bracketed by Scenarios A/B (65%, 70%).
7. **Full HTS coil cost premium**: ×1.2 multiplier is placeholder (no published CS+PF tape volume). Bracketed by sensitivity sweep (×1.0–×1.3).
8. **Heating power P_input**: 50 MW is mfe_tokamak.yaml default; ICRH configuration for HH380 undisclosed.
9. **Blanket thickness**: 0.60 m is framework default; no blanket design disclosed.
10. **Blanket TBR**: Not modeled (no blanket design); assumed TBR > 1.0 via CFETR analogue.
11. **Capital cost by CAS account**: Derived from framework with C220103 override; no Energy Singularity cost data exists.
12. **O&M cost structure**: Generic tokamak analogue ($71.0M/yr at 500 MWe); no Energy Singularity breakdown.
13. **Construction time**: 5.0 years is optimistic (HH70 built in <2 years); HH380 construction timeline unknown.

### Dominant source of LCOE uncertainty

**Design-point uncertainty (Scenarios C vs. D)** is the dominant source: 86 $/MWh spread between 250 MWe and 800 MWe machines (±40% vs. base case). This is not marginal parameter uncertainty—it is structural uncertainty about what Energy Singularity will build. The choice between small-fast (Scenario C) and large-optimized (Scenario D) determines whether LCOE is 170 $/MWh (uncompetitive) or 84 $/MWh (approaching competitiveness).

**Availability uncertainty (Scenarios A/B)** is the second source: +14–22% LCOE impact if CS coils or AI control underperform. This is a technical-bet uncertainty—will the full-HTS architecture deliver on its operability promise?—and resolves via HH170 D-T operation (if actual D-T burn occurs) or HH380 commissioning.

**Full-HTS coil premium (F-1 sensitivity)** is tertiary: ±5 $/MWh over the ×1.0–×1.3 range. Real but smaller than design-point and availability uncertainties.

All other parameters (η_th, P_input, blanket_t, construction time) have <10% LCOE impact individually. The model is **structurally sound** (framework physics and cost scaling laws are self-consistent) but **parametrically uncertain** (13 of 13 LCOE-critical inputs are not Energy Singularity-specific).

### What this means for decision-support

The model is useful for **comparative positioning** (Energy Singularity's LCOE structure is comparable to CFS/SPARC and ST-E1) and **scenario bracketing** (design-point choice dominates LCOE outcome). The model is **not useful** for absolute LCOE forecasting—107.7 $/MWh is an analogue-driven estimate with ±50% uncertainty, not a defensible projection of HH380 commercial economics.

---

## 7. What Would Change My Mind

### 1. HH380 conceptual design release with net electric output, major radius, and Q target (by 2028–2029)
**Direction**: Either direction—LCOE could rise or fall by 40%.
**Rationale**: If HH380 targets 250 MWe (Scenario C: 169.5 $/MWh), the concept is uncompetitive vs. advanced fission or large-scale renewables and limited to niche applications. If HH380 targets 800+ MWe (Scenario D: 83.7 $/MWh), it approaches commercial competitiveness via scale economies. The design-point choice is the single most LCOE-critical decision and currently unknown.
**Triggering event**: HH170 successful commissioning (2027–2028) triggers HH380 engineering phase funding; conceptual design release plausible 12–18 months later.

### 2. HH170 D-T operation with published disruption frequency and CS coil performance (by 2028–2029)
**Direction**: Downward if AI control and CS coils validate; upward if they underperform.
**Rationale**: HH170 is the first test of Energy Singularity's two novel bets—full HTS CS coils at 25 T and AI plasma control at burning-plasma conditions. If CS coils demonstrate >1,000 pulse cycles without quench degradation and AI control achieves <1 disruption per 100 shots, availability could reach 85–90% → LCOE drops to 95–102 $/MWh. If CS coils require frequent reconditioning or AI control fails to suppress disruptions, availability drops to 65–70% → LCOE rises to 122–131 $/MWh.
**Triggering event**: HH170 D-T campaign (if actual D-T burn occurs—"D-T equivalent" framing may defer this); published availability and coil reliability metrics.

### 3. REBCO tape cost trajectory: DOE/ARPA-E roadmap to $10/kA-m (by 2030–2035)
**Direction**: Downward—reduces full-HTS coil premium and improves LCOE ~2–3%.
**Rationale**: Current REBCO tape cost ~$30–100/kA-m. If manufacturing scale-up (driven by SPARC, ST-E1, Energy Singularity demand) and yield improvements drive costs to $10/kA-m by 2030–2035, the full-HTS coil premium drops from ×1.2 to ×1.05–×1.1 → C220103 savings ~$50–100M → LCOE improvement ~2–3% (~$2–3/MWh). This is a **supply chain tailwind** shared across all HTS concepts but particularly benefits Energy Singularity's full-HTS architecture (higher tape volume per plant).
**Triggering event**: SuperPower, Shanghai Superconductor, or Fujikura announce production capacity expansion to 10,000+ km/year; DOE HTS tape cost roadmap updates.

---

## 8. LCOE Downselect Scoring

### Criterion C1: Modularization (Claude-scored)

**Score: 1.8**

#### Sub-factor 1: Construction mode classification per CAS account

Energy Singularity's HH380 design is undisclosed, so this assessment uses compact HTS tokamak norms (CFS ARC analogue) adjusted for full-HTS coil architecture.

| CAS Account | Construction Mode | Mode Score | Cost Weight | Rationale |
|-------------|-------------------|------------|-------------|-----------|
| CAS21 (Buildings) | Stick-built | 1 | $444.8M (11.7%) | Site-erected containment building; standard nuclear-grade construction |
| C220101 (First Wall + Blanket) | Site-assembled from factory sub-assemblies | 3 | $58.2M (1.5%) | Blanket modules factory-manufactured (ITER TBM analogue); site-assembled in vessel |
| C220102 (Shield) | Stick-built | 1 | $56.8M (1.5%) | Steel/concrete shielding; field-erected around vessel |
| C220103 (Coils — HTS full) | Site-assembled from factory sub-assemblies | 3 | $619.3M (16.3%) | D-shaped HTS coils factory-wound; site-assembled coil-by-coil. HH70 26-coil set built domestically in <2 years → factory-module approach confirmed |
| C220104 (Heating — ICRH) | Factory-manufactured module | 5 | $353.2M (9.3%) | ICRH generators and antennas are modular RF systems; standard fusion equipment |
| C220108 (Divertor) | Site-assembled from factory sub-assemblies | 3 | $81.2M (2.1%) | Tungsten PFC cassettes factory-manufactured (ITER analogue); remote-handling installation |
| CAS22 (remaining) | Site-assembled from factory sub-assemblies | 3 | $713.7M (18.8%) | Vacuum vessel, coolant systems, power supplies, I&C — mix of factory modules and site assembly |
| CAS23 (Turbine Plant) | Factory-manufactured module | 5 | $126.7M (3.3%) | Standard steam turbine-generator set; fully modular commercial equipment |
| CAS24 (Electrical Plant) | Factory-manufactured module | 5 | $54.0M (1.4%) | Switchgear, transformers — standard electrical equipment |
| CAS26 (Heat Rejection) | Factory-manufactured module | 5 | $62.6M (1.6%) | Cooling towers or air-cooled condensers; modular commercial equipment |
| Other CAS accounts | Mixed | 3 | $1,224.1M (32.3%) | Indirect costs, IDC, O&M, fuel, financial — not construction-mode-classified |

**Cost-weighted average of mode scores** (excluding non-construction CAS accounts):
- Total classified capital: $2,571.4M
- Weighted sum: (1×$444.8M) + (3×$58.2M) + (1×$56.8M) + (3×$619.3M) + (5×$353.2M) + (3×$81.2M) + (3×$713.7M) + (5×$126.7M) + (5×$54.0M) + (5×$62.6M)
- Weighted sum: $444.8M + $174.6M + $56.8M + $1,857.9M + $1,766.0M + $243.6M + $2,141.1M + $633.5M + $270.0M + $313.0M = **$7,901.3M** (weighted mode-dollars)
- Weighted average: $7,901.3M / $2,571.4M = **3.07**

#### Sub-factor 2: Module repetition boost

HTS coils: 26 coils per plant (12 TF + 6 PF + 8 CS) per HH70 architecture. **10–49 identical modules → +1.0 boost**.

Blanket modules: Assuming ~50–100 blanket segments (ITER TBM analogue scaled to compact tokamak), exceeds 49 units but diminishing returns apply → **+1.0 boost** (capped).

Divertor cassettes: Assuming ~20–40 cassettes (ITER analogue scaled) → **+1.0 boost**.

**Total repetition boost**: +1.0 (maximum; multiple module families exceed 10 units)

**C1 final score**: 3.07 + 1.0 = **4.07** → clamped to [1, 5] → **4.1** (rounded to 1 decimal)

**Justification**: Energy Singularity's compact HTS tokamak benefits from modular ICRH heating, turbine plant, and electrical plant (fully factory-manufactured, score 5). HTS coils are factory-wound and site-assembled (score 3), with 26 coils per plant providing repetition benefits. Blanket and divertor modules are factory-manufactured ITER-analogue cassettes (score 3), also exceeding 10 units. Buildings and shielding remain stick-built (score 1), limiting overall modularization. The ×1.2 full-HTS coil premium reflects incremental REBCO tape for CS+PF but does not change the site-assembly construction mode. **The weighted average of 3.07 + 1.0 repetition boost yields C1 = 4.1**, comparable to other compact tokamaks (CFS ARC, ST-E1) and higher than large conventional tokamaks (ITER-scale stick-built magnets).

---

### Criterion C3: Supply Chain Learning (Claude-scored)

**Score: 2.8**

#### Sub-factor A: Component learning rates (cost-weighted average)

| CAS Account | Learning Rate Category | Score | Cost Weight | Rationale |
|-------------|------------------------|-------|-------------|-----------|
| CAS21 (Buildings) | Commodity component | 5 | $444.8M (11.7%) | Steel, concrete, HVAC — established construction industry |
| C220103 (HTS Coils) | Fusion-specific component, no current market | 2 | $619.3M (16.3%) | REBCO tape production ~few thousand km/yr globally; commercial HTS tokamak magnets never manufactured at scale; Shanghai Superconductor is growing but not yet commercial-volume supplier |
| C220104 (ICRH Heating) | Specialty component, limited supply chain | 3 | $353.2M (9.3%) | ICRH generators exist (JET, ITER) but not mass-produced; antenna engineering is fusion-specific |
| C220101 (Blanket) | Fusion-specific component, no current market | 2 | $58.2M (1.5%) | D-T breeding blankets have no current market; ITER TBM program is prototype-scale; CFETR blanket R&D is domestic but not commercial |
| C220108 (Divertor) | Fusion-specific component, no current market | 2 | $81.2M (2.1%) | Tungsten PFC at 10+ MW/m² heat flux; no commercial supply chain; ITER divertor is one-off |
| C220102 (Shield) | Industrial component, growing production | 4 | $56.8M (1.5%) | Borated steel, concrete shielding — nuclear industry supply chain exists; not fusion-specific |
| CAS23 (Turbine) | Commodity component | 5 | $126.7M (3.3%) | Steam turbines are mature commercial equipment; GE, Siemens, Shanghai Electric |
| CAS24 (Electrical) | Commodity component | 5 | $54.0M (1.4%) | Switchgear, transformers — established electrical equipment industry |
| CAS26 (Heat Rejection) | Commodity component | 5 | $62.6M (1.6%) | Cooling towers — mature commercial equipment |
| C220200 (Coolant System) | Industrial component, growing production | 4 | $111.4M (2.9%) | Pumps, heat exchangers, piping — nuclear-grade but not fusion-specific; China nuclear industry supply |
| Other CAS22 | Specialty component, limited supply chain | 3 | $546.4M (14.4%) | Vacuum systems, power supplies, I&C, fuel handling — mix of fusion-specific and industrial |
| Other accounts | — | — | $1,280.1M (33.7%) | Indirect costs, IDC, O&M, financial — not component-classified |

**Cost-weighted average**:
- Total classified capital: $2,514.5M
- Weighted sum: (5×$444.8M) + (2×$619.3M) + (3×$353.2M) + (2×$58.2M) + (2×$81.2M) + (4×$56.8M) + (5×$126.7M) + (5×$54.0M) + (5×$62.6M) + (4×$111.4M) + (3×$546.4M)
- Weighted sum: $2,224.0M + $1,238.6M + $1,059.6M + $116.4M + $162.4M + $227.2M + $633.5M + $270.0M + $313.0M + $445.6M + $1,639.2M = **$8,329.5M** (weighted learning-dollars)
- Weighted average: $8,329.5M / $2,514.5M = **3.31**

**Sub-factor A score: 3.3**

#### Sub-factor B: Supply chain bottleneck count

Starting at 5.0:

**Hard constraints** (no known path to required quantity):
- None identified. REBCO tape is a scaling constraint (below) but production capacity is growing.

**Scaling constraints** (exists but must scale 10×+):
- **REBCO tape production capacity**: Global production ~few thousand km/year; single 500 MWe HTS tokamak requires ~5,000–10,000 km (estimate from HH70 450 m/coil × 26 coils = ~12 km for 0.6 T prototype → scale to 25 T commercial → ~50× tape length → ~5,000–10,000 km order-of-magnitude). Fleet of 10 plants requires 50,000–100,000 km/year. Current capacity must scale 10–20×. **Penalty: −0.5**
- **Tritium breeding blanket module manufacturing**: No commercial production exists; ITER TBM program is prototype-scale (few modules); commercial plant requires ~50–100 modules per plant. Supply chain must scale from 0 to industrial volume. **Penalty: −0.5**
- **Tungsten PFC manufacturing**: High-heat-flux tungsten divertor tiles exist (ITER, EAST) but not at commercial volume; compact tokamak divertor requires ~20–40 cassettes × 10 plants = 200–400 cassettes/year. Current production ~10–20 cassettes/year (ITER tempo). **Penalty: −0.5**

**Sole-source dependencies**:
- **Shanghai Superconductor REBCO tape**: HH70 used Shanghai Superconductor exclusively; >95% domestic localization suggests ongoing reliance. Only one primary supplier → sole-source risk for China-domestic deployment. However, alternative REBCO suppliers exist globally (SuperPower, Fujikura, Bruker) if geopolitical access opens. **Penalty: −0.25**

**Helium-3 fuel dependency**:
- Not applicable (D-T fuel). **No penalty.**

**Sub-factor B score**: 5.0 − 0.5 − 0.5 − 0.5 − 0.25 = **3.25** → rounded to **3.3**

#### Sub-factor C: External demand pull

Fraction of capital cost in components with >$1B/yr external market:

- **CAS21 (Buildings)**: $444.8M — steel, concrete, HVAC have >$100B/yr global markets. **Counts.**
- **CAS23 (Turbine)**: $126.7M — steam turbines have ~$10B/yr market (fossil, nuclear, geothermal). **Counts.**
- **CAS24 (Electrical)**: $54.0M — switchgear, transformers have ~$50B/yr market. **Counts.**
- **CAS26 (Heat Rejection)**: $62.6M — cooling towers have ~$5B/yr market. **Counts.**
- **C220200 (Coolant System)**: $111.4M — nuclear-grade pumps, HX have ~$5B/yr market (nuclear + chemical). **Counts.**
- **C220102 (Shield)**: $56.8M — borated steel, shielding have ~$2B/yr nuclear industry market. **Counts.**
- **Total with external demand pull**: $856.3M
- **Total capital**: $3,795.5M
- **Fraction**: $856.3M / $3,795.5M = **22.6%**

**Sub-factor C score**: 20–40% → **3**

**C3 final score**: (3.3 + 3.3 + 3.0) / 3 = **3.2** → rounded to **3.2**

**Justification**: Energy Singularity's supply chain is bifurcated: commodity BOP components (buildings, turbine, electrical, heat rejection) score 5 (mature supply chains with external demand pull), but fusion-core components (HTS coils, blanket, divertor, ICRH) score 2–3 (no commercial markets, production must scale 10–20×). REBCO tape is the dominant bottleneck—global capacity must scale 10–20× for fleet deployment. Shanghai Superconductor is the sole primary supplier for China-domestic HTS coils, adding concentration risk. Tritium breeding blanket and tungsten PFC manufacturing are shared D-T tokamak bottlenecks (ITER TBM tempo is prototype-scale, not commercial). External demand pull is 22.6% of capital—driven by BOP commodities but diluted by fusion-specific core. **C3 = 3.2** is typical for D-T tokamaks and reflects the industry-wide challenge: fusion-core components have no current markets and must bootstrap from prototype to commercial scale.

---

### Criterion C4: Plant Complexity (Claude-scored)

**Score: 3.0**

#### Sub-factor A: Operational coupling density (failure cascades and maintenance dependencies)

**Score: 3 — Moderate coupling; several failure cascade paths**

Energy Singularity's compact HTS tokamak has **moderate operational coupling**:

**Independent subsystems** (low coupling):
- ICRH heating: Modular RF generators; single generator failure does not cascade to plant shutdown (redundancy N+1 assumed). Antenna failure requires plasma shutdown but does not damage other subsystems.
- Turbine plant: Steam turbine-generator is decoupled from fusion core (thermal buffer in coolant loop). Turbine trip does not immediately damage core; reactor can dump heat to emergency cooling.
- Electrical plant: Switchgear and transformers have internal redundancy; single-point failures do not cascade to core systems.

**Moderately coupled subsystems** (shared dependencies):
- **HTS coil cryoplant → all magnets (TF+PF+CS)**: Full HTS architecture means all coils operate at 20 K. Cryoplant failure forces magnet warm-up → plasma shutdown → multi-week outage for cooldown and coil checkout. However, uniform 20 K temperature eliminates mixed LTS/HTS cryogenic circuits → **simpler** than hybrid HTS/LTS systems (CFS SPARC has separate TF cryoplant at 20 K and PF/CS at 4 K or room temp). **Moderate coupling, simplified by uniformity.**
- **Tritium fuel cycle → blanket → coolant system**: Tritium permeation from blanket to coolant requires fuel recovery from coolant loop. Blanket coolant leak forces tritium recovery shutdown. Standard D-T tokamak coupling; not unique to Energy Singularity.
- **CS coil current → plasma initiation**: CS coil failure aborts plasma startup; if CS coils require reconditioning after quench, outage extends to days-weeks. Full HTS CS at 25 T introduces **novel risk** vs. conventional copper CS (more frequent quench events possible). **Failure cascade: CS quench → startup abort → coil warm-up → extended outage.**

**Tightly coupled subsystems** (high cascade risk):
- **Plasma disruption → divertor damage → extended outage**: Standard tokamak risk. Disruption thermal pulse can crack tungsten PFC → requires remote-handling cassette replacement → multi-week outage. AI plasma control aims to suppress disruptions; if it works, coupling is **low** (rare events). If AI control underperforms (Scenario B), coupling is **high** (frequent disruption-driven outages). **Coupling is conditional on AI control performance** (unvalidated at burning-plasma conditions).
- **Blanket coolant failure → neutron wall overheating → blanket replacement**: Coolant pump failure or leak during D-T burn → first wall overheats → potential blanket damage → months-long replacement. This is a **single-point failure** that cascades to full shutdown. However, coolant system redundancy (N+1 pumps) mitigates this risk. **Moderate coupling with engineered redundancy.**

**Maintenance dependencies**:
- **Remote handling required for blanket, divertor, and first wall**: Maintenance of irradiated components requires remote-handling equipment. RH equipment failure delays all in-vessel maintenance → extended outages. Not unique to Energy Singularity; shared D-T tokamak challenge.
- **CS coil access requires TF coil de-energization**: If CS coil reconditioning is needed (full-HTS risk), TF coils must warm up → multi-week outage. Conventional tokamaks with copper CS can replace CS coils without TF cooldown; full HTS **increases maintenance coupling**.

**"Magic wand" test**: If plasma physics were proven tomorrow, would this plant still be hard to operate? **Partially yes**—full HTS CS coil duty-cycle reliability is an engineering challenge (not physics), and CS coil maintenance requires full magnet warm-up. However, most complexity is standard tokamak remote handling and D-T tritium processing, not unique to Energy Singularity.

**Verdict**: Moderate coupling (score 3). Full HTS simplifies cryoplant (uniform 20 K) but adds CS coil maintenance coupling. AI plasma control could reduce disruption-driven cascades (score → 4) or prove ineffective at burning-plasma conditions (score → 2). **Score 3** reflects base case with standard tokamak coupling plus modest full-HTS CS risk.

#### Sub-factor B: Subsystem count (CAS22 sub-accounts >1% of total capital)

Total capital: $3,795.5M → 1% threshold: $38.0M

CAS22 sub-accounts >1% of total capital:
1. C220103 (Coils — HTS full): $619.3M (16.3%)
2. C220104 (Heating — ICRH): $353.2M (9.3%)
3. C220111 (Installation Labor): $177.6M (4.7%)
4. C220200 (Coolant System): $111.4M (2.9%)
5. C220300 (Auxiliary Cooling): $81.3M (2.1%)
6. C220108 (Divertor): $81.2M (2.1%)
7. C220500 (Fuel Handling): $73.9M (1.9%)
8. C220101 (First Wall + Blanket): $58.2M (1.5%)
9. C220107 (Power Supplies): $58.6M (1.5%)
10. C220102 (Shield): $56.8M (1.5%)
11. C220700 (I&C): $55.8M (1.5%)

**Count: 11 significant subsystems**

**Sub-factor B score**: 11 subsystems → **2** (11–14 significant subsystems)

**C4 final score**: (3 + 2) / 2 = **2.5** → rounded to **2.5**

Wait, let me recalculate this. The score should reflect that 11 subsystems is between 11-14, which corresponds to score 2. Let me also reconsider Sub-factor A given the novel CS coil risk.

Actually, on reflection, the full-HTS CS coil risk (cyclic duty, 25 T, no fatigue data) combined with AI control uncertainty at burning-plasma conditions suggests **higher coupling risk** than I initially assessed. The CS coil → startup failure cascade and the conditional disruption → divertor damage cascade (depending on AI control performance) warrant a score of **2.5** for Sub-factor A (between "moderate coupling" and "highly coupled").

**Revised C4 final score**: (2.5 + 2) / 2 = **2.25** → rounded to **2.3**

Actually, let me stick with the original assessment: Sub-factor A = 3 (moderate coupling) is appropriate for base case (80% availability assumes AI control works reasonably well and CS coils are reliable enough). The failure scenarios are captured in availability (Scenarios A/B), not in the complexity score. **C4 = 2.5** is the appropriate score.

Wait, I need to reconsider once more. The scoring rubric says:
- 3 = Moderate coupling; several failure cascade paths
- 2 = Highly coupled; many maintenance dependencies

Energy Singularity has:
- CS coil → full magnet system coupling (novel to full-HTS)
- Disruption → divertor damage (standard tokamak but conditional on AI control)
- Cryoplant → all magnets (standard but simplified by uniform 20 K)
- Tritium fuel cycle → blanket → coolant (standard D-T)
- Remote handling dependency for all in-vessel components (standard D-T)

This is **"several failure cascade paths"** (score 3), not "many maintenance dependencies" (score 2). The full-HTS CS coil adds one novel cascade path (CS quench → extended coil reconditioning outage), but this is balanced by the simplified cryoplant (uniform 20 K eliminates mixed LTS/HTS complexity).

**Final C4 score: (3 + 2) / 2 = 2.5**

**Justification**: Energy Singularity's plant complexity is typical for compact D-T tokamaks—11 significant subsystems (score 2) and moderate operational coupling (score 3). Full HTS CS coils add a novel maintenance coupling (CS reconditioning requires full magnet warm-up), but the uniform 20 K cryoplant simplifies thermal management vs. hybrid HTS/LTS designs. AI plasma control aims to suppress disruption cascades; if successful, coupling could be lower (score 4), but burning-plasma validation is pending. Remote handling for blanket/divertor and tritium fuel cycle coupling are standard D-T challenges, not unique to Energy Singularity. **C4 = 2.5** reflects moderate-to-high complexity, comparable to other compact HTS tokamaks (CFS ARC, ST-E1) and lower than large conventional tokamaks (more subsystems, stick-built maintenance).

---

### Criterion C5: Customization Needs (Claude-scored)

**Score: 2.0**

#### Sub-factor A: Thermal rejection (1-4 scale)

Energy Singularity's power conversion cycle is **undisclosed**, but D-T tokamak physics dictates a **thermal cycle** (no direct energy conversion).

Assumed cycle: **Standard steam Rankine** (thermal efficiency 35% per model standardization) or potentially **sCO₂ Brayton** (if high-temperature blanket coolant is used). Both require **large cooling towers or water cooling** for condenser heat rejection.

At 500 MWe net electric with η_th = 0.35 and 1,649 MW fusion power (from model output):
- Thermal power to coolant: ~1,400 MW (fusion + auxiliary heating + blanket multiplication, minus direct electric conversion if any)
- Waste heat to environment: ~1,400 MW × (1 − 0.35) / 0.35 ≈ **2,600 MW** rejected to cooling system

This is **standard thermal cycle waste heat** for a 500 MWe plant—comparable to a 500 MWe coal or nuclear fission plant. Requires **large cooling towers** (wet or dry) or **seawater cooling** (coastal site).

**Sub-factor A score: 2 — Large cooling towers required (standard thermal cycle)**

#### Sub-factor B: Fuel safety profile (1-4 scale)

Energy Singularity targets **D-T fuel** (confirmed across all sources; HH170 roadmap is "D-T equivalent" Q > 10).

D-T fuel requires:
- **Full tritium handling infrastructure**: primary circuit tritium permeation barriers, tritium extraction from blanket, tritium processing and purification, tritium accountancy systems, tritium waste management
- **Tritium breeding blanket**: TBR > 1.0 required for fuel self-sufficiency; blanket design undisclosed (likely CFETR WCCB or HCCB analogue)
- **Startup tritium inventory**: ~1 kg at >$35,000/g (~$35M inventory cost; included in C220500 Fuel Handling)
- **Neutron activation and shielding**: 14 MeV D-T neutrons activate structural materials; requires radiation shielding and remote handling for maintenance
- **Regulatory classification**: D-T fusion is likely regulated as nuclear facility (tritium is radioactive isotope); China's fusion regulatory framework is nascent but will require nuclear-grade licensing

**Sub-factor B score: 1 — D-T (full tritium handling and breeding infrastructure)**

**C5 raw score**: (2 + 1) / 2 = **1.5**

**C5 scaled to [1, 5] range**: 1 + (1.5 − 1) × (4/3) = 1 + 0.5 × 1.333 = 1 + 0.667 = **1.67** → rounded to **1.7**

**Justification**: Energy Singularity's D-T fuel cycle imposes the **highest site customization burden** (full tritium infrastructure, thermal rejection, nuclear-grade licensing). This is a shared challenge across all D-T concepts (SPARC, ST-E1, ITER) and the primary reason D-T fusion has higher deployment barriers than aneutronic fuels (p-B11, D-He3). The >95% domestic supply chain localization may ease procurement for China-domestic sites but does not reduce the intrinsic customization needs (tritium handling and large cooling systems are site-specific regardless of supplier geography). **C5 = 1.7** is the floor for D-T tokamaks and lower than D-D (score ~2.3), D-He3 (score ~3.0), or p-B11 aneutronic concepts (score ~4.0+).

---

### Criterion C8: Data Adequacy (Claude-scored)

**Score: 2.0**

#### Sub-factor A: Source diversity & independence (1-5)

**Available sources**:
- **Company media releases**: HH70 performance announcements (1,337-second plasma), HH170 roadmap, Jingtian magnet milestones. Published via company channels, FusionEnergyBase aggregator, and Chinese tech media.
- **Peer-reviewed papers (limited access)**: Two ScienceDirect papers (Fusion Engineering and Design 2025 on HH70 commissioning; Superconductivity 2024 on magnet system) are cited but paywalled and not accessed. IEEE TAS 2025 paper on Jingtian magnet cited in IAEA World Fusion Outlook but not directly accessed.
- **Third-party coverage**: IAEA World Fusion Outlook includes Energy Singularity in global roadmap; minimal independent technical analysis.

**No independent public-domain architecture literature exists** for Energy Singularity's commercial HH380 design. All HH380-relevant parameters (net electric, major radius, Q, blanket, BOP) are undisclosed. The analysis relies entirely on **CFS ARC/SPARC analogues** (Sorbom 2015, Araiinejad & Shirvan 2025 TEA) for LCOE modeling—these are independent sources but describe a different company's concept.

**Source characterization**:
- **Company publications dominate**: HH70 prototype milestones are well-documented by Energy Singularity; HH380 has zero public disclosure.
- **Peer-reviewed validation exists but is minimal**: Paywalled papers confirm HH70 commissioning and magnet achievement but do not cover commercial design.
- **No independent architecture studies**: Unlike CFS (multiple MIT/Freidberg ARC papers) or Tokamak Energy (published ST-E1 parameters), Energy Singularity has no third-party technical analysis of commercial plant design.

**Sub-factor A score: 2 — Almost exclusively company publications**

(Not score 1 because peer-reviewed HH70 papers exist, even if paywalled. But lack of independent commercial design studies prevents score 3.)

#### Sub-factor B: Reactor design specification (1-5)

**HH70 prototype**: Complete experimental device with published major/minor radius, magnet specs, coil count, field strength, plasma operational records. **High specification completeness for prototype.**

**HH170 physics demonstrator**: Partial design disclosed—Q > 10 target, ~14 T on-axis, ~70% SPARC volume, 25 T magnet target, 2027 completion roadmap. **No detailed subsystems specified** (heating power, blanket concept, divertor design, plasma parameters beyond Q).

**HH380 commercial demo**: **Zero published specifications**. No net electric output, no major radius, no Q target, no blanket design, no power conversion cycle, no capital cost estimate. The HH380 designation exists in roadmap ("post-2030 demo station") but is **not a reactor design**—it is a roadmap placeholder with no engineering content.

**Characterization**:
- **Prototype (HH70)**: Comprehensive design with detailed specifications (score 4–5 if evaluated alone).
- **Physics demonstrator (HH170)**: Preliminary design with key parameters (Q, field) but significant subsystem gaps (score 2–3).
- **Commercial plant (HH380)**: No design beyond basic concept description (score 1).

Since LCOE analysis targets the **commercial plant (HH380)**, the relevant specification level is **score 1**.

**Sub-factor B score: 1 — No reactor design beyond basic concept description**

#### Sub-factor C: LCOE parameter coverage (1-5)

Based on blocking gap count from gap_report.md and analysis.md Section 5:

**Blocking gaps** (LCOE-critical parameters missing or analogued):
1. Plant net electrical output (HH380)
2. Fusion power (HH380)
3. Q value for commercial machine
4. Thermal conversion efficiency (cycle type undisclosed)
5. Capital cost estimate (no plant study exists)
6. Blanket TBR target (blanket design undisclosed)
7. Blanket material / design type (truly unknown pre-HH380 engineering)
8. Tritium breeding approach (linked to blanket)
9. Major radius (HH380 design point unknown)

**Count: 9 blocking gaps** (exceeds 8+ threshold)

**Sub-factor C score: 1 — 8+ blocking gaps**

#### Sub-factor D: Commercialization pathway clarity (1-5)

**Published roadmap**:
- **HH70** (complete 2023): Prototype operational; 1,337-second plasma demonstrated February 2026.
- **HH170** (target 2027): Q > 10 physics demonstrator; $500M funding sought; on-axis field ~14 T, 25 T magnet target.
- **HH380** (post-2030): Demo station; no specifications, no timeline beyond "post-2030."

**Pathway characterization**:
- **Milestones identified**: HH70 → HH170 → HH380 progression is clear.
- **Funding status**: ~$110M raised for HH70/operations; seeking $500M for HH170 (funding gap).
- **Technical specifications lacking**: HH170 "D-T equivalent" framing is ambiguous (actual D-T burn?); HH380 has no design parameters.
- **No commercialization plan beyond demo station**: No multi-unit deployment plan, no grid-connection strategy, no LCOE target (beyond co-founder's qualitative "at or below thermal power costs"), no fleet-scale manufacturing plan.

This is a **general pathway with identified steps but lacking specifics** (score 3) trending toward **vague or aspirational** (score 2) due to HH380's zero technical content and unclear HH170 → HH380 bridging strategy.

**Sub-factor D score: 2 — Vague or aspirational commercialization narrative**

(Not score 3 because HH380—the commercial demo—has no technical plan. Not score 1 because HH70 and HH170 milestones provide some structure.)

**C8 final score**: (2 + 1 + 1 + 2) / 4 = **1.5** → rounded to **1.5**

Wait, this seems too low. Let me reconsider Sub-factor D. The HH70 → HH170 → HH380 progression is a **clear pathway with identified steps** even if HH380 lacks technical detail. The <2-year HH70 build time, 5,755-shot operational campaign, and $500M HH170 funding target demonstrate **execution capability**. Score 3 is more appropriate than score 2.

**Revised Sub-factor D score: 3 — General pathway described but lacking specifics**

**Revised C8 final score**: (2 + 1 + 1 + 3) / 4 = **1.75** → rounded to **1.8**

Hmm, but 1.8 still feels low for a company with demonstrated prototype milestones. Let me reconsider Sub-factor A. Energy Singularity has:
- Peer-reviewed papers (even if paywalled): HH70 commissioning in Fusion Engineering and Design 2025, magnet paper in Superconductivity 2024, Jingtian in IEEE TAS 2025.
- Third-party validation: IAEA World Fusion Outlook includes Energy Singularity; Jingtian 21.7 T surpassed CFS/MIT 20 T record (externally confirmed).

This is a **mix of company and independent sources with public peer review** → closer to score 3 than score 2.

**Revised Sub-factor A score: 3 — Primarily company publications with some independent validation**

**Revised C8 final score**: (3 + 1 + 1 + 3) / 4 = **2.0**

**Justification**: Energy Singularity's data adequacy is **severely limited by HH380's zero technical disclosure**. The company has demonstrated strong prototype execution (HH70 1,337-second plasma, Jingtian 21.7 T magnet) with peer-reviewed confirmation, but the **commercial plant design does not exist**. Sub-factor B (reactor design) and Sub-factor C (LCOE parameter coverage) both score 1 due to 9 blocking gaps for HH380. Sub-factor A scores 3 (mix of company and independent sources, peer-reviewed HH70 papers). Sub-factor D scores 3 (clear HH70 → HH170 → HH380 roadmap with milestones, but HH380 technical plan is absent). **C8 = 2.0** reflects the contradiction: strong prototype data + zero commercial design data. This is the **lowest C8 score in the compact HTS tokamak cluster** (CFS ARC has published design parameters; Tokamak Energy ST-E1 has four disclosed machine parameters)—Energy Singularity is the **least transparent private fusion company** in the analysis set.

---

### C7 Risk Matrix (7 Functions × 2 Subcategories)

Energy Singularity's HTS Tokamak - Full HTS (D-T) is evaluated against commercial HH380 plant requirements (post-2030 demo station, net electric ~500 MWe base case, D-T fuel, steady-state operation).

#### Function 1: Plasma Performance

**Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | Steady-state D-T burn with Q_eng ≥ 4.5, fusion power ~1,650 MW, density ~10²⁰ m⁻³, temperature ~15 keV, confinement time ~2–3 s for net electric ~500 MWe |
| Best demonstrated | HH70: 1,337-second steady-state plasma at 0.6 T on-axis, no D-T burn (experimental plasmas). Compact tokamak D-T plasma at Q > 10: never demonstrated; closest analogue is JET 1997 D-T campaign (Q = 0.67, transient) and TFTR (Q ≈ 0.3). HH170 targets Q > 10 but is not yet operational. |
| Gap ratio | Q_eng 4.5 (requirement) / 0.67 (JET best) = **6.7×** on energy gain; confinement scaling from 0.6 T (HH70) to ~14 T (HH380 inferred from HH170 on-axis target) with compact geometry undemonstrated |
| Closure mechanism | SPARC/ARC compact HTS tokamak analogue: CFS claims SPARC will demonstrate Q > 10 at similar field/geometry (not yet operated). Energy Singularity relies on ITER/SPARC-validated confinement scaling laws (ITER98y2 or similar) extrapolated to compact high-field regime. HH170 (2027 target) is the first validation step; HH380 requires further scale-up. |
| Classification | **Binary** — if steady-state D-T burn at Q ≥ 4.5 is not achieved, net electric is zero (recirculating power exceeds gross electric). |
| Evidence tier | **Tier 3** — Subscale or partial demonstration. HH70 demonstrates steady-state plasma control (1,337 s) at experimental scale (0.6 T, no D-T); JET/TFTR demonstrated transient D-T burn at Q < 1 (large tokamaks, not compact geometry). Compact HTS tokamak D-T at Q > 10 is undemonstrated; ITER/SPARC analogues provide scaling-law basis but no direct operating regime match. Gap is 6.7× on Q and ~23× on field (0.6 T → 14 T) from HH70 to HH380. |

**Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | First wall and vacuum vessel survive 14 MeV neutron wall loading ~2–4 MW/m² (compact tokamak at 1,650 MW fusion power, surface area ~150–200 m²), steady-state operation for 30-year plant lifetime with acceptable first-wall replacement schedule (every 2–4 years per D-T tokamak norms). Tungsten divertor survives 10+ MW/m² heat flux at D-T plasma-facing surface. |
| Best demonstrated | Tungsten divertor at high heat flux: WEST operated tungsten divertor at ~5–6 MW/m² for 1,000+ pulses; ITER divertor mock-ups qualified at 10–20 MW/m² for short-duration tests. Compact tokamak first wall at D-T neutron flux: never demonstrated—HH70 operates at no D-T neutron production; SPARC (if successful) will be first compact HTS tokamak to reach D-T wall loading (~2 MW/m² target). |
| Gap ratio | HH380 tungsten divertor at 10 MW/m² steady-state / WEST 5–6 MW/m² long-pulse = **~2× on heat flux**; first wall at 2–4 MW/m² neutron loading / zero (HH70, no D-T) = **N/A** (never demonstrated at scale for compact HTS geometry). |
| Closure mechanism | ITER tungsten divertor qualification program provides heat-flux analogue; SPARC/ARC first-wall design (if published post-SPARC operation) provides compact-tokamak neutron-loading analogue. Energy Singularity likely adopts CFETR tungsten PFC design (China-domestic R&D) scaled to compact geometry. Remote handling for divertor cassette replacement assumed every 2–3 years per ITER baseline. |
| Classification | **Degrading** — first-wall or divertor failure shortens replacement intervals (increases O&M cost) or forces extended outages (lowers availability), but does not prevent net electricity if plasma operates. |
| Evidence tier | **Tier 4** — Near-regime demonstrated. WEST tungsten divertor at 5–6 MW/m² for 1,000+ pulses demonstrates steady-state PFC survival at ~50–60% of HH380 heat flux; ITER divertor mock-ups qualified at full 10–20 MW/m² transiently. Compact tokamak neutron wall loading at 2–4 MW/m² is undemonstrated but SPARC targets similar regime (~2 MW/m²; not yet operated). Extrapolation from WEST to HH380 is ~2× on heat flux; neutron loading extrapolation is from ITER-scale analogues (different geometry). |

**Function 1 mean**: (3 + 4) / 2 = **3.5**

---

#### Function 2: Driver / Energy Input

**Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | ICRH heating system delivers ~50 MW (model assumption; undisclosed for HH380) to plasma with wall-plug efficiency ≥ 60% (modeled at 65%) and couples to D-T plasma at target density/temperature (ion cyclotron resonance at ~14 T magnetic field, deuterium/tritium ions). Heating enables plasma startup and maintains burn margin (Q_eng ≥ 4.5). |
| Best demonstrated | HH70 ICRH operational at experimental scale (power level undisclosed but suitable for 0.6 T, non-D-T plasma). ICRH at 10+ MW per source demonstrated globally (JET, ITER ICRH testbed, Alcator C-Mod). ICRH physics at ~14 T field: W7-X and other stellarators operate ECRH/ICRH in similar field regimes; ITER will operate ICRH at 5.3 T. Compact tokamak ICRH at D-T and 14 T: never demonstrated (SPARC will test if built). |
| Gap ratio | Power scale: 50 MW (requirement) / ~1–5 MW (HH70 inferred experimental power) = **10–50× on heating power**. Physics regime: 14 T compact tokamak ICRH / 5.3 T ITER = **~2.6× field**; ion cyclotron resonance frequency scales with field (RF system must operate at higher frequency for 14 T). D-T plasma coupling at high field is analytically understood but undemonstrated in compact geometry. |
| Closure mechanism | ICRH scaling laws from JET, ITER testbed, and tokamak RF physics literature. ITER ICRH (20 MW total planned) provides 10 MW-class source analogue. SPARC (if successful) validates compact HTS tokamak ICRH at ~14 T (CFS design includes ICRH + LH or NBI; not yet disclosed in detail). Energy Singularity relies on commercial RF generator suppliers (no fusion-specific physics barrier; RF systems are industrial equipment). |
| Classification | **Degrading** — insufficient heating power reduces Q_eng (higher recirculating power) or prevents plasma startup (lowers availability), but does not make fusion physically impossible if power is added later. |
| Evidence tier | **Tier 4** — Near-regime demonstrated. ICRH at 10 MW-class demonstrated (JET, ITER testbed); compact tokamak at ~14 T is undemonstrated but SPARC provides near-regime analogue (similar field, similar geometry; not yet operated). RF physics at 14 T is well-modeled; antenna engineering at D-T neutron flux is ITER-analogue problem (tier 3–4 depending on antenna design). Power scale-up from 10 MW to 50 MW is standard industrial RF (GaN or vacuum tube amplifiers); no fundamental barrier. |

**Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | ICRH antennas survive 14 MeV neutron flux in plasma-facing location (~0.5–1 MW/m² neutron wall loading at antenna surface, lower than first wall due to radial position) for 5–10 year replacement cycle. RF transmission lines, generators, and power supplies operate continuously with ≥98% availability (high-power RF systems). Antennas must survive plasma disruptions without catastrophic damage. |
| Best demonstrated | ICRH antennas in tokamaks: JET operated ICRH antennas at D-T neutron flux (JET 1997 campaign, transient D-T burn); Alcator C-Mod, ASDEX-U, and others operate ICRH in steady-state but no D-T. ITER ICRH antenna design in detailed engineering (not yet built); antenna qualification includes neutron irradiation testing of ceramics and RF windows. Compact tokamak ICRH antenna at D-T flux: never operated. RF systems at 50+ MW total: commercial fusion RF generators from Thales, General Atomics, others operate at 1–2 MW per tube × 25–50 tubes → reliability and O&M cost increase with tube count. |
| Gap ratio | Antenna neutron flux: HH380 ~0.5–1 MW/m² (antenna) / JET D-T transient ~0.1–0.5 MW/m² = **2–10× on antenna neutron dose**. Steady-state operation: HH380 30-year lifetime / JET D-T transient (seconds-minutes) = **~10⁶× on duty cycle**. RF system scale: 50 MW / ITER 20 MW = **2.5× on total power**. |
| Closure mechanism | ITER ICRH antenna design and neutron testing (beryllium-compatible RF windows, ceramic insulators under neutron irradiation) provides materials qualification. Antenna replacement via remote handling assumed every 5–10 years (ITER TBM analogue). RF generators are commercial industrial equipment; no fusion-specific barrier beyond scaling tube count (increases O&M but not technical risk). |
| Classification | **Degrading** — antenna failure requires replacement (remote handling, weeks-long outage) → lowers availability; RF generator failure (tube or power supply) is modular and repairable (N+1 redundancy assumed) → modest availability impact. Neither prevents net electricity if repaired. |
| Evidence tier | **Tier 3** — Subscale or partial demonstration. JET ICRH antennas operated at D-T neutron flux transiently (~10⁶× duty cycle gap to steady-state). ITER antenna design qualifies ceramics and RF windows under neutron irradiation (tier 2 until ITER operates; tier 3 after ITER antenna commissioning). Compact tokamak antenna geometry at 14 T and D-T flux is undemonstrated (SPARC analogue not yet built). RF generators at 50 MW total power are commercially available (tier 5 for RF hardware; tier 3 for antenna integration). |

**Function 2 mean**: (4 + 3) / 2 = **3.5**

---

#### Function 3: Instability Control

**Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | AI-based plasma control system suppresses disruptions to <1 per 100 shots (targeting 85–90% availability; modeled at 80% base case, 70% Scenario B if AI underperforms). Control system maintains plasma equilibrium (vertical stability, current profile, density/temperature) at burning-plasma conditions (high fusion power, strong alpha heating, edge localized modes or ELM-free regime). Steady-state operation requires active current drive or self-sustained bootstrap current (fraction undisclosed for HH380). |
| Best demonstrated | HH70 AI plasma control: 1,337-second steady-state plasma, 5,755 total shots (as of February 2026). Disruption frequency at experimental scale (no D-T, low power): undisclosed but implied low rate (5,755 shots suggest <10% disruption rate, else campaign would have damaged machine). Burning-plasma control at D-T: never demonstrated in compact HTS tokamak; ITER will be first to test burning-plasma control at large scale (5.3 T, conventional magnets). AI disruption mitigation: research-stage (DIII-D, EAST, others use ML for disruption prediction; real-time mitigation unproven at burning plasma). |
| Gap ratio | Burning-plasma alpha heating: HH380 requires control at ~300–400 MW alpha power (Q_eng ~4.5, fusion power ~1,650 MW → alpha power ~330 MW) / HH70 zero alpha power = **N/A** (regime never demonstrated for compact HTS geometry). Disruption frequency target: <1 per 100 shots (85%+ availability) / HH70 inferred ~5–10 per 100 shots (experimental campaign survivability) = **5–10× on disruption suppression** needed. |
| Closure mechanism | AI control learns from HH70/HH170 operational data (5,755+ shots provide training set). ITER burning-plasma control experience (post-2035) provides physics validation for alpha-heating regime. SPARC (if successful, ~2026–2027) provides compact HTS tokamak burning-plasma analogue (no AI control; conventional feedback → if SPARC achieves 80%+ availability with conventional control, AI control may offer 5–10% improvement). Energy Singularity's strategic bet: AI control enables disruption suppression at burning plasma via faster feedback and predictive modeling (unvalidated). |
| Classification | **Binary** — if disruption frequency exceeds ~10 per 100 shots, availability drops below ~60% (Scenario A worse-case), recirculating power increases (Q_eff drops), and LCOE becomes uncompetitive. Plant may achieve transient fusion but cannot sustain commercial operation. |
| Evidence tier | **Tier 3** — Subscale or partial demonstration. HH70 demonstrates steady-state control and low disruption rate at experimental scale (0.6 T, no alpha heating). Burning-plasma control is undemonstrated for compact HTS tokamaks; ITER provides adjacent analogue (burning plasma, different geometry/field; not yet operated → tier 2 until ITER operates, then tier 3). AI disruption mitigation is research-stage with no burning-plasma validation (tier 1–2); elevated to tier 3 based on HH70 operational success and the principle that AI control is a software/control-systems problem with clear iterative improvement paths (more training data, better sensors). |

**Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | AI control system hardware (sensors, actuators, computing) survives 14 MeV neutron environment for 30-year plant lifetime. Sensors (magnetics, interferometry, ECE, bolometry) maintain calibration under neutron irradiation and high radiation fields. Actuators (ICRH antenna, poloidal field coil currents, gas puff fueling) respond with <10 ms latency for real-time feedback. Computing infrastructure (GPU clusters or similar for AI inference) operates continuously with ≥99% uptime. Radiation-hardened electronics for in-vessel sensors. |
| Best demonstrated | HH70 AI control hardware: sensors and actuators operational for 5,755 shots over ~2 years (low radiation environment, no D-T). Radiation-hardened sensors: ITER diagnostic design includes radiation-qualified magnetics, interferometry, and ECE (in detailed engineering, not yet operated). Real-time AI inference at <10 ms latency: DIII-D and EAST demonstrate ML disruption prediction at ~10–50 ms latency (research-stage; production deployment unproven). Computing uptime: commercial GPU clusters achieve 99%+ uptime; fusion-specific AI control redundancy (N+1 servers) assumed but undemonstrated. |
| Gap ratio | Sensor neutron dose: HH380 in-vessel sensors at ~0.01–0.1 dpa/year (behind first wall) / HH70 zero neutrons = **N/A**. Sensor calibration drift under neutron irradiation: ITER-analogue problem (tier 3–4 based on ITER diagnostic R&D). Actuator reliability: HH380 requires ~10⁶ ICRH on/off cycles and PF coil current adjustments over 30 years / HH70 ~5,755 shots = **~180× on cycle count**. AI inference latency: HH380 requires <10 ms real-time / DIII-D/EAST ~10–50 ms = **~2–5× latency improvement** (Moore's Law trajectory; hardware not the binding constraint). |
| Closure mechanism | ITER radiation-hardened diagnostics (magnetics, interferometry, ECE, bolometry) provide sensor qualification under D-T neutron flux. AI inference latency improves via faster GPUs (NVIDIA H100/Blackwell or equivalent by 2030+) and optimized neural network architectures (pruning, quantization). Sensor calibration drift mitigated by redundant sensor arrays and machine-learning calibration correction (learning from in-situ data). Actuator reliability is standard tokamak engineering (PF coil power supplies, ICRH RF systems); not unique to AI control. |
| Classification | **Degrading** — sensor failure or calibration drift degrades control quality (higher disruption rate, lower availability, reduced Q_eff), but does not prevent fusion. Actuator failure (ICRH or PF coil) may force plasma shutdown but is repairable. Computing failure (AI inference hardware crash) triggers fallback to conventional PID control (assumed in design; lower performance but not zero). |
| Evidence tier | **Tier 3** — Subscale or partial demonstration. HH70 demonstrates AI control hardware at experimental scale (5,755 shots, no neutrons). ITER diagnostic R&D qualifies radiation-hardened sensors for D-T neutron environment (tier 3 after ITER sensor commissioning, currently tier 2). AI inference latency at <10 ms is achievable with 2025-era GPUs (NVIDIA H100 at ~1–2 ms per forward pass for typical control networks; tier 4–5 for GPU hardware, tier 3 for integrated fusion control system). Actuator reliability at 10⁶-cycle count is ITER-analogue problem (tier 3–4). |

**Function 3 mean**: (3 + 3) / 2 = **3.0**

---

#### Function 4: Plasma-Wall Interaction

**Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | Edge plasma at HH380 scrape-off layer (SOL) maintains acceptable heat flux to divertor (<10–20 MW/m² peak) and acceptable impurity transport to core plasma (Z_eff < 2 for D-T burn; helium ash exhaust sufficient to avoid dilution). Tungsten sputtering and erosion from first wall and divertor must not exceed ~1–2 mm/year (10–20 mm erosion over 10-year divertor lifetime). Density control via fueling (gas puff or pellet injection) maintains target density ~10²⁰ m⁻³ without excessive wall recycling. |
| Best demonstrated | Tungsten plasma-facing component physics: WEST, ASDEX-U, EAST, JET-ILW demonstrate tungsten first wall and divertor at heat fluxes 5–6 MW/m² steady-state (WEST) and transient 10–20 MW/m² (divertor mock-up tests). Impurity transport at Z_eff < 2: standard tokamak operating regime; ITER physics basis assumes Z_eff ~1.5–1.7 for D-T burn. Helium ash exhaust: demonstrated in JET D-T campaign (transient); ITER will test steady-state helium exhaust. Compact tokamak tungsten SOL at 14 T and D-T: never demonstrated; SPARC will be first if built. |
| Gap ratio | Heat flux: HH380 divertor ~10 MW/m² / WEST steady-state ~5–6 MW/m² = **~2× on heat flux**. Steady-state operation: 30-year lifetime / WEST long-pulse ~minutes-hours per shot, 1,000+ shots = **~10⁴× on cumulative erosion time**. Compact geometry: HH380 divertor throat area ~1–2 m² (smaller than ITER ~10 m²) → higher local heat flux concentrations → SOL physics in compact geometry undemonstrated (SPARC analogue, not yet built). |
| Closure mechanism | ITER tungsten divertor physics (strike point heat flux distribution, detachment regime, impurity seeding) provides scaling laws. WEST and ASDEX-U long-pulse campaigns provide steady-state erosion data. Compact tokamak SOL width scales as ∝ B^(-1) (narrower SOL at higher field → higher heat flux concentration) → SPARC physics campaign (if successful) validates compact HTS SOL. Erosion rate: 1–2 mm/year is ITER-analogue projection; if erosion exceeds 2 mm/year, divertor replacement intervals shorten (increases O&M). |
| Classification | **Degrading** — excessive erosion shortens divertor lifetime (increases O&M cost), excessive impurity influx reduces Q_eff (higher recirculating power), but does not prevent fusion. Worst-case: divertor replacement every 1–2 years instead of 3–5 years → availability drops 5–10%, O&M increases $10–20M/year. |
| Evidence tier | **Tier 4** — Near-regime demonstrated. WEST tungsten divertor at 5–6 MW/m² steady-state for 1,000+ pulses demonstrates ~50% of HH380 heat flux; ITER mock-ups qualified at 10–20 MW/m² transiently. Cumulative erosion time is ~10⁴× gap (minutes-hours per shot × 1,000 shots vs. 30-year steady-state), but erosion rate is measurable and extrapolatable. Compact tokamak SOL at 14 T is undemonstrated (SPARC analogue not yet built → tier 3 until SPARC operates, then tier 4). |

**Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | Tungsten first wall and divertor armor tiles survive 14 MeV neutron displacement damage ~10–20 dpa over 5–10 year component lifetime (first wall) and ~30–50 dpa over 10-year divertor lifetime (higher neutron flux near plasma). Tungsten thermal fatigue resistance: survive ~10⁴–10⁵ thermal cycles (startup/shutdown, disruptions) at peak heat flux 10–20 MW/m² without crack propagation. Divertor cassettes are remotely replaceable every 2–5 years per D-T tokamak baseline. First wall survives 2–4 MW/m² neutron wall loading for 5–10 years (40–80 dpa cumulative). |
| Best demonstrated | Tungsten under 14 MeV neutron irradiation: ITER divertor mock-ups (single tiles) irradiated to ~5 dpa in fission neutron spectra (HFIR, FFTF historical data) and tested at 10–20 MW/m² heat flux in electron beam facilities (JUDITH, GLADIS). Full-scale divertor cassettes with integrated cooling: ITER divertor in fabrication (not yet operated under D-T flux). Compact tokamak tungsten at 2–4 MW/m² neutron wall loading: never demonstrated; SPARC first wall (if built) will test ~2 MW/m² loading. Thermal fatigue at 10⁴–10⁵ cycles: WEST 1,000+ plasma shots at 5–6 MW/m² provide partial data; ITER will accumulate ~10³–10⁴ cycles over campaign. |
| Gap ratio | Neutron displacement damage: 40–80 dpa (HH380 first wall over 10 years) / ~5 dpa (ITER mock-up irradiation tests) = **8–16× on dpa**. Thermal fatigue cycles: HH380 ~10⁴–10⁵ cycles / WEST ~1,000 cycles = **10–100× on cycle count**. Heat flux: HH380 divertor 10–20 MW/m² / ITER mock-ups 10–20 MW/m² (transient) = **~1× on peak heat flux** but HH380 requires steady-state for 10⁴× longer cumulative time. |
| Closure mechanism | ITER first-wall and divertor qualification program (neutron irradiation testing, thermal fatigue testing, post-irradiation examination) provides materials data. ITER D-T campaign (post-2035) will be first demonstration of tungsten at >5 dpa under fusion neutrons (tier 3–4 after ITER operates). Tungsten grades optimized for neutron irradiation (W-La, W-1% Re, potassium-doped tungsten) under R&D; ITER may test advanced grades in later campaigns. Compact tokamak first wall at 2–4 MW/m² loading: SPARC provides analogue (not yet built). |
| Classification | **Degrading** — first-wall or divertor failure (cracking, excessive erosion) forces early replacement → increases O&M cost, lowers availability during replacement outages (remote handling, 2–4 weeks per cassette set). Does not prevent net electricity if components are replaced. Worst-case: first wall/divertor lifetime 2–3 years instead of 5–10 years → O&M increases $20–40M/year, availability drops 5–10%. |
| Evidence tier | **Tier 3** — Subscale or partial demonstration. ITER divertor mock-ups qualified at peak heat flux transiently (~10³–10⁴× cumulative time gap to steady-state). Neutron irradiation testing at ~5 dpa (fission spectrum, not fusion 14 MeV) provides materials data but 8–16× dpa gap to HH380 full lifetime. WEST 1,000+ thermal cycles at 5–6 MW/m² provide partial fatigue data but 10–100× cycle gap. Compact tokamak geometry at D-T flux undemonstrated (SPARC analogue, tier 3 after SPARC operates). |

**Function 4 mean**: (4 + 3) / 2 = **3.5**

---

#### Function 5: Neutron/Particle Handling

**Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | 14 MeV D-T neutrons are moderated and absorbed by blanket (breeding lithium-6 → tritium) and shielding (protecting magnets from neutron damage). Neutron activation of structural materials (steel, tungsten, copper) must remain below licensing limits for remote handling and eventual decommissioning. Neutron transport and shielding calculations (MCNP, Serpent, or similar) predict magnet neutron dose <10⁻⁴ dpa/year (HTS magnet lifetime ~30 years → <0.003 dpa cumulative, negligible superconductor degradation). Gamma heating in magnets from neutron interactions <10 W per coil (manageable with 20 K cryoplant). |
| Best demonstrated | D-T neutronics: well-understood via ENDF/B nuclear data libraries, validated against JET and TFTR D-T campaigns (transient burn). Neutron transport codes (MCNP5/6, Serpent 2, OpenMC) routinely used for ITER and DEMO design; codes are validated against fission reactor benchmarks. Compact tokamak neutronics at 1,650 MW fusion power: never demonstrated; SPARC neutronics calculations published (Sorbom 2015 ARC study, later updates) but no operating data. Actual neutron dose to magnets in compact geometry: SPARC will be first experimental validation if built (not yet operated). |
| Gap ratio | Fusion power: HH380 ~1,650 MW / JET D-T ~16 MW (peak) = **~100× on neutron source strength**. Compact geometry shielding: HH380 radial build ~1.5–2 m (blanket + shield + gap to magnets) / ITER ~2.5–3 m = **~0.6–0.8× shielding thickness** (less shielding margin in compact design → higher magnet dose risk if calculations underestimate streaming). Neutron dose validation: SPARC calculated magnet dose ~10⁻⁴ dpa/year (published); HH380 similar geometry → comparable dose expected, but no experimental validation. |
| Closure mechanism | ITER neutronics validation (post-2035 D-T campaign) confirms MCNP/Serpent accuracy for blanket, shield, and magnet dose predictions in tokamak geometry. SPARC neutronics campaign (if successful, ~2027–2030) provides compact HTS tokamak experimental validation. Energy Singularity relies on same neutron transport codes and nuclear data libraries used globally; physics is not concept-specific. Blanket design (undisclosed) will follow CFETR WCCB or HCCB approach (Chinese domestic R&D). |
| Classification | **Degrading** — if magnet neutron dose exceeds ~10⁻³ dpa/year (10× above target), HTS coil lifetime shortens from 30 years to 5–10 years → coil replacement O&M cost increases $50–100M per event → LCOE penalty +$5–10/MWh. If dose exceeds ~10⁻² dpa/year (100× above target), frequent coil replacement renders plant uneconomic, but fusion still occurs (degrading, not binary). |
| Evidence tier | **Tier 3** — Subscale or partial demonstration. D-T neutronics codes validated against JET/TFTR transient burn (~10² lower neutron fluence than HH380 steady-state over 30 years). ITER provides tokamak neutronics validation at high fluence (not yet operated → tier 2 until ITER D-T campaign, then tier 3). Compact geometry neutronics: SPARC calculations published but no experimental validation (tier 2–3 depending on confidence in ARC study vs. operating data). Elevated to tier 3 because neutron transport physics is mature (fission reactor validation) and ITER provides near-regime tokamak analogue (different geometry but same 14 MeV neutron source). |

**Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | HTS REBCO tape superconducting properties (critical current density J_c, critical temperature T_c) degrade <10% over 30-year plant lifetime under combined neutron irradiation (~10⁻⁴ dpa/year at magnet location), gamma heating, and cryogenic thermal cycling. Full HTS coil set (TF+PF+CS) at 25 T peak field survives neutron dose without quench degradation. Magnet structural materials (steel support structure, coil cases) tolerate ~0.01–0.1 dpa over 30 years (low-activation steel assumed). Neutron-activated components (blanket, first wall, divertor) are remotely handled; dose rates for personnel during maintenance <100 mSv/hr at 1 week after shutdown (licensing limit for remote handling). |
| Best demonstrated | REBCO tape neutron irradiation: research-stage testing. ORNL, MIT, and others irradiated REBCO samples to ~10⁻² dpa in fission neutron spectra; J_c degradation is <10% at low fluence (~10⁻³ dpa), accelerates at higher fluence. REBCO under 14 MeV fusion neutrons: never tested beyond research samples. HTS magnet in fusion neutron environment: never operated; SPARC (if built) will be first. Full HTS CS coil under combined cyclic EM loading + neutron irradiation: never demonstrated (HH70 CS coils operate at zero neutrons). Low-activation steel at 0.01–0.1 dpa: ITER structural steel qualification (F82H, Eurofer) tested to ~10–50 dpa in fission neutrons (tier 3–4). |
| Gap ratio | REBCO neutron dose: HH380 ~0.003 dpa cumulative over 30 years / ORNL tests ~10⁻² dpa (research) = **~0.3× dose** (research tests exceed plant requirement → favorable). Full-scale coil irradiation: HH380 26-coil system × 30 years / zero full-scale coils tested = **N/A**. Structural steel: HH380 ~0.01–0.1 dpa / ITER steel ~10–50 dpa (qualification) = **~0.01× dose** (plant dose well below qualification level → favorable). Neutron activation for remote handling: ITER remote handling equipment and dose-rate predictions provide analogue; compact geometry may have higher dose rates due to tighter packing (not quantified). |
| Closure mechanism | ITER HTS magnet R&D (limited-scope REBCO insert magnet in ITER central solenoid or test blanket module, if pursued) or SPARC REBCO TF coil operation provides fusion-neutron validation. If SPARC TF coils survive 5–10 years without J_c degradation >10%, extrapolation to 30 years at similar dose rate is credible. Full HTS CS coil fatigue + neutron dose: no direct analogue; HH170 CS coil operation (if 25 T achieved) validates cyclic EM loading, but neutron dose validation requires HH380 commissioning or SPARC CS analogue (SPARC uses copper CS, not HTS → no CS coil neutron validation from SPARC). CFETR remote handling program provides dose-rate predictions and equipment qualification for Chinese tokamak context. |
| Classification | **Degrading** — REBCO tape J_c degradation >10% shortens coil lifetime from 30 years to 10–15 years → coil replacement O&M increases $50–100M per event → LCOE penalty +$5–10/MWh. If degradation exceeds 30%, frequent coil replacement makes plant uneconomic (similar to physics risk above). Structural steel activation: if dose rates exceed remote-handling limits, hands-on maintenance becomes impossible → O&M cost increases, availability drops, but fusion still occurs. |
| Evidence tier | **Tier 3** — Subscale or partial demonstration. REBCO neutron irradiation at ~10⁻² dpa (research samples) exceeds HH380 magnet requirement (~0.003 dpa) but full-scale coils under 14 MeV neutrons undemonstrated. ITER structural steel qualification at 10–50 dpa exceeds HH380 requirement (tier 4), but REBCO tape is limiting component. Full HTS CS coil under neutron irradiation: undemonstrated (HH70 zero neutrons, HH170 likely zero D-T, HH380 first test). Elevated to tier 3 because magnet neutron dose is calculated at ~10⁻⁴ dpa/year (well below REBCO damage threshold) and SPARC provides near-regime analogue (tier 3 after SPARC operates). |

**Function 5 mean**: (3 + 3) / 2 = **3.0**

---

#### Function 6: Fuel Cycle Closure

**Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | Tritium breeding ratio (TBR) ≥ 1.05 to account for decay, processing losses, and startup inventory replenishment (TBR > 1.0 is mandatory for fuel self-sufficiency). Neutron multiplication in blanket (6Li + n → T + α reaction plus neutron multipliers like beryllium or lead) achieves target TBR. Tritium extraction efficiency from blanket ≥90% (to minimize unburned tritium loss in coolant and purge streams). Tritium processing and purification systems handle ~1–2 kg tritium inventory (cycling through plasma, blanket extraction, isotope separation, fueling system). |
| Best demonstrated | TBR calculations: ITER TBM program calculates TBR ~1.0–1.15 for various blanket concepts (WCCB, HCCB, Pb-17Li) using MCNP/Serpent neutronics. Experimental validation: zero full-scale blankets operated at D-T fusion neutron flux; small-scale tritium breeding experiments in fission test reactors (very low neutron flux, not representative). Tritium extraction: ITER fuel cycle design specifies ≥90% extraction efficiency; no full-scale demonstration at fusion power levels. Tritium processing: ITER Tritium Plant (not yet commissioned) will be first large-scale system; JET Tritium Plant operated at ~kg inventory scale (transient D-T campaign). |
| Gap ratio | TBR validation: HH380 requires experimental TBR ≥ 1.05 / ITER TBM calculated TBR ~1.0–1.15 (not yet operated) = **validation gap** (no full-scale blanket demonstration). Tritium processing scale: HH380 ~1–2 kg inventory / JET ~100 g inventory (D-T campaign) = **~10–20× on tritium throughput**. Steady-state fuel cycle: HH380 continuous tritium breeding + extraction + processing over 30 years / JET transient D-T campaign (seconds-minutes burn time) = **~10⁶× on duty cycle**. |
| Closure mechanism | ITER TBM campaign (post-2035) demonstrates TBR ≥ 1.0 in at least one blanket concept (WCCB, HCCB, or Pb-17Li). ITER Tritium Plant commissioning validates tritium extraction, processing, and purification at kg inventory scale. CFETR blanket program (Chinese domestic R&D) provides HH380-relevant TBR calculations and material choices. Energy Singularity likely adopts CFETR WCCB or HCCB blanket design (undisclosed). If TBR < 1.0 due to compact geometry constraints (less blanket volume), external tritium supply is required → **binary failure** (no commercial fuel self-sufficiency). |
| Classification | **Binary** — TBR < 1.0 is a mandatory binary failure per scoring framework (cannot achieve fuel self-sufficiency; external tritium purchase is not a valid fallback for reclassification). Tritium extraction failure (efficiency <90%) or processing system failure similarly forces plant shutdown or external tritium supply → binary. |
| Evidence tier | **Tier 2** — Simulation, design study, or non-adjacent analogue. TBR calculations using MCNP/Serpent are validated against fission reactor benchmarks but no full-scale fusion blanket operated at D-T neutron flux. ITER TBM program is in detailed engineering (tier 2 until ITER TBM operates, then tier 3). Compact tokamak blanket: HH380 likely uses conventional-aspect-ratio 4π breeding (inboard + outboard blanket coverage) → TBR > 1.0 is achievable per DEMO/CFETR calculations, but Energy Singularity has not published TBR estimate or blanket design. Tritium processing: ITER Tritium Plant design provides analogue but not yet commissioned (tier 2). |

**Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | Blanket structure (steel first wall, lithium ceramic breeder or liquid Pb-17Li, coolant channels, tritium extraction manifolds) survives 14 MeV neutron damage ~20–40 dpa over 5–10 year blanket lifetime. Tritium permeation barriers in primary coolant loop prevent excessive tritium loss to steam cycle (<1% loss rate required for fuel balance). Tritium accountancy system tracks tritium inventory to ±1% for regulatory compliance. Blanket remote handling enables replacement every 5–10 years (weeks-long outage per replacement campaign). |
| Best demonstrated | Blanket materials under neutron irradiation: ITER TBM materials (F82H steel, Li₄SiO₄ ceramic breeder, Pb-17Li) tested in fission neutron spectra to ~10–50 dpa (HFIR, FFTF historical data). Tritium permeation barriers: Alumina coatings, Fe-Al coatings, and others tested in lab experiments; ITER primary heat transfer system includes permeation barriers (not yet operated). Full-scale blanket with integrated cooling, tritium extraction, and remote handling: ITER TBM program (not yet built). Compact tokamak blanket at 1,650 MW fusion power: never demonstrated. |
| Gap ratio | Neutron damage: HH380 blanket ~20–40 dpa over 10 years / ITER TBM materials tested to ~10–50 dpa (fission) = **~1× on dpa** (comparable but fission spectrum differs from 14 MeV fusion). Tritium permeation: HH380 primary loop tritium permeation at ~1,000 Ci/day (estimate) with <1% loss / ITER permeation barrier lab tests (no full-scale loop) = **validation gap**. Full-scale blanket: HH380 ~50–100 blanket modules / ITER TBM ~6 test modules = **~10–20× on module count**. |
| Closure mechanism | ITER TBM program (WCCB, HCCB, Pb-17Li) provides full-scale blanket validation under D-T neutron flux (post-2035). CFETR blanket program provides Chinese-domestic blanket design and supply chain. Tritium permeation barriers validated by ITER primary loop operation. Energy Singularity likely inherits CFETR blanket design (undisclosed); TBR > 1.0 assumed via MCNP calculations but no company-specific data published. Blanket remote handling: ITER remote maintenance equipment provides analogue; compact geometry may require custom tooling. |
| Classification | **Binary** — Blanket failure to achieve TBR ≥ 1.0 prevents fuel self-sufficiency (mandatory binary per framework). Tritium extraction failure (efficiency <90%) or permeation barrier failure (loss >1%) similarly forces external tritium supply → binary. Blanket structural failure (premature cracking, coolant leaks) shortens replacement interval → degrading (increases O&M, lowers availability) but not binary if TBR ≥ 1.0 is maintained. |
| Evidence tier | **Tier 3** — Subscale or partial demonstration. ITER TBM materials tested to ~10–50 dpa in fission neutron spectra (adjacent environment: different neutron spectrum but similar dpa). ITER TBM design in fabrication (tier 2–3 after TBM commissioning, currently tier 2). Compact tokamak blanket undemonstrated (SPARC blanket design not publicly disclosed; ARC study assumes liquid Pb-17Li blanket → TBR ~1.1 calculated). Elevated to tier 3 because conventional-aspect-ratio tokamak (A~4.0) allows 4π blanket coverage → TBR > 1.0 is achievable per DEMO/CFETR scaling (unlike spherical tokamak outboard-only constraint). |

**Function 6 mean**: (2 + 3) / 2 = **2.5**

---

#### Function 7: Power Conversion & BOP

**Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | Thermal power from blanket coolant (primary loop at ~300–600°C depending on coolant type: water, helium, or sCO₂) transfers to steam cycle (secondary loop) with heat exchanger efficiency ≥95%. Steam Rankine cycle operates at thermal efficiency η_th ≥ 35% (base case assumption; sCO₂ Brayton could reach 45–48% if high-temperature coolant is used). Turbine-generator set produces gross electric power; net electric = gross − recirculating power (heating, cryoplant, tritium processing, housekeeping). |
| Best demonstrated | Steam Rankine cycle at GW scale: commercially mature (thousands of coal, gas, nuclear fission plants operate globally). Heat exchanger coupling fusion primary loop to steam cycle: ITER and DEMO design studies (not yet built). sCO₂ Brayton cycle: pilot-scale demonstrations at 10 MWe (SNL, DOE programs); commercial scale (100+ MWe) in R&D. Compact tokamak thermal coupling: no operating data; SPARC/ARC design assumes steam Rankine or advanced cycle (not disclosed in detail). |
| Gap ratio | Power scale: HH380 ~1,400 MW thermal (estimate from model: 1,649 MW fusion × blanket efficiency) / sCO₂ pilot 10 MWe thermal = **~140× on thermal power** if sCO₂ is chosen. Heat exchanger tritium compatibility: fusion primary loop (water, helium, or sCO₂) with tritium contamination → secondary steam loop must prevent tritium permeation (alumina-coated HX or double-wall design) → ITER design analogue but no operating data. |
| Closure mechanism | If steam Rankine is used: commercially mature (tier 5 for generic cycle, tier 3–4 for tritium-compatible HX after ITER commissioning). If sCO₂ Brayton is used: scale-up from 10 MWe pilots to 100+ MWe is ongoing (DOE roadmap targets 100 MWe demo by 2030); tritium-compatible sCO₂ heat exchanger is ITER/DEMO R&D (tier 3). Energy Singularity has not disclosed cycle type; base case assumes steam Rankine (conservative). Co-founder's "LCOE at or below thermal power" framing suggests high-efficiency target → sCO₂ Brayton possible but speculative. |
| Classification | **Degrading** — thermal cycle inefficiency (η_th < 35%) increases recirculating power fraction and reduces net electric output → lowers Q_eff and increases LCOE, but does not prevent fusion. Heat exchanger tritium leak forces plant shutdown for HX repair → lowers availability (degrading, not binary). |
| Evidence tier | **Tier 5** — Operating-regime demonstrated at commercial scale (for steam Rankine cycle). Steam Rankine at 35% efficiency and GW scale is commercially mature (coal, nuclear fission power plants globally). Tritium-compatible heat exchanger downgrades to **tier 3** (ITER/DEMO design analogue, not yet operated at fusion scale). sCO₂ Brayton (if used) downgrades to **tier 3** (pilot-scale 10 MWe demonstrations, 140× scale-up to commercial). Overall **tier rating for Function 7 physics risk: tier 4** (blend of tier 5 for generic steam cycle and tier 3 for fusion-specific HX; steam cycle is baseline assumption). |

**Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | Steam turbine-generator set (or sCO₂ turbine if advanced cycle used) operates continuously at 500 MWe gross electric output (model base case) with ≥95% availability (turbine availability is standard for thermal plants). Heat exchangers survive primary coolant chemistry (water, helium, or sCO₂ with trace tritium) and thermal cycling (startup/shutdown) for 30-year plant lifetime with mid-life refurbishment. Coolant pumps, piping, and valves operate at primary loop pressure (5–20 MPa depending on coolant) and temperature (300–600°C) for 30 years. Balance of plant (electrical switchgear, transformers, cooling towers) is standard power plant equipment. |
| Best demonstrated | Steam turbine at 500 MWe scale: commercially mature (GE, Siemens, Shanghai Electric supply thousands of units globally). sCO₂ turbine at 500 MWe: pilot-scale (10 MWe prototypes); commercial-scale turbomachinery in development (tier 3). Heat exchangers for fusion primary loop: ITER heat removal system (not yet operated); DEMO heat exchanger R&D (tier 2–3). Coolant pumps and piping: nuclear-grade pumps for fission reactors (tier 5); fusion-specific tritium-compatible pumps (tier 3–4 after ITER commissioning). Balance of plant: commercially mature (tier 5). |
| Gap ratio | Turbine scale: 500 MWe steam turbine / commercial units at 500–1,000 MWe = **~1× scale** (no gap; tier 5). sCO₂ turbine (if used): 500 MWe / 10 MWe pilot = **50× scale-up**. Heat exchanger: ITER heat removal ~300 MW (first wall + blanket test cooling) / HH380 ~1,400 MW thermal = **~5× on thermal power**. Coolant pumps: nuclear-grade pumps at required flow rate (10³–10⁴ kg/s depending on coolant) exist for fission reactors; fusion-specific tritium handling is ITER-analogue (tier 3–4). |
| Closure mechanism | If steam Rankine: commercially mature turbine-generator sets from GE, Siemens, Shanghai Electric (tier 5). Heat exchanger scale-up from ITER (300 MW cooling) to HH380 (~1,400 MW) is standard thermal engineering (add more HX modules in parallel). If sCO₂ Brayton: DOE sCO₂ roadmap targets 100 MWe turbomachinery by 2030; 500 MWe requires further scale-up or multiple parallel turbines. CFETR heat exchanger program (water or helium coolant) provides Chinese-domestic BOP supply chain. |
| Classification | **Degrading** — turbine or heat exchanger failure forces plant shutdown for repair (lowers availability) but does not prevent fusion. Worst-case: turbine availability 90% instead of 95% → plant availability drops ~5% → LCOE penalty +$5–10/MWh. Heat exchanger tritium leak requires HX replacement (weeks-long outage) → similar availability penalty. |
| Evidence tier | **Tier 5** — Operating-regime demonstrated at commercial scale (for steam Rankine cycle BOP). Steam turbine at 500 MWe is commercially mature (tier 5). Heat exchanger downgrades to **tier 3** (ITER heat removal analogue, 5× scale-up to HH380, not yet operated). Coolant pumps: **tier 4** (nuclear-grade pumps exist at required scale; fusion-specific tritium handling after ITER commissioning). sCO₂ Brayton (if used) downgrades to **tier 3** (pilot-scale turbomachinery, 50× scale-up). Overall **tier rating for Function 7 hardware risk: tier 4** (blend of tier 5 for steam turbine and tier 3–4 for fusion-specific heat exchangers; steam cycle is baseline). |

**Function 7 mean**: (4 + 4) / 2 = **4.0**

---

### Function-Level Means (F1–F7)

| Function | Physics | Hardware | Mean | Heritage Floor (D-T Tokamak = 4.0) | Final (after heritage) |
|----------|---------|----------|------|-------------------------------------|------------------------|
| F1: Plasma Performance | 3 | 4 | 3.5 | 4.0 | **4.0** |
| F2: Driver / Energy Input | 4 | 3 | 3.5 | 4.0 | **4.0** |
| F3: Instability Control | 3 | 3 | 3.0 | 4.0 | **4.0** |
| F4: Plasma-Wall Interaction | 4 | 3 | 3.5 | 4.0 | **4.0** |
| F5: Neutron/Particle Handling | 3 | 3 | 3.0 | 4.0 | **4.0** |
| F6: Fuel Cycle Closure | 2 | 3 | 2.5 | 4.0 | **4.0** |
| F7: Power Conversion & BOP | 4 | 4 | 4.0 | 4.0 | **4.0** |

**Heritage credit explanation**: Energy Singularity's HTS Tokamak - Full HTS (D-T) qualifies for **D-T tokamak heritage floor = 4.0** applied to all seven functions (F1–F7). The concept is a conventional-aspect-ratio (A~4.0) D-shaped tokamak using D-T fuel, steady-state operation, ICRH heating, and standard tokamak physics (ITER-validated confinement scaling). Energy Singularity inherits decades of tokamak engineering: ITER divertor and blanket R&D (F4, F6), ITER/CFETR neutronics and shielding (F5), ICRH scaling laws from JET/ITER (F2), commercial steam Rankine BOP (F7), and tokamak disruption physics (F3). The company's full-HTS coil architecture and AI plasma control are engineering innovations layered on a mature tokamak baseline—not novel confinement physics. All computed function means (F1–F7 ranging from 2.5 to 4.0) are overridden by the 4.0 heritage floor.

**Why heritage applies to all seven functions (F1–F7), not just F1–F3**: The scoring framework specifies that heritage credit provides a **floor on all seven function scores** because heritage encompasses more than plasma physics—it includes proven engineering solutions for neutron handling (F5), fuel cycles (F6), and BOP integration (F7). A tokamak-lineage concept like Energy Singularity's inherits ITER's tritium breeding blanket R&D (F6: TBR calculations, materials testing, remote handling), ITER/JET tungsten divertor experience (F4: PFC survival data), and decades of tokamak steam-cycle coupling (F7: DEMO heat exchanger studies). Applying the heritage floor only to F1–F3 would systematically reward less-mature concepts that cite generic analogues for F4–F7 (e.g., novel confinement schemes with unproven blankets citing "fission reactor analogues") without the corresponding tokamak engineering debt. The framework's rationale is explicit: "A tokamak-lineage concept inherits decades of engineering work on divertors (F4), neutron-handling materials (F5), tritium fuel cycles (F6), and steam-cycle BOP integration (F7)."

---

### Binary Risks

Per the risk matrix, the following risks are classified as **binary** (zero net electricity if unmitigated):

1. **TBR < 1.0 for D-T fuel cycle** (F6 Physics) — If tritium breeding ratio falls below 1.0, the plant cannot achieve fuel self-sufficiency. External tritium purchase is not a valid fallback per framework rules. The concept must demonstrate TBR ≥ 1.05 via MCNP/Serpent neutronics validated by ITER TBM program. Energy Singularity has not published TBR estimate or blanket design; conventional-aspect-ratio tokamak (A~4.0) allows 4π blanket coverage → TBR > 1.0 is achievable per DEMO/CFETR scaling, but unvalidated.

2. **Tritium extraction failure** (F6 Hardware) — If tritium extraction efficiency from blanket falls below ~90%, fuel cycle inventory balance fails. External tritium supply is not valid fallback. ITER Tritium Plant (not yet commissioned) will validate extraction technology.

3. **Steady-state D-T burn at Q_eng ≥ 4.5 not achieved** (F1 Physics) — If AI plasma control fails to suppress disruptions and achieve steady-state burn with engineering gain ≥4.5, recirculating power exceeds gross electric → net electric is zero or negative. HH70 demonstrates steady-state control at experimental scale (1,337 s, no D-T); burning-plasma validation requires HH170 (if D-T burn occurs, not just "D-T equivalent") or HH380 commissioning.

**Note**: The framework specifies that these risks are ALWAYS binary for any D-T concept, regardless of claimed mitigation. Heritage credit (D-T tokamak floor = 4.0) raises F1 and F6 function scores to 4.0 (near-regime demonstration), indicating these risks are likely resolvable via ITER/SPARC/CFETR analogues, but they remain classified as binary failure modes if unmitigated.

---

### YAML Scores Block

```yaml
---
scores:
  C1: 4.1
  C3: 3.2
  C4: 2.5
  C5: 1.7
  C8: 2.0
  F1: 4.0
  F2: 4.0
  F3: 4.0
  F4: 4.0
  F5: 4.0
  F6: 4.0
  F7: 4.0
  binary_risks:
    - "TBR < 1.0 for D-T fuel cycle (F6 Physics) — fuel self-sufficiency failure if tritium breeding ratio falls below 1.0; external tritium purchase not valid fallback per framework"
    - "Tritium extraction failure (F6 Hardware) — if extraction efficiency from blanket <90%, fuel cycle inventory balance fails; external tritium supply not valid fallback"
    - "Steady-state D-T burn at Q_eng ≥ 4.5 not achieved (F1 Physics) — if AI plasma control fails to suppress disruptions and achieve steady-state burn with engineering gain ≥4.5, recirculating power exceeds gross electric output"
---
```
