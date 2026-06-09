---
ID: 28-hts-tokamak-full-hts
Concept: HTS Tokamak Full HTS
Company: Energy Singularity
Type: synthesis
Status: draft
Created: 2026-06-08
---

# Synthesis: HTS Tokamak Full HTS (Energy Singularity)

## Executive Summary

- **The critical risk**: Energy Singularity has disclosed no power plant design. HH380 (their only power-producing machine) has zero public specifications — no scale, no blanket, no geometry. Any LCOE estimate is analogue-driven conjecture until post-2030.
- **The structural advantage**: World's first fully operational all-HTS tokamak (26 REBCO coils) with 1,337-second steady-state demonstrated. China domestic supply chain delivered HH70 in under 2 years at 96% localization. If this construction speed and cost structure translate to commercial scale, it materially undercuts Western comparables.
- **Model LCOE**: 94 $/MWh (1 GWe NOAK) using compact tokamak analogue inputs. This is a **placeholder** — not company-grounded. True corridor likely 50-130 $/MWh depending on REBCO tape price trajectory and deployment geography.
- **Confidence verdict**: **Low**. Zero enabled cost overrides. Model runs on library defaults for a generic compact HTS tokamak at assumed 500 MWe scale. The differentiation is real (full-HTS magnets, rapid construction), but the power plant design doesn't exist yet.

## What Matters Most for LCOE

Ranked by economic leverage:

### 1. REBCO tape unit cost trajectory ($10-100/kA-m range)
- **Model assumption**: Library default magnet cost (calibrated to TF-only HTS, not full-HTS)
- **Energy Singularity architecture**: All 26 coils use REBCO (TF + PF + CS), not just TF like CFS or Tokamak Energy
- **Sensitivity magnitude**: C220103 (confinement magnets) is $412M in the model for a 500 MWe plant. If REBCO stays at $100/kA-m (current high end), full-HTS penalty could push this to $600M. If Shanghai Superconductor hits the industry target of <$10/kA-m, it could drop to $250M.
- **What would flip the conclusion**: Published REBCO procurement cost from Energy Singularity or tape price floor confirmation from Shanghai Superconductor. At $10/kA-m, full-HTS becomes a capital cost *advantage* (simpler cryogenics, higher field everywhere). At $100/kA-m, it's a penalty vs. hybrid HTS/LTS designs.
- **Current best estimate**: Unknown. Model cannot resolve this without company data. The 94 $/MWh LCOE sits in the middle of the 50-130 $/MWh corridor precisely because of this uncertainty.

### 2. Power plant scale (100 MWe pilot vs. 1 GWe commercial)
- **Model assumption**: 500 MWe (compact tokamak analogue midpoint)
- **Company data**: Zero. HH380 net electric output not disclosed.
- **Sensitivity magnitude**: Tokamak capital costs scale nonlinearly with size. Modeling shows overnight capital ranges from ~$8,300/kW (500 MWe) to ~$7,800/kW (1 GWe) in library defaults. Smaller pilots (200-300 MWe) would show 1.5-1.8× higher $/kW.
- **What would flip the conclusion**: HH380 specification disclosure. If Energy Singularity targets a 200 MWe pilot (plausible for "world's smallest tokamak capable of Q>10"), LCOE could rise to 140-160 $/MWh even with favorable REBCO pricing. If they scale directly to 1 GWe (aggressive but not impossible given China backing), LCOE falls toward 70-90 $/MWh.
- **Current best estimate**: 500 MWe is a guess, not grounded. The model satisfies the three-forward contract but carries no predictive weight.

### 3. China deployment cost multiplier vs. international markets
- **Model assumption**: Generic US/EU cost structure (library default)
- **Energy Singularity data**: HH70 built in <2 years at 96% domestic localization, total cost ~$110M. This is 2-3× faster than Western tokamak construction timelines for comparable experimental scale.
- **Sensitivity magnitude**: Construction duration affects IDC (interest during construction). 2 years at 8% WACC vs. 7 years on a $4B plant → ~$200M IDC difference. Chinese labor and fabrication costs are 20-40% below US/EU for heavy manufacturing. Combined effect: China-deployed HH380 could show 15-25% lower LCOE than Western-deployed analogue.
- **What would flip the conclusion**: If Energy Singularity targets export markets (US/EU), supply chain localization advantage evaporates. REBCO tape from Shanghai Superconductor may face export restrictions. Technology transfer barriers could force rebuilding the supply chain in target markets, adding 20-40% to capital cost. The 50-130 $/MWh corridor reflects this geography-dependent bifurcation.
- **Current best estimate**: Model uses generic costs (no geography override). For China deployment, bias LCOE toward lower end of corridor (60-90 $/MWh). For US/EU deployment, bias toward upper end (100-130 $/MWh).

