---
ID: 09-qi-stellarator-hts
Concept: QI Stellarator HTS (Proxima Fusion / Stellaris)
Company: Proxima Fusion
Type: synthesis
Status: draft
Created: 2026-06-09
---

# Editorial Synthesis: QI Stellarator HTS (Proxima Fusion / Stellaris)

## 1. Executive Summary

- **Most critical risk**: HTS coil manufacturing at scale — 50 unique 3D non-planar coils at 20 T peak field, each geometrically distinct, with no demonstrated manufacturing pathway. This is a factor-of-3-5× cost uncertainty on the largest capital account.
- **Most important advantage**: Disruption-free steady-state operation with W7-X-validated QI confinement physics. This eliminates the tokamak disruption-mitigation tax (structural reinforcement, vertical stability systems, runaway electron protection) and enables true steady-state without current-drive systems.
- **LCOE estimate**: **148 $/MWh** at 1 GWe NOAK projection (model output), with ±30% confidence bounds driven primarily by magnet cost uncertainty. This is competitive with advanced tokamaks under optimistic magnet scaling assumptions but could reach 200+ $/MWh if 3D coil fabrication proves prohibitively expensive.
- **Confidence verdict**: **Medium** — physics basis is strong (W7-X heritage), engineering integration is comprehensive (first stellarator with cross-domain optimization), but economic analysis is entirely absent from published data and magnet manufacturing is unvalidated.

## 2. What Matters Most for LCOE

**Ranked by LCOE sensitivity (model-derived and qualitative):**

### 1. HTS Magnet Manufacturing Cost (C220103: $4,090M, 33% of overnight capital)
- **Assumed value**: Library default scaled from tokamak HTS experience (CFS ARC: $44k/kg for REBCO coils).
- **Sensitivity**: A 50% increase in magnet cost (+$2B) would raise LCOE to ~170 $/MWh; a factor-of-2× increase would reach ~205 $/MWh. The CAS22 sub-account breakdown shows magnets dominate direct capital.
- **What would flip the economic conclusion**: If 3D coil fabrication costs 3× more per kilogram than tokamak D-coils due to geometric uniqueness (no series production learning across identical units), LCOE exceeds 200 $/MWh and competitiveness collapses. Conversely, if Proxima's planned magnet factory achieves tokamak-equivalent costs despite 3D geometry, LCOE stays near 150 $/MWh.
- **Source confidence**: Zero — Stellaris paper explicitly defers cost analysis; Alpha demo budget (€2B) is a FOAK facility estimate, not a component cost breakdown. Override C220103 is disabled pending SMC demo (2027) or Alpha data (2031).

### 2. Auxiliary Heating Power (C220104: model-sensitive via override)
- **Assumed value**: 50 MW ECRH at 230-240 GHz (stellaris-design-details.md §2.6, Table 1).
- **Sensitivity**: The override reduces C220104 from $250M (library default) to $50M (design-grounded), saving $200M overnight capital and reducing LCOE by ~3 $/MWh. This is a **backward-looking correction**, not a forward-looking sensitivity: prior modeling errors set `p_input = 2700 MW` (fusion power instead of auxiliary heating), back-solving to 13 GW fusion power for 1 GWe output and inflating LCOE to 303 $/MWh. F9 now blocks `p_input/P_native > 0.5` to prevent recurrence.
- **What would flip the economic conclusion**: If ignition requires sustained 200 MW ECRH (rather than 50 MW startup + <1 MW steady-state), capital cost rises by ~$150M and LCOE increases by ~2 $/MWh. This is unlikely given QI confinement quality, but depends on achieving the assumed plasma gain (Q_eng).

