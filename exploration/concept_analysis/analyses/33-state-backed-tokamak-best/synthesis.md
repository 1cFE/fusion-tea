---
ID: 33-state-backed-tokamak-best
Concept: State-Backed Tokamak (Neo / ASIPP-class)
Company: Neo Fusion
Type: synthesis
Status: draft
Created: 2026-06-08
---

## 1. Executive Summary

- **Most important risk:** The entire LCOE projection rests on achieving βN = 5.75 with H98 = 1.65 at Greenwald density — a physics performance combination no tokamak has demonstrated. If confinement degrades to H98 = 1.3 (still aggressive), major radius increases 15% and LCOE rises proportionally.
- **Most important advantage:** This is the only fusion concept with a complete systems-analysis heritage dating to the 1990s (ARIES program). The cost structure is traceable to 30+ years of integrated modeling, not speculative startups or back-of-envelope projections.
- **LCOE ballpark:** 162 $/MWh (1 GWe NOAK), 203 $/MWh (400 MWe native scale). This is expensive but assumes conservative Nb3Sn magnets at $10-20/kA-m; the study predates HTS compact tokamaks that now dominate commercial fusion.
- **Confidence verdict:** Medium. The physics is risky (advanced performance regime) but the cost methodology is the most mature in fusion. The dominant uncertainty is whether you can actually build what the models describe.

## 2. What Matters Most for LCOE

### 1. Power scrape-off width (λq) — direct sizing constraint

**Assumed:** 3-5 mm (modern formulation), driving R = 6.25 m to keep peak divertor heat flux ≤ 14 MW/m²

**Sensitivity:** ±50% uncertainty. If scrape-off widths prove narrower (2-3 mm), major radius must increase to R > 7 m to maintain tolerable divertor loading.

**What would flip the conclusion:** A 12% increase in R (6.25 → 7.0 m) increases CAS22 by ~20-25% and overnight capital by 15-20%. This would push 1 GWe NOAK LCOE from 162 $/MWh to ~185-190 $/MWh — still marginal but crossing above most competitive renewables + storage.

### 2. Advanced physics performance shortfall (H98, βN, bootstrap fraction)

**Assumed:** H98 = 1.65, βN = 5.75, 91% bootstrap current, all at Greenwald density

**Sensitivity:** No tokamak has demonstrated this combination. ITER targets H98 ~ 1.0 at n/nGr ~ 0.85. If ACT1 falls to H98 = 1.3, the required fusion power increases ~27% to maintain net output, forcing either (a) larger major radius (+15%) or (b) higher field/current with same radius (increasing magnet and power supply costs proportionally).

**What would flip the conclusion:** H98 degradation to 1.3 would increase R from 6.25 m to ~7.2 m and CAS22 from $7.3B to ~$9B (1 GWe scale). LCOE would rise from 162 $/MWh to ~190 $/MWh. This crosses the threshold where tokamaks lose competitiveness against compact HTS designs.

### 3. SiC composite maturity for 58% thermal efficiency

**Assumed:** SiC/SiC structural blanket enables 1000°C operation and 58% Brayton cycle efficiency

**Sensitivity:** Current SiC composites "have still not reached the properties required for a structural material" per the ARIES study itself. Fallback to RAFM steel with DCLL blanket reduces thermal efficiency to ~45%.

**What would flip the conclusion:** Dropping from 58% to 45% efficiency requires 30% more fusion power for the same electric output. At constant R, this means higher field/current (magnet cost +20%) or accepting lower net output. At constant net output, R increases ~10% (6.25 → 6.9 m), adding 15-18% to CAS22. LCOE rises from 162 $/MWh to ~185 $/MWh. The SiC gamble is worth ~$25/MWh.

### 4. Divertor lifetime under ELMs and erosion/redeposition

**Assumed:** 5 full-power years (FPY) with 90% radiated power fraction and ELM mitigation

**Sensitivity:** The study notes that ~100 million ELMs over one year of operation require ELM energy release reduced by 10× to avoid tungsten melting. If ELM control fails or erosion/redeposition shortens lifetime to 2-3 FPY, replacement frequency doubles.

**What would flip the conclusion:** Halving divertor lifetime increases levelized replacement cost 50-100% and reduces availability ~5 percentage points. LCOE rises from 162 $/MWh to ~175 $/MWh. Not catastrophic but erases margin against cheaper tokamak variants.