### 4. Blanket chemistry and tritium breeding approach
- **Model assumption**: Library default (likely FLiBe molten salt for D-T tokamak archetype)
- **Company data**: None. No blanket design disclosed for HH380.
- **Sensitivity magnitude**: C220101 (first wall + blanket) is $144M in the model. CAS27 (special materials — blanket inventory) is $7M. Combined: $151M for a 500 MWe plant. If Energy Singularity adopts solid breeder (HCPB-style with Be multiplier), cost could rise to $300-400M. If they adopt LiPb liquid metal, different cost structure (higher inventory, lower fabrication). China's CFETR program develops WCCB, HCCB, and sCO2-cooled LiPb blankets — possible technology sharing but no public connection.
- **What would flip the conclusion**: Blanket design disclosure or CFETR technology transfer confirmation. This is a $100-250M swing depending on chemistry choice. It doesn't flip the economic verdict (tokamaks of this scale are LCOE-competitive if capital costs are controlled), but it materially affects the capital cost breakdown and TBR risk profile.
- **Current best estimate**: Cannot override. Model uses library default with low confidence. Flag as major uncertainty driver.

### 5. Capacity factor and divertor heat flux management
- **Model assumption**: Library default capacity factor (likely 0.7-0.8 for steady-state tokamak)
- **Energy Singularity data**: HH70 demonstrated 1,337-second steady-state. HH170 targets Q>10 in ~70% of SPARC volume with ~110% of SPARC field — implies high power density, severe divertor heat flux.
- **Sensitivity magnitude**: Capacity factor directly multiplies LCOE denominator. 0.7 CF vs. 0.5 CF is a 40% LCOE penalty. Compact high-field tokamaks universally face divertor challenges. If Energy Singularity requires advanced divertor solutions (liquid metal, detached plasma) or frequent cassette replacement, availability drops. C220108 (divertor) is $81M in model; could double if advanced solutions required.
- **What would flip the conclusion**: HH170 divertor performance data (2027+) or HH380 divertor design disclosure. If Energy Singularity demonstrates steady-state at high power density without exotic divertor tech, capacity factor optimism is warranted. If HH170 shows unmanageable heat flux or frequent disruptions, capacity factor pessimism dominates.
- **Current best estimate**: Model assumes steady-state enables high CF, but no company-grounded divertor design. This is a qualitative risk, not a quantitative override.

## Risk Verdicts

### 1. Unknown power plant scale and design (blocking gap)
- **Verdict**: Genuinely uncertain
- **Rationale**: Energy Singularity operates in a rapid-iteration private-sector model (HH70 → HH170 → HH380 in <10 years) but has not disclosed HH380 engineering decisions. Timeline is post-2030; design may not be finalized yet.
- **What would retire this risk**: HH380 specification release (power output, geometry, blanket, balance of plant). Unlikely before HH170 commission (2027-2028). Until then, analogue-based modeling is the only path forward.

### 2. Full-HTS cost penalty vs. hybrid HTS/LTS designs
- **Verdict**: Genuinely uncertain (depends on REBCO price trajectory)
- **Rationale**: Energy Singularity's all-REBCO architecture (TF + PF + CS) is structurally different from comparables (CFS uses TF-only HTS, state-backed programs use LTS). More tape → higher conductor cost, but simpler cryogenics (20 K only, no 4 K). Net effect depends on whether REBCO prices fall to <$10/kA-m (industry target) or remain at $30-100/kA-m (current range).
- **What would retire this risk**: Multi-year REBCO production cost data from Shanghai Superconductor or published HH380 magnet procurement costs. If tape prices stay high, full-HTS is uneconomical. If they fall to target, full-HTS becomes a competitive advantage (higher field, faster fabrication, lower cryogenic OPEX).

### 3. Tritium breeding pathway completely unknown
- **Verdict**: Likely resolvable via CFETR technology sharing (but unconfirmed)
- **Rationale**: Energy Singularity operates in China's fusion ecosystem. CFETR (state-backed) is developing WCCB, HCCB, and LiPb blankets. Technology transfer from national program to private-sector developer is plausible (cf. SpaceX/NASA in US context), but no public evidence of connection exists.
- **What would retire this risk**: Blanket design disclosure or CFETR collaboration announcement. If Energy Singularity adopts a CFETR-developed blanket, development risk is shared. If they design from scratch, TBR demonstration becomes a FOAK blocking challenge.