### 3. Capacity Factor / Availability (90% target, 4-year operating cycle)
- **Assumed value**: 90% availability based on 4-year operation + 4-5 month blanket replacement (stellaris-design-details.md §Remote Maintenance).
- **Sensitivity**: Dropping to 75% availability (due to divertor failures, longer maintenance, or component degradation) would increase LCOE by ~20% (to ~178 $/MWh). The model does not expose availability as a direct CAS line item; it compounds through fixed-cost amortization over fewer operating hours.
- **What would flip the economic conclusion**: If divertor heat flux control at 4 MW/m² proves unachievable without frequent target replacement (every 1-2 years rather than 4 years), availability drops to 70-80% and LCOE exceeds 170 $/MWh. The Stellaris paper warns EMC3-Lite divertor simulations "should not be mistaken for accurate heat flux predictions" and defers control validation to future work.

### 4. Balance of Plant Thermal Efficiency (implicit in library scaling)
- **Assumed value**: ~32% overall plant efficiency (3.3 GW thermal → 1 GW electrical implies steam Rankine or sCO₂ Brayton at ~45% thermal conversion × ~70% recirculating power factor).
- **Sensitivity**: A 5-percentage-point efficiency loss (e.g., forced to use lower-temperature coolant due to EUROFER97 <550°C limit) would require 15% more fusion power for the same net output, increasing CAS22 reactor equipment proportionally and raising LCOE by ~12 $/MWh.
- **What would flip the economic conclusion**: If sCO₂ Brayton proves incompatible with the 3D stellarator geometry (piping complexity, MHD effects in PbLi flow) and the plant falls back to steam Rankine at 38% instead of 45% thermal, LCOE rises to ~165 $/MWh.

### 5. First Wall / Coil Lifetime (10 full-power years assumed)
- **Assumed value**: 10 FPY for EUROFER97 first wall (DBTT-limited); 10 FPY for REBCO coils (neutron fluence degradation) — stellaris-design-details.md §Neutronics, §Coils.
- **Sensitivity**: If actual lifetimes are 5 FPY instead of 10, replacement costs double and scheduled downtime increases. The Stellaris paper notes "significant uncertainties due to the limited material dataset available for radiation damage at 14 MeV neutron energy." Halving coil lifetime would front-load capital amortization and raise LCOE by ~10 $/MWh; halving first-wall lifetime would reduce capacity factor and raise LCOE by ~8 $/MWh.
- **What would flip the economic conclusion**: If coils degrade in 3-5 years (rather than 10), the capital recovery schedule compresses and effective LCOE rises to ~175 $/MWh, making the plant uneconomic relative to advanced tokamaks with replaceable TF coils.

## 3. Risk Verdicts

### HTS Coil Manufacturing at Scale (50 unique 3D coils, 668-777 km REBCO tape)
- **Verdict**: **Genuinely uncertain**
- **Rationale**: No full-scale 3D non-planar stellarator coil has ever been built at 20 T. Tokamak HTS coils (CFS, Tokamak Energy) are planar or toroidal; stellarator coils are geometrically unique and cannot leverage series production learning.
- **What would retire this risk**: (1) SMC demo (2027) successfully manufactures one full-scale coil and publishes cost breakdown, or (2) Alpha demo (2031) completes magnet system fabrication on-time/on-budget and provides validated $/kg or $/coil data. Until then, this is the dominant cost uncertainty.

### Divertor Heat Flux Control at 4 MW/m² (detachment, impurity seeding, steady-state)
- **Verdict**: **Unlikely resolvable without high-power demonstration**
- **Rationale**: W7-X validated island divertor physics at <0.1 MW/m²; Stellaris requires 40× higher power density. The paper explicitly warns EMC3-Lite simulations "should not be mistaken for accurate heat flux predictions" and lists divertor control as critical future work.
- **What would retire this risk**: Alpha demo achieves >1 MW/m² neutron wall load with stable detached island divertor and confirms control algorithms, or alternative stellarator (Helios, Type One) demonstrates high-power-density island divertor. Without this, assume divertor becomes a life-limiting component and availability drops below 80%.