### 5. H/CD wall-plug efficiency (η_CD)

**Assumed:** 0.4 for all heating systems (down from 0.7 in older studies)

**Sensitivity:** Range is 0.25-0.5 per recent reviews. ACT1 requires 42.7 MW at 0.4 efficiency. Degradation to 0.35 adds ~12 MW recirculating power, reducing net output ~2% and Q_eng from 6.6 to 5.8.

**What would flip the conclusion:** Each 0.05 efficiency drop increases LCOE by ~$3/MWh. At 0.30 efficiency (low end), recirculating power reaches ~70 MW and LCOE rises ~$12/MWh. Not dominant but compounds with other risks.

**Ranked elasticity (rough estimate):**
1. Scrape-off width: ±20% LCOE per ±30% sizing error
2. Physics performance (H98): ±18% LCOE per ±20% confinement shortfall
3. SiC maturity (thermal efficiency): +15% LCOE if technology fails
4. Divertor lifetime: +8% LCOE if lifetime halves
5. H/CD efficiency: +7% LCOE if efficiency drops from 0.4 to 0.3

## 3. Risk Verdicts

### Divertor heat flux management (λq = 3-5 mm scrape-off width)

**Verdict:** Genuinely uncertain

**Rationale:** ITER will provide the first high-power experimental validation at reactor-relevant field/current/size, but results won't arrive until late 2030s.

**What would retire this risk:** ITER D-T campaign measurements of λq at 500 MW fusion power with detached divertor operation. If ITER demonstrates 4-6 mm scrape-off widths at high power, ACT1's R = 6.25 m is validated. If ITER measures <3 mm, all large tokamaks must upsize.

### Advanced physics (βN = 5.75, H98 = 1.65 at Greenwald density)

**Verdict:** Unlikely resolvable before construction

**Rationale:** This requires simultaneous achievement of high normalized beta, high confinement, high density, and high bootstrap fraction — well beyond ITER's mission. BEST aims for Q~5 but at more conservative physics assumptions.

**What would retire this risk:** A dedicated advanced-tokamak experiment demonstrating steady-state operation with βN > 5, H98 > 1.5, and n/nGr > 0.95 for hundreds of seconds. No such facility is funded. ITER will operate at βN ~ 2-2.5 and H98 ~ 1.0. The gap between ITER and ACT1 is larger than the gap between current experiments and ITER.

### SiC composite structural blanket (1000°C, 100+ dpa tolerance)

**Verdict:** Unlikely resolvable without fusion neutron source

**Rationale:** Fission irradiation can reach high dpa but lacks the 14 MeV neutron spectrum and helium generation rates of fusion. The study explicitly states "testing with a fusion-relevant neutron source is required."

**What would retire this risk:** A fusion neutron source facility irradiating full-thickness SiC structures to 150+ dpa with simultaneous thermal cycling and PbLi compatibility testing. No such facility exists or is funded. The fallback is to abandon SiC and accept RAFM steel blankets at 45% thermal efficiency.

### ELM control for tungsten divertor survival

**Verdict:** Likely resolvable

**Rationale:** ITER's research plan includes dedicated ELM control experiments using resonant magnetic perturbations (RMP) and pellet pacing. Multiple existing tokamaks (DIII-D, ASDEX-U, KSTAR) have demonstrated partial ELM suppression.

**What would retire this risk:** ITER demonstration of 90% ELM energy reduction or complete suppression via RMP in Q > 5 plasmas for multi-pulse campaigns. Success by ~2035 would validate ACT1's 5 FPY divertor lifetime assumption.

### Tritium breeding ratio (TBR > 1.05 with 40% 6Li enrichment)

**Verdict:** Likely resolvable

**Rationale:** TBR is calculable with reasonable confidence from neutronics codes validated against D-T experiments and fission critical assemblies. ITER Test Blanket Module (TBM) program will provide first fusion-environment validation.

**What would retire this risk:** ITER TBM demonstration of measured TBR > 1.0 with uncertainties <±5% in PbLi and ceramic breeder configurations. Post-irradiation examination of BEST/CFEDR TBMs validating 6Li depletion models. Success likely by early 2030s.

### Remote maintenance reliability (80% availability target)

**Verdict:** Genuinely uncertain