### 4. China supply chain advantage vs. international deployment barriers
- **Verdict**: Likely resolvable for China deployment, unlikely resolvable for US/EU markets
- **Rationale**: HH70 achieved 96% domestic localization and 2-year construction timeline. For China-deployed plants, this is a structural cost advantage. For international deployment, export controls on HTS tape, technology transfer restrictions, and supply chain rebuilding eliminate the advantage and likely impose a 20-40% cost penalty.
- **What would retire this risk**: Energy Singularity's deployment strategy disclosure. If they target China-only markets (plausible given domestic policy support for fusion), the advantage is real. If they pursue Western markets, the penalty is unavoidable unless REBCO supply chains globalize (unlikely under current geopolitical climate).

### 5. Compact high-field divertor heat flux challenge
- **Verdict**: Unlikely resolvable without advanced divertor solutions or scale-up
- **Rationale**: HH170 is ~70% of SPARC volume with ~110% of SPARC field → power density is higher than SPARC. High power density → high divertor heat flux. Standard tungsten monoblock divertors (ITER-style) are designed for ~10-20 MW/m² steady-state. Compact tokamaks typically require detached plasma, radiative divertor, or liquid metal solutions. Energy Singularity has disclosed no divertor approach.
- **What would retire this risk**: HH170 divertor performance data showing manageable heat flux without exotic solutions, or HH380 divertor design publication. If Energy Singularity scales up HH380 to larger size (less compact, lower power density), the challenge softens. If they maintain compact philosophy, divertor R&D becomes critical path.

## Structural Advantages and Disadvantages

### Advantages (vs. conventional D-T tokamak baseline)

1. **Full-HTS magnet system eliminates 4 K cryogenics**: Conventional tokamaks (ITER-heritage) use LTS (Nb3Sn) requiring 4.2 K helium refrigeration. Hybrid HTS tokamaks (CFS, Tokamak Energy) use HTS for TF coils only, still need 4 K for PF/CS. Energy Singularity's all-REBCO approach operates at 20 K (single cryogenic system). **Capital cost impact**: Cryogenic plant cost is ~50% lower (20 K vs. dual 4 K + 20 K). OPEX advantage: refrigeration power scales as ~(T_ambient / T_cryo)², so 20 K vs. 4 K is ~25× easier thermodynamically. Quantified advantage: ~$50-100M CAPEX saving on CAS22.4 (cryogenic systems) for a 500 MWe plant, plus ~10-20% lower cryogenic OPEX.

2. **Demonstrated construction speed (2-year HH70 timeline)**: If this translates to HH380, IDC savings are ~$150-200M vs. 7-year Western construction baseline on a $4B plant at 8% WACC. Learning curve acceleration: faster FOAK → NOAK iteration reduces nth-plant delivery time, improving fleet economics.

3. **Domestic supply chain localization (96%) in large manufacturing economy**: China's heavy manufacturing cost structure (labor, steel fabrication, power supplies) is 20-40% below US/EU. If deployment targets China market, this compounds the construction speed advantage. Combined LCOE impact: 15-25% reduction vs. Western-deployed analogues.

4. **Higher operational tempo demonstrated (100 shots/day vs. 20-30/day at JET)**: Suggests efficient plasma control and power supply performance. If this translates to commercial operation, it improves capacity factor via faster recovery from transients and reduced downtime between campaigns.

### Disadvantages (vs. conventional D-T tokamak baseline)

1. **Full-HTS increases conductor inventory cost if REBCO prices remain elevated**: HH380 requires km-scale REBCO tape for TF + PF + CS coils. At $100/kA-m, this is a $300-500M penalty vs. hybrid HTS/LTS designs. At $10/kA-m target, penalty disappears. Current pricing: uncertain. **Net verdict**: This is a *bet* on REBCO cost reduction, not a demonstrated advantage.

2. **Compact high-field design implies severe divertor heat flux**: No disclosed solution. C220108 (divertor) could double from $81M (model default) to $150-200M if advanced solutions required. Availability risk if divertor becomes life-limiting component.

3. **Unknown blanket design and TBR pathway**: Conventional tokamaks (ITER, CFETR) have decades of blanket R&D investment. Energy Singularity's HH380 blanket is greenfield. If they adopt CFETR technology, risk is mitigated. If they design from scratch, TBR demonstration is a FOAK blocking challenge with $200-500M capital cost uncertainty (C220101 + CAS27).

4. **International deployment eliminates supply chain advantage**: 96% localization in China is a strength for domestic deployment, a *liability* for export markets. REBCO tape export restrictions, technology transfer barriers, and supply chain rebuilding turn the cost advantage into a 20-40% penalty.

### Structural cost eliminations (none)