### Material Lifetime Under 14.1 MeV Neutrons (EUROFER97, REBCO tape)
- **Verdict**: **Likely resolvable** (shared D-T fusion challenge, not stellarator-specific)
- **Rationale**: DBTT shift for RAFM steels and critical-current degradation for REBCO are being studied across all D-T programs. IFMIF-DONES (EU fusion materials test facility, targeting operations ~2030) will provide 14 MeV neutron irradiation data at scale. The 10 FPY lifetime assumption has large error bars but is not fundamentally implausible.
- **What would retire this risk**: IFMIF-DONES validates EUROFER97 and REBCO radiation tolerance at 40-50 dpa (full-power-year equivalent) and confirms yield-strength margins remain above safety thresholds. Alternatively, High-Entropy Alloys or ODS steels could extend first-wall lifetime to 15-20 FPY, reducing replacement frequency and improving availability.

### Tritium Breeding at TBR = 1.074 (WCLL blanket, stellarator geometry)
- **Verdict**: **Likely resolvable** (neutronic modeling is mature, extraction is the challenge)
- **Rationale**: TBR = 1.074 exceeds the 1.05 self-sufficiency threshold and includes margins for uncertainties. The WCLL blanket concept is adapted from EUROfusion DEMO with well-characterized neutronics. The risk is not whether the blanket breeds enough tritium, but whether extraction from PbLi at kg/day rates works in a 3D magnetic field (MHD effects, permeation control, corrosion).
- **What would retire this risk**: TBM-equivalent testing in a stellarator (e.g., Alpha demo with integrated blanket module) or tokamak DEMO programs demonstrate PbLi tritium extraction at fusion-relevant rates. Proxima's patent-pending alternative blanket may sidestep WCLL issues entirely, but that remains undisclosed.

### Remote Maintenance Turnaround (sector-split, 4-5 month target)
- **Verdict**: **Genuinely uncertain** (novel maintenance paradigm, no prototype)
- **Rationale**: The sector-split approach is detailed on paper (10-step horizontal extraction process) but has never been demonstrated. ITER remote handling took decades to develop for tokamak geometry; stellarator sector-split is structurally different. The 4-5 month turnaround is provisional and drives the 90% availability target.
- **What would retire this risk**: Full-scale maintenance mockup (radiation-hardened robotics, crane systems, sector handling) validates <5-month blanket replacement in a non-radioactive environment, or Alpha demo executes a blanket replacement campaign and publishes turnaround time. If actual maintenance takes 8-10 months, availability drops to ~75% and LCOE rises to ~175 $/MWh.

## 4. Structural Advantages and Disadvantages

### Advantages vs. D-T Tokamak Baseline

**Eliminates ~5-10% of tokamak direct capital (CAS22 sub-accounts):**
- **No disruption mitigation systems** (C220109: structural reinforcement, vertical stability coils, runaway electron diagnostics). Stellarators are intrinsically disruption-free due to 3D equilibrium. This is a ~$100-200M capital savings and eliminates a major operational risk.
- **No steady-state current drive** beyond startup ECRH. Tokamaks at high duty cycle (>50%) require neutral beams or ECRH for continuous current drive; stellarators sustain confinement without plasma current. Stellaris uses 50 MW ECRH for startup only, dropping to <1 MW in ignited phase. This saves ~$100-150M in beam systems and ~20-30 MW recirculating power.
- **Reduced divertor thermal stress** (potentially). The island divertor distributes heat over larger wetted area than tokamak SOL divertors, which may extend divertor lifetime. However, this is speculative — the Stellaris paper notes divertor design is "critical future work."

**Trades ~10-15% tokamak capital for stellarator-specific costs:**
- **3D coil complexity premium**. Stellaris requires 50 unique non-planar coils with tight tolerances (<1 mm coil placement error). Tokamak TF coils are identical toroidal wedges manufactured in series. The complexity premium is captured in C220103 (magnets) but the magnitude is unknown. If 3D coils cost 50% more per kilogram than tokamak D-coils, the net capital impact is +$2B (~15% of overnight).
- **Stellarator-specific buildings and maintenance** (CAS21: $629M). The sector-split maintenance approach requires specialized cranes, rail systems, and remote handling adapted to 3D geometry. Tokamak port-based maintenance is more mature but may require more frequent interventions. The cost delta is ambiguous.