**Rationale:** ITER will demonstrate remote handling hardware but not operational reliability over decades. The difference between "can replace a blanket module in a test facility" and "routinely maintain a commercial plant at 80% availability" is large.

**What would retire this risk:** First-of-a-kind demonstration reactor (CFEDR, ARC, or equivalent) achieving >75% availability over 5+ years of D-T operation with remote-only maintenance. This won't be known until the 2040s.

## 4. Structural Advantages and Disadvantages

**vs. conventional D-T tokamak baseline (ITER-class magnets, RAFM/water-cooled blanket, conservative physics):**

### Advantages

**High thermal efficiency (+30% vs. baseline):** The SiC/PbLi blanket at 58% efficiency eliminates ~20-25% of required fusion power compared to RAFM/water-cooled at 45%. This shrinks the reactor ~10% in linear dimensions and reduces CAS22 non-magnet costs proportionally. **Quantified benefit:** ~$1.5B capital cost reduction (15% of CAS22) at 1 GWe scale, assuming SiC matures.

**High bootstrap fraction reduces H/CD cost:** 91% bootstrap current means only 42.7 MW of external heating is required for 1813 MW fusion power. Conventional tokamaks with 50-70% bootstrap require proportionally more H/CD. **Quantified benefit:** ACT1 H/CD capital cost is ~$240M (C220104); a 50% bootstrap design would require ~80 MW H/CD at $400-500M capital.

**Flexible operating zone:** ACT1 can trade major radius (6.0-6.75 m), field (5.25-7.25 T), and beta (4.0-5.0) while maintaining LCOE within 5% of reference. This allows optimization for supply-chain constraints (e.g., upsize radius to reduce field if magnet costs spike).

### Disadvantages

**No HTS magnet cost reduction:** ACT1 uses Nb3Sn at 11.8 T peak field. Compact HTS tokamaks (SPARC, ST80, HH70) achieve 2-3× smaller major radius by using REBCO at 20-23 T, shrinking CAS21 (buildings) and some CAS22 accounts (vacuum vessel, shield) despite higher magnet $/kA-m. **Quantified penalty:** ACT1 CAS21 is $667M (1 GWe); SPARC-class designs estimate $200-400M due to compactness. ACT1 sacrifices ~$300-400M in building cost to avoid HTS magnet risk.

**Advanced physics risk premium:** The βN = 5.75, H98 = 1.65 regime is unvalidated. Conservative designs (βN ~ 3, H98 ~ 1.0) can achieve comparable LCOE by accepting lower power density and compensating with modest size increase. **Risk-adjusted cost:** If ACT1 physics assumptions fail (50% probability), fallback to conservative physics increases R by 15% and capital cost by $1.5-2B, erasing the bootstrap advantage.

**Material qualification bottleneck:** SiC composites, 180 dpa RAFM steel, and PbLi MHD/corrosion behavior all require fusion neutron testing unavailable until a fusion neutron source is built. Conservative designs using well-characterized materials (316 stainless steel, water coolant) sacrifice efficiency but eliminate this timeline risk.

**Net structural position:** ACT1 is a high-efficiency, high-physics-risk, large-scale tokamak. It wins on thermal efficiency and plasma performance (if achieved) but loses on compactness and technology readiness compared to HTS tokamaks. The cost structure is conventional — dominated by CAS22 reactor equipment ($7.3B at 1 GWe) with minimal exotic cost elements. The advantage over baseline is incremental (~15-20% capital reduction if SiC and advanced physics both succeed) rather than revolutionary.

## 5. Cross-Concept Positioning

**This concept sits in:** The conservative wing of magnetic confinement fusion — D-T tokamaks with Nb3Sn magnets and conventional aspect ratio. It shares this neighborhood with ITER, CFEDR, and K-DEMO.

**Concepts with similar economics:**

**28-hts-tokamak-full-hts (Energy Singularity HH70):** Both are state-backed D-T tokamaks with similar physics assumptions (likely H98 ~ 1.2-1.5, βN ~ 4-5). HH70 uses HTS magnets for compactness; ACT1 uses LTS magnets with high-efficiency blanket. The trade-off is magnet $/kA-m vs. thermal efficiency. If HTS supply chains mature before SiC composites, HH70 wins; if SiC matures first, ACT1 wins.