Energy Singularity's full-HTS approach does not eliminate major cost accounts. It shifts costs (higher conductor inventory, lower cryogenics) but does not structurally simplify the power plant (still requires blanket, divertor, vacuum vessel, balance of plant, remote maintenance).

### Structural cost additions (none)

Full-HTS does not add cost accounts beyond what D-T tokamak baseline requires. The architecture is tokamak-conventional except for magnet technology.

## Cross-Concept Positioning

Energy Singularity sits in the **compact HTS tokamak family** alongside CFS (01-hts-compact-tokamak) and Tokamak Energy (21-spherical-tokamak-hts). Differentiators:

1. **vs. CFS (01-hts-compact-tokamak)**: CFS uses TF-only HTS (LTS for PF/CS). Energy Singularity uses full-HTS. CFS has published power plant design (ARC: FLiBe blanket, demountable TF joints, 500 MWe). Energy Singularity has zero HH380 design disclosure. **Economic positioning**: If REBCO costs fall and China deployment is targeted, Energy Singularity could undercut CFS by 20-30% LCOE via construction speed and supply chain advantages. If REBCO costs stay high or international deployment is required, CFS likely has lower capital cost (hybrid HTS/LTS is conductor-cheaper).

2. **vs. Tokamak Energy (21-spherical-tokamak-hts)**: Tokamak Energy uses spherical tokamak geometry (A ~1.7-2.0, higher power density, smaller major radius). Energy Singularity uses conventional aspect ratio (A ~2.4-3.0, based on HH70). Different physics optimization paths. **Economic positioning**: Spherical tokamaks have more severe center-column neutron flux challenges but better plasma confinement at small scale. Conventional compact tokamaks (Energy Singularity) have easier engineering but require higher field for equivalent performance. LCOE comparison is ambiguous without full designs, but both face similar divertor and blanket challenges.

3. **vs. state-backed tokamaks (33-state-backed-tokamak-best, ASIPP-class)**: ASIPP (EAST, CFETR) uses LTS (Nb3Sn) and conventional scale (R0 = 1.7-7 m). Energy Singularity uses HTS and compact scale. **Economic positioning**: State-backed programs have lower cost of capital (government funding, no commercial return requirement) but slower iteration (science-driven, not commercial-driven). Energy Singularity's private-sector model enables rapid construction (HH70 in 2 years) but must achieve commercial LCOE. If Energy Singularity benefits from CFETR blanket technology sharing, they get the best of both (rapid iteration + state R&D leverage). If no technology transfer, they face higher development risk.

4. **vs. negative triangularity tokamaks (29-negative-triangularity-tokamak)**: Firefly and DIII-D derivatives use negative-δ shaping for divertor heat flux mitigation. Energy Singularity uses positive-δ (HH170 described as "D-shaped") and high field for performance. **Economic positioning**: Negative-δ is a divertor cost mitigation strategy. Energy Singularity's compact high-field approach requires different divertor solution (not yet disclosed). If Firefly demonstrates cheaper divertor via shaping, it could undercut compact high-field concepts on C220108. If Energy Singularity's high field enables smaller machine (lower absolute capital), it wins on CAS22 total despite divertor penalty.

**Overall family position**: Energy Singularity is the **most aggressive HTS architecture** (full-REBCO, not hybrid) with the **most demonstrated integration** (HH70 operational, 5,755 shots, 1,337 seconds) but the **least disclosed power plant engineering** (zero HH380 specs). It occupies the "demonstrated magnets, speculative reactor" quadrant. CFS is the inverse ("published reactor, SPARC not operational yet"). Tokamak Energy is "spherical niche, moderate disclosure." State-backed programs are "mature but slow, LTS-based."

## Modeling Confidence

**Rating**: Low

**Rationale**: Zero enabled overrides. The model runs on library defaults for a generic 500 MWe compact HTS tokamak. The design point (R0=2.6m, plasma_t=0.87m, B=14T, p_input=85MW) is extrapolated from HH170 targets scaled 2× linearly — not company-grounded. Analysis Section 5b completed per-account walkthrough (C220101 through CAS80) and found no company data sufficient for overrides. The top override candidate (C220103 magnets, due to full-HTS architecture) cannot be overridden without HH380 magnet costs or REBCO tape procurement pricing.

**Dominant source of LCOE uncertainty**: **REBCO tape unit cost trajectory**. If Shanghai Superconductor hits $10/kA-m (industry target), full-HTS becomes a capital cost advantage → LCOE toward 60-80 $/MWh. If tape prices remain at $30-100/kA-m (current range), full-HTS is a penalty → LCOE toward 110-130 $/MWh. Secondary uncertainty: **deployment geography** (China vs. international markets, 15-25% LCOE swing due to supply chain and construction cost differentials).