**Neutral (shared with tokamaks):**
- Tritium breeding blanket (WCLL), RAFM structural materials (EUROFER97), tungsten plasma-facing components, balance-of-plant thermal cycle, and D-T fuel cycle challenges are identical to advanced tokamaks (SPARC, ARC, UKAEA STEP).

### Disadvantages vs. D-T Tokamak Baseline

**Higher Physics Risk for LCOE (not cost, but viability):**
- **Unvalidated QI optimization at power-plant scale**. W7-X demonstrated QI confinement at <0.1 MW/m² neutron wall load; Stellaris requires 40× scale-up. The confinement degradation with size (stellarator beta limits, neoclassical transport) is less well-characterized than tokamak scaling laws (IPB98y2). If QI confinement degrades faster than expected, the plant requires larger plasma volume (higher capital) or accepts lower fusion power (lower output).
- **No demonstrated burning plasma in stellarators**. All D-T burning-plasma experience is in tokamaks (JET, future ITER). Stellaris assumes alpha-heating and ignition work similarly in stellarators, but this is untested. Alpha demo (2031) is the first stellarator targeting Q>1; Stellaris assumes Q>>1 (50 MW ECRH for 2700 MW fusion → Q_eng ~18 after accounting for recirculating power). If Q_eng is lower, LCOE rises via higher auxiliary heating capital and operating cost.

## 5. Cross-Concept Positioning

**Stellaris sits at the intersection of three economic clusters:**

### Cluster 1: Advanced Tokamaks (HTS, compact, D-T)
- **Peers**: CFS SPARC/ARC (01), Tokamak Energy ST-E1 (03), UKAEA STEP (02)
- **Shared economics**: HTS magnet cost dominates capital (~30-40% of overnight), D-T fuel cycle (tritium breeding, RAFM blankets, 14 MeV neutron damage), balance-of-plant at ~1 GWe scale
- **Stellaris advantage**: Disruption-free operation (eliminates tokamak disruption-mitigation tax, higher availability ceiling)
- **Stellaris disadvantage**: 3D coil manufacturing complexity (unique coil shapes, no series production learning), less mature physics scaling (tokamaks have 60 years of confinement data, stellarators have W7-X + LHD only)
- **LCOE comparison**: Stellaris 148 $/MWh vs. CFS ARC ~120-140 $/MWh (literature estimates). The spread is within magnet cost uncertainty — if 3D coils are ≤20% more expensive than tokamak D-coils per kilogram, Stellaris is competitive; if >50% premium, tokamaks win.

### Cluster 2: Planar-Coil Stellarators (Thea Helios, Type One)
- **Peers**: Thea Energy Helios (05), Type One Energy (20a)
- **Shared economics**: Stellarator steady-state advantage, QI confinement, island divertor, D-T fuel cycle
- **Stellaris advantage**: Leverages W7-X heritage (Max Planck IPP spin-off, validated QI physics), integrated cross-domain optimization (first stellarator with electromagnetic/structural/thermal/neutronic coupling)
- **Stellaris disadvantage**: 3D coil complexity vs. planar coil arrays. Helios uses 12+324 planar coils ("all flat and convex, wound in tension, tolerances relaxed via control system"). Type One uses modular cassettes (plug-and-play replacement). Stellaris's 50 unique 3D coils trade manufacturing simplicity for plasma optimization.
- **LCOE comparison**: Helios claims ~120-140 $/MWh (unpublished); Stellaris 148 $/MWh. The gap is the 3D coil premium. If planar coils are 30-40% cheaper to manufacture, Helios undercuts Stellaris by ~10-20 $/MWh. If 3D coils enable higher fusion power density (smaller plasma volume for same net output), capital scales down and Stellaris catches up.

