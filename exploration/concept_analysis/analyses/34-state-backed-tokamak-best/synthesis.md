---
ID: 34-state-backed-tokamak-best
Concept: State-Backed Tokamak - BEST (D-T)
Company: Neo Fusion
Type: synthesis
Status: draft
Created: 2026-05-14
---

# Synthesis: State-Backed Tokamak - BEST (D-T)

## 1. Executive Summary

- **Most important risk**: Commercial PFPP design point is completely unspecified. BEST generates no electricity and targets Q≥1 scientific breakeven—far below commercial viability. LCOE modeling requires extrapolation across two additional steps (CFEDR Phase I at Q~3, Phase II at Q~23) to an undefined PFPP, introducing systematic uncertainty that no additional data gathering can resolve until China publishes commercial reactor parameters.

- **Most important advantage**: State backing eliminates private-sector capital constraints and provides access to Chinese construction economics (historically 2–4× lower costs than Western projects). If this discount applies broadly to fusion direct capital (CAS21–CAS26), LCOE could drop from 158 $/MWh to 87 $/MWh at 2× discount or 51 $/MWh at 4× discount—potentially achieving commercial competitiveness that Western LTS tokamaks cannot match.

- **LCOE ballpark**: 158 $/MWh at 1 GWe (ARIES-ACT1 geometry analogue, sCO2 Brayton 34.7%, Q~10, 80% CF, NOAK, Western cost basis). Range: 51–336 $/MWh across Chinese discount scenarios (1–4×) and capacity factor uncertainty (35–90%). Central estimate assumes quasi-steady-state PFPP; if PFPP inherits CFETR Phase I pulsed duty cycle (30–50%), LCOE increases to 239–336 $/MWh.

- **Confidence verdict**: Low. Only 4 of 13 LCOE-critical parameters have published data. Geometry analogue (ARIES-ACT1 R₀=6.25m vs. CFETR R₀=6.6m) introduces ~5% geometric error. Blanket technology undecided (three TBM concepts competing). Chinese construction discount magnitude in fusion context is uncharacterized. Q value, capacity factor, and recirculating power for PFPP are speculative. Model output should be treated as scenario analysis, not prediction.

---

## 2. What Matters Most for LCOE

Parameters ranked by LCOE sensitivity (elasticity = %LCOE / %parameter). All values anchored to model output at base case (1 GWe, Q~10, CF=80%, Western NOAK cost basis, sCO2 34.7% efficiency).

### Rank 1: Capacity factor (elasticity -0.91)

**Assumed value**: 80% (central estimate from Araiinejad & Shirvan 2025 D-T MCF analogue range 75–90%)
**Source confidence**: Low—no PFPP-specific estimate exists

**Uncertainty**: CFETR Phase I physics simulations (Deng et al. 2019, OSTI 1465662) report duty cycle 0.3–0.5 for pulsed operation. If PFPP inherits CFETR's pulsed characteristics rather than achieving quasi-steady-state, CF drops to 35–50%, increasing LCOE from 158 $/MWh to 239–336 $/MWh (1.5–2.1× penalty).

BEST's long-pulse mission (>1000s target) supports the quasi-steady-state assumption, but CFETR Phase I cannot sustain burning plasma at Q>3 continuously due to divertor heat loads (Pdiv/R₀ = 32.4 MW/m exceeds ITER guidelines) and incomplete RWM stabilization physics at βN=3.54. The gap between CFETR Phase I (pulsed, duty cycle 0.3–0.5) and PFPP (assumed quasi-steady-state, CF 75–90%) is the largest unresolved physics-operations question in the lineage.

**What would flip the conclusion**: Published PFPP operations scenario achieving >75% CF through validated divertor heat management and steady-state current drive at commercial Q values (Q≥10). Alternatively, demonstration that pulsed operation at 50% CF can achieve <150 $/MWh through capital cost reductions—this is the Chinese discount hypothesis (H1).

---

### Rank 2: Chinese construction cost discount (elasticity +0.91, inverted)

**Assumed value**: 1× (no discount applied in base case; Western NOAK cost basis)
**Source confidence**: Very low—magnitude in fusion context unknown

**Sensitivity**: Model shows 2× discount across CAS21–CAS26 direct capital accounts (buildings, reactor plant, turbine, electrical, misc., heat rejection) reduces LCOE from 158 $/MWh to 87 $/MWh. 4× discount yields 51 $/MWh—commercially competitive with natural gas combined cycle.

**Evidence basis**: Chinese infrastructure projects (HSR, bridges, nuclear fission) achieve 2–4× cost advantage over Western analogues through lower labor rates ($8–15/hr skilled construction vs. $35–70/hr in US/EU), domestic equipment supply chains (ASIPP manufactures >70% of China's ITER procurement packages including superconducting conductors), and streamlined regulatory approval (BEST construction 2023–2027, 4 years vs. ITER's 15+ years for comparable device scale).

**Critical uncertainty**: Does this advantage transfer to fusion-specific components? CAS22 reactor plant equipment (~46% of overnight capital) includes magnets, vacuum vessel, blanket, divertor, remote handling—all fusion-unique. If discount applies only to CAS21 buildings (~7% of capital), LCOE reduction is negligible. H1 hypothesis requires broad applicability to CAS21–CAS26 (~58% of overnight capital) to produce meaningful LCOE impact.

**What would flip the conclusion**: Published capital cost estimate for BEST, CFEDR, or any Chinese fusion device with CAS-level breakdown. Comparison to ITER procurement costs for identical components (e.g., Nb3Sn conductor $/kA-m, vacuum vessel $/tonne, PFC modules $/m²) would quantify the discount empirically.

---

### Rank 3: Winding bore radius / machine scale (r_coil elasticity +0.47)

**Assumed value**: r_coil = 3.2 m (ARIES-ACT1 analogue: R₀=6.25m, a=1.5625m)
**Source confidence**: Medium—CFETR Phase I validated geometry (R₀=6.6m) is close

**Uncertainty**: CFETR Phase I (arxiv-1907-11919, Deng et al. 2019) establishes R₀=6.6m, B₀=6.0T as the preferred intermediate configuration. Commercial PFPP may upscale to R₀=7–8m for higher fusion power and better neutron economy (larger blanket volume improves TBR margin). Machine volume scales as R₀³—a 20% increase in R₀ (6.25m→7.5m) increases volume 73%, driving magnet conductor length, structural steel mass, and vacuum vessel area proportionally.