**29-negative-triangularity-tokamak (Firefly):** Shares the D-T tokamak architecture but bets on plasma shaping (negative triangularity) to enable ELM-free operation and potentially higher power density. If negative-δ proves viable, Firefly achieves similar LCOE with simpler divertor (no ELM mitigation, 10+ FPY lifetime). If negative-δ underperforms, Firefly falls back to ACT1-like positive-δ configuration and the concepts converge.

**01-hts-compact-tokamak (CFS SPARC/ARC):** Different architecture (HTS, compact) but similar fuel cycle and confinement physics. SPARC uses conservative physics (βN ~ 3, H98 ~ 1) to offset HTS magnet risk; ACT1 uses conservative magnets (Nb3Sn) to offset advanced physics risk. **LCOE comparison:** SPARC's compactness likely wins on CAS21/CAS22 absolute cost, but ACT1 may achieve lower $/kWe at GW scale due to economies of scale. Both are in the 150-200 $/MWh range under optimistic assumptions.

**What makes this one fundamentally different:**

**1. Heritage:** ACT1 is the endpoint of 30 years of ARIES tokamak systems studies (ARIES-I through ARIES-ACT). The cost methodology, component scaling laws, and integration logic are validated against ITER engineering and decades of tokamak operations. No other private fusion concept has this depth of systems-analysis heritage.

**2. State backing with transparency:** Most state-backed fusion programs (China's CFEDR, Korea's K-DEMO) publish technical details but not cost breakdowns. ACT1 (via ARIES) and BEST (via the published Research Plan) provide unusual transparency, enabling traceable cost estimates. Private companies (CFS, TAE, Helion) publish limited data.

**3. Technology conservatism with performance ambition:** ACT1 uses proven magnet technology (Nb3Sn), proven fuel (D-T), and proven confinement geometry (tokamak) — but pushes plasma performance to the edge of theory (βN = 5.75, H98 = 1.65). This is the opposite of most startups, which use conservative physics with exotic technology (HTS, aneutronic fuels, alternative confinement).

**Positioning verdict:** ACT1 is the "ITER successor" — what you build if you want a large, high-performance D-T tokamak with the lowest technical risk consistent with commercial LCOE. It is not the cheapest concept (compact HTS tokamaks win on capital cost) or the fastest to deploy (private companies target 2030s, ACT1 is a 2040s design). It is the highest-confidence path to a working fusion power plant, conditional on physics assumptions being validated.

## 6. Modeling Confidence

**Rating: Medium**

**Data-anchored parameters (high confidence):**
- Geometry: R, a, κ, δ from published ARIES-ACT1 design (Table I)
- Magnetic field: B0 = 6.0 T, B_peak = 11.8 T (Table I)
- H/CD power: 42.7 MW (Table I)
- Thermal efficiency: 58% (stated for SiC/PbLi Brayton cycle)
- Component lifetimes: 5 FPY (first wall, blanket, divertor), 20 FPY (vacuum vessel)

**Speculative parameters (low confidence):**
- Physics performance: βN = 5.75, H98 = 1.65, 91% bootstrap — all undemonstrated in combination
- SiC composite properties: 1000°C operation, 180 dpa tolerance — "have still not reached properties required for structural material"
- Divertor lifetime: 5 FPY assumes 10× ELM energy reduction and erosion/redeposition models validated only at <1 FPY in existing devices
- PbLi blanket behavior: MHD pressure drop, corrosion, tritium extraction all require fusion-environment validation
- Remote maintenance availability: 80% capacity factor assumes reliability demonstrated only in concept, not operation

**Dominant source of LCOE uncertainty:**

**Physics performance shortfall.** The ACT1 design is optimized for βN = 5.75 and H98 = 1.65. If actual performance falls to βN = 4.0 and H98 = 1.3 (still aggressive by ITER standards), the reactor must upsize 15-20% or accept lower net output. This uncertainty dominates because:

1. **It propagates through all cost accounts:** Larger R increases CAS21 (buildings), CAS22 (reactor equipment), CAS30 (capitalized equipment replacement), and CAS50 (construction management) proportionally.
2. **It cannot be retired without a burning-plasma experiment exceeding ITER's performance:** ITER targets βN ~ 2-2.5 and H98 ~ 1.0. The gap between ITER and ACT1 is comparable to the gap between JET and ITER. No experiment between ITER and a DEMO-scale device is funded.
3. **It interacts with other uncertainties:** If physics underperforms AND SiC composites fail, the reactor must use RAFM blankets (45% efficiency) with conservative physics (H98 = 1.3), requiring R ~ 7.5-8 m and LCOE ~ 220-250 $/MWh — no longer competitive.