### Cluster 3: Large-Scale Conventional Stellarators (ARIES-CS legacy, LHD-type)
- **Peers**: Helical-coil stellarators (36), potential Gauss Fusion design (10)
- **Shared economics**: 3D coil geometry, stellarator maintenance challenges
- **Stellaris advantage**: HTS magnets (ARIES-CS used LTS at 5-8 T; Stellaris uses 20 T REBCO, enabling 50% smaller major radius for same confinement). Sector-split maintenance (ARIES-CS required serial extraction of 222 components through vertical ports, identified as a "maintenance nightmare").
- **Stellaris disadvantage**: None — Stellaris explicitly addresses ARIES-CS failure modes (oversized coil structure, poor maintainability, low magnetic field). This is a generational leap, not a peer comparison.
- **LCOE comparison**: ARIES-CS estimated ~200-250 $/MWh (late-2000s, inflation-adjusted). Stellaris at 148 $/MWh represents 40% cost reduction via HTS magnets and integrated maintenance design.

**Strategic positioning**: Stellaris is the "optimized 3D stellarator" competing against both tokamaks (via disruption-free operation and steady-state capability) and planar-coil stellarators (via QI confinement quality and physics maturity). Its LCOE viability depends on whether 3D coil manufacturing costs converge toward tokamak-equivalent $/kg (making it competitive with tokamaks and superior to planar stellarators in confinement) or remain 2-3× higher (making planar stellarators cheaper and tokamaks safer bets).

## 6. Modeling Confidence

**Rating: Medium**

### Data-Anchored Parameters (~60% of LCOE drivers)
- Plasma geometry (R0, plasma volume, B field), fusion power (2.7 GW), net electric output (1 GW), auxiliary heating (50 MW ECRH), TBR (1.074), material choices (EUROFER97, tungsten, WCLL), coil specifications (50 coils, 20 T peak field, REBCO tape) — all directly sourced from stellaris-design-details.md with high confidence.
- Balance-of-plant efficiency (~32% overall), availability target (90%), component lifetimes (10 FPY) — documented in the Stellaris paper but noted as provisional ("economic aspects outside the scope").

### Speculative Parameters (~40% of LCOE drivers)
- **HTS magnet cost** — the largest single capital item (33% of overnight) is scaled from tokamak experience with zero stellarator-specific data. The 3D coil complexity premium is unknown. Override C220103 is disabled pending SMC/Alpha demos.
- **Divertor performance** — heat flux control at 4 MW/m² is unvalidated; the Stellaris paper explicitly warns simulations are not "accurate heat flux predictions." If divertor lifetime is half the assumed value, capacity factor drops and LCOE rises by ~20%.
- **Maintenance turnaround time** — the sector-split approach is novel and untested. The 4-5 month replacement interval is a provisional estimate driving the 90% availability target. If actual turnaround is 8-10 months, LCOE rises to ~175 $/MWh.

### Dominant Source of LCOE Uncertainty
**HTS coil manufacturing cost** is the single largest uncertainty, representing ±$2-4B capital swing (±15-30% LCOE impact). The Stellaris paper provides coil geometry and material specifications but explicitly defers cost analysis: "detailed cost analysis of large-scale HTS tape production" is listed as a key gap. Until Proxima publishes vendor quotes, SMC demo results (2027), or Alpha magnet system costs (2031), the LCOE estimate relies on tokamak-derived scaling that may underestimate 3D coil complexity by a factor of 2-3×.

**Confidence breakdown by CAS account:**
- CAS22 Reactor Equipment: **Low-Medium** (magnet cost dominates, zero grounded data)
- CAS21 Buildings: **Medium** (stellarator-specific maintenance infrastructure, but scales generically with device volume)
- CAS23 Turbine Plant, CAS24 Electric Plant, CAS25 Misc Plant, CAS26 Heat Rejection: **High** (mature BOP technologies, standard power-plant engineering)
- CAS50 Capitalized Supplementary Costs, CAS60 Capitalized Owner's Costs, CAS70 Capitalized Financial Costs: **Medium** (financial structure assumptions, first-of-a-kind risk premiums are judgmental)

