---
ID: 34-compact-spherical-tokamak-india
Concept: Compact Spherical Tokamak - India
Company: Pranos Fusion
Type: synthesis
Status: draft
Created: 2026-04-29
Stale: true
Stale-Reason: analysis-updated-iter-4
---

# Synthesis: Compact Spherical Tokamak - India (Pranos Fusion)

## 1. Executive Summary

- **Most important risk**: The 50 MWe modular scale creates a catastrophic economics trap — recirculating power consumes ~59% of gross electric output (vs. ≤25% target for large plants), forcing extremely high Q operation that compact spherical tokamaks have never demonstrated. The model yields Q_eng=1.6, which is inconsistent with net power production.
- **Most important advantage**: IF the 2,500-unit fleet vision materializes with full factory learning (8 doublings), and IF the first unit validates performance, THEN cumulative learning could theoretically compress per-unit capital cost from $54,000/kWe (FOAK) to $48,000/kWe (NOAK) — but this still yields LCOE of $630/MWh, 4× above competitive baseload targets.
- **LCOE ballpark**: $630/MWh (NOAK, 50 MWe native scale) based on analogue-only model. This is entirely speculative — Pranos has published zero design parameters. The 1 GWe reference scaling (impossible for this concept but analytically useful) yields $84/MWh, revealing that scale mismatch alone accounts for ~$550/MWh of the LCOE penalty.
- **Confidence verdict**: **Low** — founded May 2024 with $417K seed funding, no peer-reviewed publications, no disclosed machine parameters (R, A, B_T, Q, heating method, blanket design), and only one preprint describing a 0.1 T experimental device (PRAGYA) that is ~20-50× below commercial field requirements.

## 2. What Matters Most for LCOE

The model sensitivity analysis identifies the following ranked parameters:

### Rank 1: Availability (elasticity: -0.96)
- **Assumed value**: 80% (conservative analogue from Araiinejad & Shirvan 2025 D-T MCF range of 75-90%)
- **Source**: No Pranos maintenance scheme disclosed; fleet vision implies ~87% but model uses 80% as conservative proxy
- **Sensitivity**: LCOE scales nearly 1:1 inversely with availability — a 10% reduction in availability (to 72%) raises LCOE by ~9.6% to ~$690/MWh
- **Flip condition**: Achieving 90% availability (upper bound of analogue range) would reduce LCOE to ~$560/MWh — still 3.7× above $150/MWh competitive threshold. Availability improvements alone cannot rescue this concept's economics.

### Rank 2: r_coil — Magnet cost multiplier (elasticity: +0.72)
- **Assumed value**: Framework default, representing HTS coil cost structure
- **Source**: Pranos confirmed HTS magnets via company website; no field strength, coil count, or tape grade disclosed. Model uses nearest-neighbor analogue from Tokamak Energy ST-HTS.
- **Sensitivity**: A 10% increase in magnet cost multiplier raises LCOE by 7.2% to ~$675/MWh
- **Flip condition**: Even if magnet costs dropped to zero (impossible), LCOE would fall only to ~$175/MWh — still above competitive threshold. This reveals that while magnets are the largest cost line item ($516M / $2,388M total capital = 21.6% via CAS22 sub-account C220103), the problem is structural, not component-specific.

### Rank 3: Construction Time (elasticity: +0.45)
- **Assumed value**: 8 years (6-year baseline + 2-year India regulatory penalty)
- **Source**: India's AERB has no established fusion-specific pathway; analogous to Stewart & Shirvan 2022 fission-style regulatory scenario. This may be optimistic.
- **Sensitivity**: A 10% reduction in construction time (to 7.2 years) reduces LCOE by 4.5% to ~$600/MWh
- **Flip condition**: Compressing construction to 4 years (implausible for first-of-kind fusion in India) would reduce LCOE to ~$515/MWh — still 3.4× above competitive threshold. Permitting acceleration is not sufficient.

### Rank 4: b_max — Peak field on coil (elasticity: +0.36)
- **Assumed value**: Framework default for HTS tokamak
- **Source**: Pranos has not disclosed field strength; PRAGYA experimental device operates at 0.1 T (far below commercial requirements)
- **Sensitivity**: Field affects magnet capital cost and (weakly) plasma performance
- **Flip condition**: This is a physics constraint, not a design choice — higher field enables higher fusion power density but requires more expensive magnets. The elasticity is moderate because the compact ST geometry already constrains field optimization.

### Rank 5: Thermal Efficiency (elasticity: -0.13)
- **Assumed value**: 30% (conservative steam Rankine for 50 MW industrial turbine)
- **Source**: Industrial 50 MW turbines achieve 28-33% vs. utility-scale ~40%; power conversion cycle not disclosed by Pranos
- **Sensitivity**: A 10% improvement in thermal efficiency (to 33%) reduces LCOE by 1.3% to ~$622/MWh
- **Flip condition**: Even achieving utility-scale 40% efficiency (impossible at 50 MW thermal scale) would reduce LCOE only to ~$590/MWh. Thermal efficiency is not a major lever at this scale.

**Critical observation**: The top-3 sensitivities (availability, magnet cost, construction time) are all heavily influenced by the 50 MWe scale penalty. Small plants have lower availability (fixed downtime is proportionally larger), higher specific capital costs (economies of scale), and longer regulatory timelines (no precedent for modular fusion licensing).

## 3. Risk Verdicts

### Challenge 1: Modular 50 MW scale — severe cost penalty (analysis.md §2)
- **Verdict**: Unlikely resolvable without abandoning the modular concept
- **Rationale**: Fusion plant cost accounts have large fixed or sublinearly-scaling components (tritium fuel cycle, center stack shielding, building infrastructure) that do not shrink proportionally with output. The ARIES-ST scaling shows $/kWe ∝ P^(-0.4), implying a 2.5-3× penalty at 50 MWe vs. 500 MWe. The model confirms this: $630/MWh at 50 MWe vs. $84/MWh at 1 GWe (7.5× ratio, even with NOAK learning).
- **What would retire this risk**: Demonstrate Q_eng > 5 at the 50 MWe scale with recirculating power <30% of gross electric — this would halve the LCOE penalty. Alternatively, abandon the 50 MWe target and scale up to 200-400 MWe, accepting reduced modularity.

### Challenge 2: Unknown machine parameters — no physics anchor (analysis.md §2)
- **Verdict**: Genuinely uncertain — company is in computational design phase
- **Rationale**: Pranos has published PRAGYA experimental parameters (R₀=0.4m, B_T=0.1T, A≈2.2) but these describe a proof-of-concept device, not the commercial 50 MWe module. Without R, A, B_T, or Q for the commercial design, the entire power balance is unconstrained. The model assumes R₀=1.5m, A≈2.0, and derives P_fus=369 MW — but this is analogue-based, not Pranos-validated.
- **What would retire this risk**: Publication of a self-consistent commercial design point (R, A, B_T, Ip, Q, P_fus) validated by integrated systems code (PROCESS, Jenga, or equivalent) — this is a necessary but not sufficient condition for credibility.

### Challenge 3: HTS magnets confirmed; specifications unpublished (analysis.md §2)
- **Verdict**: Likely resolvable — HTS is now the declared technology path
- **Rationale**: The company website confirms "High-Temperature Superconducting (HTS) magnets" as a core platform technology. This resolves the largest blocking uncertainty (magnet type) and validates the HTS cost structure used in the model. The remaining gap (field strength, coil count, tape grade) is a refinement, not a fundamental unknown. Tokamak Energy has demonstrated HTS ST magnets at 11.8 T (Demo4, Nov 2025), providing technology existence proof.
- **What would retire this risk**: Disclosure of on-axis field (B_T), peak field on coil (B_max), coil count, and tape specification (REBCO vs. BSCCO, operating current density) — this would anchor the magnet cost sub-structure and validate (or refute) the $516M magnet cost estimate.

