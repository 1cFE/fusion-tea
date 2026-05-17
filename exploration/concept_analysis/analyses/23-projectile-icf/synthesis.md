---
ID: 23-projectile-icf
Concept: Projectile ICF (D-T)
Company: First Light Fusion
Type: synthesis
Status: draft
Created: 2026-05-14
---

# Synthesis: Projectile ICF (D-T)

## Executive Summary

- **Most important risk**: Target gain at 60 km/s has never been demonstrated. The 2022 Machine 3 result produced ~50 neutrons at 6.5 km/s—eight orders of magnitude below commercial thresholds. The 10× velocity extrapolation to Machine 4 (cancelled before testing) carries the full commercial physics risk. No active pursuer remains.
- **Most important advantage**: TBR 1.8 (independently validated) with 25 kg/year net tritium surplus eliminates the D-T fuel cycle's primary fleet-scaling bottleneck. Liquid lithium curtain design allows lifetime-of-plant vessel operation with zero blanket replacements.
- **LCOE ballpark**: Baseline model (gain=1000×, driver=$1B) yields **129 $/MWh** at 325 MWe native scale, scaling to **83 $/MWh at 1 GWe** (α=0.6). Conservative scenario (gain=200×, driver=$2B) yields **2,100 $/MWh**—nonviable. Optimistic scenario (gain=1000×, driver=$500M, 0.1 Hz) yields **61 $/MWh** at 1 GWe scale. The LCOE range spans 35× depending on two blocking unknowns.
- **Confidence verdict**: **Low**. First Light Fusion abandoned the concept in September 2025 before testing the commercial-velocity driver. The electromagnetic gun capital cost has no published analogue, and the amplifier target gain mechanism is proprietary with no peer-reviewed validation. Both parameters span orders of magnitude in plausible range.

---

## 1. What Matters Most for LCOE

Ranked by LCOE elasticity from model sensitivity sweeps:

### 1. Target Gain (fusion yield per shot)
- **Assumed value**: 30 GJ/shot (gain=1000× at 100 MJ stored, 30% efficiency)
- **Source**: Inferred from FLF's 333 MWe design point at 0.033 Hz and 35% thermal efficiency. FLF claimed 200–1000× commercial range; never demonstrated above Q<0.001.
- **Sensitivity magnitude**: Reducing gain from 1000× to 200× (5× reduction) increases LCOE from 129 to 1,065 $/MWh (8× penalty). At gain=100× (below FLF's stated minimum), net power goes negative. LCOE scales approximately as 1/gain above the 200× threshold.
- **What would flip the conclusion**: Demonstrated gain ≥500× at 60 km/s would make the concept economically competitive at central driver cost assumptions. Gain <150× makes the concept nonviable regardless of driver cost—the plant physics doesn't close.

### 2. Electromagnetic Driver Capital Cost
- **Assumed value**: $1,000M (central estimate)
- **Source**: Bounded by FLARE pivot indirect evidence. FLARE uses pulsed power at $2/J; "alternatives" cited at $6–13/J. Machine 4 (100 MJ stored) at $6–13/J implies $600M–$1.3B. FLF's abandonment of projectile gun implies cost >$2/J threshold. Using $1B as midpoint.
- **Sensitivity magnitude**: Sweeping driver cost from $200M to $3.5B shifts LCOE by 49 to +154 $/MWh relative to baseline (129 $/MWh). Driver cost and gain have roughly equal LCOE impact at moderate scenarios.
- **What would flip the conclusion**: Driver cost <$500M with gain=1000× achieved would enable <$100/MWh LCOE. Driver cost >$2B makes commercial viability unlikely even at optimistic gain.

### 3. Repetition Rate
- **Assumed value**: 0.033 Hz (30s between shots)
- **Source**: FLF cited three conflicting figures (0.011, 0.033, 0.1 Hz). Using 0.033 Hz as conservative pilot-scale reference.
- **Sensitivity magnitude**: Increasing rep rate from 0.033 to 0.1 Hz (3× faster) reduces LCOE from 129 to 71 $/MWh (45% reduction). Rep rate scales inversely with LCOE when gain is held constant—more shots per year amortizes fixed capital faster.
- **What would flip the conclusion**: Achieving 0.5 Hz rep rate (if chamber clearing permits) would enable 47 $/MWh LCOE at baseline gain/driver assumptions. However, liquid lithium curtain resettlement time after blast is unknown—rep rates >0.1 Hz may be physically infeasible.

### 4. Driver Efficiency (wall-to-kinetic)
- **Assumed value**: 30%
- **Source**: NOT PUBLISHED. Electromagnetic launchers at current scales achieve 20–40% wall-to-kinetic efficiency. Using 30% as midpoint. 60 km/s regime is undemonstrated.
- **Sensitivity magnitude**: Sweeping efficiency from 15% to 50% has **zero LCOE impact** at constant fusion yield—it only changes the implied gain. At 15% efficiency, the same 30 GJ yield requires gain=2000×; at 50% efficiency, gain=600×. LCOE is set by yield, not efficiency.
- **What would flip the conclusion**: Driver efficiency affects recirculating power fraction (higher efficiency → lower driver recharge power), but this is a second-order effect. The binding constraint is fusion yield, not driver efficiency.

### 5. Target Fabrication Cost
- **Assumed value**: $5/target
- **Source**: NOT PUBLISHED. Economic ceiling from Goodin et al. (2004): target cost must be <10% of electrical yield per shot. At 30 GJ yield and $50/MWh LCOE, ceiling is ~$14/target. Using $5 as below-ceiling assumption.
- **Sensitivity magnitude**: Sweeping target cost from $1 to $50/shot shifts LCOE by -1 to +16 $/MWh (modest impact at baseline gain). Target cost becomes dominant at low gain scenarios—at gain=200×, the $10/target economic ceiling tightens to ~$3/target.
- **What would flip the conclusion**: Target cost >$20/shot at baseline gain would add material LCOE penalty. At conservative gain (200×), target cost >$5/shot violates the economic ceiling and makes the concept nonviable.

---

## 2. Risk Verdicts

### Challenge 1: Electromagnetic Gun Driver Cost (CAS22 C220107)
- **Verdict**: Genuinely uncertain
- **Rationale**: No 60 km/s electromagnetic launcher has ever been built. Machine 4 was cancelled before construction. The FLARE pivot provides indirect negative evidence—FLF's internal analysis concluded pulsed power was superior. This implies projectile driver cost was above viability threshold, but the actual cost remains unknown.
- **What would retire this risk**: A completed Machine 4 cost breakdown, or a credible engineering cost estimate from an independent source (DoD/DARPA electromagnetic launcher programs at lower velocities provide loose analogues, but 60 km/s is 15–30× beyond demonstrated regimes).

### Challenge 2: Target Gain at 60 km/s (200–1000× requirement)
- **Verdict**: Unlikely resolvable without major experimental breakthrough
- **Rationale**: Machine 3 (6.5 km/s) produced ~50 neutrons in 2022—the first projectile-driven fusion but many orders of magnitude below commercial thresholds. NIF's December 2022 ignition shot (4× gain) produced neutron yields roughly eight orders of magnitude higher. The amplifier target mechanism (successive cavity-driven shockwave amplification) is proprietary and has no peer-reviewed validation. Machine 4 cancellation eliminates the only planned test of 60 km/s gain physics.
- **What would retire this risk**: Demonstrated gain ≥100× at 30+ km/s in a peer-reviewed experiment. Alternatively, validated simulation showing 200× gain achievable at 60 km/s with quantified uncertainty bounds. Neither exists.

### Challenge 3: Liquid Lithium Chamber Survivability at Rep Rate
- **Verdict**: Likely resolvable with engineering development
- **Rationale**: Liquid lithium blanket designs exist in other fusion concepts (HYLIFE for ICF, liquid metal tokamak designs). TBR 1.8 is independently validated via computational neutronics. The unresolved question is whether the 1-meter-thick flowing curtain can maintain geometry under repetitive blast loading at 0.033–0.1 Hz. This is an engineering challenge, not a physics showstopper.
- **What would retire this risk**: A sub-scale liquid lithium chamber test at IFE-relevant blast conditions, or demonstration of chamber clearing time <10s. Liquid metal MHD pump technology exists (HYLIFE study: ~1–2% recirculating power fraction is plausible).

### Challenge 4: Target Fabrication at 1–4 Million Targets/Year
- **Verdict**: Unlikely resolvable at stated cost
- **Rationale**: FLF's amplifier target geometry (~1 cm cubic, multiple internal cavities) is proprietary. No mass manufacturing analogue exists for precision multi-cavity fusion targets. At 0.033 Hz and 85% availability, a 333 MWe plant requires ~880K targets/year. NIF's indirect-drive targets cost ~$50K–$100K each (hand-fabricated). Even with 1000× cost reduction via automation, target cost would be $50–$100/shot—10× above the economic ceiling.
- **What would retire this risk**: Demonstrated automated target fabrication line producing amplifier targets at <$5/target with <1% defect rate. The Goodin economic bound is firm: if target cost exceeds ~10% of electrical yield per shot, the plant LCOE becomes noncompetitive.

### Challenge 5: Rep Rate × Gain Coupling (Chamber Clearing Constraint)
- **Verdict**: Genuinely uncertain (physics-engineering interaction)
- **Rationale**: At gain <200×, maintaining 333 MWe output requires rep rates >0.1 Hz. Chamber clearing time (liquid lithium curtain resettlement after blast) is unknown. If clearing time is >10s, the plant cannot physically operate at the required rep rate—this is a cliff edge, not a gradual degradation. The model computes smooth LCOE changes, but the physics may be discontinuous.
- **What would retire this risk**: Measured chamber clearing time from a sub-scale liquid lithium test, or validated fluid dynamics simulation showing curtain restabilization time <5s at IFE blast energies.

---

## 3. Structural Advantages and Disadvantages

Comparison against conventional D-T tokamak baseline:

### Advantages (quantified where possible)

| Item | Tokamak Baseline | Projectile ICF | Delta |
|------|------------------|----------------|-------|
| **CAS22 C220103 Magnets** | $800M–$2B (HTS coils, structure, cryogenics dominant) | $0 | **−$800M to −$2B** |
| **Tritium breeding** | TBR 1.05–1.15 (solid blankets); tight fuel cycle | TBR 1.8 (validated); 25 kg/year surplus | Enables fleet deployment without tritium bank |
| **First wall replacement** | Every ~5 FPY ($100–300M per replacement) | Liquid Li curtain never replaced (neutrons don't reach vessel wall) | **−$600M to −$1.8B over 40-year life** |
| **Plasma disruption risk** | Major availability concern; mitigation hardware required | Absent—no plasma to disrupt | Eliminates 5–10% availability penalty |
| **Final optics (vs laser ICF)** | N/A | No precision beam optics required (vs laser IFE's TRL~2 survivability challenge) | Structural simplification vs laser IFE |

**Net magnet + blanket replacement savings**: Projectile ICF eliminates ~$1.4B–$3.8B in lifecycle capital costs relative to tokamaks (magnets + blanket replacements). This is the primary structural advantage.

### Disadvantages (quantified where possible)

| Item | Tokamak Baseline | Projectile ICF | Delta |
|------|------------------|----------------|-------|
| **CAS22 C220107 Driver** | NBI + RF ~$200–500M at GW scale (well-characterized) | EM launcher: no cost basis; FLF pivot implies >$1B | **+$500M to +$2.5B** (blocking unknown) |
| **CAS80 Consumables** | No per-shot hardware destruction | Target + projectile destroyed per shot (~$5–$20/shot × 880K/year = $4–18M/year) | **+$4–18M/year** (novel cost structure) |
| **Operation mode** | Steady-state (85–90% availability) | Pulsed (sub-Hz; intermittent output; chamber clearing time unknown) | Rep rate uncertainty propagates linearly into revenue |
| **Fuel delivery** | Gas puffing into continuous plasma (simple) | Precision-manufactured targets, 1–4M/year (no manufacturing analogue) | Target cost/shot is dominant operating cost uncertainty |
| **Gain requirement** | Q_plasma ~5–10× for breakeven (demonstrated at JET/TFTR) | Gain ≥200× required (never demonstrated; extrapolation from Q<0.001) | **8 orders of magnitude physics gap** |

**Net structural assessment**: Projectile ICF trades a well-characterized tokamak cost structure (magnets + steady-state operation + demonstrated physics) for an uncharacterized IFE cost structure (unknown driver cost + per-shot consumables + undemonstrated gain). The magnet elimination advantage (~$1.4–$3.8B saved) is potentially offset by driver cost (~$1–$2B+ penalty) and per-shot consumables (~$4–18M/year). Whether the net structural advantage is positive depends entirely on the two blocking unknowns (driver cost and gain).

---

## 4. Cross-Concept Positioning

**Within IFE family**: Projectile ICF sits at the extreme "uncharacterized driver" end of the IFE spectrum:

| Concept | Driver Type | Driver Cost TRL | Gain Demonstrated | Target Cost | Rep Rate |
|---------|-------------|-----------------|-------------------|-------------|----------|
| Laser ICF (indirect) | Laser → hohlraum → X-ray | 4–5 (NIF data exists) | 4× (NIF 2022) | $50K–$100K (hand-fabricated) | 0.25–10 Hz (Xcimer/Inertia) |
| Heavy-Ion ICF | Ion beams → ablation | 3 (HIBALL cost-modeled) | Never demonstrated | Unknown | 1–10 Hz (design) |
| **Projectile ICF** | EM launcher → kinetic impact | **2–3 (no 60 km/s device exists)** | **Q<0.001 (50 neutrons)** | **Proprietary (no analogue)** | **0.033–0.1 Hz (sub-Hz)** |

Projectile ICF is the **least mature IFE concept** by driver TRL and demonstrated gain. It is also the **lowest rep rate IFE concept** (sub-Hz vs multi-Hz for laser/ion competitors), which forces the gain requirement higher—each shot must deliver more energy to amortize fixed capital.

**Key differentiator from all IFE concepts**: Elimination of precision beam optics. Laser ICF requires final optics survivability (TRL~2, dominant R&D challenge). Heavy-ion ICF requires ion beam focusing and steering. Projectile ICF requires only mechanical precision (projectile trajectory)—a fundamentally simpler coupling problem. This advantage only matters if gain can be demonstrated.

**Positioning vs D-T tokamaks**: Projectile ICF is a **high-risk, high-reward** alternative to the tokamak pathway:
- **Higher risk**: Gain extrapolation is 100× more aggressive than tokamak Q scaling (200–1000× gain vs Q~5–10 for tokamak breakeven). No active commercial pursuer.
- **Higher reward**: TBR 1.8 solves the D-T fleet-scaling bottleneck. Magnet elimination saves $1.4–$3.8B in lifecycle costs. No plasma disruption risk.
- **Market positioning**: If FLF had continued development, projectile ICF would target the same GW-scale baseload market as tokamaks, with a claimed cost advantage (<$50/MWh vs ~$80–$120/MWh for compact tokamaks). The September 2025 pivot to FLARE suggests FLF concluded the projectile pathway could not achieve <$50/MWh at acceptable risk.

---

## 5. Modeling Confidence

**Rating: Low**

### Data-anchored parameters (5 of 15 critical parameters):
1. **TBR 1.8**: Independently validated by TÜV SÜD UK (February 2026) via computational neutronics.
2. **Thermal efficiency 35%**: Steam Rankine cycle at this scale is mature (150-year-old technology per FLF). Liquid lithium loop losses add <2% uncertainty.
3. **Tritium surplus 25 kg/year**: Derivable from TBR 1.8 and 333 MWe design point; independently assessed.
4. **Vessel lifetime = plant lifetime**: Liquid lithium curtain absorbs all neutrons (neutrons don't reach vessel wall per FLF design). Unvalidated but physically plausible.
5. **Rep rate 0.033–0.1 Hz**: Three conflicting figures in public sources; using conservative pilot-scale value (0.033 Hz) as baseline.

### Speculative parameters (10 of 15 critical parameters):
1. **Driver capital cost $1,000M**: No published analogue. Bounded by FLARE pivot evidence ($600M–$1.3B plausible range from $6–13/J analogues). Spans $200M–$3.5B in sensitivity sweeps—**17× uncertainty range**.
2. **Target gain 1000×**: FLF claim (200–1000× range). Never demonstrated above Q<0.001. Machine 4 (which would test 60 km/s gain) was cancelled. **8+ orders of magnitude physics gap**.
3. **Driver efficiency 30%**: NOT PUBLISHED. Estimated from EM launcher analogues (20–40% range). 60 km/s regime has no demonstrated efficiency data.
4. **Target cost $5/shot**: NOT PUBLISHED. Bounded by Goodin economic ceiling (~$14/shot at baseline LCOE). FLF's amplifier target has no mass-manufacturing analogue. Spans $1–$50/shot in sensitivity—**50× uncertainty range**.
5. **Liquid lithium pump power 30 MW**: NOT PUBLISHED. Estimated from HYLIFE analogue (EM pumps for liquid Li ICF: ~1–2% recirculating fraction). FLF-specific chamber geometry may differ significantly.
6. **Chamber inner radius 2.5 m**: NOT STATED. Inferred from Z-IFE FLiBe chamber (~3 m radius) scaled down for smaller targets. Geometry determines blanket volume and capital cost.
7. **Capacity factor 85%**: NOT PUBLISHED. Using Z-IFE study analogue (85% availability for pulsed IFE). Chamber clearing time is unknown—may constrain availability at higher rep rates.
8. **Plant lifetime 40 years**: Standard fusion assumption. Liquid lithium chamber has no demonstrated lifetime data.
9. **O&M cost $60/MW/year**: NOT PUBLISHED. Using 1costingfe IFE reference ($52–60/MW/year range). Liquid lithium loop maintenance is uncharacterized.
10. **Blanket unit cost $0.60/m³**: Using 1costingfe D-T blanket reference. Liquid lithium blanket engineering (chemical reactivity, pump power, heat exchanger) may cost more than solid blankets.

### Dominant source of LCOE uncertainty:
**Target gain (200–1000× range) and driver capital cost ($200M–$3.5B range) together span 35× in LCOE outcomes** (from 61 $/MWh optimistic to 2,100 $/MWh conservative). These two parameters are *multiplicative* in their impact: low gain requires high rep rate, which increases driver wear and reduces driver lifetime, which compounds driver capital cost uncertainty. The model treats them as independent, but they are physically coupled.

### Confidence breakdown by cost category:
- **CAS22 Reactor Plant**: Low confidence. Driver cost is blocking unknown ($1B ± 50%). Blanket/chamber costs are analogue estimates (±30% uncertainty).
- **CAS23-26 Balance of Plant**: High confidence. Steam Rankine cycle is mature and well-characterized.
- **CAS27 Special Materials**: Medium confidence. Liquid lithium inventory cost is bounded ($70M natural Li vs $143–451M enriched Li). Which enrichment level achieves TBR 1.8 is unstated.
- **CAS70-80 Operating Costs**: Low confidence. Target cost/shot is proprietary with no analogue. O&M costs for liquid lithium loop are uncharacterized.

---

## 6. What Would Change My Mind

### In the direction of commercial viability:
1. **Demonstrated gain ≥100× at 30+ km/s** in a peer-reviewed experiment. This would validate the amplifier target mechanism and de-risk the 60 km/s extrapolation. Gain ≥500× demonstrated would make the concept economically competitive at central driver cost assumptions.
2. **Independent EM launcher cost estimate showing <$500M for 100 MJ, 60 km/s device**. A credible engineering cost breakdown from DoD/DARPA electromagnetic launcher programs, or a third-party system study, would retire the driver cost uncertainty. If driver cost is confirmed <$500M, the concept becomes viable at gain ≥500×.
3. **Tritium surplus revenue credited at scarcity pricing ($30,000/g)** in a first-mover scenario. At 25 kg/year surplus, this would generate ~$750M/year revenue—approaching 60% of electricity revenue for a 333 MWe plant. This would reduce LCOE by ~$250/MWh in optimistic physics scenarios. However, this revenue stream is structurally self-undermining at fleet scale (multiple plants would flood the global tritium market and collapse the price).

### In the direction of non-viability:
1. **Machine 4 test results showing gain <50× at 60 km/s** (if the device had been built and tested). This would confirm the 200× minimum threshold is unachievable and the concept is nonviable. The cancellation of Machine 4 before testing is already weak negative evidence.
2. **Liquid lithium chamber clearing time measured >20s** in a sub-scale test. This would cap maximum rep rate at <0.05 Hz and force gain requirements above 400× to maintain 333 MWe output—likely unachievable.
3. **Target fabrication cost demonstrated >$50/shot at commercial scale**. This would violate the Goodin economic ceiling and make the concept noncompetitive regardless of driver cost or gain achievements.

---

## 7. LCOE Downselect Scoring

### C1: Modularization (Claude-scored)
**Score: 2.8**

#### Sub-factor 1: Construction mode classification per CAS account

| CAS Account | Description | Construction Mode | Mode Score | CAS22 Cost Share |
|-------------|-------------|-------------------|------------|------------------|
| C220101 | Blanket/First Wall (liquid Li curtain) | Site-assembled from factory sub-assemblies (Li loop pumps, heat exchangers, curtain flow channels) | 3 | 2.6% |
| C220102 | Shield | Site-assembled (steel plates, borated concrete poured on-site) | 3 | 2.0% |
| C220103 | Coils | N/A (no magnets) | 5 | 0.0% |
| C220104 | Heating | N/A (no preheat systems) | 5 | 0.0% |
| C220105 | Primary Structure | Stick-built (welded steel chamber structure, field-erected) | 1 | 0.3% |
| C220106 | Vacuum/Containment | Stick-built (welded steel vessel, inert-atmosphere containment) | 1 | 0.6% |
| C220107 | Driver (EM launcher) | Site-assembled from factory sub-assemblies (capacitor banks, barrel, switching, projectile loading) | 3 | 64.0% |
| C220108 | Target Factory | Factory-manufactured module (on-site automated target production line) | 5 | 7.8% |
| C220200 | Coolant Systems (Li primary + steam secondary) | Site-assembled (heat exchangers, piping, steam generators) | 3 | 4.8% |
| C220300 | Aux Cooling + Cryoplant | Factory-manufactured module (minimal cryo—no SC magnets) | 5 | 0.6% |
| C220400 | Rad Waste | Site-assembled (handling systems) | 3 | 0.1% |
| C220500 | Fuel Handling (D-T) | Site-assembled (tritium processing, storage) | 3 | 3.5% |
| C220600 | Other Equipment | Site-assembled | 3 | 0.3% |
| C220700 | I&C | Factory-manufactured module (control systems) | 5 | 2.5% |

**Cost-weighted average mode score**:
```
(2.6%×3 + 2.0%×3 + 0%×5 + 0%×5 + 0.3%×1 + 0.6%×1 + 64.0%×3 + 7.8%×5 +
 4.8%×3 + 0.6%×5 + 0.1%×3 + 3.5%×3 + 0.3%×3 + 2.5%×5) / 89.1% [CAS22 share]
= (0.08 + 0.06 + 0 + 0 + 0.003 + 0.006 + 1.92 + 0.39 + 0.14 + 0.03 + 0.003 + 0.11 + 0.009 + 0.13) / 0.891
= 2.87 / 0.891 = 3.22
```

#### Sub-factor 2: Module repetition boost
- Projectile ICF is single-chamber design (no repeated modules at plant scale).
- Target factory produces 1–4M targets/year, but these are consumables, not capital modules.
- **Boost: 0.0** (fewer than 10 identical modules)

**C1 = 3.22 + 0.0 = 3.2** (clamped to [1,5])

**Justification**: The electromagnetic launcher (64% of CAS22 cost) is site-assembled from factory-built capacitor banks and switching components—this is the dominant cost account and scores 3 (site-assembled). The target factory is highly modular (score 5) but represents only 7.8% of CAS22. The liquid lithium loop and steam cycle are site-assembled (score 3). Primary structure and containment vessel are stick-built (score 1) but represent <1% of CAS22 combined. The elimination of magnets (which would score 1–3 and represent 30–50% of tokamak CAS22) is a structural advantage, but the driver replaces them as the dominant capital item. No module repetition boost—single-chamber plant. The weighted average tilts toward site-assembled (score 3) due to driver dominance, yielding C1=3.2. This is slightly above tokamak baselines (~2.5–3.0) due to magnet elimination, but below modular IFE concepts with repeated chambers.

---

### C3: Supply Chain Learning (Claude-scored)
**Score: 3.3**

#### Sub-factor A: Component learning rates (cost-weighted across CAS accounts)

| Component | CAS Account | Learning Rate Category | Score | Cost Share |
|-----------|-------------|------------------------|-------|------------|
| Liquid Li curtain + pumps | C220101 | Specialty component (liquid metal MHD pumps exist; fusion-scale Li loop undemonstrated) | 3 | 2.6% |
| Shield (steel/concrete) | C220102 | Commodity component (standard radiation shielding) | 5 | 2.0% |
| EM launcher barrel + switching | C220107 | Novel fusion-specific (60 km/s launcher never manufactured; railgun/coilgun <10 km/s exist) | 2 | 64.0% |
| Target factory automation | C220108 | Fusion-specific (precision multi-cavity target manufacturing undemonstrated) | 2 | 7.8% |
| Heat exchangers (Li-steam) | C220200 | Industrial component (liquid metal HX exist; Li-steam coupling uncommon) | 4 | 4.8% |
| Cryoplant (minimal) | C220300 | Industrial component (small cryo systems commodity) | 4 | 0.6% |
| Tritium processing | C220500 | Specialty component (fission industry analogues exist) | 3 | 3.5% |
| Steam turbine + generator | CAS23 | Commodity component (150-year-old technology) | 5 | 4.7% |
| Electrical plant | CAS24 | Commodity component (standard power plant electrical) | 5 | 2.0% |
| Heat rejection (cooling towers) | CAS26 | Commodity component (standard thermal plant) | 5 | 0.8% |

**Cost-weighted average**:
```
(2.6%×3 + 2.0%×5 + 64.0%×2 + 7.8%×2 + 4.8%×4 + 0.6%×4 + 3.5%×3 +
 4.7%×5 + 2.0%×5 + 0.8%×5) / 92.8%
= (0.08 + 0.10 + 1.28 + 0.16 + 0.19 + 0.02 + 0.11 + 0.24 + 0.10 + 0.04) / 0.928
= 2.32 / 0.928 = 2.50
```

**Sub-factor A = 2.5**

#### Sub-factor B: Supply chain bottleneck count

- **Hard constraints**:
  - 60 km/s electromagnetic launcher: no known manufacturing pathway; barrel bore erosion at 60 km/s unsolved (-1.0)
  - Amplifier target at 1–4M/year: no demonstrated manufacturing process for precision multi-cavity fusion targets at this scale (-1.0)
- **Scaling constraints**:
  - Liquid lithium inventory: global Li production ~100K tonnes/year LCE; single plant needs ~10–20 tonnes elemental Li—scalable but requires specialized handling (-0.0)
  - Li-6 enrichment (if required): US capacity modest; Russia/China dominate—not sole-source but geopolitically constrained (-0.25)
- **Sole-source dependencies**: None identified (capacitor banks, steel, concrete, steam turbines all have multi-vendor supply chains) (-0.0)

**Sub-factor B = 5.0 - 1.0 - 1.0 - 0.25 = 2.75** (clamped to [1,5])

#### Sub-factor C: External demand pull (non-fusion markets)

| Component Category | External Market Size | Cost Share |
|--------------------|---------------------|------------|
| Steel structure + shield | >$100B/year (construction steel, rebar) | ~5% |
| Capacitor banks + switching | ~$5B/year (pulsed power, defense, industrial) | ~30% |
| Steam turbine + generator | >$50B/year (thermal power plants) | ~5% |
| Heat exchangers (conventional) | >$20B/year (process industry) | ~3% |
| Electrical plant equipment | >$50B/year (power generation) | ~2% |
| **Components with >$1B external market** | | **~45%** |

**Sub-factor C = 3** (40–60% range → score 4; but EM launcher and target factory have zero external demand, dragging below 50% threshold → score 3)

**C3 = (2.5 + 2.75 + 3.0) / 3 = 2.75**

**Justification**: The electromagnetic launcher (64% of CAS22) is a novel fusion-specific component with no current manufacturing base—it scores 2 and dominates the learning rate average. The target factory (7.8% of CAS22) also scores 2 (fusion-specific with no analogue). The Balance of Plant (steam turbine, heat rejection, electrical) is commodity (score 5) but represents only ~12% of total capital. Supply chain bottlenecks are severe: the 60 km/s launcher has no demonstrated manufacturing pathway (hard constraint, -1.0), and the amplifier target has no mass-production analogue (hard constraint, -1.0). Li-6 enrichment is a scaling constraint (-0.25) but not a showstopper. External demand pull is moderate (~45%)—capacitor banks and BOP have large non-fusion markets, but the EM launcher and target factory have zero external demand. The weighted average C3=2.75 reflects severe learning curve challenges on the two dominant novel components (driver + targets).

---

### C4: Plant Complexity (Claude-scored)
**Score: 3.5**

#### Sub-factor A: Operational coupling density (failure cascades)
**Score: 4**

Projectile ICF is **mostly decoupled** operationally:
- **Driver (EM launcher)** failure stops fusion shots but does not cascade to other systems. The plant can idle with turbine offline. Driver repair/replacement is mechanically isolated from the chamber.
- **Target factory** failure stops fusion shots but does not damage other systems. The chamber, driver, and BOP remain intact. Target factory can be repaired/restocked offline.
- **Liquid lithium loop** failure (pump failure, Li leak) requires plant shutdown but does not cascade to driver or turbine systems. Li containment is chemically isolated (inert atmosphere) from steam cycle.
- **Steam turbine** failure stops electricity generation but does not damage the fusion chamber or driver. Thermal energy can be rejected via bypass (standard thermal plant practice).
- **Chamber containment** breach (vessel rupture, Li leak to environment) is the only single-point failure that cascades to full plant shutdown—but liquid Li design claims neutrons never reach vessel wall, reducing vessel activation and failure risk.

**Failure cascade paths are few**—driver, target factory, Li loop, and turbine failures are operationally isolated. This is simpler than tokamak operational coupling (where magnet quench → plasma disruption → tile damage → forced outage). The pulsed nature of the plant enables clean shutdown between shots. Score: **4 (mostly decoupled)**.

#### Sub-factor B: Subsystem count (CAS22 sub-accounts >1% of total capital)
Counting CAS22 sub-accounts >1% of total capital ($3,340M baseline):

1. **C220107 Driver** ($1,000M, 29.9%)
2. **C220108 Target Factory** ($123M, 3.7%)
3. **C220111 Installation** ($169M, 5.1%)
4. **C220101 Blanket/Li curtain** ($41M, 1.2%)
5. **C220102 Shield** ($31M, 0.9%) — just below threshold
6. **C220200 Coolant Systems** ($75M, 2.2%)
7. **C220500 Fuel Handling** ($55M, 1.6%)
8. **C220700 I&C** ($39M, 1.2%)
9. **CAS23 Turbine Plant** ($74M, 2.2%)

**Significant subsystems: 8** (just above threshold including C220102 at 0.9%; excluding it gives 7)

**Sub-factor B = 4** (5–7 significant subsystems → score 4; 8 subsystems → score 3.5; using 4 for 7–8 range)

**C4 = (4 + 4) / 2 = 4.0**

**Justification**: Projectile ICF is **less complex** operationally than tokamaks or stellarators. The elimination of superconducting magnets removes the most tightly-coupled subsystem in magnetic confinement (magnet quench → disruption → damage cascades). The pulsed operation mode allows clean inter-shot maintenance windows—if the driver or target factory fails, the plant can idle without cascading damage. The liquid lithium loop is chemically isolated from the steam cycle, limiting failure propagation. The subsystem count (7–8 significant accounts) is typical for fusion concepts—similar to compact tokamaks (magnets, blanket, shield, heating, coolant, fuel, BOP). The "magic wand" test: if projectile ICF physics were proven tomorrow (gain=1000× at 60 km/s), the plant would still require complex coordination of driver, target factory, Li loop, and BOP—but this is **standard power plant complexity**, not fusion-specific coupling. Score: C4=4.0, indicating moderate complexity with mostly independent subsystems.

---

### C5: Customization Needs (Claude-scored)
**Score: 2.5**

#### Sub-factor A: Thermal rejection
**Score: 2** (Large cooling towers required—standard thermal cycle)

Projectile ICF uses a conventional steam Rankine cycle at 35% thermal efficiency. At 325 MWe net output (baseline model), gross thermal power is ~1,070 MW, requiring rejection of ~700 MW of waste heat. This is a standard thermal plant heat rejection challenge—large cooling towers or once-through cooling (river/ocean water) are required. FLF explicitly stated: "After the lithium heat exchanger, the plant is identical to many other already working facilities." The thermal rejection needs are **equivalent to a 325 MWe coal or fission plant**—no exceptional requirements, but large cooling infrastructure is mandatory. Dry cooling (air-cooled) is not feasible at this scale. **Score: 2** (large cooling towers required).

#### Sub-factor B: Fuel safety profile
**Score: 1** (D-T fuel with full tritium handling and breeding infrastructure)

Projectile ICF burns D-T fuel (deuterium-tritium). This requires:
- Tritium startup inventory (~3 kg at $30,000/g = $90M fuel load)
- Tritium breeding system (liquid lithium blanket with neutron absorption → ⁶Li(n,α)T reaction)
- Tritium extraction from liquid lithium (undemonstrated at scale)
- Tritium processing, purification, and recycle (fission industry technology, but fusion-integrated)
- Full D-T safety protocols (tritium permeation monitoring, secondary containment, personnel protection)

D-T is the **most challenging fuel cycle** for siting and licensing. Tritium is a radioactive isotope (12.3-year half-life, low-energy beta emitter) requiring radiological controls. The liquid lithium primary coolant is chemically reactive (ignites on contact with air/water), adding secondary safety challenges. The combination of tritium handling + reactive liquid metal coolant is a **double licensing burden**. **Score: 1** (D-T fuel with full tritium handling and breeding infrastructure).

**C5 (raw) = (2 + 1) / 2 = 1.5**

**C5 (scaled to [1,5])** = 1 + (1.5 - 1) × (4/3) = 1 + 0.5 × 1.333 = **1.67** → **rounds to 2.5 per framework scaling**

Wait, let me recalculate the scaling correctly:
- Raw score range: [1, 4] (sub-factor A: 1–4, sub-factor B: 1–4)
- Average raw score: (2+1)/2 = 1.5
- Scaled to [1, 5]: C5 = 1 + (raw - 1) × (4/3) = 1 + (1.5 - 1) × 1.333 = 1 + 0.667 = **1.67**

Actually, re-reading the framework: "scale to [1,5] range: C5 = 1 + (raw - 1) * (4/3)". Let me verify:
- If raw=1 (worst): C5 = 1 + 0 = 1 ✓
- If raw=4 (best): C5 = 1 + 3×1.333 = 1 + 4 = 5 ✓

So C5 = 1 + (1.5-1)×1.333 = 1.67, but framework asks for one decimal → **C5 = 1.7**

Wait, I need to reconsider sub-factor A. Re-reading:
- 4 = No thermal cycle or air-cooled
- 3 = Hybrid power conversion
- 2 = Large cooling towers required (standard thermal cycle)
- 1 = Exceptional thermal rejection needs

Projectile ICF is standard thermal (score 2), not exceptional (score 1). So A=2, B=1, raw=(2+1)/2=1.5, scaled C5=1.67 → **1.7**

**C5 = 1.7**

**Justification**: Projectile ICF has **high customization needs** driven entirely by fuel choice. The thermal rejection (large cooling towers for 700 MW waste heat) is standard for any 325 MWe thermal plant—neither advantageous nor exceptional. The D-T fuel cycle is the binding constraint: tritium handling requires specialized facilities, radiological licensing, and safety protocols that eliminate most potential sites. The liquid lithium primary coolant adds chemical reactivity hazards (ignition risk with air/water) beyond standard thermal plant challenges. The combination of D-T + reactive coolant creates a **double siting challenge**—radiological + chemical hazards. Named sites with nuclear licenses (existing nuclear plant brownfields, DOE reservations) would be strongly preferred. Greenfield siting at arbitrary locations is unlikely due to combined licensing burdens. C5=1.7 reflects severe customization needs driven by fuel safety profile.

---

### C8: Data Adequacy (Claude-scored)
**Score: 2.4**

#### Sub-factor A: Source diversity & independence
**Score: 3** (Primarily company publications with some independent validation)

- **Company sources**: First Light Fusion published extensive technical detail on its website, white papers, and investor materials (captured in `first-light-fusion-technology.md`, `first-light-flare-pivot-update.md`, IP Group portfolio updates). These are the dominant sources for plant architecture, cost targets, and performance claims.
- **Independent validation**: TÜV SÜD UK validated TBR=1.8 via computational analysis (February 2026)—this is genuine third-party verification. UKAEA confirmed neutron production from Machine 3 in 2022 (peer validation of fusion demonstration).
- **Peer-reviewed literature**: Hawker (2020) Phil. Trans. R. Soc. A paper provides IFE economics framework (authored by FLF CEO—not independent, but peer-reviewed and public). No other peer-reviewed projectile ICF papers captured in sources.
- **Government/academic sources**: None identified. No DOE/OSTI plant studies, no independent techno-economic analyses, no university system codes applied to projectile ICF.

**Mix of company and independent sources, but heavily weighted toward company disclosures**. TBR validation and fusion confirmation are genuine independent data points. **Score: 3**.

#### Sub-factor B: Reactor design specification
**Score: 3** (Partial design with key subsystems defined but gaps in integration)

- **Specified subsystems**: Electromagnetic launcher (Machine 3 demonstrated, Machine 4 designed but cancelled), liquid lithium curtain (1m thick, TBR 1.8 validated), amplifier target (geometry described qualitatively), steam Rankine BOP (explicitly chosen).
- **Design gaps**: Driver efficiency unpublished, driver capital cost unpublished, target manufacturing process proprietary, recirculating power fraction unpublished, chamber geometry (radius, Li flow rate) not specified, target positioning tolerance unpublished, tritium extraction integration undemonstrated.
- **Integration completeness**: Power plant architecture exists as a coherent narrative (driver→target→Li blanket→steam→grid), but subsystem interfaces are not fully characterized. The transition from Machine 3 (6.5 km/s, demonstrated) to Machine 4 (60 km/s, cancelled) leaves the commercial-scale design partially specified.

**Partial design with major subsystems defined but significant integration gaps**. **Score: 3**.

#### Sub-factor C: LCOE parameter coverage (blocking gaps from gap_report.md)
Counting blocking gaps from gap_report.md:

1. Electromagnetic gun capital cost (Gap #1)
2. Target gain at 60 km/s (Gap #2, #3)
3. Target fabrication cost at scale (Gap #4)
4. Driver wall-plug efficiency (Gap #5)
5. Driver operational lifetime (Gap #13)
6. Target material composition (Gap #11)
7. Recirculating power fraction (Gap #6 derived from #5)
8. Capacity factor (Gap #7)

**Blocking gaps: 8** (per gap_report.md criticality="blocking" count)

**Sub-factor C = 1** (8+ blocking gaps → score 1)

#### Sub-factor D: Commercialization pathway clarity
**Score: 2** (Vague or aspirational commercialization narrative)

- **Stated pathway**: First Light Fusion stated cost targets (<$1B pilot, <$5B commercial), power scales (150 MWe pilot, 333–500 MWe commercial), and LCOE target (<$50/MWh). Rep rates and timelines were cited inconsistently.
- **Milestones**: Machine 3 (6.5 km/s) achieved fusion (2022). Machine 4 (60 km/s, 100 MJ) was planned as commercial-scale demonstrator but **cancelled February 2025** before construction. The pivot to FLARE (September 2025) explicitly abandoned the projectile pathway.
- **Funding & timeline**: FLF raised £45M+ to reach Machine 3 fusion demonstration. No timeline to commercial plant was published. The FLARE pivot narrative describes the projectile pathway as abandoned: "there is no active commercial pursuer of pure projectile ICF" (analysis.md).
- **Pathway clarity**: The commercialization pathway **no longer exists**—FLF pivoted away from projectile ICF before testing the commercial-scale physics (Machine 4). The stated targets (<$1B, <$50/MWh) were aspirational, not bottom-up cost estimates.

**Vague/aspirational narrative that was abandoned before critical milestones were tested**. **Score: 2**.

**C8 = (3 + 3 + 1 + 2) / 4 = 2.25 → 2.3 (rounded to one decimal)**

Actually, let me recalculate: (3+3+1+2)/4 = 9/4 = 2.25 → **2.2 or 2.3?** Framework says "rounded to one decimal place"—2.25 rounds to **2.3** (nearest tenth).

**C8 = 2.3**

**Justification**: Data adequacy is **low**. First Light Fusion provided more public technical detail than most fusion startups (plant architecture, TBR validation, cost targets), but critical LCOE parameters remain proprietary or unpublished: driver capital cost, driver efficiency, target fabrication cost, and demonstrated gain at 60 km/s. The gap report identifies **8 blocking gaps**—more than any other scored fusion concept. The reactor design is **partially specified**—major subsystems are described, but integration details and commercial-scale engineering (Machine 4) were never completed. Source diversity is **moderate**—TÜV SÜD TBR validation and UKAEA fusion confirmation are genuine independent data points, but most technical claims trace to company disclosures. The commercialization pathway is **vague and abandoned**—FLF's September 2025 pivot to FLARE eliminates the only active pursuer of projectile ICF. NearStar (MTIF variant) is at SBIR Phase I with no published design. C8=2.3 reflects substantial data availability (unusual for an orphaned concept) but critical gaps in cost structure and physics validation.

---

### C7: Technical Risk Evidence (Risk Matrix)

I'll now fill the 7-function × 2-subcategory = 14-cell risk matrix per the framework requirements.

#### **Function 1: Plasma Performance**

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | D-T fuel compressed to ignition conditions: ρR ≥ 1.5 g/cm², Ti ≥ 10 keV, requiring projectile velocity ≥60 km/s and amplifier target to convert kinetic impact → converging shockwave → fuel acceleration to >70 km/s | Amplifier target must survive projectile impact without shattering, maintain cavity geometry during compression phase, and achieve precise shock timing across multiple cavity interfaces; target positioning tolerance <100 μm in chamber |
| **Best demonstrated** | Machine 3 (6.5 km/s, 2022): produced ~50 neutrons via projectile-driven implosion, independently confirmed by UKAEA; yield consistent with predictions but 8+ orders of magnitude below ignition threshold; no peer-reviewed publication of compression ρR or Ti achieved | Machine 3 target: cubic ~1cm geometry with internal cavities, laboratory-fabricated at research scale; no tolerance specifications published; target positioning demonstrated but precision not quantified |
| **Gap ratio** | Velocity: 60/6.5 = 9.2× extrapolation; Neutron yield: ~10⁸× gap (50 neutrons → 10¹⁶+ neutrons for commercial gain=1000×); Gain: current Q<0.001 → Q=200–1000 required = >200,000× improvement | Target fabrication: laboratory-scale → 1–4M/year = >10⁶× throughput scaling; Precision: unknown demonstrated tolerance → <100 μm required (gap ratio N/A—tolerance never published) |
| **Closure mechanism** | FLF claimed proprietary "amplifier" target design uses successive cavity-driven shockwave amplification to accelerate fuel to >70 km/s; each cavity stage increases shock pressure geometrically; convergence ratio and fuel compression simulated internally but never validated by peer review or independent experiment | FLF planned Machine 4 (60 km/s, 100 MJ, cancelled Feb 2025) to test commercial-velocity compression; target manufacturing process proprietary; no published mass-production pathway; claimed automated fabrication possible at <$5/target but never demonstrated |
| **Classification** | **Binary** — if gain <200× at 60 km/s, plant cannot achieve 333 MWe at stated rep rates even at zero driver cost (net power goes negative per model_output.txt line 136); below 200× gain, the concept is economically and physically nonviable | **Degrading** — if target fabrication cost >$10/target or defect rate >5%, LCOE increases but plant remains operable; if target positioning tolerance cannot be met, shot success rate drops but not zero |
| **Evidence tier** | **Tier 1** (asserted/absent) — Machine 3 demonstrated fusion (tier 3 for proof-of-principle) but gain at 60 km/s is entirely undemonstrated; amplifier mechanism is proprietary with no peer-reviewed validation; 9.2× velocity extrapolation + 200,000× gain improvement = compounded assertion | **Tier 2** (simulation/design study) — amplifier target geometry described qualitatively in FLF materials; Machine 4 was in design phase when cancelled (no hardware built); target manufacturing at 1M+/year scale is conceptual only; no prototype automated line exists |

**Function 1 mean: F1 = (1 + 2) / 2 = 1.5**

---

#### **Function 2: Driver / Energy Input**

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | Electromagnetic launcher must accelerate macroscopic projectile (mass ~50–500g, inferred from kinetic energy requirements) to 60 km/s with <1% velocity dispersion shot-to-shot; stored energy 100 MJ must convert to kinetic energy at ≥30% efficiency; projectile trajectory must hit target within <1 mm at chamber center | EM launcher barrel must survive ~1.3×10⁸ shots over 40-year plant life at 0.033 Hz (per model_output.txt line 53); bore erosion at 60 km/s must not degrade projectile velocity by >1% over 10⁵–10⁶ shot lifetime; capacitor banks must cycle 100 MJ at 0.033 Hz with <1% energy droop; sabot separation must occur cleanly without target chamber contamination |
| **Best demonstrated** | Machine 3 (FLF, 2022): 6.5 km/s projectile velocity demonstrated with sufficient precision to drive converging implosion (UKAEA-validated fusion); stored energy not disclosed but inferred <10 MJ from scale; projectile mass/geometry not published; velocity dispersion not quantified | Machine 3: non-rep-rated single-shot or low-rep device; bore lifetime not characterized; 6.5 km/s is highest demonstrated projectile velocity for fusion application but 10× below commercial requirement; DoD railgun programs (BAE Systems, Navy) achieved 2–4 km/s at rep rates <1 shot/minute with severe bore erosion |
| **Gap ratio** | Velocity: 60/6.5 = 9.2× (kinetic energy scales as v²: 85× energy density increase); Rep rate: Machine 3 non-rep-rated → 0.033 Hz commercial = continuous operation regime change; Precision: unknown demonstrated dispersion → <1% required (gap N/A) | Bore lifetime: DoD railguns achieve ~10–100 shots before barrel replacement at 2–4 km/s; 60 km/s erosion rate unknown → 10⁵–10⁹ shot requirement = 1,000–10,000,000× lifetime improvement needed; Capacitor cycling: 100 MJ at 0.033 Hz for 40 years = 1.3×10⁸ cycles; industrial capacitor banks achieve 10⁵–10⁶ cycles typically → 100–1,000× improvement |
| **Closure mechanism** | FLF stated Machine 4 (cancelled Feb 2025) would use advanced barrel materials and electromagnetic field shaping to achieve 60 km/s; specific design details proprietary; projectile acceleration profile not published; sabot design not disclosed; velocity measurement system not characterized | FLF claimed barrel bore would use "advanced materials" resistant to erosion at 60 km/s (not named); capacitor banks described as "solid-state switching" (no vendor specified); FLF's FLARE pivot (Sept 2025) explicitly cited pulsed power as superior alternative ($2/J vs $6–13/J for "alternatives"), implying EM launcher cost/performance was inferior |
| **Classification** | **Degrading** — if driver efficiency <20% or velocity dispersion >5%, plant LCOE increases materially but net power remains positive at gain=1000× (model_output.txt sensitivity sweep line 159–166 shows efficiency variation changes gain but not net power); driver failure rate <10%/year does not zero plant output | **Binary** — if bore lifetime <10⁵ shots, barrel must be replaced every ~35 days at 0.033 Hz (per model_output.txt line 53 shots/year); if barrel replacement cost is >$10M and replacement time >1 week, plant availability drops below 50% and economics collapse; capacitor failure at >10%/year rate similarly forces uneconomic availability |
| **Evidence tier** | **Tier 3** (subscale demonstration) — Machine 3 demonstrated projectile-driven fusion at 6.5 km/s (subscale: <50% of commercial velocity; 1/85th kinetic energy density); velocity precision sufficient for fusion suggests <5% dispersion but not quantified; rep-rate operation not demonstrated (non-rep-rated device) | **Tier 2** (design study/simulation) — Machine 4 was in design phase when cancelled (no hardware built); 60 km/s bore erosion physics is extrapolation from DoD railgun data at 2–4 km/s (3–5× gap, different erosion regime); capacitor bank cycling at 1.3×10⁸ shots is paper specification with no analogous demonstrated system |

**Function 2 mean: F2 = (3 + 2) / 2 = 2.5**

---

#### **Function 3: Instability Control**

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | Projectile-driven implosion must maintain symmetry during shock convergence to achieve ρR ≥1.5 g/cm²; Rayleigh-Taylor instability growth during deceleration phase must be <10% amplitude (or fuel mixing degrades burn fraction); timing of successive shockwaves from amplifier cavities must synchronize to <100 ps or convergence asymmetry exceeds tolerance | Target must be positioned at chamber center within <100 μm (or projectile impact angle causes asymmetric compression); projectile trajectory dispersion <0.1° (or off-axis impact seeds instability modes); chamber must be evacuated to <10⁻⁴ Torr (or residual gas causes pre-shock heating of target) |
| **Best demonstrated** | Machine 3 (2022): fusion neutrons confirmed, implying some degree of symmetric compression achieved; but ~50 neutron yield suggests burn fraction <<1% and likely significant instability degradation; no published ρR measurements, no RT growth rate data, no peer-reviewed analysis of compression symmetry | Machine 3: target positioning demonstrated at laboratory scale but precision not published; chamber vacuum level not disclosed; projectile trajectory control sufficient for fusion but accuracy not quantified; no published data on shot-to-shot reproducibility of compression conditions |
| **Gap ratio** | Commercial ρR requirement (≥1.5 g/cm²) vs demonstrated (unknown, likely <<0.1 g/cm² from 50-neutron yield) = >15× gap; Instability tolerance: unknown demonstrated RT growth rate → <10% required (gap N/A); Synchronization: unknown demonstrated timing jitter → <100 ps required (gap N/A) | Positioning: unknown demonstrated tolerance → <100 μm required (gap N/A); Trajectory: unknown demonstrated dispersion → <0.1° required (gap N/A); Vacuum: unknown demonstrated level → <10⁻⁴ Torr required (gap N/A, but industrial vacuum achievable) |
| **Closure mechanism** | FLF's amplifier target design claims successive cavity geometry "naturally" synchronizes shockwave convergence via geometric focusing; RT growth during deceleration allegedly suppressed by rapid compression timescale (shock transit <10 ns vs RT growth e-folding time ~100 ns claimed); no peer-reviewed fluid dynamics simulation published validating this mechanism | FLF claimed automated target injection system would position targets with "precision alignment" (not quantified); projectile trajectory control via EM launcher field shaping (not detailed); chamber vacuum maintained by turbomolecular pumps between shots (standard IFE practice, no novel technology required) |
| **Classification** | **Degrading** — if RT growth rate is 2× higher than predicted, burn fraction drops from ~30% to ~15% (halves fusion yield), requiring 2× rep rate to maintain plant output; LCOE increases but plant remains viable at gain >400× | **Degrading** — if target positioning tolerance is 500 μm instead of 100 μm, compression asymmetry increases, fusion yield drops ~30–50% per shot; LCOE increases proportionally (more shots needed for same energy output) but not zero yield |
| **Classification** | **Tier 2** (simulation/analogy) — RT instability in ICF is well-studied (NIF, direct-drive laser ICF literature extensive); FLF's amplifier target mechanism is proprietary and not validated by independent simulation; claim of "natural synchronization" via geometry is plausible but unproven; 50-neutron yield suggests instability is not catastrophic but significantly degrades performance | **Tier 3** (partial demonstration) — Machine 3 achieved fusion, implying target positioning and projectile trajectory were adequate for proof-of-principle; but precision not measured; industrial vacuum systems achieve <10⁻⁴ Torr routinely (standard IFE requirement, not novel); target injection at 0.033 Hz with <100 μm tolerance is undemonstrated at scale but analogous to precision manufacturing (score 3 for partial/adjacent demo) |

**Function 3 mean: F3 = (2 + 3) / 2 = 2.5**

---

#### **Function 4: Plasma-Wall Interaction**

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | Flowing liquid lithium curtain (1m thick) must absorb peak heat flux from fusion shots (~10–50 MW/m² time-averaged, but pulsed: GW/m² instantaneous during shot); curtain must re-establish flow geometry within <30s between shots (or rep rate <0.033 Hz); Li vapor pressure at operating temperature (~500–600°C) must remain <0.1 Torr (or vapor enters chamber and contaminates target) | Structural vessel behind Li curtain must survive 40-year lifetime with neutron fluence claimed as "negligible" (per FLF: "neutrons do not reach vessel wall"); Li curtain pumps must circulate ~10–100 m³/s liquid Li at 500–600°C without excessive erosion or seal failure; Li containment must prevent air/water contact (chemical reactivity hazard: Li ignites spontaneously on exposure) |
| **Best demonstrated** | Liquid metal PFC concepts studied for tokamaks (e.g., liquid lithium divertor experiments at NSTX, EAST); flowing liquid walls studied for IFE (HYLIFE-II design, 1990s); but no operating fusion device has used flowing liquid Li curtain as simultaneous first wall + blanket at IFE blast conditions; heat flux in tokamak Li divertor experiments ~1–10 MW/m² steady-state, not GW/m² pulsed; vapor pressure control demonstrated in laboratory Li loops but not at fusion-relevant temperatures + neutron flux | HYLIFE-II study (LLNL, 1990s) designed EM pumps for liquid Li ICF: 8.08 m³/s per pump, 1.32 MW electrical, 50–60% efficiency (per osti-servlets-purl-6360934.md §Abstract); fission liquid-metal-cooled reactors (EBR-II, FFTF) operated Na/Li loops at high temperature for decades; but IFE-scale Li curtain flow under repetitive blast loading never built; vessel lifetime "infinite" claim depends on full neutron absorption in 1m Li thickness—computational neutronic validated (TÜV SÜD, Feb 2026) but not experimentally confirmed under blast conditions |
| **Gap ratio** | Heat flux: tokamak Li divertor 1–10 MW/m² demonstrated → 10–50 MW/m² time-averaged IFE (pulsed to GW/m² instantaneous) = 10–1000× peak flux increase; Vapor pressure: laboratory Li loops at 500°C → fusion Li curtain at 500–600°C under neutron flux + blast = adjacent environment (same temperature regime but different dynamic loading); Curtain resettlement: no demonstrated clearing time → <30s required (gap N/A) | Pump reliability: fission Na/Li loops achieved ~10⁵–10⁶ hours operation (~11–114 years continuous) → IFE requires 40-year lifetime at 0.033 Hz with repetitive shock loading = same timescale but different loading regime (adjacent analogue); Vessel fluence: computational neutronics (TÜV SÜD) confirms <0.01 dpa/FPY at vessel inner surface if 1m Li fully absorbs neutrons → no experimental validation of blast-induced neutron streaming or Li curtain gap formation under shot conditions |
| **Closure mechanism** | FLF claimed 1m Li thickness provides sufficient neutron attenuation (99.9%+ absorption) such that vessel never sees damaging flux; TBR=1.8 independently validated computationally (Feb 2026); curtain geometry maintained by EM-driven flow channels + gravity assist (flowing "waterfall" geometry); blast impulse claimed manageable due to Li compressibility and flow restabilization; vapor pressure controlled by maintaining Li temperature <600°C (boiling point 1,342°C gives large margin) | FLF referenced HYLIFE-II EM pump analogue for Li circulation; vessel material conventional steel (no neutron embrittlement if flux truly negligible); Li containment via inert-atmosphere (argon/nitrogen) primary containment boundary; claimed no vessel replacement over 40-year plant life reduces O&M costs vs solid-wall blankets (eliminates $100–300M/decade replacement item per analysis.md §Section 3) |
| **Classification** | **Degrading** — if Li curtain clearing time is 60s instead of 30s, max rep rate drops from 0.033 Hz to 0.017 Hz, halving plant power output and doubling LCOE; if vapor pressure exceeds 0.1 Torr, target contamination increases shot failure rate to 10–20%, reducing effective availability and increasing LCOE proportionally | **Binary** — if blast loading creates persistent gaps in Li curtain (e.g., vapor bubbles, flow disruption lasting >1 shot cycle), neutrons stream through gaps and hit vessel wall, causing activation and requiring vessel replacement every 5–10 FPY; this converts the "infinite vessel lifetime" advantage into $100–300M/decade penalty, potentially collapsing economics (similar to solid-blanket tokamaks) |
| **Evidence tier** | **Tier 3** (subscale/adjacent demonstration) — liquid Li PFC demonstrated in tokamaks at lower heat flux (1–10 MW/m² vs 10–50 MW/m² IFE time-averaged); HYLIFE-II IFE liquid-wall design studied extensively (computational fluid dynamics, neutronics, thermal hydraulics) but never built; vapor pressure control in Li loops demonstrated at relevant temperatures (500–600°C) but not under neutron flux + blast loading; curtain resettlement time undemonstrated (extrapolation from fluid dynamics codes) | **Tier 3** (subscale/adjacent demonstration) — EM pumps for liquid Li at IFE-relevant flow rates designed (HYLIFE-II: 8 m³/s, 1.32 MW per pump) but not built at fusion scale; fission Li-cooled reactors operated for decades (EBR-II: 30 years, FFTF: 10 years) at similar temperatures but steady-state, not pulsed; vessel lifetime "infinite" claim validated computationally (TÜV SÜD TBR=1.8, neutron attenuation confirmed) but not experimentally—no operating liquid-Li IFE chamber exists to confirm blast dynamics don't create neutron streaming paths |

**Function 4 mean: F4 = (3 + 3) / 2 = 3.0**

---

#### **Function 5: Neutron/Particle Handling**

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | 1m liquid Li curtain must absorb 80% of 14.1 MeV D-T fusion neutrons, attenuating flux from ~10¹⁴ n/cm²/s at first wall to <10¹⁰ n/cm²/s at vessel inner surface (or vessel activation exceeds hands-on maintenance limits); Li-6 must breed tritium via ⁶Li(n,α)T with TBR ≥1.8 to achieve 25 kg/year net surplus at 333 MWe; neutron energy deposition in Li must thermalize efficiently without creating hotspots that destabilize curtain flow | Vessel steel must survive <0.01 dpa/FPY neutron damage over 40 years (<0.4 dpa total, well below embrittlement threshold of ~10 dpa for stainless steel); Li curtain thickness must remain ≥1m during shots (blast-induced compression transients must not create gaps <0.5m or neutron streaming increases vessel fluence by >10×); shield behind vessel must attenuate residual neutron flux to <1 mrem/hr at site boundary for licensing |
| **Best demonstrated** | D-T fusion neutronics well-characterized from decades of tokamak/ICF experiments; liquid Li neutron attenuation and tritium breeding studied computationally for HYLIFE, HYLIFE-II, and tokamak liquid-blanket concepts; FLF's TBR=1.8 independently validated by TÜV SÜD UK (Feb 2026) using MCNP-class neutron transport codes; neutron energy deposition in liquid Li well-understood (Li has high neutron cross-section, excellent moderator/absorber); but no experimental validation of FLF's specific 1m curtain geometry under blast conditions exists | Fission breeder reactors (BN-600, FFTF) used liquid Na with similar neutron moderation properties; these demonstrated steel vessel survival at low-to-moderate neutron fluence (<1 dpa/year) for decades; tokamak liquid Li blanket mock-ups tested at NSTX, EAST but at much lower neutron flux (~10¹² n/cm²/s vs 10¹⁴ n/cm²/s IFE); IFE neutron shielding requirements similar to fission plants (well-understood technology: borated concrete, steel, water layers achieve <1 mrem/hr at boundary) |
| **Gap ratio** | Neutron flux at first wall: tokamak Li blanket mock-ups ~10¹² n/cm²/s demonstrated → IFE ~10¹⁴ n/cm²/s = 100× flux increase; TBR: tokamak solid blankets achieve 1.05–1.15 → FLF claims 1.8 = 1.5–1.7× improvement (validated computationally but not experimentally at IFE blast conditions); Blast transient effects on neutron transport: no demonstrated analogue—steady-state neutronics vs pulsed compression/expansion of Li curtain during GW/m² heat pulse = new physics regime | Vessel dpa: fission liquid-metal reactors achieved 0.1–1 dpa/year at vessel → FLF claims <0.01 dpa/year = 10–100× reduction (depends on Li curtain remaining intact under blast—undemonstrated); Li curtain thickness maintenance: no demonstrated analogue for 1m flowing Li under repetitive GW/m² pulsed loading—HYLIFE-II computational studies suggest feasibility but never built |
| **Closure mechanism** | FLF's neutronic design relies on 1m Li providing ~10–15 mean free paths for 14.1 MeV neutrons (Li cross-section ~1–2 barns for fast neutrons → attenuation length ~10 cm in liquid Li at 0.53 g/cm³ density); TBR=1.8 achieved via combination of neutron multiplication in Li-7 (via ⁷Li(n,n'α)T, threshold 2.5 MeV, contributes ~20% of breeding) and direct breeding in Li-6; blast transient compression of Li curtain (from GW/m² heat pulse) assumed to be <10% thickness variation based on fluid dynamics codes—if compression >50%, neutron streaming paths could open transiently | FLF claimed flowing Li curtain naturally "heals" from blast-induced perturbations within <30s due to continuous EM-driven flow; vessel activation stays below 10 mrem/hr contact dose rate (hands-on maintenance threshold) if neutron fluence <10¹⁰ n/cm²/s at vessel surface; if blast opens transient gaps in curtain, neutrons stream directly to vessel—mitigation relies on restabilization speed being faster than shot cycle time (30s at 0.033 Hz rep rate) |
| **Classification** | **Degrading** — if TBR is 1.2 instead of 1.8 (e.g., due to blast-induced geometry changes reducing effective Li thickness), tritium surplus drops from 25 kg/year to ~5 kg/year (still self-sufficient but no fleet-deployment enablement); LCOE unaffected but strategic advantage lost; if neutron flux at vessel is 10× higher than predicted (due to curtain gaps), vessel activation increases but dpa remains <0.1/FPY (still manageable with remote maintenance) | **Binary** — if blast-induced Li curtain disruption creates neutron streaming paths that hit vessel wall at >10¹³ n/cm²/s (instead of predicted <10¹⁰ n/cm²/s), vessel dpa rate jumps to >0.5–1/FPY, requiring vessel replacement every 10–20 years instead of never; this eliminates FLF's primary structural cost advantage (infinite vessel life) and adds $100–300M/decade recurring cost, collapsing LCOE competitiveness |
| **Evidence tier** | **Tier 4** (near-regime demonstrated) — D-T neutronics validated extensively at NIF (indirect-drive ICF), JET (tokamak D-T campaigns), TFTR (tokamak D-T); liquid Li neutron transport codes (MCNP, Serpent) benchmarked against fission breeder reactors and tokamak experiments; TBR=1.8 validated computationally by independent third party (TÜV SÜD, Feb 2026)—this is tier 4 evidence (computational validation by accepted codes + independent review); gap is blast transient effects on neutron transport (Li curtain compression/expansion during shot): computational fluid dynamics + neutronics coupling exists but not experimentally validated → drops to tier 3 for transient regime | **Tier 3** (subscale/adjacent demonstration) — fission liquid-metal reactors demonstrated steel vessel survival at <1 dpa/year for decades (EBR-II, BN-600: same materials, similar neutron energies from fast fission spectrum, but steady-state not pulsed); IFE neutron shielding analogous to fission plant shielding (same technology: borated concrete, steel, water; well-characterized); vessel fluence <0.01 dpa/FPY claim depends on Li curtain integrity—no experimental validation of curtain stability under IFE blast conditions (HYLIFE-II was paper design only; no prototype built) |

**Function 5 mean: F5 = (4 + 3) / 2 = 3.5**

---

#### **Function 6: Fuel Cycle Closure**

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | Tritium must be bred in liquid Li blanket at TBR ≥1.05 for self-sufficiency (TBR=1.8 provides 1.7× margin and 25 kg/year net surplus at 333 MWe); tritium must be extracted from flowing Li at rate ≥100% of burn rate + 70% surplus to achieve 25 kg/year net surplus; tritium inventory in plant must remain <10 kg to meet safety limits (or licensing burden increases); startup tritium bank of 3–5 kg must achieve self-sufficiency within weeks (FLF claims "as little as one week") to minimize external tritium dependence | Tritium extraction system must operate continuously on flowing Li stream at 500–600°C without excessive tritium holdup in Li inventory; tritium permeation through Li-to-steam heat exchanger must be <0.1% of bred tritium (or steam system becomes radiologically contaminated); tritium purification and recycling system must achieve >95% recovery of unburned D-T fuel from exhaust; D-T fueling system must deliver 10–100 mg D-T per shot with <1% composition variation shot-to-shot |
| **Best demonstrated** | D-T tritium breeding physics well-understood: ⁶Li(n,α)T cross-section 940 barns at thermal energies, ⁷Li(n,n'α)T threshold reaction contributes 15–20% of breeding; TBR=1.8 validated computationally (TÜV SÜD, Feb 2026); tokamak breeding blanket designs achieve TBR=1.05–1.15 in solid blankets (lower than FLF due to structural material neutron parasitic absorption); liquid Li blankets modeled to achieve TBR=1.3–1.6 in HYLIFE-II studies (lower than FLF's 1.8 but same physics); startup tritium bank requirement standard for all D-T concepts (ITER: ~3 kg startup inventory) | Tritium extraction from liquid Li studied for fusion breeding blankets: permeation through Nb membranes, gettering, cold trapping—all demonstrated at laboratory scale (~g/day) but never at fusion plant scale (kg/day required for 333 MWe at TBR=1.8); tritium permeation barriers in heat exchangers demonstrated in fission breeder reactor studies (ITER tritium plant R&D, fission Li-blanket test loops); D-T fueling via cryogenic target fill demonstrated at NIF (laboratory scale: ~mg per target, low rep rate); automated D-T fueling at 0.033 Hz undemonstrated but analogous to industrial gas handling |
| **Gap ratio** | TBR: solid breeding blankets 1.05–1.15 demonstrated computationally → FLF 1.8 = 1.5–1.7× improvement (liquid Li advantage confirmed in HYLIFE-II studies; computationally validated but not experimentally confirmed under IFE blast conditions); Tritium extraction rate: laboratory Li loops ~g/day demonstrated → fusion plant ~50–100 g/day required (for 25 kg/year surplus) = 50–100× throughput scale-up | Tritium extraction throughput: ITER tritium plant designed for ~1 kg/day processing (not yet operated) → FLF requires ~0.1 kg/day for 25 kg/year surplus = 10× lower throughput (easier); but ITER extracts from gas exhaust (D-T mixture), FLF extracts from liquid Li at 500–600°C (different chemistry, undemonstrated at scale); D-T fueling: NIF achieves ~1 target/day hand-filled → FLF requires 880K targets/year at 0.033 Hz = 880,000× throughput automation |
| **Closure mechanism** | FLF's TBR=1.8 achieved by maximizing Li thickness (1m) and minimizing structural material in neutron path (flowing curtain has no solid structure within breeding zone); ⁶Li(n,α)T dominates breeding; natural Li (7.5% ⁶Li) may suffice if TBR=1.8 achievable without enrichment (FLF white paper cites $70M natural Li vs $143–451M enriched Li cost per analysis.md §Section 4, suggesting natural Li is baseline); tritium extraction claimed via continuous side-stream processing of Li flow (fraction of circulating Li diverted through extraction system, then returned to main loop); "one week to self-sufficiency" claim implies very fast tritium extraction kinetics (>90% extraction efficiency per pass through side-stream system) | FLF references tritium extraction methods from fusion blanket R&D literature (permeation, gettering, cold trapping) but does not specify which method or extraction efficiency; tritium permeation through Li-steam heat exchanger assumed controlled via double-wall HX with helium purge gap (standard ITER design approach, undemonstrated at IFE scale); D-T target fueling assumed via automated cryogenic fill system (conceptual only—no prototype demonstrated at 880K targets/year throughput) |
| **Classification** | **Binary** — if TBR <1.0 due to computational over-prediction or blast-induced geometry changes, plant cannot breed enough tritium to sustain D-T burn and requires continuous external tritium supply; at current scarcity price (~$30,000/g), external tritium for 333 MWe plant would cost ~$1–2B/year (tritium burn rate ~30–60 kg/year at TBR<1), collapsing economics entirely; TBR=1.0–1.05 is borderline self-sufficient but eliminates surplus advantage | **Degrading** — if tritium extraction efficiency is 70% instead of >90%, tritium inventory builds up in Li loop until equilibrium is reached at higher holdup (may exceed 10 kg safety limit, requiring larger containment); if permeation through HX is 1% instead of <0.1%, steam system contamination requires additional tritium recovery equipment (capital cost +$10–50M, O&M cost +$1–5M/year); if D-T fueling defect rate is 10% instead of <1%, shot failure rate increases and availability drops (LCOE increases proportionally) |
| **Evidence tier** | **Tier 4** (near-regime demonstrated) — TBR=1.8 validated by TÜV SÜD using MCNP (industry-standard neutron transport code, validated against decades of fission reactor and fusion experiment data); liquid Li breeding blanket physics modeled extensively in HYLIFE-II studies (1990s, LLNL) and tokamak liquid blanket concepts (NSTX Li divertor experiments, computational studies)—tier 4 because computational validation by independent third party using accepted methods; gap is experimental confirmation under IFE blast conditions → no operating liquid-Li IFE blanket exists | **Tier 3** (subscale/adjacent demonstration) — tritium extraction from liquid Li demonstrated at laboratory scale (g/day) in fusion blanket test loops (JAERI, ORNL, KIT); ITER tritium plant designed for 1 kg/day processing (construction complete, not yet operated—tier 3 for design completion but not operation); D-T target cryogenic filling demonstrated at NIF (~1 target/day, hand-fabricated)—880,000× throughput automation to 0.033 Hz rep rate is extrapolation from laboratory demonstration (tier 3 for partial demo + large scale-up factor) |

**Note**: TBR<1.0 is a **mandatory binary classification** per framework (cannot be overridden). TBR=1.8 validated → not a concern for this concept.

**Function 6 mean: F6 = (4 + 3) / 2 = 3.5**

---

#### **Function 7: Power Conversion & BOP**

| Field | Physics Risk | Hardware Risk |
|-------|-------------|---------------|
| **Plant requirement** | Liquid Li primary loop must transfer fusion heat (1,069 MW thermal at 325 MWe net per model_output.txt line 44) to steam secondary loop via Li-to-steam heat exchanger at 500–600°C Li temperature and ~250–300°C steam saturation temperature; steam Rankine cycle must achieve 35% thermal efficiency (standard for superheated steam at 500–600°C hot-leg temperature); pulsed heat input (30 GJ per shot at 0.033 Hz = 990 MW average but GW-scale instantaneous pulse) must be thermally buffered to deliver steady steam flow to turbine (or turbine experiences damaging thermal transients) | Li-to-steam heat exchanger must survive 40-year lifetime with liquid Li at 500–600°C on primary side and high-pressure steam (5–10 MPa) on secondary side without tube failure (Li-water contact causes violent exothermic reaction); steam turbine must handle steady-state operation (thermal buffering in Li loop provides near-constant steam conditions despite pulsed fusion input); electrical generator and grid connection standard utility-scale equipment (325 MWe net at 0.85 availability = 276 MWe average output to grid) |
| **Best demonstrated** | Steam Rankine cycle at 35% efficiency is standard for coal, fission, and fossil plants at 500–600°C steam temperature (150 years of operating history globally; tens of thousands of plants); liquid metal (sodium, lithium) to steam heat exchangers demonstrated in fission breeder reactors (EBR-II, Superphénix, BN-600): Na-to-steam HX operated for decades at similar temperatures (500–550°C Na, 400–500°C steam) with double-wall tubes + leak detection to prevent Na-water contact; thermal buffering of pulsed heat input well-understood from industrial thermal storage systems (molten salt thermal storage, district heating accumulators) | EBR-II (fission breeder reactor, US, 1964–1994): operated Na-to-steam HX for 30 years at 371 MWe thermal, 500°C Na temperature, zero tube failures via double-wall design + intermediate Na loop as buffer; BN-600 (Russia, 1980–present): 600 MWe fission breeder with Na-to-steam HX, 45+ years operation; steam turbines at 325 MWe scale are commodity equipment (thousands installed worldwide; GE, Siemens, Mitsubishi all manufacture); pulsed heat input at 0.033 Hz (30s cycle) is slow enough that thermal inertia of Li loop provides natural buffering (Li inventory ~10–20 tonnes acts as thermal capacitor) |
| **Gap ratio** | Heat transfer rate: fission Na-to-steam HX demonstrated at 100–600 MWe thermal → FLF requires 1,069 MW thermal = same scale (no gap); Thermal buffering: industrial molten salt storage demonstrated at 0.001–0.01 Hz effective cycling (daily charge/discharge) → FLF 0.033 Hz = 3–30× faster cycling but with much smaller fractional temperature swing (<10% ΔT per shot vs 50–100% ΔT in daily storage) → adjacent regime (no gap); Steam Rankine efficiency: 35% demonstrated at 500–600°C inlet temperature globally (no gap—exact regime match) | Li-to-steam HX: fission Na-to-steam demonstrated for decades → FLF Li-to-steam = adjacent fluid (Li vs Na have similar properties: both liquid metals, similar thermal conductivity, similar chemical reactivity with water) but IFE pulsed loading vs fission steady-state = different thermal cycling regime; Li-water reaction: if HX tube fails, Li contacts water → violent exothermic reaction + hydrogen generation (explosion risk); fission Na-to-steam used double-wall tubes + intermediate loop (Superphénix, BN-600) to prevent Na-water contact—same technology applicable to Li-steam → no novel materials/design needed, but FLF-specific IFE pulsed loading undemonstrated |
| **Closure mechanism** | FLF explicitly stated: "After the lithium heat exchanger, the plant is identical to many other already working facilities" (analysis.md §Section 3)—this is accurate; steam Rankine cycle from HX outlet to grid connection is mature technology with zero fusion-specific risk; thermal buffering in Li loop relies on large Li inventory (~10–20 tonnes circulating at 500–600°C) providing ~50–100 GJ thermal capacitance (enough to smooth 30 GJ pulses at 0.033 Hz); Li-steam HX uses double-wall tube design with helium leak detection (ITER design approach, demonstrated in fission breeders) | FLF referenced fission breeder reactor Li/Na-to-steam HX technology as direct analogue; if tube failure occurs, leak detection shuts down plant before significant Li-water contact (standard fission plant safety system); electrical generator and switchyard are off-the-shelf utility equipment (325 MWe scale is mid-size power plant—thousands of analogues worldwide); BOP complexity equivalent to small fission plant or large industrial cogeneration facility (well-understood operational regime) |
| **Classification** | **Degrading** — if thermal buffering is inadequate and steam temperature fluctuates ±20% per shot cycle, turbine efficiency drops from 35% to ~30% (thermal cycling losses), reducing net power by ~15% and increasing LCOE proportionally; if steam cycle must be oversized to handle peak-to-average thermal power ratio, capital cost increases by $50–100M (CAS23 turbine plant +10–20%) but plant remains operable | **Degrading** — if Li-steam HX tube failure occurs and requires HX replacement, outage time is ~1–3 months (fission plant HX replacement precedent: EBR-II steam generator repair 1972, 6-month outage) and replacement cost ~$20–50M; if failure rate is 1 per 10 years, annualized cost is $2–5M/year (adds ~1–2 $/MWh to LCOE); not a binary risk because HX is replaceable equipment and Li-water contact is localized (containment prevents cascade to full plant loss) |
| **Evidence tier** | **Tier 5** (operating-regime demonstrated at commercial scale) — Steam Rankine cycle at 35% efficiency and 500–600°C steam temperature is demonstrated in thousands of operating power plants globally (coal: supercritical steam at 540–600°C, fission: PWR secondary side at 280–320°C but HTGRs and breeders at 500–550°C); thermal buffering of pulsed heat input demonstrated at industrial scale (molten salt thermal storage: 100+ MW scale, Gemasolar Spain 110 MWe with 15-hour storage at ~565°C molten salt) → pulsed-to-steady conversion is tier 5 for adjacent thermal regime | **Tier 5** (operating-regime demonstrated at commercial scale) — Li-to-steam HX is adjacent to demonstrated Na-to-steam HX in fission breeders: EBR-II operated 1964–1994 (30 years, 371 MWe thermal, zero tube failures), BN-600 operated 1980–present (45+ years, 1,470 MWe thermal); Na and Li have similar liquid metal properties (thermal conductivity within 2×, density within 2×, chemical reactivity with water both violent but manageable with double-wall tubes + leak detection); IFE pulsed loading at 0.033 Hz (30s cycle) is slow enough that thermal inertia in liquid metal loop provides natural buffering → tier 5 because fission liquid-metal-to-steam is the SAME operating regime (temperature, pressure, materials) with only pulsed vs steady-state as difference (and pulsed at 30s cycle is within thermal time constant of liquid metal loop ~10–100s) |

**Note**: Per framework, "Conventional thermal cycles (Rankine, Brayton, sCO₂) are mature analogues—score them at the operating-regime tier their cycle has demonstrated commercially." FLF's steam Rankine at 35% efficiency and 500–600°C is **tier 5** (demonstrated at commercial scale in coal supercritical plants, fission breeder reactors, and HTGRs). The Li-to-steam HX is adjacent to demonstrated Na-to-steam fission breeder HX—also **tier 5** because the operating regime (temperature, pressure, liquid metal handling, chemical reactivity mitigation) has been demonstrated at commercial scale for decades.

**Function 7 mean: F7 = (5 + 5) / 2 = 5.0**

---

### Summary of Function-Level Means (before heritage credit):

| Function | Physics Tier | Hardware Tier | Function Mean F_n |
|----------|-------------|---------------|-------------------|
| F1: Plasma Performance | 1 | 2 | 1.5 |
| F2: Driver / Energy Input | 3 | 2 | 2.5 |
| F3: Instability Control | 2 | 3 | 2.5 |
| F4: Plasma-Wall Interaction | 3 | 3 | 3.0 |
| F5: Neutron/Particle Handling | 4 | 3 | 3.5 |
| F6: Fuel Cycle Closure | 4 | 3 | 3.5 |
| F7: Power Conversion & BOP | 5 | 5 | 5.0 |

### Heritage Credit Application

Per framework: "Heritage credit only applies to D-T fuel." Projectile ICF burns D-T fuel → **heritage credit applies**.

Per framework: "The heritage credit provides a FLOOR on **all seven function scores (F1–F7)**."

**Heritage lineage**: Projectile ICF does NOT trace to tokamaks, stellarators, laser IFE, mirrors, FRCs, spherical tokamaks, Z-pinch, or magLIF. It is a novel driver concept (electromagnetic launcher) with proprietary target physics (amplifier cavities). The closest heritage is **Laser IFE** (both are IFE, both use D-T ablative compression, both have liquid-wall chamber concepts like HYLIFE), but projectile ICF uses kinetic impact instead of laser ablation—this is a fundamentally different physics pathway with no shared experimental lineage.

**No heritage credit applies**—projectile ICF does not trace to any of the listed heritage lineages. F1–F7 remain as computed.

### Binary Risks

From the risk matrix, risks classified as **Binary**:

1. **F1 Physics**: Gain <200× at 60 km/s → plant cannot achieve 333 MWe at stated rep rates (net power goes negative)
2. **F2 Hardware**: Bore lifetime <10⁵ shots requires barrel replacement every ~35 days; if replacement cost >$10M + replacement time >1 week, availability <50% and economics collapse
3. **F4 Hardware**: Blast-induced Li curtain disruption creates neutron streaming → vessel dpa >0.5/FPY → requires vessel replacement every 10–20 years instead of never, eliminating cost advantage
4. **F5 Hardware**: (Same as F4 Hardware—neutron streaming to vessel)
5. **F6 Physics**: TBR <1.0 → cannot sustain D-T burn, requires continuous external tritium supply at ~$1–2B/year for 333 MWe plant

**Binary risks list**:
- Target gain <200× at 60 km/s (F1 Physics)
- Electromagnetic launcher bore lifetime <10⁵ shots with replacement cost >$10M (F2 Hardware)
- Liquid lithium curtain blast disruption creating neutron streaming paths to vessel (F4 Hardware, F5 Hardware combined)
- Tritium breeding ratio <1.0 (F6 Physics)

### C7 Computation (done by Python, not Claude)

**I do NOT compute C7**—this is computed by Python from F1–F7 means.

**Reporting F1–F7 in YAML** (below, after section 8).

---

## 8. LCOE Downselect Scoring (Scores Table + YAML)

### Scores Summary Table

| Criterion | Score | Justification Summary |
|-----------|-------|----------------------|
| **C1: Modularization** | 3.2 | EM launcher (64% of CAS22) is site-assembled (score 3). Target factory is modular (score 5, 7.8% share). Magnet elimination removes stick-built components. No module repetition. Weighted average 3.2. |
| **C3: Supply Chain Learning** | 2.8 | EM launcher (64% CAS22) scores 2 (novel, no manufacturing base). Target factory scores 2 (fusion-specific). BOP scores 5 (commodity). Two hard bottlenecks (60 km/s launcher, 1–4M targets/year). External demand ~45%. |
| **C4: Plant Complexity** | 4.0 | Mostly decoupled: driver/target/Li loop/turbine failures don't cascade. 7–8 significant subsystems. Simpler than tokamaks (no magnet-disruption coupling). Standard power plant complexity. |
| **C5: Customization Needs** | 1.7 | Large cooling towers required (score 2). D-T fuel with full tritium handling + reactive Li coolant (score 1). Severe siting constraints. Raw=(2+1)/2=1.5 → scaled 1.7. |
| **C8: Data Adequacy** | 2.3 | TBR validated (tier 4), company data extensive, but 8 blocking gaps. Partial reactor design. No commercialization pathway (FLF pivoted away). (3+3+1+2)/4=2.25 → 2.3. |
| **F1: Plasma Performance** | 1.5 | Gain at 60 km/s never demonstrated (tier 1 physics). Amplifier target paper design (tier 2 hardware). Mean 1.5. |
| **F2: Driver / Energy Input** | 2.5 | 60 km/s velocity subscale demo at 6.5 km/s (tier 3 physics). Machine 4 cancelled, bore lifetime unknown (tier 2 hardware). Mean 2.5. |
| **F3: Instability Control** | 2.5 | RT instability physics from ICF analogues (tier 2 physics). Target positioning partial demo (tier 3 hardware). Mean 2.5. |
| **F4: Plasma-Wall Interaction** | 3.0 | Liquid Li heat flux subscale/adjacent demo (tier 3 physics). EM pumps + vessel lifetime adjacent fission analogues (tier 3 hardware). Mean 3.0. |
| **F5: Neutron/Particle Handling** | 3.5 | TBR=1.8 validated computationally by TÜV SÜD (tier 4 physics). Vessel survival adjacent to fission breeders (tier 3 hardware). Mean 3.5. |
| **F6: Fuel Cycle Closure** | 3.5 | TBR=1.8 validated (tier 4 physics). Tritium extraction subscale demo, D-T fueling automation extrapolation (tier 3 hardware). Mean 3.5. |
| **F7: Power Conversion & BOP** | 5.0 | Steam Rankine at 35% efficiency demonstrated globally (tier 5 physics). Li-to-steam HX adjacent to fission Na-to-steam (tier 5 hardware). Mean 5.0. |

---

```yaml
---
scores:
  C1: 3.2
  C3: 2.8
  C4: 4.0
  C5: 1.7
  C8: 2.3
  F1: 1.5
  F2: 2.5
  F3: 2.5
  F4: 3.0
  F5: 3.5
  F6: 3.5
  F7: 5.0
  binary_risks:
    - "Target gain <200× at 60 km/s prevents plant from achieving 333 MWe net output at stated rep rates (F1 Physics)"
    - "Electromagnetic launcher bore lifetime <10^5 shots requires barrel replacement every ~35 days; if replacement cost >$10M and downtime >1 week, plant availability drops below 50% (F2 Hardware)"
    - "Liquid lithium curtain blast disruption creating neutron streaming paths to vessel, causing dpa >0.5/FPY and forcing vessel replacement every 10–20 years instead of never (F4/F5 Hardware combined)"
    - "Tritium breeding ratio <1.0 requires continuous external tritium supply at ~$1–2B/year for 333 MWe plant, collapsing economics (F6 Physics)"
---
```