## 7. What Would Change My Mind

### Developments That Would Lower LCOE Estimate (→ 120-130 $/MWh range)

1. **Proxima publishes magnet system cost breakdown showing 3D coil fabrication at ≤$50k/kg (tokamak-competitive)**
   *Source*: SMC demo (2027) cost postmortem, Alpha demo (2031) magnet procurement report, or partnership announcement with REBCO tape supplier (e.g., Faraday Factory Japan) quoting NOAK pricing at $/km for stellarator application.
   *Impact*: Confirms library default C220103 is reasonable; 3D coil premium is <20%. LCOE drops to ~135 $/MWh (Stellaris becomes cost-competitive with advanced tokamaks).

2. **Alpha demo (2031) validates island divertor control at >1 MW/m² with stable detachment**
   *Source*: Proxima peer-reviewed publication or conference presentation showing sustained detached operation, impurity seeding control, and <10% peak-to-average heat flux variation at high power.
   *Impact*: Retires divertor risk; confirms 90% availability target is achievable. Combined with magnet cost validation, LCOE could reach ~125 $/MWh.

### Developments That Would Raise LCOE Estimate (→ 180-220 $/MWh range)

1. **SMC demo (2027) reveals 3D coil fabrication costs >$100k/kg (2-3× tokamak baseline)**
   *Source*: Proxima investor update, magnet factory feasibility study, or partnership announcement citing higher-than-expected winding/assembly costs for complex 3D geometry.
   *Impact*: Confirms 3D coil premium is 100-200% above tokamak D-coils. C220103 rises to $8-12B (doubling magnet cost), pushing LCOE to ~200-220 $/MWh. At this level, planar-coil stellarators (Helios, Type One) and advanced tokamaks become economically superior.

2. **Alpha demo (2031) requires >10 MW sustained ECRH to maintain ignition (vs. <1 MW assumed)**
   *Source*: Proxima operational reports showing Q_eng = 5-10 instead of Q_eng >>10, requiring higher auxiliary heating to sustain fusion power.
   *Impact*: Recirculating power fraction rises; net electric output drops for same fusion power; LCOE increases by ~10-15 $/MWh. Alternatively, if Alpha requires 200+ MW ECRH for ignition ramp (vs. 50 MW assumed), C220104 quadruples and adds ~8 $/MWh to LCOE. This would indicate QI confinement degrades at power-plant scale, a physics failure mode that could render the concept uneconomic.

3. **W7-X follow-on experiments show island divertor cannot sustain detachment at >0.5 MW/m²**
   *Source*: Max Planck IPP publications from W7-X upgrade campaigns, or alternative stellarator programs (LHD, Helios) reporting detachment control failures at intermediate power density.
   *Impact*: Divertor becomes a life-limiting component requiring replacement every 1-2 years instead of 4 years. Availability drops to 70-75%, LCOE rises to ~180-190 $/MWh. Combined with high magnet cost, LCOE exceeds 220 $/MWh and the concept becomes uneconomic.

---

**Bottom line**: Stellaris is a technically comprehensive stellarator design with strong physics heritage (W7-X) and integrated engineering (cross-domain optimization), but its economic viability hinges entirely on whether 3D HTS coil manufacturing can approach tokamak cost-per-kilogram benchmarks. The LCOE estimate of 148 $/MWh is a **conditional projection** assuming tokamak-equivalent magnet costs and 90% availability. If either assumption fails, LCOE rises above 180 $/MWh and the concept loses to planar-coil stellarators or advanced tokamaks. The SMC demo (2027) and Alpha demo (2031) are the critical validation gates.