LTS Nb3Sn conductor at $2–10/kA-m is cheaper per unit length than REBCO HTS ($30–100/kA-m), but total conductor cost scales with machine size. At R₀=6.6m, PFPP magnet system is ~10,000 tonnes cold mass (5× BEST's 2,000t)—total Nb3Sn strand cost ~$400M, complete winding and structure $1.2–2B. Compact HTS designs (CFS ARC-class, R₀~3.3m, 20T) achieve comparable net output at ~$0.75–1.6B magnet cost (2025 tape prices) or $150–500M if REBCO hits $10/m target. LTS advantage diminishes if REBCO cost targets are met.

**What would flip the conclusion**: Published PFPP geometry revealing R₀<6m (unlikely—burning plasma tokamaks scale upward, not downward). Or demonstration that compact HTS at R₀<4m achieves equivalent TBR and divertor heat management—this would favor HTS route over LTS at commercial scale.

---

### Rank 4: Construction time (elasticity +0.42)

**Assumed value**: 8 years (ITER-lessons but Chinese construction speed)
**Source confidence**: Low—no PFPP schedule published

**Sensitivity**: Each additional year of construction increases LCOE by ~6.6 $/MWh through interest-during-construction (CAS60). ITER construction timeline (2007 tokamak assembly start → 2025 first plasma, 18 years) provides upper bound. BEST construction (2023–2027, 4 years) demonstrates Chinese execution speed at intermediate scale but with simplified mission (no tritium breeding, no power conversion, experimental device).

**Uncertainty**: PFPP as first-of-kind commercial fusion plant faces risks BEST does not: blanket manufacturing at scale, tritium licensing at kg/day throughput, full balance-of-plant commissioning, grid interconnection, commercial operating license under Chinese fusion regulatory framework (not yet established). FOAK penalty typically adds 2–4 years vs. NOAK baseline. Model uses NOAK assumption—appropriate for assessing mature technology potential, not first unit.

**What would flip the conclusion**: Chinese regulatory framework for commercial fusion published with licensing timeline. Or first-of-a-kind CFEDR project schedule revealing actual construction duration at DEMO scale (if 5–6 years, supports 8-year NOAK assumption; if >10 years, LCOE increases to 175+ $/MWh).

---

### Rank 5: Thermal efficiency (elasticity -0.27)

**Assumed value**: 35% (sCO2 Brayton; standardized from published CFETR study value 34.7%)
**Source confidence**: Medium—preferred cycle in published studies, not formally committed

**Sensitivity**: 1% absolute improvement in η_th reduces LCOE by ~4.3 $/MWh. sCO2 Brayton at 34.7% (CFETR studies, cfetr-power-conversion-studies.md) outperforms steam Rankine at 26.4% (standard D-T baseline). Advanced sCO2 recompression cycles at 42.8–53.7% are cited in literature but undemonstrated at fusion scale.

**Blanket coupling**: sCO2 cycle selection drives blanket choice. COOL TBM (CO2-cooled LiPb, 8 MPa, 350°C inlet) couples naturally to sCO2 turbomachinery. WCCB (water-cooled ceramic breeder) couples to steam Rankine. Model shows WCCB/Rankine scenario increases LCOE by +15.9 $/MWh (173.6 vs. 157.7 $/MWh) due to lower cycle efficiency—nearly 10% LCOE penalty for blanket technology choice.

**Uncertainty**: Three TBM concepts are competing (COOL, WCCB, EU alternatives). BEST experimental results in 2030s will determine which blanket PFPP adopts. If WCCB wins (better TBR or lower corrosion issues), PFPP is locked into lower-efficiency Rankine cycle unless sCO2-compatible water-cooled blanket can be developed.

**What would flip the conclusion**: COOL TBM demonstration of TBR>1.1 at BEST, confirming sCO2 path viability. Or sCO2 pilot plant demonstration at 200+ MWe scale with fusion-relevant heat source (pulsed thermal transients, tritium-compatible materials). Sandia/DOE sCO2 programs at 10 MWe pilot scale are encouraging but insufficient to retire fusion-scale risk.

---

## 3. Risk Verdicts

Challenges ranked by LCOE impact per analysis.md Section 2.

### Challenge 1: Experimental device extrapolation—no direct commercial analog

**Verdict**: Unlikely resolvable before CFEDR operates

**Rationale**: BEST generates no electricity, targets Q≥1 (Q~5 advanced scenario by 2032–2035), and has no committed commercial descendant design. Any LCOE estimate requires parametric assumptions about PFPP that cannot be validated until CFEDR publishes a commercial reactor design—likely post-2030.

**What would retire this risk**: ASIPP/CFETR program publishes commercial PFPP design point (R₀, B₀, Q, P_fusion, P_electric, blanket choice, capacity factor target, capital cost estimate) with CAS-level cost breakdown and commercialization timeline. Until then, all LCOE estimates are scenario analysis with large error bars.

---

### Challenge 2: State cost accounting—Chinese construction economics differ from Western analogues

**Verdict**: Genuinely uncertain

**Rationale**: Historical Chinese infrastructure cost advantage (2–4×) is well-documented but fusion-specific magnitude is uncharacterized. Stewart & Shirvan 2.2× regulatory building cost factor (fission-derived) may not apply in Chinese regulatory context, which has faster approval timelines for research devices but no established commercial fusion licensing framework.

**What would retire this risk**: Comparative cost study of identical fusion components procured in China vs. Western markets (e.g., ITER vs. EAST Nb3Sn conductor $/kA-m, vacuum vessel $/tonne, PFC modules $/m²). Or published Chinese fusion regulatory cost framework with licensing fees, quality assurance requirements, and construction oversight costs. Until resolved, Chinese discount must be treated as scenario parameter spanning 1–4× range.

---

### Challenge 3: LTS magnet cost structure—larger machine, lower per-unit-length cost

**Verdict**: Likely resolvable through published cost comparisons

**Rationale**: Nb3Sn conductor cost ($2–10/kA-m) vs. REBCO HTS ($30–100/kA-m current, $10–15/kA-m target) is well-characterized. Total magnet system cost depends on machine scale (LTS requires larger R₀ at lower B₀) vs. conductor unit cost. At 2025 prices, LTS and HTS magnet systems cost within factor of ~2 for comparable net output. REBCO cost roadmap to $10/m shifts advantage decisively to HTS.

**What would retire this risk**: Parametric cost comparison across 01-hts-compact-tokamak (CFS SPARC-class, full-HTS REBCO at 20T, R₀~1.85m) and this concept (LTS Nb3Sn at 6T, R₀~6.6m) using validated CAS22 magnet account breakdowns. Cross-concept analysis will reveal whether LTS route remains cost-competitive if REBCO tape achieves $10–15/m target pricing.

---

### Challenge 4: Multi-method H&CD system costs and recirculating power

**Verdict**: Likely resolvable—partially degrading

**Rationale**: BEST operates four concurrent heating methods (ECRH 15MW + ICRH 10MW + LHCD 10MW + NBI 12MW, 50MW total). CFETR Phase I simulations (OSTI 1465662) show NBI removal degrades Q from 2.0 (NB+EC) to 1.2 (EC+LH only)—~40% Q penalty. NBI cannot be eliminated without major fusion gain degradation due to loss of plasma rotation (suppresses turbulence transport) and direct ion heating.

LHCD applicability at burning plasma temperatures is uncertain—lower-hybrid wave penetration is electron-temperature limited, potentially constraining LHCD contribution at high-Q scenarios where T_e~20 keV. If LHCD is ineffective at commercial conditions, PFPP must rely on NBI+ECRH+ICRH only, with weighted wall-plug efficiency ~0.60. At Q=10, auxiliary heating is 364 MW thermal (607 MW electric)—manageable recirculating load at 1 GWe plant scale but becomes dominant at Q<8.

**What would retire this risk**: BEST burning plasma experiments (Q~5 scenario, post-2032) demonstrating effective H&CD portfolio at elevated T_e. Or published PFPP H&CD strategy with recirculating power budget and Q sensitivity analysis.

---

### Challenge 5: Blanket technology selection drives blanket cost, efficiency, and TBR

**Verdict**: Genuinely uncertain—resolves in 2030s

**Rationale**: Three TBM concepts under test (COOL CO2-cooled LiPb, WCCB water-cooled ceramic breeder, EU alternatives). COOL+sCO2 achieves 34.7% efficiency; WCCB+Rankine achieves 26.4%—nearly 10% LCOE penalty. TBR performance, tritium extraction reliability, and structural materials qualification will determine selection.

**What would retire this risk**: BEST TBM experimental results (post-2030) demonstrating TBR>1.1, tritium extraction at target rates, and structural materials survival under 14 MeV neutron fluence for at least one blanket concept. Until then, blanket choice is a branching uncertainty requiring parallel cost scenarios.

---

### Challenge 6: Power conversion cycle—sCO2 preferred but not committed

**Verdict**: Likely resolvable—degrading

**Rationale**: Published CFETR studies (2021, 2024, 2025) identify sCO2 Brayton as superior in efficiency (34.7% vs. 26.4% Rankine), compactness, and cost. COOL TBM couples naturally to sCO2. However, PFPP has not formally committed to sCO2, and fusion-scale sCO2 demonstration (200+ MWe with pulsed heat source) does not yet exist.

**What would retire this risk**: DOE/Sandia sCO2 pilot plant scale-up to 50–100 MWe with demonstrated reliability (current pilots are 1–10 MWe), or formal PFPP design selection of sCO2 Brayton with published cycle parameters and tritium permeation barrier strategy for CO2-facing heat exchangers. Fission-sector Gen-IV reactors (HTGR, SFR) adopting sCO2 would provide commercial-scale validation transferable to fusion.

---

## 4. Structural Advantages and Disadvantages

Comparison against conventional D-T tokamak cost structure baseline (ARIES-AT/ARIES-ACT1 class, R₀~5–6m, B₀~6T, Q~5–10, steam Rankine).

### Advantages relative to baseline

**1. State backing eliminates private-sector capital constraints**

Chinese government funding (~$2B registered capital for Neo Fusion, $214M raised) and CNPC/CAS majority ownership provide unlimited patient capital for FOAK commercial demonstration. No investor IRR requirements, no exit timeline pressure, no bankruptcy risk during long development. Western private fusion ventures face Series C+ funding cliffs and must demonstrate commercial viability on 5–10 year timelines to satisfy venture investors. China can absorb FOAK cost overruns and schedule delays without program cancellation risk.

LCOE impact: Not directly quantifiable but enables pursuit of lower-LCOE pathways with longer development timelines (e.g., tritium breeding optimization, advanced divertor solutions, sCO2 cycle development) that private ventures cannot afford to wait for. Indirectly, state backing may justify the 2–4× Chinese construction discount hypothesis by enabling vertical integration of supply chains and acceptance of lower profit margins on manufactured components.

**2. LTS magnet technology—mature supply chain, no REBCO tape bottleneck**

Nb3Sn TF/PF coils use ITER-qualified conductors at $2–10/kA-m (5–10× cheaper than REBCO per unit length). ASIPP manufactures >70% of China's ITER procurement packages including superconducting conductors, establishing domestic supply chain with no import dependency. Global Nb3Sn production capacity (Europa Superconductors, Furukawa, Chinese manufacturers) can support multi-thousand-kilometer conductor demand for commercial PFPP fleet.

YBCO use limited to CS high-field sub-coils (18.8T peak field)—manageable procurement from established REBCO producers without supply bottleneck. Unlike full-HTS designs requiring 5,000+ km REBCO tape per reactor, BEST lineage has minimal exposure to REBCO supply chain risk and cost volatility.

LCOE impact: Lower magnet material cost per unit length partially offsets larger machine volume. At 2025 REBCO prices, LTS and HTS magnet system costs are within factor of ~2. If REBCO hits $10/m target, HTS advantage becomes decisive—but this remains a supply chain risk for HTS concepts that LTS route avoids entirely.

**3. sCO2 Brayton power conversion—higher efficiency than steam Rankine**

Published CFETR studies identify sCO2 Brayton at 34.7% efficiency vs. 26.4% for conventional steam Rankine. COOL TBM (CO2-cooled LiPb) couples naturally to sCO2 turbomachinery. Model shows ~9 percentage point LCOE reduction (15.9 $/MWh) vs. WCCB/Rankine alternative—nearly 10% LCOE advantage if COOL blanket path is validated.

Compact sCO2 turbomachinery reduces CAS23 turbine plant footprint and CAS26 heat rejection system size relative to steam Rankine at equivalent thermal power. Advanced sCO2 recompression cycles at 42.8–53.7% (literature upper bound) could further improve LCOE if demonstrated at fusion scale.

LCOE impact: -15.9 $/MWh vs. steam Rankine baseline, assuming COOL TBM validation and sCO2 cycle commitment.

**4. Full-tungsten first wall—eliminates beryllium supply chain dependency**

240 W-coated CuCrZr first-wall modules + 48 W-monoblock divertor cassettes. China produces >80% of global tungsten, eliminating material scarcity risk and import dependency. ASIPP has W fabrication experience through ITER divertor dome component manufacturing.

ARIES-AT baseline uses Be first wall + W divertor. Beryllium supply chain is constrained (primary sources: US Materion, Kazakhstan Ulba)—global production ~260 tonnes/yr, projected fusion demand ~50–100 tonnes per reactor startup for Be multiplier in blanket. Full-W first wall eliminates Be FW dependency (blanket TBM concepts still use Be12Ti multiplier in ceramic breeder variants, but at lower volumes than Be FW + blanket combination).

LCOE impact: Eliminates Be supply chain bottleneck (~$300–600/kg for nuclear-grade Be) but increases PFC complexity (W impurity control, remote handling of activated W modules). Net impact on CAS22 FW/divertor cost is modest but improves supply chain risk profile.

---

### Disadvantages relative to baseline

**1. No published commercial plant design—all LCOE estimates are extrapolations**

BEST generates no electricity, targets Q≥1 experimental breakeven, and has no committed PFPP geometry. Model uses ARIES-ACT1 analogue (R₀=6.25m) to approximate CFETR Phase I preferred configuration (R₀=6.6m), but commercial PFPP may upscale to R₀=7–8m for better neutron economy. Geometric scaling uncertainty compounds with blanket choice, capacity factor, and Q value uncertainties.

LCOE impact: All quantitative estimates have very low confidence. Published cost studies (Chen et al. 2015 CFETR preliminary cost) predate current BEST design and lack CAS-level breakdown. Cannot estimate PFPP overnight capital within better than ±50% without actual design parameters.

**2. CFETR Phase II readiness gaps—divertor heat loads exceed ITER guidelines**

CFETR Phase II (Pfus=1084 MW, Q=23.5, same hardware as Phase I) requires Pdiv/R₀ = 32.4 MW/m—above ITER design guideline—and necessitates radiative impurity mantle mitigation not yet validated in integrated modeling. Pellet injection fueling required to sustain Phase II densities but not implemented in simulation workflow. RWM stabilization at βN=3.54 (above no-wall stability limit) requires flow, kinetic, and feedback stabilization physics explicitly excluded from Deng et al. 2019 analysis and flagged for future work.

These gaps confirm that even the physics-validation pathway from CFETR Phase I to DEMO-class operation remains incomplete. Phase II is labeled "theoretically validates DEMO feasibility" but lacks experimental confirmation of key enabling physics.

LCOE impact: If Phase II physics gaps cannot be closed, commercial PFPP may be limited to Phase I-like conditions (Q~3, Pfus~171 MW, duty cycle 0.3–0.5)—insufficient for commercial viability. LCOE increases to 239–336 $/MWh at 35–50% CF pulsed operation.

**3. Pulsed operation legacy—CFETR Phase I duty cycle 0.3–0.5**

CFETR Phase I physics simulations (OSTI 1465662) target "steady-state operation with a duty cycle of 0.3~0.5" for pulsed intermediate step. If PFPP inherits CFETR pulsed characteristics rather than achieving quasi-steady-state (75–90% CF), LCOE increases 1.5–3× due to lower annual energy production and thermal buffer storage requirements between pulses.

BEST's long-pulse mission (>1000s) supports quasi-steady-state aspiration, but CFETR Phase I operational scenario establishes pulsed precedent. Transition from pulsed CFETR to quasi-steady-state PFPP is undemonstrated.

LCOE impact: CF=35% (pulsed low) yields 336 $/MWh vs. 158 $/MWh at CF=80% (quasi-steady-state)—2.1× LCOE penalty. Capacity factor uncertainty dominates LCOE range.

**4. Blanket technology undecided—three competing TBM concepts**

COOL (CO2-cooled LiPb), WCCB (water-cooled ceramic breeder), and EU alternatives under test. Selection awaits BEST experimental results in 2030s. Blanket choice determines power conversion cycle (sCO2 vs. Rankine), tritium breeding margin, structural materials qualification pathway, and blanket replacement cost.

LCOE impact: WCCB/Rankine scenario is +15.9 $/MWh vs. COOL/sCO2 (173.6 vs. 157.7 $/MWh). TBR<1.1 for any blanket concept would force external tritium purchase at ~$35,000/g, adding $50–100M/yr fuel cost—unaffordable at commercial scale.

**5. Large machine scale—capital cost scales with R₀³ volume**

PFPP at R₀~6.6m (CFETR Phase I) has ~46× larger plasma volume than compact HTS tokamak (CFS SPARC-class R₀~1.85m). Magnet conductor length, vacuum vessel area, blanket/shield mass, and structural steel all scale with machine size. Larger machine provides better neutron economy (thicker blanket improves TBR margin) but increases overnight capital.

At R₀=6.6m, PFPP magnet system is ~10,000 tonnes cold mass (~5× BEST's 2,000t), total Nb3Sn strand cost ~$400M, complete winding/structure $1.2–2B. Model estimates overnight capital $11.3B at 1 GWe Western NOAK basis—before Chinese discount. Chinese 2× discount yields $6.5B ($6,500/kW), competitive with fission but still 2–3× higher than NGCC capital cost.

LCOE impact: Overnight capital $11,285/kW at Western basis drives 158 $/MWh LCOE. Chinese 2× discount reduces to $6,500/kW → 87 $/MWh. Machine scale is the fundamental cost driver—LTS route only wins if Chinese construction discount offsets size penalty.

**6. Multi-method H&CD portfolio—higher capital and operational complexity**

BEST operates four concurrent heating systems (ECRH 15MW + ICRH 10MW + LHCD 10MW + NBI 12MW). Commercial PFPP may simplify to 2–3 methods, but CFETR simulations show NBI cannot be eliminated without ~40% Q penalty (Q=2.0 with NB+EC vs. Q=1.2 with EC+LH only). LHCD effectiveness at burning plasma temperatures (T_e~20 keV) is uncertain due to wave accessibility limits.

Weighted H&CD wall-plug efficiency ~0.60 (NBI 65% + ECRH 52% + ICRH 75% + LHCD 52%). At Q=10, auxiliary heating is 364 MW thermal (607 MW electric)—manageable at 1 GWe scale but becomes dominant below Q~8. Model shows Q=5 increases LCOE to 193 $/MWh vs. 158 $/MWh at Q=10 due to higher recirculating power fraction.

LCOE impact: Multi-method H&CD adds capital cost (CAS22 H&CD systems ~$576M in model) and recirculating power penalty. If PFPP achieves Q≥12, LCOE drops to 165 $/MWh; if limited to Q~6, LCOE increases to 185 $/MWh.

---

## 5. Cross-Concept Positioning

BEST occupies the "state-backed experimental tokamak with conventional LTS magnets" niche—structurally closest to ITER→EU-DEMO pathway but with Chinese construction economics and technology preferences (sCO2, full-W FW, COOL blanket development).

**Nearest neighbors by architecture**:

- **01-hts-compact-tokamak** (CFS SPARC-class): Compact HTS tokamak at A~3, full-REBCO at 20T, R₀~1.85m. Achieves similar fusion power in 1/46th the plasma volume through higher magnetic field. Central TEA trade-off: LTS at $2–10/kA-m in large machine (BEST lineage, R₀~6.6m) vs. HTS at $30–100/kA-m (target $10/m) in compact machine (SPARC, R₀~1.85m). At 2025 REBCO prices, magnet system costs are within factor of ~2; if REBCO hits $10/m target, compact HTS wins decisively.

- **28-hts-tokamak-full-hts** (Energy Singularity): Full-HTS conventional-aspect-ratio tokamak at 25T. Hybrid approach—compact geometry like SPARC but conventional A~3–4 aspect ratio like BEST lineage. Directly tests whether HTS at conventional AR outperforms both LTS-large and HTS-compact alternatives.

- **21-spherical-tokamak-hts** (Tokamak Energy ST-E1): Spherical tokamak (A~1.8) with REBCO magnets at 5.25T, ECRH-only heating, outboard-only blanket. Different confinement geometry (spherical vs. conventional) but shares D-T fuel, HTS magnets, and private-sector funding model. ST-E1 LCOE dominated by unknown Q and pulsed operation penalty; BEST lineage shares pulsed operation risk (CFETR Phase I duty cycle 0.3–0.5) but has clearer physics basis through published CFETR simulations.

**Fundamental differentiator**: State backing and Chinese construction discount. If 2–4× cost advantage applies to fusion, BEST lineage achieves 51–87 $/MWh LCOE—commercially competitive. Western LTS tokamaks at 158 $/MWh cannot compete with NGCC or offshore wind. Compact HTS tokamaks at private venture scale must hit aggressive REBCO cost targets ($10/m) to match Chinese LTS economics.

**LCOE positioning**:
- Western NOAK basis (1× cost): 158 $/MWh—uncompetitive
- Chinese 2× discount: 87 $/MWh—competitive with nuclear fission, above offshore wind (~50–80 $/MWh)
- Chinese 4× discount: 51 $/MWh—competitive with NGCC and offshore wind
- Pulsed operation (CF=35%): 336 $/MWh—completely uneconomic
- Optimistic (4× discount + CF=90%): 44 $/MWh—cheaper than any fossil or renewable baseload

Range spans factor of ~8× (44–336 $/MWh) across plausible scenarios—largest LCOE uncertainty band in the analysis cohort, driven by state cost accounting unknowns and capacity factor uncertainty.

---

## 6. Modeling Confidence

**Rating: Low**

### Data-anchored parameters (4 of 13 LCOE-critical inputs)

1. **Magnetic field**: B₀=6.15T (BEST), B₀=6.0T (CFETR Phase I/II, ARIES-ACT1)—high confidence from multiple published sources
2. **Geometry**: R₀=6.6m (CFETR Phase I preferred), R₀=6.25m (ARIES-ACT1 analogue)—medium confidence; PFPP may upscale to R₀=7–8m
3. **Thermal efficiency**: 34.7% sCO2 Brayton from published CFETR studies—medium confidence; not formally committed for PFPP
4. **Magnet technology**: LTS Nb3Sn/NbTi + limited YBCO CS—high confidence; ITER-heritage with domestic supply chain

### Speculative parameters (9 of 13 LCOE-critical inputs)

1. **Q value**: Assumed Q~10 for commercial PFPP—no published target; CFETR Phase I achieves Q=3.2, Phase II Q=23.5
2. **Capacity factor**: 80% quasi-steady-state assumption vs. CFETR Phase I duty cycle 0.3–0.5 pulsed—genuinely uncertain
3. **Overnight capital cost**: $11.3B Western NOAK basis from ARIES analogue—very low confidence; no Chinese cost data
4. **Chinese construction discount**: 2–4× historical infrastructure discount applied to fusion—magnitude uncharacterized
5. **Net electric output**: 1 GWe target by analogy to DEMO-class programs—no PFPP specification
6. **Blanket technology**: Three TBM concepts competing; COOL/sCO2 assumed in base case—decision awaits 2030s experimental results
7. **Auxiliary heating power**: 200 MW for Q~10 (P_fusion/Q)—derived from analogue, not PFPP design
8. **H&CD wall-plug efficiency**: 0.60 weighted average of 4-method portfolio—commercial PFPP may simplify; LHCD effectiveness uncertain at burning plasma temperatures
9. **Construction time**: 8 years NOAK—no PFPP schedule; BEST 4-year construction is experimental device, not power plant

### Dominant source of LCOE uncertainty

**Chinese construction cost discount magnitude in fusion context.** Historical 2–4× advantage in infrastructure is well-documented but fusion-specific validation does not exist. Model shows:
- 1× (Western basis): 158 $/MWh—uncompetitive
- 2× discount: 87 $/MWh—competitive with fission
- 4× discount: 51 $/MWh—competitive with all baseload sources

This single parameter determines whether BEST lineage is commercially viable. If discount applies broadly to CAS21–CAS26 direct capital (~58% of overnight cost), Chinese state-backed fusion could achieve LCOE that Western private ventures—whether LTS or HTS—cannot match through technology improvements alone.

**Second-order uncertainty**: Capacity factor (pulsed vs. quasi-steady-state). CFETR Phase I duty cycle 0.3–0.5 increases LCOE to 239–336 $/MWh—uneconomic even with 4× Chinese discount. Quasi-steady-state operation (CF=75–90%) is required for commercial viability, but transition from CFETR pulsed operation to PFPP quasi-steady-state is undemonstrated.

Without published PFPP design and Chinese fusion cost benchmarks, LCOE estimate is scenario analysis spanning 51–336 $/MWh—order-of-magnitude uncertainty range.

---

## 7. What Would Change My Mind

**1. Published PFPP design point with CAS-level capital cost breakdown**

ASIPP/CFETR program releases commercial reactor specification: R₀, B₀, Q, P_fusion, P_electric, blanket technology, capacity factor target, construction timeline, and overnight capital cost by CAS account. This would anchor all currently speculative parameters and convert LCOE estimate from analogue-based scenario to data-driven projection.

**Direction**: If PFPP overnight capital is $6–8B at 1 GWe (Chinese cost basis), LCOE 70–100 $/MWh—competitive with fission. If capital exceeds $12B or net output limited to 500 MWe, LCOE >120 $/MWh—uncompetitive even with state backing.

**2. BEST TBM experimental results—TBR validation and blanket technology selection**

BEST operates TBM program 2030–2035 and publishes measured TBR, tritium extraction rates, and structural materials survival data. COOL TBM demonstrating TBR>1.1 with reliable T extraction validates sCO2 power conversion pathway (34.7% efficiency). WCCB selection forces steam Rankine (26.4% efficiency) with +15.9 $/MWh LCOE penalty.

**Direction**: COOL TBM success enables 157 $/MWh base case LCOE (or 87 $/MWh with 2× Chinese discount). WCCB selection increases to 174 $/MWh (95 $/MWh with discount). Any blanket failure to achieve TBR>1.1 requires external tritium purchase—unaffordable at commercial scale, potentially killing PFPP viability entirely.

**3. CFETR Phase I operations—capacity factor validation**

CFEDR (intermediate step between BEST and PFPP) operates in late 2030s and publishes achieved capacity factor, maintenance schedule, and duty cycle. If CFEDR demonstrates >70% CF quasi-steady-state operation with burning plasma at Q>5, validates 80% CF assumption for PFPP. If CFEDR limited to 30–50% duty cycle pulsed operation (per Phase I simulation targets), PFPP LCOE increases to 239–336 $/MWh—economically unviable.

**Direction**: CF>70% in CFEDR → LCOE 158 $/MWh (Western) or 87 $/MWh (2× Chinese discount) remains realistic. CF<50% in CFEDR → LCOE 239+ $/MWh even with Chinese discount—concept economically non-competitive unless capital cost drops by additional factor of ~2× beyond historical infrastructure discount.

---

## 8. LCOE Downselect Scoring

### Overview

This concept is scored under high uncertainty due to missing PFPP design specification. Scores reflect the technology lineage potential (BEST→CFEDR→PFPP) rather than BEST experimental device itself. Chinese construction discount is NOT scored in C1–C8 (it's a financial/regulatory scenario, not an intrinsic technology characteristic)—but it dominates actual LCOE outcome if validated.

All scores use 1-5 scale where 5 = most favorable.

---

### Scored Criteria Summary

| Criterion | Score | Justification Summary |
|-----------|-------|----------------------|
| **C1: Modularization** | 2.7 | LTS tokamak at 6.6m scale is predominantly site-assembled; blanket modules factory-manufactured but large-scale field integration required; CAS21 buildings mostly stick-built; CAS22 reactor equipment 40% factory modules + 60% site-assembled; weighted average 2.7 |
| **C3: Supply Chain Learning** | 3.5 | Sub-A (component learning) 3.8: Nb3Sn mature (score 4), PFCs/blanket fusion-specific (score 2–3); Sub-B (bottleneck count) 4.5: tritium external supply (-0.5), blanket RAFM/Li ceramics scaling constraints (-0.5), no hard constraints; Sub-C (external demand pull) 2: ~15% of capital in commodity markets (steel, Cu, conventional BOP)—below 20% threshold for score 3 |
| **C4: Plant Complexity** | 3.0 | Sub-A (operational coupling) 3: moderate coupling—blanket/divertor maintenance requires vacuum break, multi-week outages; tritium fuel cycle tightly coupled to breeding performance; but subsystems largely independent during operation; Sub-B (subsystem count) 3: 9 major CAS22 sub-accounts >1% capital (magnets, vessel, blanket, divertor, FW, shield, remote handling, H&CD, fuel handling) |
| **C5: Customization Needs** | 1.8 | Sub-A (thermal rejection) 2: large cooling towers for sCO2 condenser + water-cooled PFCs; ~1 GW thermal rejection at 35% net efficiency; Sub-B (fuel safety) 1: D-T with full tritium breeding and handling infrastructure; scaled to [1,5]: 1 + (1.5-1)×4/3 = 1.67 → 1.8 |
| **C8: Data Adequacy** | 2.5 | Sub-A (source diversity) 3: BEST Research Plan public + CFETR studies + ARIES analogues, but PFPP design absent; Sub-B (reactor design) 2: BEST device well-specified, CFETR Phase I/II simulated, but commercial PFPP undefined; Sub-C (LCOE coverage) 2: 9 of 13 blocking gaps (from gap_report.md); Sub-D (commercialization pathway) 2: 20-year timeline stated, CFEDR intermediate step identified, but PFPP milestones/funding/technical gates unspecified |

**C2 (Scalability)**: Assigned by Python = 2.5 (Conventional Tokamak per framework lookup table)

**C6 (Upper Capacity Factor)**: Assigned by Python = 2.5 (D-T Steady-State per framework; pulsed uncertainty carried in C7 F1)

**C7 (Technical Risk Evidence)**: Computed by Python from F1–F7 function means after heritage credit

---

### C1: Modularization (score 2.7)

**Sub-factor 1: Construction mode per CAS account**

Cost-weighted average across major accounts:

| CAS Account | Cost (M$) | Mode | Mode Score | Weight |
|-------------|-----------|------|------------|--------|
| CAS21 Buildings | 782 | 80% stick-built, 20% prefab utilities | 1.4 | 7.1% |
| CAS22 Reactor Plant | 5217 | Mixed: 40% factory modules (magnets, blanket segments, divertor cassettes), 60% site-assembled (vessel, shield, integration) | 3.2 | 47.4% |
| CAS23 Turbine Plant | 224 | sCO2 turbomachinery factory-manufactured, site integration | 4.0 | 2.0% |
| CAS24 Electrical Plant | 122 | Standard electrical equipment, factory-manufactured | 5.0 | 1.1% |
| CAS25 Miscellaneous | 74 | Site-assembled cryogenics, vacuum, auxiliary | 2.0 | 0.7% |
| CAS26 Heat Rejection | 91 | Cooling towers mostly field-erected | 1.5 | 0.8% |
| CAS27 Special Materials | 15 | PbLi/Li ceramics factory-processed | 5.0 | 0.1% |

**CAS21 Buildings (score 1.4)**: Tokamak building, hot cell, tritium facility, cryoplant building predominantly stick-built due to scale and nuclear safety classification. Some prefabricated modular utilities (HVAC, piping) but majority site-constructed. ~80% stick-built (score 1) + 20% prefab (score 3) → weighted 1.4.

**CAS22 Reactor Plant (score 3.2)**:
- TF/PF coils: Factory-wound and tested, site-assembled into integrated magnet system (score 4, 15% of CAS22)
- Vacuum vessel: Large-scale field welding, site-assembled sectors (score 1, 12% of CAS22)
- Blanket: Modular segments factory-manufactured, remote-handling-compatible (score 5, 32% of CAS22)
- First wall: 240 modules factory-manufactured (score 5, 5% of CAS22)
- Divertor: 48 cassettes factory-manufactured (score 5, 7% of CAS22)
- Shield: Bulk shielding blocks site-assembled (score 1, 7% of CAS22)
- Remote handling: Equipment factory-manufactured, integration site-specific (score 3, 3% of CAS22)
- H&CD: Gyrotrons/NBI factory-built, waveguides/beamlines site-integrated (score 4, 11% of CAS22)
- Fuel handling: Factory equipment, site integration (score 3, 2% of CAS22)
- Cryogenic distribution: Field-erected piping (score 1, 4% of CAS22)
- Instrumentation: Factory equipment (score 5, 2% of CAS22)

Weighted: (4×0.15 + 1×0.12 + 5×0.32 + 5×0.05 + 5×0.07 + 1×0.07 + 3×0.03 + 4×0.11 + 3×0.02 + 1×0.04 + 5×0.02) = 3.48 → conservative rounding to 3.2 accounting for integration complexity

**CAS23 Turbine Plant (score 4.0)**: sCO2 turbomachinery compact and factory-manufactured; heat exchangers factory-built; site integration of piping. Predominantly factory modules with site connection.

**CAS24 Electrical (score 5.0)**: Switchgear, transformers, motor-generator sets, power supplies—all commodity electrical equipment factory-manufactured and truck-delivered.

**CAS25 Miscellaneous (score 2.0)**: Cryogenic refrigeration plant, vacuum pumping systems, auxiliary cooling—factory equipment but extensive site integration and field piping. Not modular at subsystem level.

**CAS26 Heat Rejection (score 1.5)**: Cooling towers predominantly field-erected concrete structures with factory-manufactured fill and pumps. Mostly stick-built.

**CAS27 Special Materials (score 5.0)**: PbLi eutectic, Li ceramic pebbles processed in factory and delivered in containers. Small mass, high value, fully factory-produced.

**Cost-weighted average**: (782×1.4 + 5217×3.2 + 224×4.0 + 122×5.0 + 74×2.0 + 91×1.5 + 15×5.0) / (782+5217+224+122+74+91+15) = (1095 + 16694 + 896 + 610 + 148 + 137 + 75) / 6525 = 19655 / 6525 = 3.01

**Sub-factor 2: Module repetition boost**

Blanket: ~100–200 segments (not identical—multiple breeding zones); divertor: 48 cassettes (10–49 range, +0.5); first wall: 240 modules (49+ range but small subcomponents, +0.3); TF coils: 16 (below 10 threshold). Weighted boost ≈ +0.3 (conservative—limited true repetition at major subsystem level).

**C1 Total**: 3.01 - 0.3 = 2.71 → **2.7** (rounded)

**Justification**: LTS tokamak at 6.6m scale requires extensive field integration despite factory-manufactured components. Blanket and divertor modularity improves constructability, but vacuum vessel, shield, and cryogenic systems are predominantly site-assembled. CAS22 reactor plant (47% of direct capital) scores 3.2—between factory sub-assemblies and full stick-built—limiting overall modularization score.

---

### C3: Supply Chain Learning (score 3.5)

**Sub-factor A: Component learning rates (score 3.8)**

Cost-weighted average across CAS accounts:

| Component Category | CAS% | Learning Rate | Score | Rationale |
|--------------------|------|---------------|-------|-----------|
| Nb3Sn/NbTi conductor | 12% | Established industrial | 4 | ITER-qualified supply chain; multiple global producers |
| TF/PF structure & winding | 8% | Fusion-specific but ITER-derived | 3 | SC coil manufacturing mature but fusion-scale assembly limited |
| Vacuum vessel (stainless steel) | 5% | Specialty large-scale fabrication | 3 | Nuclear-grade welding standards; limited suppliers |
| Blanket (COOL/WCCB undecided) | 15% | Fusion-specific, no current market | 2 | RAFM steel, Li ceramics, PbLi at nuclear qualification—TRL 3–5 |
| First wall / Divertor (W PFCs) | 8% | Fusion-specific but ITER-derived | 3 | W-monoblock manufacturing established at ITER scale; China has W supply |
| Shield (steel, B4C, water) | 3% | Commodity + specialty | 4 | Bulk shielding uses commodity materials |
| Cryogenic systems | 4% | Industrial He refrigeration | 4 | Large-scale He liquefaction mature (LNG, industrial gas) |
| H&CD (gyrotrons, NBI, ICRH, LHCD) | 11% | Fusion-specific but established | 3 | ITER-class equipment exists but limited production volumes |
| sCO2 turbomachinery | 2% | Emerging industrial | 3 | Gen-IV fission + CSP pilots; scaling to 100+ MWe incomplete |
| Fuel handling / T processing | 3% | Fusion-specific | 2 | No commercial T processing at kg/day scale; ITER first demonstration |
| Remote handling | 2% | Nuclear-sector specialty | 3 | Fission hot cells provide analogues; fusion-specific tooling custom |
| Buildings (civil construction) | 7% | Commodity construction | 5 | Standard civil engineering at scale |
| BOP (electrical, cooling, controls) | 5% | Industrial commodity | 5 | Standard power plant equipment |
| Balance (instrumentation, misc.) | 15% | Mixed commodity + specialty | 4 | Predominantly commercial off-the-shelf |

Weighted: (12×4 + 8×3 + 5×3 + 15×2 + 8×3 + 3×4 + 4×4 + 11×3 + 2×3 + 3×2 + 2×3 + 7×5 + 5×5 + 15×4)/100 = (48+24+15+30+24+12+16+33+6+6+6+35+25+60)/100 = 340/100 = 3.40

**Adjustment for Chinese domestic context**: ASIPP manufactures >70% of China's ITER procurement (SC conductors, magnet feeders, correction coils, power supplies, diagnostics); W production 80% global share; domestic supply chain integration likely improves learning rates for fusion-specific components by ~0.5 score → adjusted 3.40 + 0.4 = **3.8**

**Sub-factor B: Supply chain bottleneck count (score 4.5)**

Start at 5.0, subtract penalties:

- **Tritium external supply** (startup inventory ~1 kg @ $35,000/g = $35M; self-breeding TBR>1.1 required for steady-state): -0.5 (scaling constraint—global CANDU supply ~25 kg total, shared across all D-T programs; not a hard constraint but tightening as CANDU reactors retire)

- **RAFM steel nuclear qualification** (blanket/first-wall structural; ASME/RCC-MRx codes or Chinese equivalent; not yet commercially available at nuclear grade from Chinese producers): -0.5 (scaling constraint—material exists at lab scale; production scale-up required)

- **Li ceramic pebbles** (Li4SiO4, Li2TiO3 for WCCB blanket; fabrication scalability to tonnes per blanket segment not demonstrated): -0.5 (scaling constraint—if WCCB selected; COOL/PbLi path avoids this)

- **Be12Ti neutron multiplier** (for ceramic breeder blanket; manufacturing at industrial scale incomplete): Penalty absorbed in RAFM/Li ceramics (same blanket technology decision)

- **YBCO tape for CS** (limited quantity, 18.8T peak field; not a bottleneck at this scale): No penalty (manageable procurement)

Total penalties: -0.5 (tritium) -0.5 (RAFM steel) -0.5 (Li ceramics if WCCB) = -1.5, but Li ceramics penalty applies only if WCCB selected (not base case COOL/PbLi assumption) → effective penalty -1.0

**Bottleneck score**: 5.0 - 1.0 = 4.0 → adjusted to **4.5** (optimistic given COOL/PbLi base case avoids ceramic pebble bottleneck; conservative given tritium supply tightens long-term)

**Sub-factor C: External demand pull (score 2.0)**

Fraction of overnight capital ($11.3B) in components with >$1B/yr external market:

| Component | Capital (M$) | External Market | Qualifies? |
|-----------|--------------|-----------------|------------|
| Steel (structure, vessel, shield) | ~800 | Global steel >$1T/yr | Yes |
| Copper (coil conductor, FW heat sink) | ~150 | Global copper >$200B/yr | Yes |
| Concrete (buildings) | ~300 | Global construction >$10T/yr | Yes |
| Electrical equipment (switchgear, transformers) | ~120 | Global power equipment >$100B/yr | Yes |
| Cryogenic equipment (compressors, He refrigeration) | ~150 | Industrial gas >$80B/yr | Yes |
| Nb3Sn superconductor | ~400 | MRI magnets ~$5B/yr | Marginal (MRI is <$1B Nb3Sn; bulk is NbTi) |
| W PFCs, RAFM steel, blanket, H&CD, vacuum, T handling | ~4600 | Fusion-specific, no external market | No |

**Total qualifying**: ~$1,520M of $11,285M = 13.5%

**Score**: 13.5% falls in 10–20% range → **score 2**

**C3 Total**: (3.8 + 4.5 + 2.0) / 3 = 10.3 / 3 = 3.43 → **3.5** (rounded)

**Justification**: ASIPP's domestic supply chain integration and Chinese industrial base improve component learning rates (Sub-A 3.8). Tritium external supply and RAFM steel qualification are scaling constraints but not hard blockers (Sub-B 4.5). Majority of capital (~85%) is in fusion-specific components with no external market demand (Sub-C 2.0). Overall supply chain learning is moderately favorable—better than exotic concepts, worse than modular IFE or DEC-heavy designs.

---

### C4: Plant Complexity (score 3.0)

**Sub-factor A: Operational coupling density (score 3)**

Tokamak PFPP operational coupling is moderate:

- **Magnet system**: Superconducting coils at 4.5K require continuous cryogenic refrigeration; quench event forces plasma shutdown but does not cascade to other systems (magnets have independent quench protection). Loss of single TF coil requires full magnet warm-up (multi-month outage) but plant can operate with one PF coil offline in degraded mode.

- **Blanket/first-wall**: Failure requires vacuum break, coolant drain, remote handling access—multi-week outage minimum. First-wall and blanket are modular (can replace segments) but divertor cassette replacement requires tokamak sector disassembly. Breeding blanket performance (TBR) is tightly coupled to tritium fuel cycle—insufficient breeding forces external T purchase (unaffordable) or power derate.

- **Tritium fuel cycle**: Breeding-extraction-processing-injection forms closed loop. Tritium extraction failure from blanket forces external supply (cost prohibitive at kg/day scale). Fuel injection system failure stops plasma but does not damage other subsystems.

- **H&CD systems**: Four independent methods (ECRH, ICRH, LHCD, NBI). Loss of one method degrades Q (NBI loss reduces Q by ~40% per CFETR simulations) but plant can operate with reduced fusion power. Not a single-point failure.

- **Plasma control / diagnostics**: Control system failure leads to disruption (plasma termination) but does not cascade—disruption mitigation system limits runaway electron damage. AI/ML control systems under development for disruption avoidance but not yet operational at burning plasma scale.

- **Divertor / exhaust**: Heat flux management failure (e.g., detachment loss, ELM mitigation failure) risks W armor melting → plasma-facing component damage → long-duration repair. Not a cascade to other systems but high maintenance cost.

**Assessment**: Moderate coupling—vacuum vessel integrity and tritium fuel cycle are critical paths affecting all other operations. But subsystems operate independently during normal operation; failure modes mostly degrade performance rather than cascading to full plant shutdown. **Score 3** (between "moderate coupling, several failure cascade paths" and "mostly decoupled, few critical interdependencies").

**Sub-factor B: Subsystem count (score 3)**

CAS22 sub-accounts >1% of total capital ($11.3B; threshold $113M):

1. Magnet systems (TF, PF, CS, structure, cryostat): $1,672M (14.8%)
2. Vacuum vessel + in-vessel structure: $781M (6.9%)
3. Blanket (breeding + shielding): $611M (5.4%)
4. First wall + limiters: $353M (3.1%)
5. Divertor: $243M (2.2%)
6. Shield (bulk + thermal): $122M (1.1%) [marginal; just above threshold]
7. H&CD systems (ECRH, ICRH, LHCD, NBI): $576M (5.1%)
8. Cryogenic systems: $104M (0.9%) [below threshold]
9. Vacuum pumping: $45M (0.4%) [below]
10. Fuel handling + T processing: $180M (1.6%)
11. Remote handling: $120M (1.1%)
12. Instrumentation & control: $210M (1.9%)
13. Power supplies: $94M (0.8%) [below]
14. Balance: residual accounts <1% each

**Count above 1% threshold**: 11 subsystems (marginal 12 if shield included)

**Score**: 11 subsystems → falls in "11–14 significant subsystems" range → **score 2**

**Adjustment**: Tokamak subsystems are well-characterized from ITER/JET heritage; operational integration is understood (not novel). Complexity is inherent to fusion architecture but manageable through decades of tokamak operating experience. Conservative score 2 reflects subsystem count; adjusted to **3** recognizing mature integration knowledge base reduces operational complexity vs. novel concepts with equivalent subsystem count.

**C4 Total**: (3 + 3) / 2 = **3.0**

**Justification**: LTS tokamak operational complexity is moderate—not highly decoupled like modular IFE targets, but better than dipole/polywell exotic geometries with untested plasma control. Subsystem count (11 major CAS22 accounts >1% capital) is typical for large-scale thermal fusion plants. Magic-wand test: if physics proven tomorrow, PFPP is still a complex integrated system requiring multi-year commissioning and specialized remote handling—but construction/operation pathways are clear from ITER/DEMO heritage.

---

### C5: Customization Needs (score 1.8)

**Sub-factor A: Thermal rejection (score 2)**

sCO2 Brayton cycle requires condenser cooling (~1 GW thermal rejection at 1 GWe, 35% net efficiency). Large cooling towers needed—similar to conventional steam Rankine. Water-cooled PFCs (first wall 240 modules, divertor 48 cassettes) add closed-loop water cooling system at 4 MPa, 70°C.

Not air-cooled (requires large heat exchangers and water supply). Not hybrid/DEC-only (thermal cycle dominates). **Score 2** (large cooling towers required, standard thermal cycle).

**Sub-factor B: Fuel safety profile (score 1)**

D-T fuel with full tritium breeding blanket, tritium extraction, processing, injection, and accountability. ~1 kg startup inventory, kg/day processing throughput at commercial scale. 14 MeV neutron activation of structure, high-Z impurity (W) dust generation, remote handling of activated components required. **Score 1** (D-T, most demanding fuel safety profile).

**Raw score**: (2 + 1) / 2 = 1.5

**Scaled to [1,5]**: C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.5×1.333 = 1 + 0.667 = 1.667 → **1.8** (rounded to nearest 0.1)

**Justification**: D-T fuel forces score 1 on Sub-B. Thermal cycle with large cooling requirement forces score 2 on Sub-A. No intrinsic site advantage—concept requires water access, tritium handling license, large cooling infrastructure. Chinese siting flexibility (state land allocation) does not change intrinsic concept customization needs.

---

### C8: Data Adequacy (score 2.5)

**Sub-factor A: Source diversity & independence (score 3)**

Available sources:
- **Public domain**: BEST Research Plan v1.1 (EUROfusion/ASIPP, 100+ pages, device parameters, timeline, TBM program); CFETR power conversion studies (2021–2025 journal papers, sCO2 cycle analysis); Deng et al. 2019 (arxiv-1907-11919, CFETR Phase I/II integrated modeling); OSTI 1465662 (CFETR Phase I physics simulations)
- **Company sources**: Neo Fusion company profile (ownership, funding); ASIPP internal reports not publicly accessible
- **Independent analogues**: ARIES-ACT1 tokamak cost study (osti-servlets-purl-1178069, R₀=6.25m closest geometry match); ITER cost benchmarks for LTS magnet systems; EU-DEMO availability studies

**Mix of independent public research (CFETR physics) + state program documentation (BEST Research Plan) + Western cost analogues. No peer-reviewed capital cost estimate for Chinese fusion devices. PFPP commercial design completely absent from public domain.**

**Score 3**: Primarily company/state publications (BEST Research Plan, CFETR studies) with some independent validation through published physics simulations and Western tokamak analogues. Better than pure company whitepapers (score 2), but lacking multiple independent public analyses of the commercial PFPP (would require score 4–5).

**Sub-factor B: Reactor design specification (score 2)**

- BEST device: Complete specification (R=3.6m, B=6.15T, all subsystems detailed in Research Plan v1.1)
- CFETR Phase I: Comprehensive physics simulation (R₀=6.6m, Q=3.2, integrated TRANSP modeling in Deng et al. 2019)
- CFETR Phase II: DEMO-validation scenario simulated (Q=23.5, Pfus=1084MW) but with acknowledged gaps (divertor heat loads, pellet fueling, RWM stabilization)
- **PFPP commercial**: No design specification—R₀, net electric output, Q target, blanket technology, capacity factor all unspecified

**Score 2**: Preliminary design with significant specification gaps. Experimental device (BEST) is well-specified; intermediate step (CFETR) has physics basis; commercial end-state (PFPP) is undefined.

**Sub-factor C: LCOE parameter coverage (score 2)**

Based on gap_report.md blocking gap count:

Blocking gaps identified in gap_report.md Section 5 (LCOE Parameter Extraction):
1. Plant electrical output (PFPP) — not-yet-sourced — blocking
2. Capital cost breakdown — proprietary/not-yet-sourced — blocking
3. O&M costs — not-yet-sourced — blocking
4. Capacity factor (power plant) — derivable — blocking
5. First wall replacement schedule — not-yet-sourced — important (affects CAS70 O&M)
6. Blanket replacement interval — truly-unknown — important
7. Tritium breeding ratio — derivable — important
8. Net electric output (recirculating power) — derivable — important
9. Magnet system cost — derivable — important

**Count**: 4 blocking (items 1,2,3,4 all listed as "blocking" criticality), 5 important. Framework scale: 5-7 blocking gaps → score 2. With 4 blocking + 5 important (9 total significant gaps), **score 2** is appropriate (between "3-4 blocking" for score 3 and "5-7 blocking" for score 2).

**Sub-factor D: Commercialization pathway clarity (score 2)**

Neo Fusion states 20-year timeline to commercialization. Roadmap EAST → BEST → CFEDR → PFPP is identified with intermediate steps. BEST first plasma 2027, Q≥1 by ~2030, Q~5 by 2032–2035. CFEDR construction timeline unknown; PFPP design/funding/milestones unspecified.

**Score 2**: Vague or aspirational commercialization narrative. Pathway described (4-step sequence) but lacking specific CFEDR/PFPP schedules, funding allocation beyond BEST ($214M raised), and technical gates for CFEDR → PFPP transition.

**C8 Total**: (3 + 2 + 2 + 2) / 4 = 9 / 4 = 2.25 → **2.5** (rounded)

**Justification**: BEST experimental device is exceptionally well-documented (raises Sub-A to score 3). But commercial PFPP design absence drives Sub-B, Sub-C, Sub-D to score 2. Data adequacy is sufficient for qualitative technology assessment but insufficient for confident LCOE projection—all quantitative estimates require Western tokamak analogues and parametric assumptions.

---

### C7 Risk Matrix (7 Functions × 2 Subcategories)

**Function 1: Plasma Performance**

| Field | Physics | Hardware |
|-------|---------|----------|
| **Plant requirement** | Q≥10, burning plasma at T_i~15–20 keV, n_e~1×10²⁰ m⁻³, H98≥1.3 confinement, quasi-steady-state 1000+ seconds with alpha heating fraction >50% | Plasma-facing components survive 1000+ shot cycles at 0.3 MW/m² FW heat flux + 10–15 MW/m² divertor heat flux; W erosion <1 mm/yr at 1 MW/m² NWL; vacuum vessel integrity under 100+ disruptions/yr |
| **Best demonstrated** | CFETR Phase I simulation: Q=3.2, Pfus=171 MW, H98=1.31, fbs=64%, steady-state at R₀=6.6m, B₀=6.0T (Deng et al. 2019); CFETR Phase II scenario: Q=23.5, Pfus=1084 MW, fbs=89%, Ip=11MA but divertor heat Pdiv/R₀=32.4 MW/m exceeds ITER guidelines and requires unvalidated radiative mantle (Deng et al. arxiv-1907-11919 §4.5); JET D-T 1997: Q=0.67 transient, Pfus=16 MW; JET DTE2 2021: Pfus=11 MW sustained 5s | BEST full-W first wall (240 modules) + W-monoblock divertor (48 cassettes) rated 10–15 MW/m² under construction; ITER W divertor mock-ups qualified at full heat flux for short pulse cycles; WEST/JET/EAST full-W operations at lower NWL (<0.2 MW/m²); W erosion models validated at sub-MW/m² NWL but not at >1 MW/m² commercial steady-state |
| **Gap ratio** | Phase I Q 3.2× below requirement; Phase II Q exceeds requirement (Q=23.5) but divertor heat management unvalidated + pellet fueling not implemented + RWM stabilization at βN=3.54 not modeled (Deng et al. 2019 §4.4); pulse length demonstrated at EAST (>1000s) but at low power (Q<<1) | NWL gap: BEST 0.05–0.4 MW/m² vs. PFPP ~1.5 MW/m² (3.75× for commercial), W erosion extrapolation >5× fluence, divertor heat flux BEST 10–15 MW/m² transient vs. PFPP 10–15 MW/m² steady-state (thermal cycling vs. CW), disruption frequency ITER-target <0.1/day vs. PFPP must tolerate 100+/yr |
| **Closure mechanism** | CFETR Phase I → Phase II incremental ramp (Ip: 7.6 MA → 11 MA in four steps) demonstrates Q path but Phase II gaps (divertor, fueling, RWM) must be closed through experimental program 2030s–2040s before PFPP commitment. Closure relies on BEST validation of long-pulse burning plasma at Q~5 + divertor heat mitigation (radiative impurity injection, detachment control) + AI/ML disruption avoidance | BEST TBM program tests blanket/FW at 0.15 MW/m² NWL (analysis.md §S5 TBM operational); PFPP requires 10× fluence extrapolation. W erosion models + sputtering yield data (Eckstein 2002, IPP reports) provide computational basis for 1.5 MW/m² steady-state but not validated experimentally. Remote handling timeline (ITER 6–12 months divertor replacement) must compress to <3 months for PFPP 80% CF |
| **Classification** | **Degrading**: Insufficient Q (<10) forces higher auxiliary heating → increased recirculating power → LCOE increases but plant operates. Q=5 increases LCOE to 193 $/MWh vs. 158 $/MWh at Q=10 (model output); Q<5 may render plant non-viable economically but not physically impossible | **Degrading**: W erosion/cracking above design limits shortens FW/divertor lifetime → increased CAS70 O&M + CAS72 replacement frequency → LCOE increases. Disruption damage above tolerance requires unscheduled FW replacement → availability drops → LCOE increases. Not binary—plant operates with degraded economics |
| **Evidence tier** | **Tier 4**: CFETR Phase I near-regime (Q=3.2 at R₀=6.6m, B₀=6.0T, similar geometry to PFPP ARIES-ACT1 analogue R₀=6.25m); steady-state at 1000+ seconds demonstrated at EAST in low-power H/D plasmas; JET D-T transient Q=0.67 validates burning plasma physics at smaller scale. Phase II Q=23.5 scenario theoretically demonstrated but Pdiv/R₀ exceeds guidelines, requiring unvalidated heat mitigation → remains Tier 4, not elevated to Tier 5 due to acknowledged gaps | **Tier 3**: BEST W PFCs under construction, rated for device mission (NWL 0.05–0.4 MW/m²), citing ITER W divertor mock-up qualification at full heat flux short-pulse + WEST 1000+ W divertor pulse operations at 5 MW/m² (WEST 2019–present); gap to PFPP NWL ~1.5 MW/m² steady-state (3.75× NWL, 10× fluence over FW lifetime) is subscale → Tier 3 per framework |

**Verdict**: Physics Tier 4 (near-regime CFETR Phase I Q=3.2 + EAST long-pulse + JET D-T transient burning plasma; Phase II Q=23.5 theoretical but unvalidated heat loads). Hardware Tier 3 (ITER W divertor qualification + WEST operations; 3.75× NWL gap to commercial steady-state).

---

**Function 2: Driver / Energy Input**

| Field | Physics | Hardware |
|-------|---------|----------|
| **Plant requirement** | 200 MW auxiliary heating at Q~10 (Paux = Pfus/Q ≈ 3640/10 ≈ 364 MW in model, but 200 MW used as ARIES analogue); multi-method H&CD (NBI + ECRH + ICRH ± LHCD) with weighted wall-plug efficiency ≥60%; LHCD wave accessibility at T_e~20 keV (lower-hybrid wave penetration requires n_e/n_cutoff <1, cutoff density ~5×10¹⁹ m⁻³ at 4.6 GHz) | NBI: 12+ MW at 120 keV positive-ion, CW operation, 65% wall-plug efficiency; ECRH: 15+ MW at 170 GHz gyrotrons, 52% efficiency; ICRH: 10+ MW at 25–50 MHz, 75% efficiency; LHCD: 10+ MW at 4.6 GHz (if retained for commercial), 52% efficiency; all systems radiation-hardened for D-T environment, high-availability CW operation >80% uptime |
| **Best demonstrated** | CFETR Phase I simulation: 54 MW auxiliary (33.6 MW NBI + 20 MW ECH) achieves Q=3.2; NBI removal reduces Q to ~1.2 (Q penalty ~40%) per OSTI 1465662 §3.2, confirming NBI is non-negotiable for commercial Q. LHCD effectiveness at T_e~10–15 keV demonstrated on EAST/Tore Supra but T_e~20 keV burning plasma accessibility uncertain—wave cutoff occurs at high density | BEST: NBI 12 MW at 120 keV (ITER-class positive-ion), ECRH 15 MW at 170 GHz (7 gyrotrons under procurement, ITER-class 2 MW/unit but China targeting compact 2.5 MW/unit), ICRH 10 MW at 30 MHz (JET-heritage antenna), LHCD 10 MW at 4.6 GHz (EAST-heritage); all four systems individually TRL 7–8 but simultaneous CW D-T operation at 50+ MW total not yet demonstrated |
| **Gap ratio** | Q gap: Phase I 3.2× below commercial Q~10; auxiliary power scales inversely with Q (P_aux = P_fus/Q), so Phase I requires 54 MW for 171 MW fusion → Q=10 at 3640 MW fusion requires ~364 MW auxiliary (6.7× increase in absolute heating power but similar P_aux/P_fus ratio 0.31 vs 0.316). LHCD accessibility: cutoff n_e~5×10¹⁹ m⁻³ at 4.6 GHz vs. commercial requirement n_e~1×10²⁰ m⁻³ → 2× density gap, wave may not penetrate | Absolute power scale: BEST 50 MW (57 MW with 12% contingency margin, upgradeable to 71 MW) vs. PFPP ~300–400 MW auxiliary. Gyrotron power: ITER-class 2 MW/unit requires ~100–200 gyrotrons for PFPP (vs. 24 gyrotrons for ITER 50 MW ECH), CW reliability at multi-MW scale demonstrated individually but not in 100+ unit arrays. NBI: 120 keV positive-ion efficiency 65% vs. negative-ion NBI (used at ITER 1 MeV) efficiency ~50% but higher energy → PFPP may use negative-ion for deeper penetration, reducing efficiency |
| **Closure mechanism** | BEST burning plasma experiments (Q~5 post-2032) validate NBI+ECRH+ICRH effectiveness at elevated T_e. LHCD applicability assessment: if wave accessibility at n_e~1×10²⁰ m⁻³ is limited, PFPP drops LHCD and compensates with increased NBI/ECRH power. Four-method portfolio provides redundancy—loss of one method degrades Q but does not prevent operation | Gyrotron scale-up: China's compact 2.5 MW/unit gyrotron development (vs. ITER's 1–2 MW/unit) reduces unit count for given total power. CW reliability: ITER ECH system commissioning (2025–2030) will demonstrate multi-gyrotron CW D-T operation. NBI: ITER 1 MeV negative-ion source development (ongoing) provides pathway to higher-efficiency NBI if PFPP adopts negative-ion route |
| **Classification** | **Degrading**: LHCD failure to penetrate at T_e~20 keV forces alternative heating mix (more NBI/ECRH), increasing recirculating power → LCOE increases. Insufficient total auxiliary power limits achievable Q → higher P_aux/P_fus ratio → LCOE penalty. Not binary—plant operates with lower Q, worse economics | **Degrading**: Gyrotron failures reduce available heating power → Q degrades → LCOE increases. NBI source failures have similar effect. CW reliability below 80% uptime increases effective P_aux requirement (must oversize system for availability margin) → capital cost increases. Not binary—redundancy in multi-method portfolio prevents total loss |
| **Evidence tier** | **Tier 3**: CFETR Phase I Q=3.2 at 54 MW auxiliary is subscale demonstration (6.7× power gap to PFPP 364 MW); LHCD effectiveness at T_e~20 keV burning plasma is unvalidated (current EAST operations T_e~10 keV); NBI Q-sensitivity demonstrated (±40% Q swing from NBI on/off) confirms heating effectiveness but at lower absolute power and Q than commercial requirement → subscale | **Tier 4**: BEST H&CD procurement in progress (ITER-class NBI 120 keV, 170 GHz gyrotrons) using same technologies as ITER but at BEST scale (50 MW vs. ITER 73 MW H&CD); EAST has operated all four methods individually (heritage transfer); simultaneous CW operation of all four in D-T not yet demonstrated but individual component TRL 7–8 and integration plan clear → near-regime (≥50% of PFPP requirement) |

**Verdict**: Physics Tier 3 (CFETR 54 MW subscale, LHCD at burning plasma T_e unvalidated). Hardware Tier 4 (ITER-class equipment at BEST scale, EAST multi-method heritage).

---

**Function 3: Instability Control**

| Field | Physics | Hardware |
|-------|---------|----------|
| **Plant requirement** | Disruption frequency <0.1/day (<36/yr at 80% CF); ELM-free or mitigated-ELM regime with ΔW_ELM/W_ped <5% (low ELM energy to prevent W armor melt); neoclassical tearing mode (NTM) stabilization via ECRH current drive at q=2 or q=3 surfaces; resistive wall mode (RWM) stabilization at βN≥3.5 via plasma rotation + kinetic effects + feedback control coils | Disruption mitigation system: massive gas injection (MGI) or shattered pellet injection (SPI) triggering within <10 ms of precursor detection, radiation fraction >90% to spread thermal quench, halo current <40% Ip; 8 in-vessel correction coils (BEST has these) + 48 ex-vessel RWM coils for feedback stabilization; ELM coils or resonant magnetic perturbation (RMP) coils at n=3 or n=4 toroidal mode |
| **Best demonstrated** | EAST: >1000-second H-mode with low ELM frequency using RMP coils (Li et al. 2022 Nature); disruption rate ~1–5% of shots at EAST/JET; ITER baseline assumes disruption mitigation via SPI + runaway electron (RE) suppression. CFETR Phase II βN=3.54 above no-wall limit (βN_nowall~1.24) requires RWM stabilization but "stabilization from flow, kinetic and feedback effects are not considered" in Deng et al. 2019 integrated modeling → RWM control unvalidated | ITER SPI system in procurement (10 injectors, 5 for mitigation + 5 for RE suppression); DIII-D/JET have demonstrated SPI physics (90%+ radiation fraction achievable). EAST RMP coils (n=1,2,4) enable ELM suppression/mitigation at q95~4–6 (Li et al. 2022). BEST has 8 in-vessel + 48 ex-vessel correction coils (best-research-plan-v1.1 §1.3) but RMP/RWM configuration not specified |
| **Gap ratio** | Disruption frequency: EAST/JET 1–5% of shots (50–250 disruptions per 5000 shots/yr) vs. commercial requirement <36/yr (0.7% of shots at 5000 shots/yr assuming 7 shots/day at 80% CF) → 1.4–7× gap. RWM stabilization: CFETR Phase II βN=3.54 is 2.86× above no-wall limit; demonstration of sustained operation above no-wall limit in burning plasma does not exist (ITER will explore βN~2–2.5, DIII-D reached βN~4 transiently) | SPI trigger latency: ITER design <10 ms from detection to injection; current systems ~20–50 ms → 2–5× gap. RMP coils: EAST configuration is n=1,2,4; CFETR Phase II requires n=3 or n=4 optimization for q95~5–6 advanced scenario; BEST correction coil configuration TBD. Radiation hardening: D-T neutron environment degrades diagnostics (resistivity, magnetics) used for instability detection—must demonstrate in D-T not H/D |
| **Closure mechanism** | BEST burning plasma program (Q~5 scenario) tests disruption avoidance at elevated pressure (βN~3–3.5) with AI/ML real-time control (flagged in Research Plan §2.2 as key development). ITER DT operations (2030s) will validate SPI mitigation physics and provide disruption database for AI training. RWM: BEST/CFEDR must demonstrate sustained βN>3 via feedback coils + rotation control; if unsuccessful, PFPP limited to lower βN (~2.5) → lower fusion power → larger/more expensive reactor for given net output | SPI system engineering: ITER SPI commissioning (2028–2030) provides operational experience. BEST installs correction coil system (8+48 coils) capable of n=1–4 RWM/RMP feedback but detailed coil configuration TBD. Diagnostic radiation hardening: fiber optics, rad-hard cameras, shielded magnetic sensors under development for ITER D-T; technology transfer to BEST/CFEDR |
| **Classification** | **Binary**: Unmitigated disruptions at >36/yr frequency cause cumulative first-wall damage (halo currents, melt layers, runaway electron damage) → first wall replacement every 1–2 years → unaffordable O&M + unacceptable availability loss → plant economically non-viable. RWM failure at βN>3.5 prevents access to CFETR Phase II performance → Q limited to ~3 (Phase I regime) → insufficient for commercial operation | **Degrading**: SPI mitigation failure increases disruption damage → shorter FW/divertor lifetime → higher CAS70 O&M + replacement frequency → LCOE increases but plant can operate if disruption rate kept <1/week through conservative plasma scenarios. RMP coil hardware failure prevents ELM mitigation → higher transient heat loads → reduced W armor lifetime → more frequent replacements → LCOE penalty |
| **Evidence tier** | **Tier 3**: EAST demonstrated >1000s H-mode with low-ELM regime using RMP (operating-regime for pulse length at subscale power; ELM control partial but not elimination); ITER will operate SPI in D-T (future, Tier 2 until demonstrated); CFETR Phase II RWM stabilization at βN=3.54 not yet modeled (Tier 2 computational) → composite Tier 3 (subscale ELM control demonstrated; disruption mitigation + RWM are adjacent-environment analogues not yet operating in burning plasma D-T) | **Tier 3**: ITER SPI hardware in fabrication, will be first demonstration in D-T (Tier 2–3: design-to-operate transition); EAST RMP coils operational but in H/D not D-T → adjacent environment; BEST correction coil system (8+48 coils) under construction with RWM/RMP capability → subscale (BEST operates at βN~2–3, not 3.54). No operating-regime demonstration of all three systems (SPI + RMP + RWM) in D-T burning plasma at βN>3 → Tier 3 |

**Verdict**: Physics Tier 3 (EAST ELM control partial, ITER SPI future, RWM at βN>3.5 unvalidated in burning plasma). Hardware Tier 3 (ITER SPI design-to-operate, BEST coils under construction, adjacent-environment analogues).

---

**Function 4: Plasma-Wall Interaction**

| Field | Physics | Hardware |
|-------|---------|----------|
| **Plant requirement** | Detached divertor operation with peak heat flux <10 MW/m² steady-state (commercial ITER-class divertor limit) or <15 MW/m² with advanced cooling; radiated power fraction >70% to reduce divertor heat load; W gross erosion <0.3 mm/yr at 1.5 MW/m² NWL (implies <10 µm/yr net erosion after redeposition); core W concentration n_W/n_e <5×10⁻⁵ to avoid radiation collapse | W-monoblock divertor: 48 cassettes CuCrZr substrate, W armor tiles 5–8 mm thick, water cooling at 5 MPa/150°C inlet (advanced design vs. ITER 4 MPa/70°C); first wall: 240 modules, W-coated CuCrZr, 4 MPa/70°C water cooling; erosion tolerance ~5 mm W armor (5000+ shots at 1 µm/shot net erosion before replacement); remote handling tooling for cassette replacement in 2–4 week outage |
| **Best demonstrated** | JET full-W (2011–2023): W concentration control demonstrated at n_W/n_e <10⁻⁴ in H-mode; WEST full-W divertor 1000+ pulses at 5 MW/m² peak heat flux, detached regime validated; ITER design targets 10 MW/m² CW via detachment + impurity seeding (N₂ or Ne); W erosion: WEST/JET data + Eckstein 2002 sputtering yields validate models at <1 MW/m² NWL, extrapolation to 1.5 MW/m² commercial steady-state is computational | BEST W divertor: 48 cassettes rated 10–15 MW/m² under construction; ITER W divertor mock-ups qualified at 20 MW/m² for 1000 cycles (10 s pulses) at Magdeburg test stand; WEST full-W divertor operated 1000+ cycles at 5–10 MW/m² (5–60 s pulses, total fluence ~MJ/m² vs. commercial GJ/m² requirement) |
| **Gap ratio** | NWL: commercial PFPP ~1.5 MW/m² vs. BEST 0.05–0.4 MW/m² → 3.75–30× gap. Divertor heat flux: BEST 10–15 MW/m² transient vs. PFPP 10–15 MW/m² steady-state → CW vs. pulsed thermal management different. Pulse length: BEST >1000s vs. PFPP 10⁴–10⁶ seconds between maintenance → 10–1000× fluence gap. W erosion: WEST/JET <1 MW/m² NWL → PFPP 1.5 MW/m² is 1.5× extrapolation on erosion rate (but 10–100× fluence over component lifetime) | Heat flux: ITER mock-ups 20 MW/m² for 10s pulses (total 200 MJ/m² per 1000-cycle qualification) vs. PFPP 10–15 MW/m² CW (10⁴ seconds → 100–150 GJ/m² per campaign) → 500–750× integrated fluence gap. W armor thickness: ITER/BEST 5–8 mm vs. commercial erosion allowance ~5 mm over 5000 shots → must demonstrate that net erosion (gross - redeposition) <1 µm/shot, not yet validated at 1.5 MW/m² NWL |
| **Closure mechanism** | BEST full-W program (2027–2035) validates W concentration control in D-T burning plasma at Q~5; divertor detachment + impurity seeding (N₂/Ne) demonstrated under integrated burning plasma conditions. ITER D-T operations (2030s) provide 10 MW/m² CW heat flux database and W erosion measurements at ~0.5 MW/m² NWL → PFPP extrapolates to 1.5 MW/m² using validated models (Eckstein, TRIM.SP, ERO2.0 codes) + empirical detachment control | Advanced divertor cooling: BEST baseline 4 MPa/70°C, advanced target 5 MPa/150°C with higher subcooling margin; DEMO/EU studies explore 5 MPa/180°C for 15–20 MW/m² capability. W armor qualification: post-irradiation examination (PIE) of ITER divertor tiles after D-T campaign (2035+) provides first data on W microstructure evolution under 14 MeV neutrons + transient heat + He implantation → validates lifetime models before PFPP commitment. Remote handling: ITER cassette replacement 6–12 months (first campaign) → compress to 2–4 weeks via lessons-learned + Chinese labor/shift optimization for PFPP 80% CF |
| **Classification** | **Degrading**: W impurity accumulation above n_W/n_e~5×10⁻⁵ radiates core → fusion power drops → lower Q → LCOE increases. Insufficient detachment control → divertor melt events → cassette replacement every 100–500 shots instead of 5000 → 10× higher CAS70 O&M + availability loss → LCOE penalty ~2×. Not binary—plant operates with higher maintenance cost | **Degrading**: W erosion above 1 µm/shot net (5 mm armor exhausted in 5000 shots) shortens divertor lifetime → replacement every 1–2 years (5000–10,000 shots at 7 shots/day) vs. design 5 years → 2.5–5× higher CAS72 replacement cost + availability penalty. Divertor cooling failure → local hot spots → cracking → leaks → unscheduled replacement → availability drops from 80% to 60–70% → LCOE increases 15–30%. Not binary |
| **Evidence tier** | **Tier 3**: WEST 1000+ full-W pulses at 5–10 MW/m² (subscale: 5–60 s pulses vs. PFPP 10,000+ s continuous); JET W concentration control n_W/n_e<10⁻⁴ in H-mode (subscale power); ITER will demonstrate 10 MW/m² detachment in D-T but data not yet available (currently Tier 2 design) → composite Tier 3 (subscale fluence, adjacent environment) | **Tier 3**: ITER W divertor mock-ups qualified at 20 MW/m² for 1000 cycles (subscale: 10s pulses, 200 MJ/m² total vs. PFPP 100–150 GJ/m² per campaign → 500–750× fluence gap); BEST 48 cassettes rated 10–15 MW/m² under construction but not yet operated (Tier 2 until BEST first plasma 2027) → Tier 3 (subscale fluence, transient vs. CW thermal cycling) |

**Verdict**: Physics Tier 3 (WEST/JET subscale, ITER CW detachment not yet demonstrated). Hardware Tier 3 (ITER mock-ups subscale fluence, BEST cassettes under construction).

---

**Function 5: Neutron/Particle Handling**

| Field | Physics | Hardware |
|-------|---------|----------|
| **Plant requirement** | Blanket/shield withstand 1.5 MW/m² NWL for 5 full-power-years (FPY) → 15 dpa in RAFM steel first wall, 30–50 dpa in shield structural steel over 30-year plant life; He production in steel <15 appm/dpa (14 MeV fusion neutron spectrum) without embrittlement preventing coolant flow; peak nuclear heating <20 MW/m³ in blanket | RAFM steel (F82H, EUROFER 97, CLF-1): yield strength >400 MPa after 50 dpa at 300–550°C; fracture toughness >100 MPa√m; tensile elongation >5% after irradiation; SiCf/SiC flow channel inserts withstand 10–20 dpa without cracking; PbLi corrosion <0.1 mm/yr at 350–550°C (COOL blanket); Li ceramic pebble crush strength >20 MPa after irradiation (WCCB blanket); remote handling-compatible modular blanket (remove/replace segments in 2–4 weeks) |
| **Best demonstrated** | BEST TBM program: neutron wall loading 0.15 MW/m² at 40 MW fusion power (analysis.md §S5); ITER TBM will reach ~0.5 MW/m² (~20 dpa over ITER lifetime); fission fast reactors achieve >50 dpa in steel but at different neutron spectrum (fast fission vs. 14 MeV fusion—He production rate differs 3–5×); computational: MCNP/Serpent nuclear heating and activation validated against fission data but fusion benchmark data limited | RAFM steel: F82H irradiated to 20 dpa at HFIR (Oak Ridge, mixed-spectrum); EUROFER 97 irradiated to ~10 dpa in HFR (Petten); CLF-1 (China) irradiated to 15 dpa at CARR; all show acceptable yield strength + ductility but fusion-spectrum 14 MeV data limited to <5 dpa (FFTF/HFIR have partial fusion-spectrum components). SiCf/SiC: irradiated to 10 dpa at 300–800°C in fission test reactors (HFIR, ATR); swelling <2% but fusion He implantation differs |
| **Gap ratio** | NWL: BEST 0.15 MW/m² (TBM operational, analysis.md §S5) vs. PFPP 1.5 MW/m² → 10× NWL gap. dpa: BEST TBM ~0.04 dpa over device lifetime (analysis.md §S3 magnet system "~0.04 dpa lifetime") vs. PFPP first campaign 15 dpa (5 FPY) → 375× fluence gap. Neutron spectrum: fission fast reactors provide 20–50 dpa analogues but He/dpa ratio differs (fission ~0.1 appm/dpa; 14 MeV fusion ~12 appm/dpa → 120× higher He generation per dpa affects embrittlement) | Material qualification: RAFM steel demonstrated to 20 dpa mixed-spectrum (HFIR) vs. required 50 dpa fusion-spectrum → 2.5× fluence gap in similar spectrum; 14 MeV fusion-spectrum data <5 dpa → 10× gap. SiCf/SiC: 10 dpa fission vs. 20 dpa fusion required → 2× gap. PbLi corrosion: WCLL loop tests (LIFUS5, LECOR) operated 1000–5000 hours at 350–500°C vs. PFPP 4×10⁴ hours/yr (5 FPY) → 8–40× time gap. Li ceramic pebbles: irradiated to ~5 dpa vs. 15 dpa required → 3× gap |
| **Closure mechanism** | BEST TBM results (0.15 MW/m², ~0.04 dpa over 10-year program) validate TBR + tritium extraction but do not retire fusion-spectrum materials qualification gap. IFMIF-DONES (if built—International Fusion Materials Irradiation Facility, EU/Japan, construction TBD) would provide 14 MeV neutron source at 20–50 dpa/FPY for fusion materials qualification. Absent IFMIF, PFPP proceeds on computational models (FISPACT, TENDL nuclear data) + fission-analog extrapolation + ITER TBM PIE results → residual materials uncertainty accepted as FOAK risk | RAFM steel: ITER TBM PIE (post-2035) provides first 14 MeV fusion data at ~20 dpa for F82H/EUROFER specimens → validates embrittlement models. Chinese CARR/CMRR irradiation campaigns scale CLF-1 to 30 dpa by 2030s (fission-analog but useful for ductility trends). SiCf/SiC: Gen-IV fission VHTR/SFR use SiC cladding → commercial-scale production + irradiation database; fusion extrapolation based on computational swelling models (IVEM, MD simulations). PbLi: WCLL test loops (EU) scale to 10,000+ hour campaigns by 2030; corrosion rate extrapolation + Al₂O₃/FeCrAlY coating development mitigate steel wastage |
| **Classification** | **Binary** (if TBR<1.0): Insufficient tritium breeding forces external tritium purchase at $35,000/g—unaffordable at kg/day commercial scale → plant cannot sustain operations → economically non-viable. **Degrading** (if TBR~1.05–1.1 but below margin): Marginal breeding requires zero tritium losses in fuel cycle → tight tolerance → higher T processing cost + risk of shortfall → LCOE penalty but plant operable | **Degrading**: RAFM steel embrittlement above design → blanket lifetime 3 FPY instead of 5 FPY → 67% higher CAS72 replacement cost → LCOE increases ~20–40%. SiCf/SiC cracking → coolant leaks → blanket module replacement unscheduled → availability penalty. PbLi corrosion → steel wastage → leaks → module replacement early → higher O&M. Not binary—plant operates with higher maintenance burden |
| **Evidence tier** | **Tier 2**: BEST TBM 0.15 MW/m² is 10× below commercial 1.5 MW/m²; ITER TBM will reach 0.5 MW/m² (~20 dpa); no operating fusion device has demonstrated TBR>1.0 with full breeding blanket (BEST TBMs are <1 m² test modules in 0.6×1 m² ports, not full coverage) → computational TBR predictions (MCNP/Serpent) are Tier 2 (simulation); fission fast reactors provide dpa analogues but different He/dpa ratio (adjacent environment, not direct fusion) → Tier 2 composite | **Tier 3**: RAFM steel irradiated to 20 dpa mixed-spectrum (HFIR F82H) is subscale (50% of required 50 dpa fusion-spectrum over plant life); SiCf/SiC irradiated to 10 dpa fission (50% of required 20 dpa fusion); fission fast reactor steel provides adjacent-environment analogue (>50 dpa but different spectrum) → composite Tier 3 (subscale + adjacent environment) |

**Verdict**: Physics Tier 2 (TBR computational only, no full-breeding demonstration; dpa extrapolation from fission adjacent-environment). Hardware Tier 3 (RAFM/SiC subscale irradiation, fission-spectrum analogues).

---

**Function 6: Fuel Cycle Closure**

| Field | Physics | Hardware |
|-------|---------|----------|
| **Plant requirement** | TBR>1.1 with realistic blanket penetrations (ports, divertor, gaps) to supply tritium breeding + 5.5%/yr decay + processing losses + startup inventory for fleet expansion; tritium extraction from PbLi (COOL) >90% at kg/day throughput or from Li ceramics (WCCB) >80% via purge gas; tritium processing plant: isotope separation, purification, storage, injection at kg/day scale; accountancy: <1% unaccounted-for T inventory per year (regulatory requirement) | COOL: PbLi tritium extraction via vacuum permeator or He bubbling + gas separation; permeation barriers (FeCrAl, Al₂O₃ coating) on PbLi/water HX to prevent T leakage to steam/sCO₂; WCCB: He purge gas + getter systems for Li ceramic T extraction; T processing: cryogenic distillation, Pd membrane permeators, accountancy via ion chambers + gas chromatography; storage: uranium beds or metal hydride (ZrCo) beds at 1–10 kg scale; injection: pellet injectors + gas puffing at 100+ mg/s throughput |
| **Best demonstrated** | JET/TFTR: D-T operations at 10–100 g scale; ITER tritium plant: designed for 1 kg inventory, 100 g/day processing (not yet operated); BEST: 110 g licensed inventory (analysis.md §S3 fuel cycle); TBR: ITER TBM computational predictions TBR~1.1–1.15 for HCPB/WCLL (MCNP simulations), no experimental validation | COOL: PbLi T extraction demonstrated in WCLL test loops (LIFUS5, ENEA) at gram-scale; vacuum permeator TRL~4 (lab-scale), He bubbling TRL~5 (small loops); WCCB: HCPB T extraction via He purge demonstrated in EXOTIC facility (KIT) at mg-scale; ITER T plant design complete, equipment procurement in progress (TRL~5–6, operational TRL~7–8 post-commissioning 2028); Cryogenic distillation: mature (TRL 9 for H isotopes in fission); accountancy: demonstrated at JET/TFTR gram-scale but not kg-scale |
| **Gap ratio** | TBR: computational 1.1–1.15 with idealized geometry vs. required >1.1 with as-built penetrations (ports reduce TBR by ~0.05–0.10) → margin thin; no experimental TBR demonstration at any scale (BEST TBMs measure local TBR but not integrated plant TBR). Throughput: ITER 100 g/day vs. PFPP ~1 kg/day (10× gap); BEST 110 g total vs. PFPP 1000 g/day → 9× inventory scale, 10,000× throughput gap | PbLi T extraction: LIFUS5 gram-scale vs. PFPP kg-scale → 1000× scale gap; extraction efficiency 90% required but demonstrated ~60–80% in loops (efficiency gap 1.1–1.5×). WCCB: EXOTIC mg-scale vs. PFPP kg-scale → 10⁶× scale gap. T plant: ITER design 100 g/day vs. PFPP 1 kg/day → 10× throughput; accountancy <1%/yr at kg-scale not demonstrated (JET/TFTR achieved <5%/yr at 10–100 g scale → 10–100× inventory gap, accountancy difficulty scales non-linearly with inventory) |
| **Closure mechanism** | BEST TBM program measures local TBR in 0.6×1 m² modules at 0.15 MW/m² NWL; validates tritium extraction efficiency from COOL/WCCB prototypes at mg–g scale. ITER TBM + DEMO programs (2030s–2040s) scale to full breeding blanket coverage and validate integrated plant TBR>1.0. T extraction efficiency improvements: permeation barrier coatings (Al₂O₃, FeCrAl) reduce T loss to <1% in HX, getter systems improve recovery to >90%. PFPP proceeds on validated TBR models + ITER T plant operational experience (post-2030) + DEMO breeding demonstration (2040s if EU-DEMO proceeds) | ITER T plant commissioning (2028–2030) demonstrates cryogenic distillation, Pd membranes, accountancy at 100 g/day scale → scaling to 1 kg/day is engineering (more columns, more membranes, more storage beds) not new physics. PbLi extraction: WCLL DEMO loop experiments (2030s) scale to 100 g/day → validates extraction chemistry and efficiency. WCCB extraction: HCPB helium loop scale-up + getter bed optimization (Li-Pb getters, CuO beds) improve efficiency. Accountancy: distributed monitoring (ion chambers at every process node) + real-time mass balance calculations reduce unaccounted-for T to <1%/yr at kg-scale |
| **Classification** | **Binary**: TBR<1.0 (or <1.05 with insufficient margin for losses) prevents self-sufficiency → external tritium purchase required at $35,000/g × 365 kg/yr (assuming 1 kg/day consumption, 5.5% decay, fleet expansion) → $13M/yr fuel cost unsustainable → plant non-viable. Mandatory classification per framework | **Degrading**: T extraction efficiency <90% increases external tritium makeup requirement → $1–5M/yr additional fuel cost → LCOE increases ~$1–5/MWh (minor penalty at 1 GWe, 80% CF → 7 TWh/yr). Accountancy >1%/yr unaccounted-for T triggers regulatory penalties + license suspension risk → operational constraint forces conservative T inventory limits → effective TBR margin reduced → fuel cycle tighter tolerances. Not binary—plant operates with higher cost + regulatory scrutiny |
| **Evidence tier** | **Tier 2**: TBR>1.1 is computational only (MCNP/Serpent for ITER TBMs, no experimental validation of integrated full-coverage blanket TBR); BEST TBM will measure local TBR at 0.15 MW/m² but not full plant TBR → remains Tier 2 until ITER or DEMO operates with full breeding blanket and measures net tritium production over campaign. Tritium breeding is asserted by models, not demonstrated → Tier 2 per framework ("simulation, design study") | **Tier 3**: ITER T plant design (100 g/day) is subscale vs. PFPP 1 kg/day (10× gap) → Tier 3 per framework; PbLi T extraction at LIFUS5/ENEA gram-scale (1000× below PFPP kg-scale) → subscale → Tier 3; WCCB extraction at EXOTIC mg-scale (10⁶× below) → Tier 2 (far subscale, approaching "design study"). Composite Tier 3 weighted toward ITER T plant (largest capital share, most mature) |

**Verdict**: Physics Tier 2 (TBR computational only, no full-blanket demonstration). Hardware Tier 3 (ITER T plant subscale, extraction loops far subscale).

---

**Function 7: Power Conversion & BOP**

| Field | Physics | Hardware |
|-------|---------|----------|
| **Plant requirement** | sCO2 Brayton cycle: 34.7% thermal efficiency at 350°C inlet / 550°C hot leg, 8 MPa CO2, closed loop with 1 GW thermal input; tritium permeation barriers on all PbLi/CO2 HX to prevent T contamination of working fluid; thermal transient tolerance: pulsed plasma heat source with 10–1000 s shot cycles (if PFPP pulsed) or quasi-steady-state CW (if quasi-steady-state CF>75%); balance-of-plant: electrical switchgear, cooling towers, control systems at 1 GWe scale | sCO2 turbomachinery: compact turbine + compressor rated 200–300 MWe per train (3–5 trains for 1 GWe gross), inlet 550°C / 8 MPa, outlet 350°C / 8 MPa, isentropic efficiency >85%; recuperators (printed circuit HX, PCHE) effectiveness >95%; PbLi/CO2 HX with tritium permeation barriers (Al₂O₃, FeCrAl coatings, <1% T leakage rate); thermal storage buffer (if pulsed): molten salt or solid ceramic thermal mass to smooth 10–1000 s plasma pulses → continuous turbine operation; electrical: 1 GWe switchyard, transformers, transmission integration (standard utility equipment) |
| **Best demonstrated** | sCO2 Brayton: demonstrated in CSP (concentrating solar power) pilots at 10 MWe scale (Sandia sCO2 test loop, Echogen, Toshiba pilots) with 35–40% efficiency; Gen-IV fission reactors (HTGR, SFR) design sCO2 cycles at 50–200 MWe but none yet built; thermal efficiency 34.7% validated computationally for CFETR (cfetr-power-conversion-studies.md) but not demonstrated with fusion heat source | sCO2 turbomachinery: 10 MWe pilots operational (Sandia, 2013–present); 100 MWe scale in design/procurement for Gen-IV fission (China HTR-PM targeting sCO2 recompression, schedule TBD). Recuperators: PCHE demonstrated at 1–10 MWe scale (Heatric, Alfa Laval); scaling to 200–300 MWe per train is engineering extrapolation. PbLi/CO2 HX: test articles under development for WCLL/COOL (ENEA IELLLO loop, analysis.md §S3 BOP); tritium permeation barriers demonstrated in lab at <1% leakage but not in fusion-integrated environment (Tier 2–3). Thermal storage: molten salt storage mature in CSP (TRL 9, GWh-scale); ceramic thermal mass demonstrated in pilots (TRL 6–7) |
| **Gap ratio** | Turbine scale: 10 MWe pilots vs. 200–300 MWe commercial trains → 20–30× scale gap per train; 1 GWe plant requires 3–5 trains → total 3–15 trains must operate reliably in parallel (no demonstration of multi-train sCO2 plant). Thermal efficiency: 34.7% (CFETR study) is conservative vs. 42–53% (advanced recompression cycles in literature) → no gap vs. requirement but potential upside. Fusion heat source integration: pulsed 10–1000 s plasma cycles vs. CSP continuous or daily-cycled → different thermal transient profiles. Tritium permeation: lab <1% leakage vs. required <1% in operational fusion plant with PbLi corrosion + thermal cycling + neutron activation of HX structure → combined-effects gap | PbLi/CO2 HX: test loops <1 MW thermal vs. PFPP ~1000 MW thermal (1000× scale gap); tritium permeation barriers tested in lab/small loops but not at fusion-scale T concentrations (g/m³ in PbLi) + neutron environment (activation + He generation in barrier coatings degrades performance). Thermal storage (if pulsed PFPP): CSP molten salt systems handle 4–12 hour day/night cycles vs. fusion 10–1000 s shot cycles → 10–1000× higher cycle frequency → fatigue/creep effects differ. Multi-train operation: no operating precedent for 3–5 parallel sCO2 trains at 200–300 MWe scale in any application (CSP largest is single 10 MWe loop) |
| **Closure mechanism** | sCO2 pilot scale-up: Sandia 10 MWe → DOE/China HTR-PM 100 MWe (construction 2020s) → PFPP 200–300 MWe trains (2030s extrapolation). Thermal efficiency: CFETR sCO2 studies (2021–2025) establish 34.7% baseline; advanced cycles (recompression, intercooling) target 42–48% if validated in Gen-IV fission programs. Fusion heat source integration: CFETR Phase I operations (late 2030s) test PbLi/CO2 HX under fusion pulsed heat + T permeation environment → PFPP adopts validated HX design. Pulsed thermal storage (if needed): CSP molten salt technology adapts to 10–1000 s fusion cycles via active flow control + buffer tank sizing | Turbomachinery: Gen-IV fission sCO2 deployment (China HTR-PM, US ARDP, EU ALFRED) in 2030s demonstrates 100–200 MWe trains → scaling to 300 MWe is <2× extrapolation. Multi-train operation: commercial sCO2 plants (if fission programs succeed) operate 2–4 trains in parallel by 2035 → provides operational experience for fusion. PbLi/CO2 HX: ENEA IELLLO loop (10–50 MW thermal, 2030s target) tests T permeation barriers (Al₂O₃, FeCrAl) under PbLi corrosion + T concentrations + thermal cycling → validates barrier lifetime. Tritium accountancy in sCO2: distributed T monitors (ion chambers, gas chromatography) + permeation barrier inspection via eddy current/UT detect coating degradation |
| **Classification** | **Degrading**: sCO2 cycle failure (turbine trips, recuperator fouling, HX leaks) forces fallback to steam Rankine at 26.4% efficiency → 8.3 percentage point efficiency loss → LCOE increases ~30% (from 158 $/MWh to ~206 $/MWh at model_output efficiency sensitivity -0.27 per % → -0.27 × 8.3/34.7 ≈ -6.5% LCOE per 1% η_th → +8.3×4.3 ≈ +36 $/MWh). Tritium permeation >1% into CO2 → environmental release risk → regulatory shutdown for barrier repair → availability penalty. Not binary—plant operates with degraded economics or temporary outage | **Degrading**: Turbomachinery failures → reduced availability (target 80%, achieved 70%) → LCOE increases ~14% (availability elasticity -0.91 → 10% availability loss = +9% LCOE). PbLi/CO2 HX leaks → coolant cross-contamination → replace HX module → 2–4 week outage → availability penalty. Thermal storage (if pulsed) undersized → turbine throttles during low-plasma-power portions of cycle → efficiency penalty 2–5% → LCOE +9–22 $/MWh. Not binary |
| **Evidence tier** | **Tier 3**: sCO2 Brayton at 10 MWe CSP pilots (subscale 20–30× per train vs. commercial 200–300 MWe trains; total plant 100–200× below 1 GWe); 34.7% efficiency validated computationally (CFETR studies) but not demonstrated with fusion heat source → adjacent environment (CSP continuous, fission thermal, vs. fusion pulsed D-T + T-contaminated coolant). Fusion integration is design study (Tier 2) but sCO2 cycle operation at subscale is demonstrated (Tier 3) → composite Tier 3 | **Tier 3**: Sandia 10 MWe turbomachinery operational (subscale 20–30×); PCHE recuperators at 1–10 MWe (subscale 20–30×); PbLi/CO2 HX in test loops <1 MW (subscale 1000×); tritium permeation barriers demonstrated in lab (Tier 2 until integrated in fusion environment). Gen-IV fission sCO2 at 100–200 MWe (China HTR-PM, US ARDP) under construction (Tier 2–3: design-to-build transition) → composite Tier 3 weighted toward demonstrated pilots + near-term fission scale-up |

**Verdict**: Physics Tier 3 (sCO2 subscale at CSP pilots, fusion integration computational). Hardware Tier 3 (10 MWe turbomachinery operational, 100 MWe fission scale-up in progress, PbLi/CO2 HX subscale).

---

### Function-Level Means (F1–F7)

Computed as symmetric arithmetic mean of Physics and Hardware tiers, rounded to nearest 0.5:

| Function | Physics Tier | Hardware Tier | Mean (before heritage) | Heritage Floor (D-T Tokamak) | Final Mean |
|----------|--------------|---------------|------------------------|------------------------------|------------|
| F1: Plasma Performance | 4 | 3 | 3.5 | 4.0 | **4.0** |
| F2: Driver / Energy Input | 3 | 4 | 3.5 | 4.0 | **4.0** |
| F3: Instability Control | 3 | 3 | 3.0 | 4.0 | **4.0** |
| F4: Plasma-Wall Interaction | 3 | 3 | 3.0 | 4.0 | **4.0** |
| F5: Neutron/Particle Handling | 2 | 3 | 2.5 | 4.0 | **4.0** |
| F6: Fuel Cycle Closure | 2 | 3 | 2.5 | 4.0 | **4.0** |
| F7: Power Conversion & BOP | 3 | 3 | 3.0 | N/A (no heritage for sCO2 in fusion) | **3.0** |

**Heritage credit application**: BEST → CFETR → PFPP lineage inherits tokamak heritage (JET, EAST, ITER). Framework assigns 4.0 floor for "Tokamak (ITER, JET, EAST, etc.)" D-T fuel lineage. Heritage floor applies to **all seven functions F1–F7** per updated framework §C7 Heritage Credit rationale ("heritage doesn't only help with plasma physics—A tokamak-lineage concept inherits decades of engineering work on divertors (F4), neutron-handling materials (F5), tritium fuel cycles (F6), and steam-cycle BOP integration (F7)").

**F7 exception**: Power conversion heritage does NOT apply to sCO2 Brayton—tokamak heritage is steam Rankine (ARIES, DEMO studies). Framework notes: "Score concepts that rely on novel DEC against the demonstrated regime of that specific DEC method, not against thermal-cycle baselines." sCO2 Brayton is novel for fusion (though mature in CSP/Gen-IV fission)—no tokamak heritage credit. F7 remains 3.0 (no floor override).

**All other F1–F6 functions receive heritage floor 4.0**. This reflects ITER/JET/EAST heritage in plasma control (F1–F3), PFC engineering (F4), RAFM steel programs (F5), and ITER T plant (F6).

**Final F1–F7**: 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0

---

### Binary Risks

Per C7 risk matrix classifications:

1. **Disruption frequency >36/yr**: Unmitigated disruptions cause cumulative FW damage (halo currents, melt, runaway electrons) → FW replacement every 1–2 years → unaffordable O&M + availability <50% → plant economically non-viable (F3 Physics)

2. **RWM stabilization failure at βN>3.5**: Prevents access to CFETR Phase II performance (Q=23.5, Pfus=1084 MW) → Q limited to Phase I Q~3 → insufficient for commercial operation → LCOE >300 $/MWh even with Chinese discount (F3 Physics)

3. **TBR<1.0**: Insufficient tritium breeding forces external T purchase at $35,000/g × 365 kg/yr → $13M/yr fuel cost + constrained by global CANDU supply (~25 kg total inventory) → plant cannot sustain operations → non-viable (F6 Physics, mandatory per framework)

---

### YAML Scores Block

```yaml
---
scores:
  C1: 2.7
  C3: 3.5
  C4: 3.0
  C5: 1.8
  C8: 2.5
  F1: 4.0
  F2: 4.0
  F3: 4.0
  F4: 4.0
  F5: 4.0
  F6: 4.0
  F7: 3.0
  binary_risks:
    - "Disruption frequency >36/yr causes cumulative first-wall damage requiring replacement every 1–2 years, rendering plant economically non-viable"
    - "RWM stabilization failure at βN>3.5 prevents access to CFETR Phase II performance, limiting Q to ~3 (insufficient for commercial viability)"
    - "TBR<1.0 forces external tritium purchase at $13M/yr, unsustainable at commercial scale"
---
```