**Quantified uncertainty bands (rough estimates):**

- **Optimistic case (all assumptions hold):** LCOE = 140-160 $/MWh. Physics performs as modeled, SiC matures, divertor lasts 5 FPY, remote handling achieves 80% availability.
- **Central case (modest physics shortfall, SiC fails):** LCOE = 180-200 $/MWh. H98 = 1.4, fallback to RAFM/DCLL (45% efficiency), divertor lifetime 4 FPY, availability 75%.
- **Pessimistic case (major physics shortfall):** LCOE = 220-260 $/MWh. H98 = 1.2, RAFM blanket, divertor lifetime 3 FPY, availability 70%, R upsized to 7.5 m.

**The cost methodology is mature; the physics is not.** This is Medium confidence because the modeling framework (ARIES systems codes, CAS account structure) is the most validated in fusion, but the input assumptions (physics performance, SiC maturity) are speculative. Confidence will remain Medium until ITER and advanced-tokamak experiments provide data to validate or refute the physics assumptions.

## 7. What Would Change My Mind

### 1. ITER achieves H98 > 1.3 at high density (n/nGr > 0.9) in Q > 5 plasmas

**Direction:** Increases confidence, lowers LCOE estimate toward optimistic case (140-160 $/MWh)

**Mechanism:** Validates that high confinement at Greenwald density is achievable in reactor-relevant regimes. Reduces uncertainty on R sizing by ±15% to ±5%. If ITER demonstrates H98 = 1.4-1.5, ACT1's assumption of H98 = 1.65 becomes plausible via modest extrapolation rather than speculative.

**Timeline:** ITER D-T campaign, late 2030s

### 2. SiC composites achieve 100 dpa with acceptable property retention under fission+modeling validation

**Direction:** Increases confidence, validates 58% thermal efficiency and SiC cost advantage

**Mechanism:** Retiring the SiC maturity risk eliminates the fallback to RAFM/DCLL (45% efficiency), preserving ACT1's 15-20% capital cost advantage over conservative tokamak designs. If SiC proves viable by 2035, ACT1 becomes the preferred large-scale tokamak architecture.

**Timeline:** Ongoing fission irradiation programs + modeling validation, results by 2030-2035

### 3. Compact HTS tokamak demonstrates <100 $/MWh LCOE at 100+ MWe scale

**Direction:** Decreases ACT1 attractiveness, shifts investment to HTS compact designs

**Mechanism:** If SPARC, ST80, or HH70 achieves <100 $/MWh via compactness + HTS magnets, ACT1's value proposition (high-confidence but expensive large-scale tokamak) evaporates. The market shifts to modular HTS plants, and ACT1 becomes a backup option for countries unable to access HTS supply chains or preferring single-GW baseload plants.

**Timeline:** SPARC first plasma ~2026, commercial demonstration ~2030-2035

### 4. Power scrape-off width measurements on ITER show λq < 2 mm at high power

**Direction:** Materially increases LCOE, forces all large tokamaks to upsize

**Mechanism:** If ITER measures scrape-off widths narrower than current models predict, ACT1's R = 6.25 m is insufficient to maintain peak divertor heat flux <15 MW/m². The design must upsize to R ~ 7.5-8 m, increasing capital cost 20-30% and LCOE from 162 $/MWh to 195-210 $/MWh. This would make large tokamaks uneconomical and shift the field toward compact designs or alternative confinement.

**Timeline:** ITER high-power divertor experiments, mid-to-late 2030s

**Which one matters most:** ITER's scrape-off width measurements (#4). This is a binary outcome with immediate implications for all tokamak designs. If λq proves narrower than modeled, the entire large-tokamak pathway (ACT1, CFEDR, K-DEMO) becomes uneconomical and the field pivots to compact HTS designs or alternatives. If λq matches predictions, ACT1 remains viable and the competition becomes physics performance (#1) and SiC maturity (#2) vs. HTS compactness (#3).