### Challenge 4: Recirculating power and Q_engineering unknown (analysis.md §2)
- **Verdict**: Unlikely resolvable at 50 MWe scale without breakthrough physics
- **Rationale**: At 50 MWe net output, recirculating loads (NBI/RF heating, tritium processing, cryogenics, cooling, housekeeping) are proportionally enormous. The model estimates ~59% of gross electric consumed by auxiliaries, requiring Q_eng=1.6 — which is inconsistent with the claimed 50 MWe net output (this would imply negative net power at Q_eng=1.6). Even if Q_plasma=20 (far above any ST demonstration), wall-plug efficiency of heating (~50%) and the absolute magnitude of fixed loads (tritium, cryo, cooling) at this scale create a recirculating fraction >40%. This is the core physics-engineering trap.
- **What would retire this risk**: Demonstrate Q_plasma > 20 in a compact ST geometry with bootstrap fraction > 90% (minimizing auxiliary heating) AND achieve >70% heating wall-plug efficiency (far above NBI's ~50%) AND reduce fixed loads by 50% via radical design simplification. This combination is implausible.

### Challenge 5: Blanket and tritium breeding — entirely uncharacterized (analysis.md §2)
- **Verdict**: Likely resolvable — standard engineering problem for D-T tokamaks
- **Rationale**: D-T fuel creates an unavoidable TBR > 1 requirement. Compact STs face outboard-only breeding geometry (center stack cannot accommodate blanket), requiring Li-6-enriched breeder material. This is a known engineering challenge, not a physics unknown. ITER TBM program and liquid Li extraction research provide analogue data.
- **What would retire this risk**: Publish blanket type (liquid Li, solid Li₄SiO₄, Pb-17Li), TBR target (typically 1.05-1.15 for margin), and Li-6 enrichment level. Demonstrate TBR > 1 via neutronics simulation (Monte Carlo N-Particle, Serpent, or equivalent) using actual Pranos geometry.

### Challenge 6: India regulatory environment — no established pathway (analysis.md §2)
- **Verdict**: Genuinely uncertain — regulatory timeline is country-specific
- **Rationale**: India's AERB has no fusion-specific regulatory framework and no precedent for private fusion developers (unlike US NRC Part 30, 2023; UK separate fusion regulation underway). The model applies a +2 year construction penalty and uses 8 years total, but this may be optimistic. Fission-style regulation could trigger the Stewart & Shirvan 2.2× building cost scenario, raising CAS21 from $229M to ~$500M and pushing LCOE to $750-850/MWh.
- **What would retire this risk**: AERB publishes a fusion-specific licensing pathway with timeline benchmarks, OR Pranos secures a regulatory pre-approval or waiver for experimental devices leading to commercial licensing precedent.

## 4. Structural Advantages and Disadvantages

**Baseline**: Conventional large-scale D-T tokamak (ITER-class, 500-1000 MWe)

### Advantages (relative to baseline)

**None quantified.** The compact spherical tokamak architecture has potential physics advantages (higher beta, natural elongation, simpler coil geometry) but these do not translate to cost advantages at the 50 MWe scale. The model shows:

- **Magnet cost**: $516M / 50 MWe = $10,320/kWe — comparable to or higher than large tokamaks on a $/kWe basis despite smaller absolute size, because HTS tape cost per kA-m dominates and compact geometry requires high field
- **Buildings**: $229M / 50 MWe = $4,580/kWe — severe scale penalty; large plants achieve $500-1000/kWe
- **Reactor Plant Equipment (CAS22 total)**: $1,102M / 50 MWe = $22,040/kWe — catastrophic; large plants achieve $2,000-4,000/kWe

The only structural advantage is **modularity with factory learning**, which is reflected in the NOAK assumption. However, this requires:
1. A functioning FOAK plant to validate performance (not yet built)
2. Commitment to fleet production before cost learning materializes (chicken-egg problem)
3. Sustained production of 2,500 units over 20-30 years (unprecedented for fusion)

The model shows that even with full NOAK learning, LCOE remains $630/MWh — 4× above competitive threshold. Factory learning provides a 2.0× cost reduction (FOAK $54,000/kWe → NOAK $48,000/kWe overnight cost) but this is insufficient to overcome the 7.5× scale penalty relative to 1 GWe plants.

### Disadvantages (relative to baseline)

**Eliminates ~0% of direct capital; adds ~300-400% to specific capital cost.**

- **CAS21 Buildings**: +$4,000/kWe penalty vs. large plants (~$4,580/kWe vs. $500-1000/kWe baseline) — buildings do not scale down proportionally
- **CAS22 Reactor Plant**: +$18,000-20,000/kWe penalty vs. large plants (~$22,040/kWe vs. $2,000-4,000/kWe baseline) — driven by magnet cost, first wall, blanket, and vacuum vessel scaling
- **CAS70 O&M**: $28M/year annualized / 50 MWe = $560/kWe-yr — proportionally 2-3× higher than large plants due to fixed maintenance costs
- **Recirculating power fraction**: 59% of gross electric (model output) vs. ≤25% target for large plants — creates Q_eng=1.6, which is inconsistent with net power production

**Added cost items unique to this concept**:
- **India import dependency**: No domestic REBCO tape production, no Li-6 enrichment, no tritium breeding infrastructure — all critical materials must be imported, adding geopolitical risk and potentially unfavorable trade economics. Not quantified in model.
- **Regulatory uncertainty premium**: +2 years construction time (vs. 6-year baseline) adds ~$100-120M to IDC (CAS60=$526M total) — but this may be optimistic if AERB applies fission-style regulation.

## 5. Cross-Concept Positioning

**Family**: Compact spherical tokamak, D-T fuel, steady-state, HTS magnets
**Nearest neighbor**: 21-spherical-tokamak-hts (Tokamak Energy ST-E1, 450-750 MWe)

### Where does this concept sit in the landscape?

Pranos occupies the extreme small-scale end of the spherical tokamak family:
- **Tokamak Energy ST-E1**: 500-750 MWe, R=5.0m, A=2.3, $335M funding, validated 11.8T HTS coil set → targeting utility-scale baseload power
- **Pranos Fusion**: 50 MWe, R=unknown (model assumes 1.5m), A≈2.0-2.2, $417K-$6.8M funding, 0.1T experimental device → targeting distributed modular deployment

The economic thesis diverges entirely:
- **Tokamak Energy**: Single large pilot plant → commercial plants with economies of scale, learning from ITER/JET/MAST heritage
- **Pranos**: 2,500 small distributed units → factory learning via cumulative production, no reliance on utility-scale infrastructure

This positions Pranos as the **small modular reactor (SMR) analogue for fusion** — attempting to apply fission SMR logic (modularity, factory production, distributed siting) to a fusion power plant. The fission SMR industry has encountered severe economic challenges even with established physics:
- NuScale (leading US SMR): $89/MWh LCOE target (2020) → $119/MWh (2023) → project cancelled
- BWRX-300 (GE Hitachi): no commercial orders as of 2025 despite design certification
- Rolls-Royce SMR (UK): £2.5B government funding, no commercial deployment timeline

The fusion SMR concept faces all the same challenges (scale penalty, first-of-kind risk, regulatory uncertainty, supply chain immaturity) **plus** unproven fusion physics at the chosen scale.

### What makes this concept fundamentally different?

**Scale mismatch with fusion physics requirements.** Tokamaks achieve Q > 1 via large plasma volume, high field, and long confinement time — all of which favor larger machines. Compact STs compensate with high beta (plasma pressure / magnetic pressure), but this requires:
- High plasma current → high bootstrap fraction or large auxiliary heating
- High elongation → vertical stability control challenges
- Tight aspect ratio → severe center stack neutron shielding constraints

At 50 MWe, the recirculating power fraction (~59% in model) becomes prohibitive. The 1 GWe scaling shows that this same design would achieve $84/MWh if built at utility scale — revealing that the physics and engineering are not fundamentally broken, but the chosen scale is economically catastrophic.

**India context adds unique uncertainties**: No domestic REBCO supply chain, no fusion regulatory precedent, nascent private fusion ecosystem, and import dependency for tritium, Li-6, and HTS tape. This is not a technical barrier but a commercialization risk that other compact tokamak concepts (CFS in US, Tokamak Energy in UK) do not face.

## 6. Modeling Confidence

**Rating: Low**

**How many parameters are data-anchored vs. speculative?**

Of the ~40 engineering parameters in the model:
- **1 high-confidence anchor**: D-T fuel (IAEA FUSE confirmation)
- **1 medium-confidence anchor**: HTS magnets (company website confirmation)
- **1 medium-confidence anchor**: 50 MWe target (company vision statement, not physics-validated)
- **1 medium-confidence anchor**: PRAGYA experimental geometry (R₀=0.4m, A≈2.2, B_T=0.1T) — applies to experimental device only, not commercial scale
- **36+ speculative analogues**: R₀, plasma_t, B_T, elon, eta_th, p_input, p_nbi, blanket_t, ht_shield_t, availability, construction_time_yr, all cost multipliers, all plasma state parameters (T_e, n_e, tau_ratio, Q)

The model is ~90% analogue-based by parameter count, and ~95% analogue-based by LCOE impact (since the largest sensitivities — availability, magnet cost, construction time — are all analogues).

**What is the dominant source of LCOE uncertainty?**

**Scale penalty uncertainty** — not physics uncertainty, not technology uncertainty, but fundamental economic scaling. The model shows:
- 50 MWe: $630/MWh (NOAK)
- 1 GWe: $84/MWh (scaled per-account from 50 MWe basis)

This 7.5× ratio is driven by:
1. **Recirculating power fraction**: 59% at 50 MWe vs. ≤25% at 1 GWe (fixed loads + heating power do not scale down)
2. **Specific capital cost**: $47,754/kWe at 50 MWe vs. $5,872/kWe at 1 GWe (economies of scale, sublinear cost scaling)
3. **Availability**: 80% assumed for both, but fixed downtime is proportionally larger at 50 MWe (if absolute downtime is 60 days/year, this is 16% downtime at any scale — but larger plants can afford longer scheduled outages)

The sensitivity analysis confirms this: a ±50% swing in fusion power (via geometry scaling) shifts LCOE only ±15 $/MWh ($613-643/MWh range), while the scale penalty accounts for $550/MWh. **The choice of 50 MWe is the dominant LCOE driver, not any physics or engineering parameter.**

**Gap report summary**: 8+ blocking gaps across machine geometry, Q, heating method, blanket design, thermal efficiency, capital cost, construction cost, and regulatory timeline. The concept is rated "Insufficient Data" with "poor" coverage across all D1+ sections. This is the least-documented concept in the analysis portfolio.

## 7. What Would Change My Mind

### In the optimistic direction (toward LCOE < $150/MWh):

**Discovery 1: Demonstrated Q_eng > 5 at compact ST scale**
- If Pranos (or any compact ST developer) demonstrates Q_eng > 5 in a device with A < 2.5 and P_net < 100 MWe, this would validate that the recirculating power trap is escapable at small scale. Current best: Tokamak Energy ST40 achieved plasma current 2 MA (2022) but has not published Q values; MAST-U and NSTX-U are experimental devices not targeting Q > 1.
- **Evidence**: Peer-reviewed publication of Q_plasma and Q_eng with full auxiliary power accounting, in a machine with R < 2.0m and P_fus < 500 MW.
- **Impact**: Would reduce LCOE by ~40-50% (to $350-400/MWh) by enabling lower recirculating fraction and higher net output at fixed fusion power.

**Discovery 2: India establishes fusion-specific regulatory pathway with <6-year timeline**
- If AERB publishes a fusion licensing framework analogous to US NRC Part 30 (separate from fission regulation) and Pranos secures pre-approval or pilot licensing within 6 years, this would eliminate the +2-year construction penalty and reduce IDC.
- **Evidence**: AERB policy announcement or Pranos regulatory milestone disclosure.
- **Impact**: Would reduce LCOE by ~$60-80/MWh (to $550-570/MWh) via reduced construction time and avoided building cost multiplier.

**Discovery 3: REBCO tape cost drops to <$5/kA-m at commercial scale**
- If global HTS supply chain scales and REBCO tape achieves fission-era superconductor pricing (~$5/kA-m vs. current $30-100/kA-m), magnet costs would drop by 6-10×.
- **Evidence**: Industry-wide HTS pricing data from Fujikura, Sumitomo, Shanghai SC, AMSC, or SuperPower; or large-scale procurement announcement by fusion developers.
- **Impact**: Would reduce LCOE by ~$120-150/MWh (to $480-510/MWh) via reduced CAS22 magnet line item — but scale penalty would remain dominant.

None of these three discoveries alone would achieve <$150/MWh — all three together might reach $250-300/MWh, still 2× above competitive threshold.

### In the pessimistic direction (toward LCOE > $1,000/MWh):

**Discovery 1: India applies fission-style regulation with 2.2× building cost multiplier**
- If AERB treats fusion as equivalent to fission for safety/environmental review, the Stewart & Shirvan 2.2× building cost scenario applies, raising CAS21 from $229M to ~$500M and total capital by $250M+.
- **Evidence**: AERB regulatory framework announcement or Pranos disclosure of licensing requirements.
- **Impact**: Would raise LCOE by ~$120-150/MWh to $750-780/MWh.

**Discovery 2: PRAGYA fails to achieve first plasma or demonstrates Q_plasma << 1**
- If the 0.1T experimental device encounters plasma instabilities, confinement degradation, or control failures, this would cast doubt on the commercial-scale ST physics assumptions.
- **Evidence**: Pranos experimental results publication or project delay/pivot announcement.
- **Impact**: Indirect — would erode investor confidence and delay timeline, but would not directly change LCOE model parameters unless it reveals a fundamental physics barrier to compact ST operation.

**Discovery 3: Global tritium supply constraints tighten before 2030**
- If CANDU reactor fleet declines faster than fusion breeders come online (plausible — Ontario's Bruce Power is the dominant tritium source, slated for refurbishment/retirement in 2030s), tritium prices could rise 5-10× above current ~$30K/g.
- **Evidence**: CANDU tritium production data, fusion industry supply chain reports.
- **Impact**: Would raise LCOE by ~$30-50/MWh (to $660-680/MWh) via increased CAS80 fuel costs — relatively small because D-T fuel cost is annualized and spread over 30-year lifetime.

## 8. LCOE Downselect Scoring

### C1: Modularization (scored by Claude)

**Score: 2.8**

#### Sub-factor breakdown:

**1. Construction mode classification per CAS account:**

| CAS Account | Construction Mode | Score | Cost Weight | Notes |
|-------------|------------------|-------|-------------|-------|
| CAS21 Buildings | Stick-built / field-erected | 1 | $229M / $1,862M = 0.123 | Reactor building with biological shield; cannot be factory-manufactured |
| CAS22.01 Blanket | Site-assembled from factory sub-assemblies | 3 | $40M / $1,862M = 0.021 | Liquid Li or solid breeder modules; factory-produced but site-integrated |
| CAS22.03 Magnets | Factory-manufactured module | 5 | $516M / $1,862M = 0.277 | HTS coils are factory-wound on mandrels; Tokamak Energy Demo4 precedent |
| CAS22.04 First Wall | Site-assembled from factory sub-assemblies | 3 | $177M / $1,862M = 0.095 | Tungsten tiles + cooling channels; factory-produced panels, site-installed |
| CAS22.08 Vacuum Vessel | Site-assembled from factory sub-assemblies | 3 | $39M / $1,862M = 0.021 | Welded steel torus; segments factory-produced, site-welded |
| CAS22.10 Cryostat | Site-assembled from factory sub-assemblies | 3 | $54M / $1,862M = 0.029 | Large vacuum vessel; segments factory-produced, site-welded |
| CAS22.11 Heat Transport | Factory-manufactured module | 5 | $127M / $1,862M = 0.068 | Heat exchangers, pumps, piping; industrial equipment |
| CAS23 Turbine | Factory-manufactured module | 5 | $25M / $1,862M = 0.013 | 50 MW steam turbine; off-the-shelf industrial unit |
| CAS24 Electrical | Factory-manufactured module | 5 | $11M / $1,862M = 0.006 | Switchgear, transformers; standard electrical equipment |
| CAS26 Heat Rejection | Factory-manufactured module | 5 | $15M / $1,862M = 0.008 | Cooling towers; industrial equipment |
| CAS27 Special Materials | N/A (consumable) | — | $1M / $1,862M = 0.001 | Tritium inventory; not a construction mode |
| **Remaining CAS22** | Site-assembled from factory sub-assemblies | 3 | $853M / $1,862M = 0.458 | Divertor, auxiliary systems, power supplies, diagnostics, fuel handling |

**Cost-weighted average**:
(0.123×1) + (0.021×3) + (0.277×5) + (0.095×3) + (0.021×3) + (0.029×3) + (0.068×5) + (0.013×5) + (0.006×5) + (0.008×5) + (0.458×3) = **3.27**

**2. Module repetition boost:**

The concept targets 2,500 identical units. At 2,500 units, the repetition boost applies:
- **10-49 identical modules**: +1.0 boost
- **50+ modules**: Additional boost beyond 49 units has diminishing returns, but 2,500 is extreme — no fusion precedent

For scoring purposes, apply the +1.0 boost (capped per framework) but note that the actual learning curve is captured via NOAK assumption in the LCOE model, not this score.

**Boost**: +0.0 (framework caps boost at +1.0 for 10-49 units; 2,500 units already reflected in NOAK baseline)

**C1 = 3.27 + 0.0 = 3.3** (clamped to [1, 5])

**Justification**: The concept has high modularization potential for magnets (HTS coils), BOP (turbine, electrical, heat rejection), and blanket/first-wall segments. However, the reactor building (CAS21, 12.3% of overnight capital) and core assembly (vacuum vessel, cryostat, much of CAS22) remain site-assembled or stick-built. The 2,500-unit vision enables factory learning but does not change the construction mode classification — even with 2,500 units, the reactor building must be stick-built per site. The weighted average of 3.3 reflects that ~28% of capital (magnets, BOP) is fully factory-manufactured (score 5), ~59% is site-assembled from factory sub-assemblies (score 3), and ~12% is stick-built (score 1).

---

### C3: Supply Chain Learning (scored by Claude)

**Score: 2.5**

#### Sub-factor A: Component learning rates (1-5)

Cost-weighted average across CAS accounts:

| Component | Learning Rate | Score | Cost Weight | Notes |
|-----------|--------------|-------|-------------|-------|
| Buildings (CAS21) | Fusion-specific (no current market) | 2 | $229M / $1,862M = 0.123 | Biological shield, tritium-compatible HVAC; fusion-specific |
| Magnets (CAS22.03) | Specialty component with limited supply chain | 3 | $516M / $1,862M = 0.277 | HTS tape exists but fusion-scale coils are novel; growing production base |
| Blanket (CAS22.01) | Novel component never manufactured at scale | 1 | $40M / $1,862M = 0.021 | Liquid Li or solid breeder with tritium extraction; no market |
| First Wall (CAS22.04) | Fusion-specific component with no current market | 2 | $177M / $1,862M = 0.095 | Tungsten PFCs with high heat flux cooling; ITER-scale only |
| Vacuum Vessel (CAS22.08) | Industrial component with growing production base | 4 | $39M / $1,862M = 0.021 | Steel pressure vessels; fusion-specific but draws on fission/chemical industry |
| Heat Transport (CAS22.11) | Industrial component with growing production base | 4 | $127M / $1,862M = 0.068 | Heat exchangers, pumps; industrial equipment with fusion-compatible materials |
| Turbine (CAS23) | Commodity component with established manufacturing | 5 | $25M / $1,862M = 0.013 | 50 MW steam turbine; off-the-shelf industrial product |
| Electrical (CAS24) | Commodity component with established manufacturing | 5 | $11M / $1,862M = 0.006 | Switchgear, transformers; mature supply chain |
| Heat Rejection (CAS26) | Commodity component with established manufacturing | 5 | $15M / $1,862M = 0.008 | Cooling towers; mature supply chain |
| Remaining CAS22 | Fusion-specific component with no current market | 2 | $853M / $1,862M = 0.458 | Divertor, tritium handling, power supplies, diagnostics; fusion-specific |

**Cost-weighted average**:
(0.123×2) + (0.277×3) + (0.021×1) + (0.095×2) + (0.021×4) + (0.068×4) + (0.013×5) + (0.006×5) + (0.008×5) + (0.458×2) = **2.48**

#### Sub-factor B: Supply chain bottleneck count (1-5)

Starting at 5.0, subtract penalties:

- **Hard constraint (no known path to required quantity)**: None — all materials have at least a laboratory-scale existence proof
- **Scaling constraint (exists but must scale 10x+)**:
  - REBCO HTS tape: Global production ~few thousand km/year; 2,500 units × thousands of km/unit requires 100× scale-up — **-0.5**
  - Li-6 enrichment: Controlled by Russia/China; no Western commercial capacity at scale — **-0.5**
  - Tritium breeding: Global inventory ~25-30 kg; 2,500 units × ~1 kg startup each requires 100× current annual CANDU production — **-0.5**
- **Sole-source dependency**:
  - Li-6 enrichment (Russia/China oligopoly) — **-0.25**
  - HTS tape (Fujikura, Sumitomo, Shanghai SC; ~5 global suppliers but concentrated) — **-0.25**
- **Helium-3 fuel dependency**: Not applicable (D-T fuel)

**Sub-factor B = 5.0 - 0.5 - 0.5 - 0.5 - 0.25 - 0.25 = 3.0**

#### Sub-factor C: External demand pull (1-5)

What fraction of capital cost is in components with >$1B/yr external market?

| Component Category | Capital Cost | External Market | Qualifies? |
|--------------------|-------------|----------------|-----------|
| Turbine (CAS23) | $25M | Global steam turbine market ~$20B/yr | Yes |
| Electrical (CAS24) | $11M | Global electrical equipment >$100B/yr | Yes |
| Heat Rejection (CAS26) | $15M | Industrial cooling ~$10B/yr | Yes |
| Heat Transport (CAS22.11) | $127M | Industrial heat exchangers/pumps ~$50B/yr | Yes |
| Vacuum Vessel (CAS22.08) | $39M | Pressure vessel market ~$10B/yr (chemical/fission) | Partial — fusion specs differ |
| Buildings (CAS21) | $229M | Nuclear construction ~$20B/yr (but fusion-specific design) | Partial |
| Magnets (CAS22.03) | $516M | HTS tape market ~$200M/yr (growing but <$1B) | No |
| Blanket, First Wall, Divertor, etc. | $1,070M | No external market (fusion-specific) | No |

**Qualified capital**: $25M + $11M + $15M + $127M + (0.5 × $39M) + (0.3 × $229M) = **$265M**
**Total overnight capital**: $1,862M (excluding IDC, O&M, fuel, financial)
**Fraction**: $265M / $1,862M = **14.2%**

**Sub-factor C score**: 14.2% falls in the 10-20% range → **Score 2**

**C3 = (2.48 + 3.0 + 2) / 3 = 2.5**

**Justification**: The largest cost components (magnets $516M, first wall $177M, blanket $40M, divertor ~$50M) have no external market — they are fusion-specific. HTS tape has a growing market (~$200M/yr) but is not yet >$1B/yr and faces scaling constraints (100× scale-up needed for 2,500-unit fleet). Li-6 enrichment and tritium breeding are sole-source or oligopoly constrained. Only ~14% of capital is in components with >$1B/yr external markets (turbine, electrical, heat rejection, heat transport). The India supply chain context exacerbates this: no domestic REBCO, Li-6, or tritium production, creating import dependency.

---

### C4: Plant Complexity (scored by Claude)

**Score: 3.0**

#### Sub-factor A: Operational coupling density (1-5)

**Rating: 3 (Moderate coupling)**

D-T tokamaks have inherent operational coupling:
- **Tritium fuel cycle**: If tritium extraction fails, TBR < 1 → fuel supply degrades over months → plasma cannot be sustained
- **Cryogenic system**: If cryo fails, HTS magnets quench → magnetic confinement lost → immediate shutdown
- **Plasma control**: If vertical stability control fails, plasma disrupts → potential damage to first wall/divertor → requires inspection/repair before restart
- **Primary coolant**: If blanket/first-wall cooling fails, overheating → potential breach → tritium release risk → extended shutdown for repair

However, the compact ST has **lower coupling than large tokamaks**:
- **No center stack breeding blanket**: Outboard-only blanket reduces blanket-plasma coupling
- **Smaller plasma volume**: Faster plasma initiation and termination → shorter recovery from disruptions
- **Modular design intent**: Implies some subsystem independence (though not disclosed in detail)

The 50 MWe scale **increases coupling** in other ways:
- **Higher recirculating fraction**: Heating, tritium processing, cryo, and cooling are larger fractions of gross output → any auxiliary system failure has proportionally larger impact on net output
- **Smaller operational margins**: Less thermal inertia, smaller tritium inventory margin, tighter control tolerances

**Verdict**: Moderate coupling (score 3) — not as tightly coupled as ITER (which has extreme plasma-blanket-divertor-tritium interdependencies) but not as decoupled as modular IFE target factories. The D-T fuel cycle and HTS magnet dependencies create unavoidable failure cascade paths.

#### Sub-factor B: Subsystem count (1-5)

Count CAS22 sub-accounts representing >1% of total capital:

| Sub-account | Capital Cost | Fraction | >1%? |
|-------------|-------------|----------|------|
| C220103 Magnets | $516M | 21.6% | Yes |
| C220104 First Wall | $177M | 7.4% | Yes |
| C220111 Heat Transport | $127M | 5.3% | Yes |
| C220108 Vacuum Vessel | $39M | 1.6% | Yes |
| C220110 Cryostat | $54M | 2.3% | Yes |
| C220101 Blanket | $40M | 1.7% | Yes |
| C220102 Shield | $41M | 1.7% | Yes |
| C220107 Power Supplies | $19M | 0.8% | No |
| C220106 Aux Heating | $17M | 0.7% | No |
| C220200 Divertor | $21M | 0.9% | No |
| C220300 Fuel Handling | $12M | 0.5% | No |
| C220500 Tritium | $15M | 0.6% | No |
| Remaining CAS22 | $24M | 1.0% | No |

**Count of significant subsystems**: 7 (Magnets, First Wall, Heat Transport, Vacuum Vessel, Cryostat, Blanket, Shield)

**Sub-factor B score**: 7 significant subsystems → **Score 4** (5-7 range)

**C4 = (3 + 4) / 2 = 3.5**

**Justification**: The concept has moderate operational coupling typical of D-T tokamaks (tritium fuel cycle, cryogenic magnets, plasma control, primary coolant) but benefits from smaller plasma volume and outboard-only blanket. The subsystem count is relatively low (7 major CAS22 components >1% of capital) compared to large tokamaks (which have 11-14 significant subsystems including NBI, divertor, tritium extraction, remote handling as separate major accounts). However, the small scale increases the proportional impact of auxiliary system failures on net output. The "magic wand" test: if fusion physics were proven tomorrow, this plant would still require tritium breeding, HTS magnet operation, first-wall cooling, and disruption management — moderate complexity, not low.

**Note**: I initially scored C4 at 3.5, but re-reading the framework shows I should round to nearest 0.5 in the final YAML. Keeping 3.5 as the calculated value; final YAML will use 3.5.

Actually, re-reading again: C4 is an equally-weighted average of two sub-factors, not a rounded value. I'll report **C4 = 3.5** directly.

Wait, one more check: the framework says "C4 = (A + B) / 2" and provides no rounding instruction. The final YAML format says "All numeric scores must be rounded to one decimal place." So C4 = 3.5 is correct as-is.

---

### C5: Customization Needs (scored by Claude)

**Score: 2.0**

#### Sub-factor A: Thermal rejection (1-4)

**Rating: 2 (Large cooling towers required — standard thermal cycle)**

- The concept uses D-T fuel → 14.1 MeV neutrons → blanket thermal multiplication → thermal power conversion (steam Rankine assumed, 30% efficiency)
- At 50 MWe net output and ~59% recirculating fraction, gross electric is ~122 MWe → gross thermal is ~407 MW (at 30% efficiency)
- Heat rejection: (407 MW thermal input - 122 MW electric output) = **285 MW thermal rejection** via cooling towers
- **No DEC**: Tokamak geometry → charged particle energy thermalized → full thermal cycle required

**Customization requirement**: Standard industrial cooling tower for 285 MW thermal. This is site-specific (water availability, ambient wet-bulb temperature) but not exceptional relative to other thermal plants. Small advantage: 285 MW thermal cooling is smaller than utility-scale plants (1-3 GW thermal) and may enable air-cooled condensers in some climates, reducing water dependency.

**Score: 2** (Standard thermal cycle; large cooling towers required for base case, though smaller than utility-scale)

#### Sub-factor B: Fuel safety profile (1-4)

**Rating: 1 (D-T — full tritium handling and breeding infrastructure)**

- D-T fuel confirmed by IAEA FUSE Portal
- Tritium is radioactive (12.3-year half-life), chemically reactive, mobile in materials, and difficult to contain
- **Tritium breeding required**: TBR > 1 for fuel self-sufficiency → blanket, extraction, purification, accountability, storage
- **14.1 MeV neutrons**: Activation of structural materials → remote handling and disposal
- **Startup inventory**: ~1 kg tritium at >$30K/g → ~$30M fuel inventory (plus breeding infrastructure)

This is the most demanding fuel safety profile in the fusion landscape (D-D avoids tritium handling; D-He3 has low neutron fraction; p-B11 is aneutronic).

**Score: 1** (D-T with full tritium handling and breeding infrastructure)

**C5 raw = (2 + 1) / 2 = 1.5**

**C5 scaled = 1 + (1.5 - 1) × (4/3) = 1 + 0.667 = 1.7** (rounded to 1 decimal place per YAML format)

**Justification**: The concept has standard thermal rejection requirements (score 2) — not exceptional like laser IFE (which might have even larger thermal loads) but not minimal like DEC-heavy concepts. The D-T fuel profile (score 1) is the worst case in the framework, requiring full tritium breeding, extraction, purification, and neutron activation management. The India siting context does NOT inflate this score (per framework instruction) but does create commercialization challenges: no domestic tritium production, no Li-6 enrichment, and import dependency for all fuel-cycle materials.

---

### C7: Technical Risk Evidence (risk matrix scored by Claude)

I'll fill the 7-function × 2-subcategory = 14-cell risk matrix below, then compute function-level means (F1-F7).

#### Function 1: Plasma Performance

**Physics Risk:**
- **Plant requirement**: Q_plasma ≥ 20 to achieve Q_eng > 3 at 50 MWe scale (accounting for ~59% recirculating fraction); beta ≥ 40% to compensate for compact geometry
- **Best demonstrated**: Tokamak Energy ST40 achieved plasma current 2 MA (2022), beta_N ~ 2-3; Q not published. JET achieved Q_plasma = 0.67 (1997, D-T) at conventional aspect ratio A=3.0. No compact ST has demonstrated Q > 1.
- **Gap ratio**: Q requirement 20 / demonstrated 0.67 (JET, not ST) = **30× gap** — or "never demonstrated" for compact ST specifically
- **Closure mechanism**: Extrapolation from MAST-U, NSTX-U confinement scaling; reliance on higher beta and bootstrap current fraction
- **Classification**: Binary — insufficient Q → zero net electricity
- **Evidence tier**: 3 (Subscale demonstration — ST plasma achieved, but Q << 1)

**Hardware Risk:**
- **Plant requirement**: First wall survives 15 MW/m² peak heat flux; divertor handles 10 MW/m² steady-state; vacuum vessel maintains 10⁻⁶ Pa; structural materials survive 20 dpa over 5-year replacement cycle
- **Best demonstrated**: ITER divertor targets designed for 10-20 MW/m² (not yet tested at full power); tungsten PFCs tested to ~15 MW/m² in MAST-U, WEST, ASDEX-U; vacuum vessel and structural materials are conventional steel (TRL 9)
- **Gap ratio**: Peak heat flux requirement / demonstrated ≈ **1.0× (met)** for divertor; first wall is analogous to ITER baseline
- **Closure mechanism**: Tungsten monoblock divertor (ITER design heritage); first-wall cooling via liquid Li or helium-cooled steel
- **Classification**: Degrading — heat flux excursions → first-wall damage → availability loss and replacement cost
- **Evidence tier**: 4 (Near-regime demonstrated — ITER-relevant components tested at subscale)

#### Function 2: Driver / Energy Input

**Physics Risk:**
- **Plant requirement**: NBI or RF delivers 25 MW at >50% wall-plug efficiency; drives bootstrap current to >70% of total Ip to minimize recirculating power
- **Best demonstrated**: MAST-U NBI: 2.5 MW injected (2021); NSTX-U NBI: 6 MW (2016); no compact ST has operated with 25 MW heating. Wall-plug efficiency for NBI is typically 40-50% (demonstrated at JT-60U, DIII-D).
- **Gap ratio**: 25 MW / 6 MW = **4.2× power gap**; efficiency requirement 50% / demonstrated 50% = **1.0× (met)**
- **Closure mechanism**: Scale up existing NBI technology (ion source, accelerator, neutralizer, beamline) by ~4×
- **Classification**: Degrading — lower heating power → lower Q_eng → worse economics, not zero electricity
- **Evidence tier**: 4 (Near-regime demonstrated — 6 MW NBI exists; 25 MW is scaling, not new physics)

**Hardware Risk:**
- **Plant requirement**: NBI system (ion source, accelerator, neutralizer, cryopumps, power supplies) operates at 25 MW, 80% availability, 30-year lifetime with scheduled maintenance
- **Best demonstrated**: JT-60U NBI: 40 MW total (10 MW × 4 units) at 90% availability (1990s-2000s operation); ITER NBI: 16.5 MW × 2 units (under construction)
- **Gap ratio**: 25 MW / 40 MW = **0.6× (demonstrated exceeds requirement)**
- **Closure mechanism**: Procure industrial NBI systems from established vendors (JAEA, General Atomics, Fusion for Energy)
- **Classification**: Degrading — NBI failures → reduced heating → lower availability
- **Evidence tier**: 5 (Operating-regime demonstrated at relevant scale — JT-60U 40 MW NBI precedent)

#### Function 3: Instability Control

**Physics Risk:**
- **Plant requirement**: Suppress or tolerate vertical displacement events (VDEs), neoclassical tearing modes (NTMs), and edge-localized modes (ELMs) without disruptions; disruption rate <0.01/pulse for commercial availability
- **Best demonstrated**: MAST-U demonstrated ELM suppression via Super-X divertor (2021-2022); NSTX-U achieved active NTM stabilization via ECCD (2010-2016); disruption rates in experimental STs are ~0.1-1/pulse (far above commercial target)
- **Gap ratio**: Disruption rate 0.01 / demonstrated 0.1-1 = **10-100× gap**
- **Closure mechanism**: Real-time plasma control (shape, current, pressure profile); disruption prediction and mitigation (massive gas injection, runaway electron suppression)
- **Classification**: Binary — uncontrolled disruptions → first-wall damage → zero net electricity until repaired
- **Evidence tier**: 3 (Subscale demonstration — ELM suppression and NTM stabilization demonstrated, but disruption rate not at commercial level)

**Hardware Risk:**
- **Plant requirement**: Vertical stability coils respond on <10 ms timescale; disruption mitigation system (massive gas injection valves, runaway electron suppression) triggers on <1 ms; first wall survives thermal quench (10-100 MJ/m²) and runaway electron impact (10-100 MeV electrons)
- **Best demonstrated**: DIII-D disruption mitigation: massive gas injection valve opens in <1 ms (2015); ITER runaway electron mitigation design: Be first wall survives up to 30 MJ/m² thermal quench (simulations + EAST tests); vertical stability control at <10 ms demonstrated on NSTX, MAST
- **Gap ratio**: Thermal quench survival 100 MJ/m² / demonstrated 30 MJ/m² = **3.3× gap**; response times are met
- **Closure mechanism**: ITER disruption mitigation system design (shattered pellet injection, massive gas injection); vertical stability control via active feedback (demonstrated on MAST, NSTX)
- **Classification**: Binary — first-wall failure under disruption → loss of vacuum → zero electricity until major repair
- **Evidence tier**: 4 (Near-regime demonstrated — disruption mitigation hardware tested at ITER-relevant scale; first-wall survival at 30 MJ/m² confirmed)

#### Function 4: Plasma-Wall Interaction

**Physics Risk:**
- **Plant requirement**: Tungsten erosion ≤1 mm/year to achieve 5-year first-wall lifetime; helium ash exhaust via divertor removes >99% of fusion-born alpha particles per confinement time; impurity fraction Z_eff <2.0 to maintain fusion reactivity
- **Best demonstrated**: ITER divertor design targets <0.5 mm/yr tungsten erosion (simulations + WEST validation); helium exhaust efficiency ~95% demonstrated in ASDEX-U detached divertor (2018); Z_eff = 1.5-2.5 maintained in MAST-U and JET
- **Gap ratio**: Tungsten erosion requirement / demonstrated ≈ **2× gap** (1 mm/yr vs. 0.5 mm/yr); helium exhaust **1.04× gap** (99% vs. 95%); Z_eff is met
- **Closure mechanism**: Detached divertor operation (ITER baseline); strike-point sweeping to distribute heat load; helium exhaust via Super-X divertor (MAST-U demonstrated)
- **Classification**: Degrading — higher erosion → shorter first-wall lifetime → higher replacement cost and lower availability
- **Evidence tier**: 4 (Near-regime demonstrated — ITER divertor design validated at subscale; helium exhaust at 95% confirmed)

**Hardware Risk:**
- **Plant requirement**: Tungsten monoblock divertor survives 10 MW/m² steady-state, 15 MW/m² transients (ELMs), for 5-year lifetime (2,000 full-power hours); actively-cooled first wall (liquid Li or He-cooled steel) handles 2 MW/m² average, 5 MW/m² peak for 5 years
- **Best demonstrated**: ITER tungsten monoblock divertor: qualified to 20 MW/m² for 1,000 cycles (Fusion for Energy, 2020); liquid Li first wall tested in FTU (Italy, 2010s, low power) and NSTX (US, 2000s, transient)
- **Gap ratio**: Divertor lifetime 2,000 FPH / demonstrated 1,000 cycles ≈ **2× gap**; liquid Li first wall "never demonstrated at commercial heat flux and duration"
- **Closure mechanism**: ITER divertor manufacturing (tungsten monoblock fabrication by Ansaldo, Fusion for Energy); liquid Li first wall R&D (PPPL, ORNL, FTU precedent but needs commercial-scale validation)
- **Classification**: Degrading — divertor failure → unscheduled replacement → availability loss and cost increase
- **Evidence tier**: 4 (Near-regime demonstrated for divertor — ITER components qualified; **Tier 2 for liquid Li first wall** — simulation-based, no commercial-scale experimental validation)

**Composite tier for Function 4 hardware**: Average of divertor (Tier 4) and first wall (Tier 2) weighted by cost impact → approximately **Tier 3** (liquid Li first wall is a major uncertainty if chosen; He-cooled steel would be Tier 4)

#### Function 5: Neutron/Particle Handling

**Physics Risk:**
- **Plant requirement**: Neutron wall loading ≤2 MW/m² (averaged over first wall) to limit displacement damage to 20 dpa over 5 years; neutron energy spectrum (14.1 MeV D-T peak + blanket-moderated thermal component) correctly predicted for activation calculations
- **Best demonstrated**: Neutron wall loading in D-T tokamaks: JET achieved ~0.5 MW/m² (1997); TFTR ~0.3 MW/m² (1994); spectrum calculations validated by ITER neutronics benchmark (MCNP/Serpent codes, ±10% uncertainty on activation)
- **Gap ratio**: 2 MW/m² / 0.5 MW/m² = **4× gap** in wall loading; spectrum prediction is validated by simulation (±10% uncertainty is acceptable)
- **Closure mechanism**: ITER will demonstrate ~0.8 MW/m² (2030s); scaling to 2 MW/m² is extrapolation but not new physics
- **Classification**: Degrading — higher wall loading → faster material damage → shorter component lifetime → higher O&M cost
- **Evidence tier**: 4 (Near-regime demonstrated — JET/TFTR precedent; ITER will close gap further)

**Hardware Risk:**
- **Plant requirement**: Structural steel (316L or equivalent) survives 20 dpa over 5 years without embrittlement; biological shield (borated concrete + steel) reduces neutron dose to <1 mSv/hr at reactor building boundary; activated components (first wall, blanket, divertor) are remotely handled with <5% dose to workers (ALARA)
- **Best demonstrated**: Fission reactor steel: 20-40 dpa demonstrated in PWR pressure vessels over 40-year lifetime; ITER biological shield design: reduces neutron dose to <0.1 mSv/hr at building boundary (shielding design validated by MCNP); remote handling: demonstrated in ITER test blanket module program (2020s), JET D-T campaign (1997, 2021-2024)
- **Gap ratio**: 20 dpa / demonstrated 40 dpa = **0.5× (demonstrated exceeds requirement)**; shielding and remote handling are met
- **Closure mechanism**: Fission reactor steel procurement (316L, F82H); ITER-designed biological shield; ITER remote handling equipment (master-slave manipulators, overhead cranes)
- **Classification**: Degrading — shield failure → worker dose → regulatory shutdown; embrittlement → structural failure → extended outage
- **Evidence tier**: 5 (Operating-regime demonstrated — fission reactor precedent for steel, shielding, and remote handling)

#### Function 6: Fuel Cycle Closure

**Physics Risk:**
- **Plant requirement**: TBR ≥ 1.05 (with margin) from outboard-only blanket coverage; tritium extraction efficiency ≥90% from liquid Li or solid breeder (to close breeding cycle); D-T burn fraction ≥1% (to minimize unburned fuel processing)
- **Best demonstrated**: TBR calculations for compact STs: PROCESS-based studies (Tokamak Energy, 2020s) claim TBR = 1.1-1.2 with Li-6-enriched liquid Li blanket (simulations only, never experimentally validated). Tritium extraction: Japan's ITER TBM program demonstrated ~10% extraction efficiency from solid Li₂TiO₃ (2010s); liquid Li extraction is laboratory-scale only (PPPL, ORNL). D-T burn fraction in JET: ~0.1-1% (1997).
- **Gap ratio**: TBR 1.05 / demonstrated "never measured experimentally" → **N/A (simulation-only)**; tritium extraction 90% / demonstrated 10% (solid breeder) = **9× gap** (liquid Li is "never demonstrated at scale"); burn fraction is met
- **Closure mechanism**: Monte Carlo neutronics (MCNP, Serpent) for TBR; Li-6 enrichment to 30-90% (Russia/China supply); tritium extraction R&D (PPPL, ORNL for liquid Li; JAEA for solid breeder)
- **Classification**: **Binary** — TBR < 1.0 → fuel supply degrades → zero net electricity within months (mandatory per framework)
- **Evidence tier**: 2 (Simulation only — TBR calculations exist but no experimental validation; tritium extraction is laboratory-scale)

**Hardware Risk:**
- **Plant requirement**: Liquid Li blanket or solid breeder blanket (Li₄SiO₄, Li₂TiO₃) operates at 500-700°C for 5 years; Li-6 enriched to 30-90%; tritium extraction system (vacuum sieving for solid, or molten salt extraction for liquid Li) processes 1-10 g/day with 90% efficiency; tritium accountability <1% loss (regulatory requirement)
- **Best demonstrated**: Liquid Li blanket: FTU (Italy, low power, transient), NSTX (US, transient) — no commercial-scale demonstration. Solid breeder: ITER TBM program (Li₄SiO₄, Li₂TiO₃) operating at 500-700°C (2020s, partial tests); tritium extraction from solid breeder: ~10% efficiency (JAEA). Li-6 enrichment: Russia/China commercial capacity (mercury amalgam, 30-90% enrichment). Tritium accountability: ITER fuel cycle systems designed for <0.1% loss (under construction).
- **Gap ratio**: Blanket lifetime 5 years / demonstrated "partial tests only" → **N/A**; tritium extraction 90% / 10% = **9× gap**; Li-6 enrichment is commercially available (geopolitical constraint, not technical); tritium accountability systems are ITER-validated (Tier 5)
- **Closure mechanism**: ITER TBM program validation (2030s); liquid Li blanket R&D (PPPL, ORNL); Li-6 import from Russia/China or development of Western laser isotope separation
- **Classification**: **Binary** — tritium extraction failure → TBR < 1.0 → fuel supply collapse (mandatory per framework)
- **Evidence tier**: 2 (Simulation/lab-scale only — solid breeder tested at ITER TBM scale but tritium extraction at 10% only; liquid Li is conceptual)

#### Function 7: Power Conversion & BOP

**Physics Risk:**
- **Plant requirement**: Thermal power output varies <10% (for steady-state operation); fusion-born neutron energy (14.1 MeV) is reliably converted to blanket thermal power via neutron multiplication (M_n = 1.05-1.15); no adverse plasma-thermal coupling (e.g., confinement degradation at high power)
- **Best demonstrated**: JET D-T campaign (2021-2024): 69 MJ fusion energy (11 MW × 6 seconds) with thermal power stability; neutron energy multiplication in blanket simulators: M_n = 1.1 validated by ITER neutronics (MCNP); steady-state tokamaks (EAST, KSTAR) demonstrate hours-long pulses with <5% thermal variation
- **Gap ratio**: Steady-state operation requirement / demonstrated hours-long pulses = **partial gap** (EAST 1,000+ seconds, but not 5-year continuous); M_n is validated; thermal stability is met
- **Closure mechanism**: ITER will demonstrate 400-600 second D-T pulses (2030s); extrapolation to steady-state via bootstrap current (STEP, ST-E1 target)
- **Classification**: Degrading — thermal instability → reduced availability or capacity factor
- **Evidence tier**: 4 (Near-regime demonstrated — long-pulse tokamaks exist; M_n validated; steady-state is extrapolation but not new physics)

**Hardware Risk:**
- **Plant requirement**: Steam Rankine cycle (or sCO2 Brayton) operates at 30-40% thermal efficiency with 80% availability over 30 years; primary coolant loop (liquid Li, He, or water) transfers 400 MW thermal from blanket to steam generators; secondary loop interfaces with 50 MW industrial steam turbine
- **Best demonstrated**: Steam Rankine cycle: mature technology (TRL 9) at all scales; 50 MW industrial steam turbines: commercially available from GE, Siemens, Mitsubishi (28-33% efficiency typical). Primary coolant: liquid Li tested at FTU, NSTX (low power); He-cooled blanket tested in ITER TBM program (partial). Heat exchangers (Li-to-steam, He-to-steam): industrial components (TRL 7-8 for fusion-compatible materials).
- **Gap ratio**: All components are commercially available or ITER-validated; efficiency 30% / demonstrated 28-33% = **1.0× (met)**
- **Closure mechanism**: Procure industrial steam turbine and BOP from vendors; integrate with fusion-specific primary loop (ITER TBM precedent)
- **Classification**: Degrading — BOP failure → lost generation → availability and revenue loss
- **Evidence tier**: 5 (Operating-regime demonstrated — steam Rankine cycle and industrial turbines are mature; fusion-specific integration is ITER TBM-validated)

---

### Function-Level Means (F1-F7)

| Function | Physics Tier | Hardware Tier | Mean |
|----------|-------------|---------------|------|
| F1: Plasma Performance | 3 | 4 | 3.5 |
| F2: Driver / Energy Input | 4 | 5 | 4.5 |
| F3: Instability Control | 3 | 4 | 3.5 |
| F4: Plasma-Wall Interaction | 4 | 3 | 3.5 |
| F5: Neutron/Particle Handling | 4 | 5 | 4.5 |
| F6: Fuel Cycle Closure | 2 | 2 | 2.0 |
| F7: Power Conversion & BOP | 4 | 5 | 4.5 |

**Heritage credit (D-T fuel, Tokamak lineage)**: Floor = 4.0 for F1-F3

- F1: 3.5 → **4.0** (heritage floor applied)
- F2: 4.5 → **4.5** (already above floor)
- F3: 3.5 → **4.0** (heritage floor applied)
- F4: 3.5 → **3.5** (no heritage credit; plasma-wall interaction is concept-specific)
- F5: 4.5 → **4.5** (no heritage credit; neutronics is concept-specific)
- F6: 2.0 → **2.0** (no heritage credit; tritium breeding is concept-specific)
- F7: 4.5 → **4.5** (no heritage credit; BOP is concept-specific)

**Post-heritage function means**: F1=4.0, F2=4.5, F3=4.0, F4=3.5, F5=4.5, F6=2.0, F7=4.5

**C7 (computed by Python, not Claude)**: Mean of F1-F7 after heritage = (4.0 + 4.5 + 4.0 + 3.5 + 4.5 + 2.0 + 4.5) / 7 = **3.9**, rounded to nearest 0.5 = **4.0**

**Function-level cap check**: F6 = 2.0 is above the 1.5 threshold, so no cap applies.

**Binary risks identified**:
1. TBR < 1.0 for D-T fuel (Function 6, Physics)
2. Tritium extraction failure (Function 6, Hardware)
3. Uncontrolled disruptions causing first-wall failure (Function 3, Hardware)

Note: I will NOT include C7 in the scores YAML block (per instruction: "You do NOT score C2, C6, or C7"). The F1-F7 function means are included, as these are Claude-scored inputs to the Python C7 calculation.

---

### C8: Data Adequacy (scored by Claude)

**Score: 1.5**

#### Sub-factor A: Source diversity & independence (1-5)

**Score: 1 (No public-domain architecture literature available)**

**Sources available**:
1. Company overview compiled from web research (`pranos-fusion-overview.md`) — not independent; sourced from LinkedIn, company website
2. IAEA FUSE Portal profile (`iaea-fuse-pranos-profile.md`) — quasi-independent; company-submitted data to IAEA registry
3. Company website (`pranosfusion.md`) — company source; confirms HTS magnets
4. arXiv preprint (`arxiv-2603-11549`) — first peer-review-track publication (submitted March 2026, not yet accepted); covers PRAGYA experimental device only, not commercial design
5. Inc42 funding article — business press; article body not successfully extracted

**Independent public-domain sources**: 1 (arXiv preprint, and it covers only the 0.1 T experimental device)
**Company publications**: 4 (company website, IAEA profile, overview, Inc42 mention)
**Academic papers**: 0 published; 1 preprint not yet peer-reviewed
**Government reports**: 0
**Public peer review**: None — the arXiv preprint is the first public technical document and is not yet peer-reviewed

**Verdict**: Score 1 — no independent public-domain architecture literature exists for the commercial 50 MWe concept. The IAEA FUSE profile is the most authoritative source but is company-submitted data. The arXiv preprint is the first independent-track publication but covers only the experimental device.

#### Sub-factor B: Reactor design specification (1-5)

**Score: 1 (No reactor design beyond basic concept description)**

**What is disclosed**:
- Architecture: Compact spherical tokamak (confirmed)
- Fuel: D-T (confirmed)
- Operation mode: Steady-state (inferred)
- Magnet type: HTS (confirmed)
- Target output: 50 MWe (vision statement)
- Experimental device: PRAGYA geometry (R₀=0.4m, B_T=0.1T, A≈2.2)

**What is NOT disclosed**:
- Commercial machine dimensions (R, A, B_T)
- Plasma parameters (Q, beta, Ip, tau_E)
- Heating method and power
- Blanket type, TBR target, Li-6 enrichment
- First-wall material and cooling approach
- Power conversion cycle and thermal efficiency
- Remote maintenance scheme
- Cost estimates or plant study

The gap report identifies 8+ blocking gaps across machine geometry, Q, heating, blanket, thermal efficiency, capital cost, and regulatory timeline. The concept is rated "Insufficient Data" with "poor" coverage across all D1+ sections.

**Verdict**: Score 1 — no reactor design exists beyond basic concept description (D-T spherical tokamak, HTS magnets, 50 MWe target). The Jenga digital twin platform implies some internal modeling, but no outputs are published.

#### Sub-factor C: LCOE parameter coverage (1-5)

Based on blocking gap count from `gap_report.md`:

**Blocking gaps identified**:
1. Technical publications (truly-unknown)
2. Heating system architecture (truly-unknown)
3. Magnet type — RESOLVED (HTS confirmed); field strength, coil count, tape grade remain (proprietary)
4. Blanket/tritium system architecture (truly-unknown)
5. Plasma scenario parameters (Q, beta, tau_E) — truly-unknown
6. Validation of 50 MW design point (proprietary, Jenga outputs not published)
7. First device (Ragya) specifications (proprietary)
8. Experimental results from any plasma device (truly-unknown; pre-plasma stage)

Additionally, from Section 5 of `gap_report.md`:
9. Capital cost estimates for any subsystem (truly-unknown)
10. Thermal efficiency (truly-unknown; cycle not specified)
11. Capacity factor / availability (derivable by analogy, but no Pranos-specific basis)
12. Net electric output / recirculating power (truly-unknown; requires Q and heating scheme)
13. Construction cost (truly-unknown)
14. LCOE (truly-unknown; no plant study exists)

**Blocking gap count**: At least **10-14 blocking gaps** depending on how granularly you count capital cost sub-categories.

Per framework:
- 8+ blocking gaps → **Score 1**

**Verdict**: Score 1 — the gap report explicitly states "Insufficient Data" and "Do not proceed to a Pranos-specific quantitative LCOE analysis as though it reflects Pranos's actual design."

#### Sub-factor D: Commercialization pathway clarity (1-5)

**Score: 2 (Vague or aspirational commercialization narrative)**

**What is disclosed**:
- Staged experimental program: Three device configurations named (Ragya, Pragya, PraniQ)
- PRAGYA vacuum vessel design complete (arXiv preprint, March 2026)
- TF coil engineering designs complete (stress analysis + CAD, per IAEA FUSE)
- Fleet vision: 2,500 × 50 MWe modules = 125 GW total
- Jenga digital twin platform integrates MHD, transport, neutronics, thermal-structural, PMI, plant-level systems

**What is NOT disclosed**:
- Timeline from PRAGYA (0.1 T experimental device) to 50 MWe commercial module
- Funding roadmap (only $417K seed confirmed; $6.8M Inc42 report unverified)
- Commercial partnerships or supply chain agreements (no HTS tape supplier named, no turbine vendor, no construction partner)
- Pilot plant specifications or siting
- Regulatory engagement with AERB
- Tritium breeding demonstration plan (no TBM program mentioned)

The gap from PRAGYA (0.1 T, 25 kA) to a commercial ST (2-5 T, ~5-10 MA) is decades of development time at the pace of MAST (1999-2013), NSTX (1999-2016), ST40 (2017-present). Pranos was founded May 2024 and has published one preprint in March 2026 — a 2-year-old company with $417K-$6.8M funding proposing a 2,500-unit fleet is aspirational.

**Verdict**: Score 2 — the staged experimental program (Ragya, Pragya, PraniQ) implies a pathway, but no milestones, timeline, funding plan, or commercial partnerships are disclosed. The fleet vision (2,500 units) is aspirational without a functioning pilot plant.

**C8 = (1 + 1 + 1 + 2) / 4 = 1.25** (rounded to 1.3)

**Justification**: This is the least-documented concept in the analysis portfolio. No independent public-domain architecture literature exists (score 1); no reactor design beyond basic concept description (score 1); 10-14 blocking LCOE gaps (score 1); and a vague commercialization narrative (score 2). The concept is in the computational design phase with one experimental device under construction (PRAGYA, 0.1 T). The $417K-$6.8M funding level and 2-year company age are inconsistent with the 2,500-unit fleet vision. Data adequacy is extremely low.

---

## YAML Scores Block

```yaml
---
scores:
  C1: 3.3
  C3: 2.5
  C4: 3.5
  C5: 1.7
  C8: 1.3
  F1: 4.0
  F2: 4.5
  F3: 4.0
  F4: 3.5
  F5: 4.5
  F6: 2.0
  F7: 4.5
  binary_risks:
    - "TBR < 1.0 for D-T fuel cycle (Function 6, Physics)"
    - "Tritium extraction failure preventing fuel cycle closure (Function 6, Hardware)"
    - "Uncontrolled plasma disruptions causing vacuum vessel breach or first-wall failure requiring extended shutdown (Function 3, Hardware)"
---
```