**Parameters that are data-anchored**:
- HH70 magnet configuration (26 REBCO coils, 12 TF + 6 PF + 8 CS, 20 K operation)
- Steady-state demonstration (1,337 seconds)
- Construction timeline (HH70 in <2 years)
- Domestic localization (96%)
- HH170 targets (Q>10, ~14T, ~70% SPARC volume)

**Parameters that are speculative**:
- HH380 power output (500 MWe assumed, not disclosed)
- HH380 geometry (R0, plasma_t, elongation all extrapolated)
- Auxiliary heating power and approach (p_input=85MW is analogue-based)
- Blanket design and TBR pathway (library default chemistry)
- Divertor heat flux management approach (no company data)
- Energy conversion pathway (thermal cycle type unknown)
- Capacity factor (library default, no HH380 operational plan disclosed)
- REBCO tape unit cost at HH380 scale (no Shanghai Superconductor pricing data)

**Confidence breakdown by CAS account**:
- CAS21 (buildings): Medium (China construction costs are knowable from industry data, but no concept-specific override)
- CAS22 (reactor equipment): Low (C220103 magnets are architectural delta, but no cost data; C220101 blanket unknown; C220108 divertor unknown)
- CAS23-26 (turbine, electric, heat rejection): Medium (mature balance-of-plant technology, library defaults are reasonable)
- CAS27 (special materials): Low (blanket chemistry unknown)
- CAS70 (O&M): Medium (operational efficiency demonstrated at HH70 scale, but no HH380 staffing or maintenance plan)
- CAS80 (fuel): Medium (D-T fuel cycle is archetype-standard, but TBR unknown)

**Overall model status**: This is a **corridor map** for a compact HTS tokamak at 500 MWe scale, not a company-validated LCOE estimate. The 94 $/MWh (1 GWe NOAK) sits in the middle of the 50-130 $/MWh corridor stated in analysis Section 2. The true LCOE depends on engineering decisions Energy Singularity has not disclosed yet (timeline: post-2030). The model satisfies the three-forward contract requirement but should be flagged as **low-grounding-confidence** in cross-concept comparisons.

## What Would Change My Mind

### 1. Shanghai Superconductor REBCO tape production cost curve disclosure (direction: either way)

If Shanghai Superconductor publishes multi-year procurement contracts or production cost breakdowns showing REBCO tape at <$15/kA-m with credible scaling pathway to $10/kA-m, full-HTS becomes a validated cost advantage. Model LCOE drops to 60-80 $/MWh (China deployment) or 75-95 $/MWh (international deployment). C220103 override: `0.7 × generic.costs.c220103` (simpler cryogenics + favorable tape pricing offsets higher inventory).

If pricing data shows REBCO floor at $30-50/kA-m due to supply chain or materials constraints, full-HTS becomes a confirmed penalty. Model LCOE rises to 110-130 $/MWh. C220103 override: `1.3-1.5 × generic.costs.c220103` (higher conductor cost dominates).

### 2. HH170 commission and performance data (2027-2028) (direction: resolve divertor and Q_eng uncertainty)

If HH170 achieves Q>10 in steady-state with manageable divertor heat flux using standard tungsten monoblock cassettes, capacity factor optimism is warranted. Compact high-field approach is validated. Model LCOE bias: lower end of corridor (70-90 $/MWh at 1 GWe).

If HH170 shows unmanageable heat flux, frequent disruptions, or requires exotic divertor solutions (liquid metal, detached plasma with severe performance penalty), capacity factor pessimism dominates. C220108 override: `2.0 × generic.costs.c220108` (advanced divertor). Model LCOE bias: upper end of corridor (100-120 $/MWh).

### 3. CFETR blanket technology transfer confirmation or HH380 blanket design disclosure (direction: resolve TBR and blanket cost uncertainty)

If Energy Singularity announces adoption of CFETR-developed blanket (WCCB, HCCB, or LiPb), development risk is retired. C220101 and CAS27 remain library defaults but with higher confidence (archetype-appropriate). TBR pathway is credible.

If HH380 blanket design is disclosed as greenfield (no CFETR connection) with novel chemistry or geometry, development risk increases. C220101 + CAS27 uncertainty widens to $200-500M range (factor of 2-3× variation depending on chemistry). LCOE corridor widens to 50-140 $/MWh.

If no blanket disclosure by 2030 (HH380 timeline slips or remains opaque), the concept should be reclassified as "pre-engineering" with LCOE estimates flagged as purely speculative.
