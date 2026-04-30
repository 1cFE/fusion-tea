---
ID: 22-projectile-icf
Concept: Projectile ICF (D-T)
Company: First Light Fusion, NearStar Fusion
Type: synthesis
Status: draft
Created: 2026-04-29
---

## 1. Executive Summary

- **Single most important risk**: Target gain at 60 km/s has never been demonstrated. The gap from Machine 3's ~50-neutron result (2022) to the required 200-1000× commercial gain is eight orders of magnitude in neutron yield. Machine 4, the only device that would have tested this, was cancelled in February 2025 before construction. This is a binary physics risk — without gain demonstration, the concept cannot produce net electricity.

- **Single most important advantage**: Eliminates all magnet capital (zero superconducting coils) and achieves TBR 1.8 (independently validated), producing 25 kg/yr tritium surplus at 333 MWe. This removes ~30-50% of tokamak reactor plant cost and enables fleet deployment without tritium scarcity constraints. The liquid lithium blanket also eliminates first-wall replacement costs over the 40-year plant life.

- **LCOE ballpark**: The baseline model (gain=1000×, driver=$1B, 0.033 Hz) produces 135 $/MWh at 304 MWe native power (84 $/MWh scaled to 1 GWe). However, this is false precision. The optimistic scenario (gain=1000×, driver=$500M, 0.1 Hz) yields 62 $/MWh. The conservative scenario (gain=200×, driver=$2B) produces 2,507 $/MWh and only 21 MWe net power. **First Light Fusion's abandonment of the projectile approach in favor of FLARE (Sept 2025) is indirect evidence that internal analysis found the electromagnetic gun economically unviable.**

- **Confidence verdict**: Low. The concept has two blocking unknowns with no published data: (1) electromagnetic gun capital cost at 60 km/s — no industrial analogue exists, and (2) target gain — never demonstrated at commercial velocity. The FLARE pivot eliminates the only organization that could have retired these unknowns. This is an orphaned concept with no active commercial pursuer.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity magnitude from model sweeps:

### #1: Target Gain (fusion yield per shot)
- **Assumed value**: 30 GJ/shot (gain=1000× at 30 MJ delivered energy to target)
- **Source**: Inferred from FLF's 333 MWe design point at 0.033 Hz rep rate; FLF claimed 200-1000× gain range
- **Sensitivity**: Nearly linear in 1/gain. Reducing from 30 GJ (1000×) to 6 GJ (200×) increases LCOE from 135 $/MWh to 1,268 $/MWh at fixed driver cost — a 9.4× penalty. Below 200× gain (3 GJ/shot), net power goes negative even at zero driver cost.
- **What would flip the conclusion**: Demonstrated gain ≥200× at 60 km/s would prove commercial viability is physically possible. Gain <200× makes the concept non-viable regardless of driver cost. The model shows LCOE improvement saturates above 400× gain (diminishing returns beyond 2× the minimum threshold).

### #2: EM Driver Capital Cost
- **Assumed value**: $1,000M (central estimate between $600M-$1.3B from FLARE analogues)
- **Source**: Machine 4 (100 MJ stored energy, cancelled Feb 2025) has no published cost. FLARE pivot data shows pulsed power at $2/J vs "alternatives" at $6-13/J. At 100 MJ stored, this implies $600M-$1.3B. FLF's abandonment suggests actual cost was above this range.
- **Sensitivity**: Sweeping $200M to $3.5B changes LCOE by +164 $/MWh (+121% penalty) at high end. Driver cost sensitivity is roughly equal to gain sensitivity in the moderate scenario.
- **What would flip the conclusion**: Driver cost below $500M would enable <$70/MWh LCOE if gain=1000× is achieved. Driver cost above $2B makes even optimistic gain scenarios uneconomical (>$200/MWh).

### #3: Repetition Rate
- **Assumed value**: 0.033 Hz (30s between shots) — pilot design point
- **Source**: FLF cited three conflicting figures (0.011, 0.033, 0.1 Hz); 0.033 Hz is the most conservative pilot-scale reference
- **Sensitivity**: 10× increase in rep rate (0.033 → 0.1 Hz) reduces LCOE by 46% (135 → 73 $/MWh) by spreading fixed capital over more shots. However, chamber clearing time for liquid Li resettlement is unknown and may impose a physical ceiling <0.1 Hz.
- **What would flip the conclusion**: If chamber physics limits rep rate to 0.011 Hz (90s cycle), LCOE rises to 415 $/MWh even at gain=1000×. Rep rate is coupled to gain: lower gain requires higher rep rate to maintain power output, potentially violating chamber clearing constraints.

### #4: Driver Wall-Plug Efficiency
- **Assumed value**: 30% (EM launcher kinetic conversion efficiency)
- **Source**: Not published. Analogue from railgun/coilgun systems at lower velocities (20-40% typical). 60 km/s efficiency is unknown.
- **Sensitivity**: Low direct LCOE impact in model sweep (efficiency 15%-50% shows <1% LCOE variation). This is because efficiency affects gain definition but not energy balance significantly when gain is high (≥200×).
- **What would flip the conclusion**: Efficiency <10% would require higher stored energy per shot, increasing driver capital cost. This is a second-order effect through driver cost, not a first-order LCOE driver.

### #5: Target Fabrication Cost
- **Assumed value**: $5/target
- **Source**: Not published. Economic ceiling from Goodin et al. (2004): target cost must be <10% of electrical yield per shot. At 30 GJ yield and 33% thermal efficiency, ceiling is ~$14/target. Using $5 as base case.
- **Sensitivity**: Modest. Sweeping $1-$50/target changes LCOE by only +18 $/MWh (+13%) at high end. At 884,585 shots/year, even $50/target adds only $44M/yr vs $275M/yr capital charge.
- **What would flip the conclusion**: Target cost >$100/shot would materially degrade LCOE, but this would violate the Goodin economic bound and make IFE fundamentally uneconomical.

---

## 3. Risk Verdicts

### Target gain at 60 km/s (200-1000× required)
- **Verdict**: Unlikely resolvable without Machine 4 or equivalent
- **Rationale**: The 2022 demonstration produced ~50 neutrons at 6.5 km/s. Scaling to 60 km/s and achieving 200-1000× gain requires eight orders of magnitude improvement in neutron yield with no experimental validation pathway. FLF's internal simulations claim the proprietary "amplifier" target achieves this, but the physics is unverified.
- **What would retire this risk**: Experimental demonstration of gain ≥100× at projectile velocities >30 km/s would provide credible scaling evidence. Alternatively, independent peer-reviewed target physics validation by non-FLF groups. Machine 4's cancellation eliminated the only planned experiment.

### EM gun capital cost at 60 km/s
- **Verdict**: Genuinely uncertain
- **Rationale**: No 60 km/s electromagnetic launcher has ever been built at any scale. Bore erosion physics, sabot materials, and capacitor/switching architecture at this velocity are uncharacterized. The FLARE pivot suggests FLF's internal cost analysis exceeded viability thresholds.
- **What would retire this risk**: Construction and costing of a rep-rated 60 km/s launcher at any scale (even sub-fusion). If driver cost is confirmed >$2B, the concept becomes uneconomical even at optimistic gain.

### Liquid lithium chamber blast survivability
- **Verdict**: Likely resolvable
- **Rationale**: Flowing liquid metal first walls have been studied extensively for IFE (HYLIFE, LIFE, Z-IFE). The 1-meter-thick curtain provides substantial neutron absorption. The TBR 1.8 validation by TÜV SÜD shows neutronic design is sound. Chamber clearing time and pump power are unknowns but not showstoppers.
- **What would retire this risk**: Subscale liquid lithium chamber test under pulsed neutron loading at representative blast energies. If curtain cannot maintain geometry at >0.033 Hz, rep rate is physically limited.

### Target fabrication at 1-4M units/year
- **Verdict**: Likely resolvable
- **Rationale**: FLF's amplifier target geometry is proprietary but not fundamentally different from NIF or laser IFE target complexity. Precision injection molding or additive manufacturing at scale is a manufacturing challenge, not a physics barrier. Cost is unknown but bounded by the Goodin limit (<10% of yield value).
- **What would retire this risk**: Pilot-scale target manufacturing line producing >1,000 units/day with yield >95% and cost <$10/unit.

### Tritium breeding and extraction
- **Verdict**: Likely resolvable
- **Rationale**: TBR 1.8 is independently validated. Liquid lithium tritium extraction is well-understood from fission and ITER blanket programs. The "self-sufficiency in one week" claim is likely a misstatement (should be months), but achieving TBR >1.1 for self-sufficiency is credible.
- **What would retire this risk**: Already substantially retired by TÜV SÜD validation. Remaining risk is tritium extraction efficiency from flowing lithium at operating temperature.

---

## 4. Structural Advantages and Disadvantages

Comparison to conventional D-T tokamak baseline (SPARC/ARC class):

### Advantages (quantified where model supports):
1. **Zero magnet capital**: Eliminates CAS220103 (HTS coils, cryostats, current leads) — typically $800M-$1.5B for a GW-scale tokamak. This is 30-50% of CAS22 reactor plant cost.
2. **No first-wall replacement**: Liquid lithium blanket absorbs all neutrons; vessel lifetime = plant lifetime. Eliminates $100-300M/decade recurring replacement cost that solid-wall D-T concepts bear.
3. **TBR 1.8 enables fleet deployment**: 25 kg/yr surplus at 333 MWe allows this concept to fuel 4-5 additional plants from each operating unit. Tokamaks at TBR 1.05-1.15 require ~multi-hundred-kg tritium banks and cannot scale fleets without external supply.
4. **No NBI or RF heating capital**: Driver delivers all energy; eliminates CAS220104 (~$200-500M at GW scale for tokamaks).
5. **No precision optics**: Unlike laser IFE, projectile ICF has no beam optics near the chamber. Eliminates final optics survivability challenge (TRL 2-3 for laser IFE).
6. **Conventional BOP**: Steam Rankine cycle is TRL 9; 33-35% thermal efficiency is well-characterized. No direct energy conversion R&D needed.

**Net advantage magnitude**: Eliminating magnets (~$1B) and first-wall replacement (~$200M over 40 years) saves roughly $1.2-1.5B in overnight capital relative to a tokamak. However, this is offset by...

### Disadvantages (quantified where model supports):
1. **EM driver capital cost unknown**: The electromagnetic gun at 60 km/s is estimated at $500M-$3.5B (central: $1B). If actual cost is >$2B, the magnet elimination advantage is entirely consumed.
2. **Pulsed operation at sub-Hz rep rate**: 0.033-0.1 Hz is 10-100× slower than Xcimer/Inertia laser IFE concepts (0.25-10 Hz). Revenue scales linearly with rep rate; slow rep rate amortizes capital poorly.
3. **Per-shot consumable costs**: Targets and projectiles are destroyed every shot. At $5/target + $1/projectile and 884K shots/year, this adds $5.3M/yr (modest, but laser IFE has similar or higher target costs).
4. **Gain requirement 50-250× higher than NIF ignition**: NIF achieved 4× gain (indirect drive, 2022). FLF requires 200-1000× — a fundamentally larger physics extrapolation than laser IFE's ~10-30× requirement.
5. **No active commercial pursuer**: FLF pivoted to FLARE (pulsed-power liner implosion). NearStar is MTIF (magnetized fuel, D-D), not pure projectile ICF. This concept has no development pathway.

**Net structural position**: Projectile ICF eliminates tokamak's most expensive subsystems (magnets, first-wall replacement) but substitutes an unknown-cost driver and extreme physics extrapolation. If driver cost is <$500M and gain ≥400×, the concept is economically superior to tokamaks. If driver cost is >$1.5B or gain <200×, tokamaks are clearly superior.

---

## 5. Cross-Concept Positioning

**Within IFE family**: Projectile ICF sits between laser ICF and heavy-ion ICF on the driver cost/efficiency spectrum. Laser ICF drivers are well-characterized ($2-10/J, <1% wall-plug efficiency). Heavy-ion drivers are modeled but never built (~$3-8/J, 25-35% efficiency). Projectile ICF's EM driver is entirely uncharacterized but likely falls in the 20-40% efficiency range (better than lasers, worse than ion beams). The key differentiator is **elimination of precision beam optics** — this is a genuine structural simplification vs laser/ion IFE.

**Gain threshold comparison**:
- Laser ICF (NIF-class indirect drive): requires ~100-200× gain for commercial viability (Xcimer/Inertia targets)
- Laser ICF (direct drive): requires ~50-100× gain (higher driver efficiency)
- Projectile ICF: requires 200-1000× gain (lower rep rate demands higher yield/shot)

FLF's gain requirement is the **most aggressive in the IFE landscape** due to the sub-Hz rep rate constraint.

**Tritium breeding position**: Projectile ICF's TBR 1.8 is the **highest validated TBR in the D-T fusion landscape** (tokamaks: 1.05-1.15; laser ICF: 1.1-1.4; MagLIF: ~1.3). This is its singular physics advantage and the only parameter where it outperforms all competitors.

**Shared challenges with MagLIF (07)**:
- Pulsed chamber clearing time (liquid metal resettlement)
- Per-shot consumable costs (targets, liners, or projectiles)
- Rep rate × gain coupling (low rep rate requires high gain to maintain power)
- Driver capital cost as dominant novel CAS22 item

**Divergence from MagLIF**:
- MagLIF uses pulsed power (~$2/J, characterized cost); projectile ICF uses EM launcher (uncharacterized)
- MagLIF requires external seed magnetic field; projectile ICF has zero magnets
- MagLIF's Pacific Fusion is actively developing the concept; projectile ICF is orphaned

**Cross-concept summary**: Projectile ICF is the **most capital-efficient IFE concept on paper** (zero magnets, zero optics, conventional BOP) but also the **least experimentally validated** (gain never demonstrated, driver never built). It is a high-risk, high-reward outlier with no development pathway.

---

## 6. Modeling Confidence

**Rating**: Low

**Data-anchored parameters** (9 of 25):
1. TBR 1.8 (independently validated)
2. Tritium surplus 25 kg/yr (derived from validated TBR)
3. Thermal efficiency 33% (steam Rankine, mature technology)
4. Rep rate 0.033 Hz (stated by FLF, though three conflicting values exist)
5. Machine 4 stored energy 100 MJ (design spec)
6. Plant size 150-500 MWe (stated targets)
7. Blanket energy multiplication 1.1 (standard D-T)
8. Capacity factor 85% (assumed from Z-IFE analogue)
9. Plant lifetime 40 years (standard)

**Speculative parameters** (16 of 25):
- **Driver capital cost**: No published estimate; FLARE analogues provide weak bounds ($600M-$1.3B); actual cost may be higher (FLF abandoned approach)
- **Driver efficiency**: No published data; 30% assumed from railgun/coilgun analogues at lower velocities
- **Target gain**: 200-1000× claimed; never demonstrated; Machine 3 achieved Q<<1
- **Target fabrication cost**: $5/shot assumed; no manufacturing pathway demonstrated
- **Recirculating power fraction**: Derived from assumed driver efficiency; liquid Li pump power (30 MW) is analogue-based, not FLF-specific
- **Chamber geometry** (inner radius, blanket thickness, shield): Inferred from liquid Li curtain description; not explicitly stated
- **Capital cost structure (CAS breakdown)**: Entirely modeled using IFE analogues; no FLF subsystem cost data
- **O&M costs**: Assumed from Z-IFE study ($60/MW-yr); no projectile-specific data

**Dominant source of LCOE uncertainty**: **Target gain** (parametric uncertainty spanning 5× in LCOE from 200× to 1000× gain) and **driver capital cost** (deep uncertainty spanning $200M to $3.5B, representing 2-3× variation in LCOE). These two unknowns are uncorrelated and multiplicative in effect — a concept with low gain AND high driver cost is unviable; a concept with high gain AND low driver cost is economically compelling. The model cannot resolve which regime is real.

**Consequence-of-modeling-without-data**: The LCOE outputs (62-2,507 $/MWh depending on scenario) span **40× range**. This is not a cost estimate; it is a bounded possibility space. The model is useful for identifying which parameters matter most (gain, driver cost, rep rate) but cannot predict actual LCOE without experimental demonstration of gain at 60 km/s and construction of a commercial-scale EM launcher.

---

## 7. What Would Change My Mind

### (a) **Machine 4 or equivalent demonstrates gain ≥100× at projectile velocity >30 km/s**
If a 60 km/s projectile-driven implosion achieves even 100× gain (half the minimum commercial threshold), it would prove the amplifier target physics is scalable and retire the dominant binary risk. This would upgrade confidence from "Low" to "Medium" and shift LCOE credibility from "speculative" to "uncertain but bounded."

Current evidence: 2022 demonstration at 6.5 km/s produced ~50 neutrons (Q<<1). Eight orders of magnitude gap to commercial requirements. Machine 4 cancelled before testing.

### (b) **EM launcher construction cost for a 60 km/s, 100 MJ device is published**
If driver capital cost is confirmed <$500M, the concept becomes economically competitive with tokamaks even at moderate gain (400-500×). If cost is confirmed >$2B, the concept is uneconomical even at optimistic gain (1000×). Removing this uncertainty collapses the 40× LCOE range to ~3× range.

Current evidence: FLARE pivot implies driver cost >$2/J (vs pulsed power), suggesting >$600M at 100 MJ. FLF's abandonment implies actual cost was above internal viability threshold, likely >$1.5B.

### (c) **Alternative projectile ICF developer publishes credible gain roadmap**
If NearStar (currently pursuing MTIF, not pure projectile ICF) or a new entrant publishes a gain scaling pathway with subscale experimental validation, it would provide an independent check on FLF's claims. This would retire the "orphaned concept" concern and provide comparative data.

Current evidence: NearStar's 2025 publication was expected but not seen in sources. No other projectile ICF developers exist.

---

## 8. LCOE Downselect Scoring

### C1: Modularization (scored)

**Sub-factor 1: Construction mode classification per CAS account**

| CAS Account | Construction Mode | Score | Cost Weight | Notes |
|-------------|------------------|-------|-------------|-------|
| CAS21 (Buildings) | Site-assembled from factory sub-assemblies | 3 | 7.0% | Standard reactor building; launcher bay is large but conventional steel structure |
| CAS22.01 (Blanket/First Wall) | Factory-manufactured module | 5 | 1.3% | Liquid Li distribution manifolds can be shop-fabricated; flow channels are modular |
| CAS22.02 (Shield) | Site-assembled | 3 | 0.9% | Spherical shield layers; site assembly likely |
| CAS22.05 (Primary Structure) | Site-assembled | 3 | 0.2% | Vessel structure; site-welded |
| CAS22.06 (Vacuum System) | Site-assembled | 3 | 0.3% | Containment vessel; site-welded |
| CAS22.07 (Driver - EM launcher) | Stick-built / field-erected | 1 | 30.5% | 60 km/s electromagnetic gun is custom, one-off construction; no factory precedent at this scale |
| CAS22.08 (Target Factory) | Factory-manufactured module | 5 | 3.6% | COTS injection molding or additive manufacturing equipment at scale |
| CAS22.20 (Coolant Systems) | Site-assembled | 3 | 2.2% | Liquid Li primary loop and steam HX; site assembly |
| CAS23 (Turbine) | Factory-manufactured module | 5 | 2.1% | Standard steam turbine; COTS 150-year-old technology |
| CAS24 (Electric Plant) | Factory-manufactured module | 5 | 0.9% | Switchgear, transformers; all COTS |
| CAS25 (Misc Plant) | Factory-manufactured module | 5 | 0.6% | COTS auxiliary systems |
| CAS26 (Heat Rejection) | Site-assembled from factory sub-assemblies | 3 | 0.4% | Cooling towers; modular components, site-assembled |
| CAS27 (Special Materials) | Factory-manufactured module | 5 | 2.1% | Liquid Li inventory is commodity material; pumped in after construction |

**Weighted average**:
Sum(score × weight) / Sum(weight) = (1×30.5 + 3×11.5 + 5×11.0) / 100 = 85.0 / 100 = **2.4** (before module repetition boost)

**Sub-factor 2: Module repetition boost**
- Modules per plant: 1 fusion chamber (no repetition within plant)
- Boost: 0.0 (no multi-module architecture)

**C1 final score**: 2.4 + 0.0 = **2.4**

**Justification**: The electromagnetic gun driver (30.5% of capital cost at $1B) is a custom, one-off device with no factory manufacturing pathway at 60 km/s. This drags the overall score to 2.4 despite mature BOP (steam turbine, electric plant) and modular target factory. The liquid Li blanket system offers some modularization potential (shop-fabricated flow channels) but the spherical chamber geometry limits mass production benefits. Projectile ICF's modularization score is worse than tokamaks (where HTS coils can be factory-wound and shipped) due to the unique EM launcher.

---

### C3: Supply Chain Learning (scored)

**Sub-factor A: Component learning rates (cost-weighted average)**

| CAS Account | Learning Rate Category | Score | Cost Weight | Rationale |
|-------------|----------------------|-------|-------------|-----------|
| CAS21 (Buildings) | Commodity component | 5 | 7.0% | Steel, concrete; established construction |
| CAS22.01 (Blanket) | Specialty component (limited supply chain) | 3 | 1.3% | Liquid Li handling at fusion scale is niche; pumps exist but not at this neutron environment |
| CAS22.07 (Driver) | Novel component (never at scale) | 1 | 30.5% | 60 km/s EM launcher has no production base; capacitor banks at this scale exist but barrel/sabot materials at 60 km/s are uncharacterized |
| CAS22.08 (Target Factory) | Specialty component | 3 | 3.6% | Precision target manufacturing at 1M units/year scale has no current market; NIF target fabrication is lab-scale |
| CAS23 (Turbine) | Commodity component | 5 | 2.1% | GW-scale steam turbines are commodity; GE, Siemens production |
| CAS24 (Electric) | Commodity component | 5 | 0.9% | Switchgear, transformers; mass-produced |
| CAS25 (Misc) | Commodity component | 5 | 0.6% | Pumps, HVAC, controls; all industrial commodity |
| CAS26 (Heat Rejection) | Commodity component | 5 | 0.4% | Cooling towers; established vendors |
| CAS27 (Li inventory) | Industrial component (growing production) | 4 | 2.1% | Lithium production is scaling for batteries; elemental Li is commodity; isotope enrichment (if needed) is constrained |
| Other CAS22 (coolant, shield, structure, fuel handling) | Specialty to commodity mix | 3.5 | 51.5% | Liquid Li loop components are specialty but based on fission/ITER analogues; shield and structure are industrial commodity |

**Weighted average**:
(1×30.5 + 3×5.0 + 3.5×51.5 + 4×2.1 + 5×10.0) / 100 = **2.7**

**Sub-factor B: Supply chain bottleneck count**
Starting at 5.0:
- **Hard constraint**: 60 km/s EM launcher barrel materials (bore erosion at hypervelocity has no known material solution) → **-1.0**
- **Scaling constraint**: Target fabrication at 1-4M units/year (precision multi-cavity targets have no current manufacturing base; must scale from lab to industrial) → **-0.5**
- **Scaling constraint**: Liquid lithium pumps at fusion neutron environment (EM pumps exist at HYLIFE scale but not commercialized for fusion) → **-0.5**
- **Sole-source dependency**: None currently (driver would be custom-built; no single vendor dependency until commercialized)
- **He-3 fuel dependency**: Not applicable (D-T fuel)

**Score**: 5.0 - 1.0 - 0.5 - 0.5 = **3.0** (clamped to [1,5])

**Sub-factor C: External demand pull (fraction of capital cost with >$1B/yr external market)**
- CAS21 (Buildings): 7.0% — **Yes** (construction industry)
- CAS22.01 (Blanket): 1.3% — No (fusion-specific)
- CAS22.07 (Driver): 30.5% — No (no commercial EM launcher market at any scale)
- CAS22.08 (Target Factory): 3.6% — Partial (additive manufacturing equipment has external demand, but fusion targets are niche)
- CAS23 (Turbine): 2.1% — **Yes** (GW power generation)
- CAS24 (Electric): 0.9% — **Yes** (power plant equipment)
- CAS25 (Misc): 0.6% — **Yes** (industrial pumps, HVAC)
- CAS26 (Heat Rejection): 0.4% — **Yes** (cooling towers for industrial/power)
- CAS27 (Li): 2.1% — **Yes** (battery industry scaling lithium production)
- Other CAS22 (coolant, shield, structure, fuel handling): 51.5% — Partial (~20% has external demand in fission, chemical processing)

**Fraction with >$1B/yr external market**: 7.0 + 2.1 + 0.9 + 0.6 + 0.4 + 2.1 + (0.20 × 51.5) = **23.4%**

**Score**: Between 20-40% → **3**

**C3 final score**: (2.7 + 3.0 + 3.0) / 3 = **2.9**

**Justification**: The electromagnetic gun driver (30.5% of capital) is a first-of-a-kind component with no external demand pull, hard material constraints at 60 km/s, and a learning rate bottleneck (score=1). This drags the overall supply chain score despite mature BOP components (turbine, electric, heat rejection) that benefit from established supply chains. Target fabrication at IFE scale is another scaling constraint with limited external demand. Liquid lithium handling borrows from fission and battery industries but remains niche. The concept scores slightly better than exotic approaches (muon-catalyzed fusion, orbital concepts) but worse than HTS tokamaks where superconductor production is scaling rapidly for grid and MRI applications.

---

### C4: Plant Complexity (scored)

**Sub-factor A: Operational coupling density (failure cascades and maintenance dependencies)**

**Score: 3** (Moderate coupling; several failure cascade paths)

**Rationale**:
- **Decoupled subsystems**: The steam Rankine BOP (turbine, condenser, cooling) is operationally independent of the fusion island. A turbine trip does not cascade to chamber failure — the liquid Li loop can continue to absorb heat and reject to atmosphere if needed (though plant output stops).
- **Moderate coupling within fusion island**: Liquid Li primary loop failure (pump seizure, leak) cascades to loss of tritium breeding and first-wall cooling — the chamber cannot operate without Li flow. However, the Li loop itself has redundancy potential (multiple pumps, bypass paths). Target injection system failure stops fusion but does not damage other systems. EM gun failure stops fusion but does not cascade to thermal management failure (unlike NBI in tokamaks, where loss of heating can trigger disruptions).
- **Failure cascade examples**:
  - Li pump failure → loss of blanket cooling + tritium breeding → plant shutdown (but no vessel damage due to low decay heat in pulsed system)
  - EM gun capacitor bank failure → no shots → revenue loss but no cascading damage
  - Target injection mis-positioning → low yield or no yield → revenue loss but no first-wall damage (unlike laser IFE where beam mis-aim can damage optics)
- **Maintenance dependencies**: EM gun barrel replacement (if required every 10^5 - 10^9 shots depending on bore erosion) requires launcher access — likely a multi-week outage. Target factory downtime stops plant operation (no buffer stock of cryogenic D-T targets). Turbine maintenance can be scheduled during Li loop maintenance.

**Comparison**: Less coupled than tokamaks (no disruption risk, no superconducting magnet quench cascades) but more coupled than steady-state laser IFE with separate driver and chamber maintenance schedules.

**Sub-factor B: Subsystem count (CAS22 sub-accounts representing >1% of total capital)**

Total capital: $3,283M (baseline model)
1% threshold: $32.8M

| CAS Account | Cost | >1% | Subsystem |
|-------------|------|-----|-----------|
| CAS22.01 (Blanket) | $41M | Yes | Liquid Li blanket + manifolds |
| CAS22.02 (Shield) | $31M | No | — |
| CAS22.05 (Structure) | $5M | No | — |
| CAS22.06 (Vacuum) | $8M | No | — |
| CAS22.07 (Driver) | $1,000M | Yes | EM launcher + capacitor banks |
| CAS22.08 (Target Factory) | $118M | Yes | Target manufacturing + injection |
| CAS22.11 (Installation) | $168M | Yes | Labor (not operational subsystem) |
| CAS22.20 (Coolant) | $72M | Yes | Li primary loop + steam HX |
| CAS22.30 (Aux Cooling) | $9M | No | — |
| CAS22.50 (Fuel Handling) | $52M | Yes | Tritium processing + storage |
| CAS22.70 (I&C) | $39M | Yes | Instrumentation (distributed, not single subsystem) |
| CAS23 (Turbine) | $70M | Yes | Steam turbine + generator |
| CAS24 (Electric) | $30M | No | — |
| CAS27 (Li inventory) | $70M | Yes | Special materials (not operational subsystem) |
| CAS50 (Spare parts, tritium startup) | $267M | Yes | Levelized cost (not operational subsystem) |

**Significant operational subsystems (>1% of capital)**:
1. EM launcher (driver)
2. Target factory + injection
3. Liquid Li blanket + primary loop
4. Steam turbine + generator
5. Tritium processing + fuel handling

**Count: 5-7** (depending on whether fuel handling and I&C are counted as single systems or aggregates)

**Score: 4** (5-7 significant subsystems)

**C4 final score**: (3 + 4) / 2 = **3.5**

**Justification**: Projectile ICF has relatively low plant complexity compared to tokamaks (5-7 subsystems vs 11-14 for HTS tokamaks with separate heating, fueling, magnet cryogenics, disruption mitigation, and PFC cooling). The dominant complexity is in the EM launcher (single-shot precision at 60 km/s, capacitor cycling, bore maintenance) and liquid Li loop (chemical reactivity, tritium extraction, pulsed thermal loading). The BOP is conventional and decoupled. Operational coupling is moderate — Li loop failure stops the plant but does not cascade to vessel damage. This is simpler than tokamaks where plasma-facing components, magnets, and auxiliary heating are tightly coupled through plasma stability.

---

### C5: Customization Needs (scored)

**Sub-factor A: Thermal rejection (1-4)**

**Score: 2** (Large cooling towers required — standard thermal cycle)

**Rationale**: Projectile ICF uses a conventional steam Rankine cycle with 33% thermal efficiency. At 304 MWe net output (baseline), gross thermal power is ~1,069 MW, requiring rejection of ~715 MW to the environment. This necessitates large wet or dry cooling towers identical to coal or fission plants. The pulsed fusion output is buffered by the liquid Li thermal mass, so the steam cycle sees quasi-steady heat input. No air-cooling option (plant is too large). No hybrid power conversion (no direct energy conversion).

**Sub-factor B: Fuel safety profile (1-4)**

**Score: 1** (D-T fuel — full tritium handling and breeding infrastructure)

**Rationale**: D-T fuel requires:
- Tritium startup inventory: 3 kg at $30,000/g = $90M (baseline model)
- Cryogenic target preparation (D-T ice layer inside each target)
- Tritium breeding in liquid Li blanket (TBR 1.8)
- Tritium extraction from Li coolant (continuous processing)
- Tritium inventory management (10-50 kg on-site at steady state)
- Regulatory burden for tritium release limits (even with high TBR, some permeation to secondary coolant and environment)
- Neutron activation of structure (though liquid Li blanket absorbs most neutrons, reducing vessel activation vs solid-wall D-T)

The TBR 1.8 advantage (25 kg/yr surplus) reduces long-term tritium supply risk but does not eliminate on-site tritium handling complexity. This is the same safety profile as tokamaks, stellarators, and other D-T IFE concepts — full radiological controls, tritium-compatible materials (avoiding tritium embrittlement), and remote handling.

**C5 raw score**: (2 + 1) / 2 = **1.5**

**Scaled to [1,5] range**: C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.67 = **1.7**

**Justification**: Projectile ICF has average to slightly worse site customization needs. The D-T fuel cycle (score=1) is the most demanding fuel safety profile, requiring full tritium infrastructure indistinguishable from tokamaks. The large cooling tower requirement (score=2) is standard for GW-thermal plants but precludes siting flexibility (needs water access or large dry cooling footprint). The concept offers no siting advantages over tokamaks — both need tritium licenses, both need large cooling, both have neutron activation (though projectile ICF's liquid Li blanket reduces structural activation). The score of 1.7 places it in the bottom quartile of the fusion landscape, tied with conventional D-T tokamaks and below D-D or aneutronic concepts.

---

### C8: Data Adequacy (scored)

**Sub-factor A: Source diversity & independence (1-5)**

**Score: 3** (Primarily company publications with some independent validation)

**Rationale**:
- **Company sources dominate**: First Light Fusion technology pages, white papers, and investor communications (captured via IP Group) are the primary data sources. These are company-controlled narratives, not peer-reviewed.
- **Independent validation exists for TBR only**: TÜV SÜD UK validated TBR 1.8 (Feb 2026) through computational neutronic analysis — this is a credible third-party check on one claim. UKAEA validated fusion neutrons from the 2022 Machine 3 shot (~50 neutrons) — this confirms fusion occurred but not gain magnitude.
- **Peer-reviewed architecture literature is absent**: No published reactor design study in Fusion Engineering & Design, IEEE, or Phil. Trans. R. Soc. A specifically on projectile ICF power plants. Hawker (2020) IFE economics paper is peer-reviewed but concept-agnostic (applies to all IFE, not projectile-specific).
- **No independent plant study**: No DOE, EPRI, or university group has modeled projectile ICF economics or validated FLF's cost targets.

The score of 3 reflects "mix of independent and company sources with some public peer review" — the TÜV validation and UKAEA neutron confirmation elevate this above pure company data (score=2), but the lack of independent reactor design studies prevents score=4.

**Sub-factor B: Reactor design specification (1-5)**

**Score: 3** (Partial design with key subsystems defined but gaps in integration)

**Rationale**:
- **Well-specified subsystems**: Liquid Li blanket geometry (1m thick curtains), TBR (1.8), tritium surplus (25 kg/yr), steam Rankine BOP, plant size (150-500 MWe), rep rate (0.011-0.1 Hz), Machine 4 driver stored energy (100 MJ).
- **Gaps in integration**:
  - EM gun architecture (barrel length, capacitor configuration, switching, bore materials) is not detailed
  - Target injection mechanism (how targets are positioned in projectile path at 0.033 Hz) is not described
  - Liquid Li pump specifications (flow rate, head, power) are not published
  - Chamber clearing time (how long for Li curtain to resettle after blast) is not quantified
  - Recirculating power breakdown (driver recharge, Li pumps, tritium processing) is not given
- **No detailed engineering drawings or CAD**: The design is conceptual-level, not preliminary or detailed design.

This is a "partial design with key subsystems defined but gaps in integration" (score=3). It is better than "preliminary design with significant specification gaps" (score=2) because the blanket, BOP, and rep rate are specified. It is worse than "comprehensive conceptual design with major subsystems specified" (score=4) due to missing driver and Li loop details.

**Sub-factor C: LCOE parameter coverage (blocking gap count from gap_report.md)**

From gap_report.md:
- **Blocking gaps**:
  1. EM gun capital cost (Gap 1)
  2. Target gain achieved (Gap 2)
  3. Gain vs velocity scaling (Gap 3)
  4. Target fabrication cost at scale (Gap 4)
  5. Driver wall-plug efficiency (Gap 5)

**Count: 5 blocking gaps**

**Score: 2** (5-7 blocking gaps)

**Rationale**: Five blocking LCOE-critical parameters have no published data: driver cost, demonstrated gain, gain scaling, target cost, and driver efficiency. These gaps span both physics (gain) and engineering (costs). The gap_report.md identifies these as "blocking" because LCOE cannot be credibly estimated without them — the model in this analysis makes assumptions for all five, producing a 40× LCOE range (62-2,507 $/MWh) that reflects deep uncertainty, not estimation error.

**Sub-factor D: Commercialization pathway clarity (1-5)**

**Score: 1** (No commercialization pathway articulated **by an active pursuer**)

**Rationale**:
- **First Light Fusion abandoned projectile ICF** in September 2025, pivoting to FLARE (pulsed-power liner implosion). The FLARE announcement explicitly states the EM gun approach was not cost-competitive: "FLARE driver cost per joule: $2 (vs $6-13 for alternatives)." This implies FLF's internal TEA found the projectile driver economically unviable.
- **No successor organization**: NearStar Fusion pursues MTIF (magnetized target, D-D fuel), which is taxonomically distinct from pure projectile ICF. No other company is developing hypervelocity projectile-driven D-T fusion.
- **No published commercialization timeline**: FLF's pre-pivot materials mentioned pilot plant targets (<$1B, 150 MWe) and commercial plant targets (<$5B, 500 MWe) but no milestone timeline. These targets are now moot.
- **Machine 4 cancellation eliminates physics validation pathway**: The only device that would have tested gain at 60 km/s was cancelled before construction. There is no experimental roadmap to retire the gain uncertainty.

This is "no commercialization pathway" (score=1) because the concept is orphaned. Even if FLF's pre-pivot commercialization narrative was "vague or aspirational" (score=2), the current status is abandonment. An active pursuer with even a speculative plan would score higher; projectile ICF has none.

**C8 final score**: (3 + 3 + 2 + 1) / 4 = **2.25** → **2.3** (rounded to 0.1)

**Justification**: Data adequacy is poor. Company-provided architecture data is partially detailed (blanket, BOP, rep rate, TBR) with limited independent validation (TÜV on TBR only). Five blocking LCOE gaps remain (driver cost, gain, target cost, driver efficiency, gain scaling). Most critically, the concept has no active commercial pursuer — FLF pivoted to FLARE, and NearStar is pursuing a different approach (MTIF). The score of 2.3 reflects "almost exclusively company publications" (source diversity), "partial design" (reactor specification), "5-7 blocking gaps" (LCOE coverage), and "no commercialization pathway" (orphaned concept). This is the lowest data adequacy score in the D-T landscape except for fully speculative concepts with no demonstrated fusion.

---

### C7: Technical Risk Evidence (Risk Matrix)

The risk matrix below scores 7 functions × 2 subcategories (physics risk, hardware risk) = 14 cells. Each cell includes: plant requirement, best demonstrated, gap ratio, closure mechanism, classification (binary/degrading), and evidence tier (1-5).

---

#### **Function 1: Plasma Performance**
*Target: Density, temperature, confinement sufficient for net energy gain (fusion yield ≥ driver energy delivered)*

**1a. Physics Risk**
- **Plant requirement**: Compressed D-T fuel must reach ρR ≥ 3 g/cm² at temperature ≥ 10 keV to achieve gain ≥200× (fusion yield ≥6 GJ per 30 MJ delivered to target)
- **Best demonstrated**: Machine 3 (2022, 6.5 km/s) produced ~50 fusion neutrons at unspecified ρR and temperature. This corresponds to Q < 0.001 (eight orders of magnitude below Q=200 commercial requirement). NIF's ignition (Dec 2022, indirect drive) achieved Q=4× at higher driver energy and different compression geometry.
- **Gap ratio**: Q_required / Q_demonstrated = 200 / 0.001 = **200,000×** (commercial vs FLF Machine 3); 50× (commercial vs NIF indirect drive at analogous physics)
- **Closure mechanism**: FLF claims proprietary "amplifier" target with multiple internal cavities creates successive shockwave amplification, compressing fuel to >10 terapascals and accelerating fuel to >70 km/s inward velocity. Simulations show gain 200-1000× at 60 km/s projectile impact. No peer-reviewed experimental validation of this mechanism exists.
- **Classification**: **Binary** — if gain <200× at 60 km/s, the concept cannot produce net electricity at FLF's rep rates (0.033 Hz baseline) even with zero driver cost. Net power becomes negative below ~3 GJ/shot per model.
- **Evidence tier**: **1** (Asserted/absent — gain at commercial velocity never tested; Machine 4 cancelled; amplifier physics is proprietary simulation only)

**1b. Hardware Risk**
- **Plant requirement**: Target must maintain concentricity, D-T ice layer uniformity, and internal cavity geometry to within tolerances that preserve implosion symmetry at 60 km/s impact. Target injection must position target in projectile path to within mm-scale precision at 0.033 Hz (or faster for higher power).
- **Best demonstrated**: Machine 3 targets were hand-fabricated at lab scale (~1-10 units). Fusion was achieved, confirming target survived projectile impact and produced compression. Target manufacturing tolerances, defect rates, and injection precision are not published.
- **Gap ratio**: **N/A** (target survived impact at 6.5 km/s; scaling to 60 km/s and mass production at 1-4M units/year is undemonstrated)
- **Closure mechanism**: Scale up precision manufacturing (injection molding, additive, or diamond-turning) to IFE production rates. NIF targets are manufactured at <100 units/year at high cost; IFE requires 10,000× higher throughput at <$10/unit cost. FLF's amplifier geometry is proprietary — materials (plastic, metal, cryogenic D-T) and tolerances are unknown.
- **Classification**: **Degrading** — target defects or injection errors reduce yield per shot (lower effective gain), increasing required rep rate to maintain power output. High defect rate (>10%) could make consumable costs prohibitive, but does not create zero net electricity if some targets work.
- **Evidence tier**: **2** (Simulation only, no mass-production validation — lab-scale targets worked at 6.5 km/s; no data on 60 km/s survival or manufacturing scalability)

---

#### **Function 2: Driver / Energy Input**
*Target: Heating, compression, or catalytic species delivery sufficient to initiate fusion*

**2a. Physics Risk**
- **Plant requirement**: Projectile must deliver ≥30 MJ of kinetic energy to target at 60 km/s with positional precision sufficient to drive symmetric implosion (impact point within <1mm of target center to avoid asymmetric compression).
- **Best demonstrated**: Machine 3 (6.5 km/s) delivered kinetic energy to target with sufficient symmetry to produce fusion neutrons. Velocity precision and impact positioning accuracy at 6.5 km/s are not published but were adequate to trigger compression. Machine 4 (60 km/s, 100 MJ stored) was never built.
- **Gap ratio**: Velocity scaling 6.5 → 60 km/s = **9.2× velocity increase**. Kinetic energy scaling is quadratic: (60/6.5)² = **85× energy increase** per projectile. Precision requirements likely scale inversely with velocity (faster impact = tighter tolerances).
- **Closure mechanism**: Machine 4 was designed to achieve 60 km/s using electromagnetic acceleration (capacitor-driven coilgun or railgun architecture, proprietary). Bore materials, sabot separation, and projectile stability at hypervelocity are engineering challenges with no demonstrated solution. Precision guidance (if needed) would require active steering or ultra-precise launcher repeatability.
- **Classification**: **Binary** — if driver cannot reach 60 km/s with sufficient repeatability, gain drops below 200× threshold (per FLF's gain-vs-velocity scaling claim), making net electricity impossible. 6.5 km/s (demonstrated) is insufficient for commercial operation.
- **Evidence tier**: **2** (Simulation only — Machine 3 validated 6.5 km/s; Machine 4 design existed but was cancelled before construction; no experimental data at 60 km/s)

**2b. Hardware Risk**
- **Plant requirement**: EM launcher barrel must survive ≥10⁵ shots (minimum for multi-year operation at 0.033 Hz) without bore erosion degrading projectile velocity or precision. Capacitor banks must cycle at 0.033-0.1 Hz for 40 years (~1.3×10⁸ total shots at 0.1 Hz). Sabot materials must survive 60 km/s acceleration stress (~10⁶ g peak) without fragmenting.
- **Best demonstrated**: Machine 3 operated at 6.5 km/s in lab setting (non-rep-rated, <100 shots total over campaign). EM launcher bore erosion at 6.5 km/s is unknown but manageable at lab scale. No rep-rated EM launcher at any velocity >5 km/s has been demonstrated. DoD railgun programs achieved 2-4 km/s at rep rates <0.01 Hz but faced severe bore erosion (barrels lasted 10-100 shots).
- **Gap ratio**: **N/A** (60 km/s rep-rated launcher never built; bore lifetime at 60 km/s is truly unknown)
- **Closure mechanism**: FLF proposed exotic barrel materials (tungsten alloys, ceramic composites, or ablative liners) and active cooling to manage bore erosion. Capacitor banks at 100 MJ scale exist (Z-machine at Sandia uses 20 MJ capacitors) but switching at 0.1 Hz for 40 years is undemonstrated. Sabot separation at 60 km/s requires materials that survive launch but detach cleanly — no validated design exists.
- **Classification**: **Degrading** — bore erosion reduces launcher lifetime, increasing replacement frequency and driving up lifecycle costs (driver replacement becomes recurring OPEX, not one-time CAPEX). Severe erosion (barrel replacement every 10⁴ shots) would make LCOE prohibitive but does not prevent net electricity if barrels are replaced frequently.
- **Evidence tier**: **1** (Asserted/absent — 60 km/s launcher never built; bore erosion at hypervelocity has no material solution demonstrated; Machine 4 cancellation means this problem was deemed unsolved by FLF)

---

#### **Function 3: Instability Control**
*Target: Suppression or tolerance of intrinsic plasma instabilities (Rayleigh-Taylor, asymmetry growth)*

**3a. Physics Risk**
- **Plant requirement**: Implosion symmetry must be maintained during projectile-driven compression to within ~5% ρR variation (standard ICF symmetry requirement for ignition). Rayleigh-Taylor instabilities at fuel-pusher interface during compression must not degrade ρR below ignition threshold.
- **Best demonstrated**: Machine 3 (2022) produced fusion neutrons, implying compression symmetry was adequate to achieve fuel heating (though yield was ~50 neutrons, far below ignition). NIF's ignition campaigns show that achieving <5% asymmetry in indirect drive requires exquisite hohlraum and capsule precision. FLF's amplifier target uses converging shocks from multiple cavities — instability growth in this geometry is not validated by peer-reviewed experiment.
- **Gap ratio**: **N/A** (symmetry at 6.5 km/s was sufficient for some fusion; symmetry at 60 km/s and gain ≥200× is undemonstrated)
- **Closure mechanism**: FLF claims the amplifier target's cavity geometry naturally symmetrizes the implosion via multiple converging shocks, reducing sensitivity to projectile impact angle and target positioning errors. This is a passive symmetrization approach (no active beam balancing as in laser ICF). Simulations show this works; no experimental validation exists.
- **Classification**: **Degrading** — asymmetry reduces gain (lower ρR, lower temperature) but does not necessarily prevent all fusion. If asymmetry limits gain to 50-100× instead of 200-1000×, LCOE degrades but net electricity may still be possible at higher rep rates.
- **Evidence tier**: **2** (Simulation only — Machine 3 validated some compression symmetry at 6.5 km/s; FLF's amplifier symmetrization mechanism is proprietary and not peer-reviewed; no subscale validation of cavity-driven symmetry at NIF or other ICF facilities)

**3b. Hardware Risk**
- **Plant requirement**: Projectile impact angle must be perpendicular to target surface within <1° to avoid asymmetric compression. Target injection must align target orientation with projectile trajectory. Launcher barrel straightness and projectile spin stabilization must maintain trajectory precision over ~10-100m barrel length.
- **Best demonstrated**: Machine 3 achieved sufficient impact symmetry to produce fusion at 6.5 km/s. Impact angle tolerances, target alignment precision, and projectile spin dynamics are not published.
- **Gap ratio**: **N/A** (6.5 km/s precision was adequate; 60 km/s precision requirements likely tighter due to faster impact — less time for course correction or alignment)
- **Closure mechanism**: Passive: launcher barrel straightness + projectile spin stabilization (like artillery shells). Active: terminal guidance using small thrusters or magnetic deflection (adds complexity and cost). FLF has not disclosed which approach is planned. Precision target injection (robotic alignment) at 0.033 Hz is achievable with industrial robotics; scaling to 0.1 Hz may require parallel injection systems.
- **Classification**: **Degrading** — misalignment reduces symmetry and thus gain, but does not prevent all fusion unless impact angle is grossly wrong (>10° off-axis).
- **Evidence tier**: **2** (Simulation + limited experimental validation — Machine 3 showed precision was achievable at 6.5 km/s; no data on 60 km/s alignment tolerances or target injection at commercial rep rates)

---

#### **Function 4: Plasma-Wall Interaction**
*Target: Erosion, heat flux management, surface damage mitigation*

**4a. Physics Risk**
- **Plant requirement**: Liquid Li curtain must absorb neutrons (80% of fusion energy) and alpha particles (20%) without excessive vaporization or hydrodynamic disruption of curtain geometry. Curtain must re-establish 1m thickness within 30s (baseline rep rate) or 10s (commercial rep rate) after each shot's blast loading.
- **Best demonstrated**: Liquid metal first walls have been studied extensively in IFE (HYLIFE, HYLIFE-II, Z-IFE FLiBe designs) but never operated under fusion neutron flux at any scale. FLF's TBR 1.8 validation by TÜV (2026) confirms neutronic design is sound (Li absorbs neutrons as expected) but does not validate hydrodynamic stability under blast.
- **Gap ratio**: **N/A** (liquid Li blanket neutronic performance is validated; hydrodynamic response to pulsed 30 GJ energy deposition is undemonstrated)
- **Closure mechanism**: Computational fluid dynamics (CFD) modeling of liquid Li curtain response to fusion blast, followed by subscale blast testing (chemical explosives or laser-driven shocks to simulate fusion energy deposition). Chamber clearing time depends on Li flow rate, gravity-driven resettlement, and vapor condensation. FLF has not published CFD results or blast test data.
- **Classification**: **Degrading** — if curtain clearing time exceeds rep rate requirement (e.g., 30s clearing at 10s rep rate target), maximum achievable rep rate is limited, reducing plant output and increasing LCOE. Does not prevent net electricity at lower rep rates.
- **Evidence tier**: **2** (Simulation only — TBR validation confirms neutron absorption; no experimental data on hydrodynamic blast response or curtain resettlement time)

**4b. Hardware Risk**
- **Plant requirement**: Liquid Li pumps must circulate curtain flow to maintain 1m thickness continuously. Structural vessel behind Li curtain must survive 40 years of pulsed thermal and pressure loading without fatigue cracking. Li containment must prevent air/water contact (Li is pyrophoric). Pump seals, heat exchangers, and piping must tolerate Li corrosion at operating temperature (400-500°C typical for Li coolant).
- **Best demonstrated**: EM pumps for liquid Li exist at HYLIFE scale (8 m³/s per pump, 1.32 MW electrical, per UCRL-53356). Fission reactors using liquid metal coolants (FFTF, EBR-II) demonstrated Li/Na pumps and heat exchangers at smaller thermal scales (~100 MWth vs 1 GWth for fusion). No pulsed Li loop has been demonstrated at fusion scale.
- **Gap ratio**: **N/A** (Li pump technology exists; scaling to 1 GWth pulsed fusion thermal output is undemonstrated)
- **Closure mechanism**: Scale up HYLIFE EM pump designs to FLF flow rates (not published, but likely ~10-20 m³/s for 1m curtain at chamber scale). Use fission liquid-metal reactor experience for Li-compatible materials (austenitic stainless steel, refractory alloys) and corrosion mitigation (oxygen control, cold traps). Heat exchanger between Li primary and water secondary requires intermediate loop or advanced Li-water barrier to prevent Li-water reaction risk.
- **Classification**: **Degrading** — Li pump failure or corrosion-driven leaks reduce plant availability and increase O&M costs, but do not prevent net electricity if repaired. Severe corrosion (requiring blanket replacement before 40 years) would add unplanned capital cost.
- **Evidence tier**: **3** (Subscale demonstration — Li EM pumps and heat exchangers exist at fission scale; HYLIFE design is detailed but never built; no operating fusion-scale Li loop)

---

#### **Function 5: Neutron/Particle Handling**
*Target: Activation, shielding, displacement damage mitigation*

**5a. Physics Risk**
- **Plant requirement**: Liquid Li curtain (1m thick) must attenuate 14.1 MeV neutrons to <1% leakage to structural vessel, preventing vessel activation and displacement damage over 40-year plant life. Neutron multiplication via Li(n,2n) reactions must not create excessive activation products or degrade TBR.
- **Best demonstrated**: TÜV SÜD UK validated TBR 1.8 via neutronic simulation (Feb 2026), confirming Li curtain captures neutrons as designed. Neutron attenuation through 1m Li is well-characterized by MCNP transport codes — 14.1 MeV neutrons are thermalized and captured primarily via ⁶Li(n,α)T reaction. No experimental validation under fusion neutron flux.
- **Gap ratio**: **N/A** (neutron transport physics is well-understood; TBR validation is computational, not experimental, but physics is not in question)
- **Closure mechanism**: Li blanket neutronic design is mature from decades of fusion blanket studies. The 1m thickness is conservative (thicker than most solid blanket designs' neutron-stopping distance). Activation products in Li (mainly tritium, ⁷Be, small amounts of ³H²) are manageable via cold traps and chemical processing. Vessel activation is claimed negligible ("neutrons do not reach vessel wall").
- **Classification**: **Degrading** — if neutron leakage is higher than simulated (e.g., due to Li curtain gaps or flow instabilities), vessel activation increases, requiring earlier decommissioning or thicker shielding (added capital cost). Does not prevent net electricity.
- **Evidence tier**: **4** (Near-regime demonstrated — neutronic simulations validated by independent third party; Li neutron cross-sections well-measured; no fusion-scale experimental confirmation but physics is standard)

**5b. Hardware Risk**
- **Plant requirement**: Structural vessel and shield must tolerate residual neutron flux (if any) and gamma radiation from activated Li without embrittlement or swelling over 40 years. Remote handling equipment must access Li loop for maintenance (pumps, heat exchangers) in activated environment. Waste disposal for activated Li at end-of-life must meet regulatory limits.
- **Best demonstrated**: Austenitic stainless steel vessel materials in fission reactors tolerate decades of neutron flux at lower energies (MeV-scale vs 14.1 MeV fusion). ITER first-wall materials (EUROFER, W-armor) are tested in fission neutron environments but not at fusion-relevant fluence (MW·yr/m²). Li activation products (tritium, ⁷Be) are manageable in fission/ITER experience.
- **Gap ratio**: Neutron fluence to vessel (if Li curtain works as claimed) is ~10⁻² of solid-wall D-T reactor. **0.01× tokamak fluence**.
- **Closure mechanism**: FLF claims "vessel never replaced" due to negligible neutron exposure. If true, structural materials see <0.1 dpa over 40 years (vs 20-50 dpa for tokamak first wall). Standard austenitic or ferritic steel survives this easily. Remote handling is simplified vs tokamak (no solid blanket module replacement every 2-4 years). Waste disposal: activated Li at end-of-life (~10-20 tonnes) is low-level waste if TBR claim holds (tritium extracted, minimal long-lived activation).
- **Classification**: **Degrading** — if neutron leakage is higher than claimed, vessel lifetime shortens (requires replacement before 40 years, adding $100-300M cost). Does not prevent operation, just increases lifecycle cost.
- **Evidence tier**: **3** (Subscale demonstration — fission reactor vessel materials tested; ITER materials program provides some high-energy neutron data; no fusion-fluence test at FLF's claimed low neutron leakage environment)

---

#### **Function 6: Fuel Cycle Closure**
*Target: Breeding, extraction, purification, recycling*

**6a. Physics Risk**
- **Plant requirement**: TBR ≥1.05 (minimum for self-sufficiency with reasonable doubling time). FLF claims TBR 1.8, enabling self-sufficiency and 25 kg/yr surplus at 333 MWe.
- **Best demonstrated**: TBR 1.8 independently validated by TÜV SÜD UK (Feb 2026) via MCNP neutronic simulations of the Li blanket design. This is the highest validated TBR in the D-T fusion landscape. No experimental tritium breeding measurement at fusion scale (ITER will be first).
- **Gap ratio**: TBR 1.8 / TBR 1.0 (breakeven) = **1.8× above self-sufficiency threshold**
- **Closure mechanism**: ⁶Li(n,α)T reaction in liquid Li blanket. Natural Li (7.5% ⁶Li) or enriched Li (up to 95% ⁶Li) can be used. FLF white paper cites natural Li cost ~$70M vs enriched ~$143-451M, implying natural Li may suffice for TBR 1.8 (though not explicitly stated). Tritium extraction from Li uses standard molten-salt/liquid-metal fuel processing (cold traps, vacuum extraction, or molten-salt scrubbing). Technology exists from MSR fission programs.
- **Classification**: **Binary** (standard D-T rule) — if TBR <1.0, plant cannot achieve self-sufficiency and requires external tritium supply indefinitely. At current tritium scarcity (~20 kg/yr global CANDU production), fleet deployment is impossible without self-sufficiency.
- **Evidence tier**: **4** (Near-regime demonstrated — TBR validated by independent third party via well-benchmarked neutronics codes; extraction technology exists in fission; no fusion-scale experimental validation but physics and chemistry are mature)

**6b. Hardware Risk**
- **Plant requirement**: Tritium extraction system must remove tritium from flowing liquid Li at sufficient rate to maintain <100 kg total tritium inventory on-site (regulatory limit varies by jurisdiction; US NRC typically <1 kg for non-fusion facilities, but fusion plants will have exemptions). Extraction must achieve >95% efficiency to minimize tritium loss to secondary coolant or environment. Purification must deliver fuel-grade D-T to cryogenic targets (>99.9% purity). Tritium inventory must be controlled via accountancy and permeation barriers.
- **Best demonstrated**: ITER's tritium processing systems (under construction) will handle ~kg-scale tritium inventory with extraction from PbLi test blankets. MSR fission programs (MSRE at ORNL) extracted fission products and tritium from molten salt at smaller scales. No fusion-scale tritium extraction from liquid Li at 1 GWth has been built.
- **Gap ratio**: ITER tritium systems handle ~4 kg inventory; FLF at 333 MWe with 25 kg/yr surplus likely holds 10-50 kg on-site inventory. **10× ITER inventory scale**.
- **Closure mechanism**: Scale up ITER tritium extraction technology (cold traps, getter beds, isotope separation via cryogenic distillation or palladium permeation). Li-tritium chemistry is well-understood (tritium dissolves in Li as LiT; extracted by vacuum degassing or reaction with H₂ to form HT gas). Permeation barriers (alumina coatings, double-wall heat exchangers) prevent tritium contamination of secondary water coolant.
- **Classification**: **Degrading** — low extraction efficiency increases tritium inventory and permeation losses, raising regulatory burden and fuel cost, but does not prevent operation. Worst case: external tritium purchase supplements breeding (expensive but not a showstopper if TBR >1.0).
- **Evidence tier**: **3** (Subscale demonstration — ITER tritium systems under construction; MSR extraction technology demonstrated at smaller scale; no fusion-scale Li-T extraction system built)

---

#### **Function 7: Power Conversion & BOP**
*Target: Energy conversion, heat rejection, auxiliaries*

**7a. Physics Risk**
- **Plant requirement**: Pulsed fusion energy deposition (30 GJ per shot at 0.033 Hz = 990 MW average) must be converted to quasi-steady thermal output via liquid Li thermal mass, then to 353 MWe gross electric via steam Rankine cycle at 33% efficiency.
- **Best demonstrated**: Steam Rankine cycles at 300-1000 MWe scale are commercial technology (TRL 9). Thermal buffering of pulsed heat sources is well-understood (molten salt solar thermal plants, batch chemical reactors). Liquid Li specific heat is 4.2 kJ/kg·K; thermal mass of 10-20 tonnes Li circulating provides natural buffering for 30 GJ pulses every 30s.
- **Gap ratio**: **1× or better** (no gap — physics of thermal buffering and steam cycles is fully mature)
- **Closure mechanism**: Not needed — steam Rankine BOP is off-the-shelf 150-year-old technology. Only novelty is coupling to pulsed Li heat source, which is standard thermal engineering (buffering via Li loop thermal mass). FLF explicitly confirmed: "After the lithium heat exchanger, the plant is identical to many other already working facilities."
- **Classification**: **Not applicable** (no risk — thermal buffering and steam conversion are solved problems)
- **Evidence tier**: **5** (Operating-regime demonstrated — GW-scale steam Rankine cycles operate globally; pulsed heat sources buffered in molten salt solar plants; Li heat transfer validated in fission)

**7b. Hardware Risk**
- **Plant requirement**: Li-to-water heat exchangers must transfer 1,069 MW thermal from liquid Li primary (400-500°C) to water/steam secondary (300-350°C) without Li-water contact (prevents explosive reaction). Heat exchangers must tolerate pulsed thermal cycling (30 GJ every 30s creates thermal stress). Steam turbine, condenser, and cooling towers must be sized for 353 MWe gross electric at 33% efficiency (standard for this scale).
- **Best demonstrated**: Li-water heat exchangers exist in fission liquid-metal reactors (EBR-II, FFTF used Na-water; technology is similar). Double-wall or intermediate-loop designs prevent Li-water contact. Steam turbines at 300-400 MWe scale are commodity (GE, Siemens, Mitsubishi supply). Cooling towers for 700 MW heat rejection (baseline) are standard.
- **Gap ratio**: **1× or better** (fission liquid-metal reactors demonstrated Li/Na heat exchangers; steam turbines at this scale are commercial off-the-shelf)
- **Closure mechanism**: Not needed — use fission liquid-metal reactor heat exchanger designs (double-wall tube-and-shell, intermediate Na or NaK loop, or advanced Li-compatible alloys for single-wall). Thermal cycling fatigue is manageable with proper materials (austenitic SS, Inconel). Turbine and cooling are COTS.
- **Classification**: **Not applicable** (no risk — all components are TRL 8-9)
- **Evidence tier**: **5** (Operating-regime demonstrated — fission liquid-metal reactors operated for decades; GW-scale steam turbines in daily use; all components mature)

---

### Function-Level Means (F1-F7)

| Function | Physics Risk Tier | Hardware Risk Tier | Mean |
|----------|------------------|-------------------|------|
| F1: Plasma Performance | 1 | 2 | **1.5** |
| F2: Driver / Energy Input | 2 | 1 | **1.5** |
| F3: Instability Control | 2 | 2 | **2.0** |
| F4: Plasma-Wall Interaction | 2 | 3 | **2.5** |
| F5: Neutron/Particle Handling | 4 | 3 | **3.5** |
| F6: Fuel Cycle Closure | 4 | 3 | **3.5** |
| F7: Power Conversion & BOP | 5 | 5 | **5.0** |

---

### Heritage Credit Assessment

**Fuel type**: D-T (qualifies for heritage credit consideration)

**Lineage check**:
- **Laser IFE (NIF, HYLIFE)**: Projectile ICF shares the same D-T implosion physics (compression to ignition conditions, alpha heating, ρR requirements) but uses a different driver (kinetic impact vs laser ablation). The target geometry (FLF's amplifier cavities) is proprietary and has no NIF/LLNL validation. Compression mechanism is analogous but not experimentally traced to NIF/LIFE pedigree.
- **Heavy-ion ICF (HIBALL)**: Similar implosion physics, different driver. No experimental heritage (HIBALL was never built).
- **Other IFE**: No direct heritage to MagLIF (uses external B-field, different target), Z-pinch (different compression mechanism), or muon-catalyzed fusion.

**Heritage credit eligibility**: **Partial** — shares D-T implosion physics with laser ICF (NIF floor of 3.5 applies to F1-F3) but driver (EM launcher) and target (amplifier cavities) have no heritage. Apply floor cautiously.

**Applying laser IFE floor (3.5) to F1-F3**:
- F1: 1.5 → **3.5** (heritage floor applied — NIF demonstrated ignition physics in D-T; FLF's amplifier target is unproven but implosion physics is analogous)
- F2: 1.5 → **3.5** (heritage floor applied — NIF demonstrated driver energy coupling to target; FLF's EM launcher is novel but energy delivery to target is conceptually validated)
- F3: 2.0 → **3.5** (heritage floor applied — NIF demonstrated instability control in ICF; FLF's cavity-driven symmetrization is novel but instability physics is shared)
- F4: 2.5 → no change (heritage does not apply to plasma-wall interaction in IFE — liquid Li first wall is novel; NIF has no liquid wall)
- F5: 3.5 → no change (already above floor; neutron handling is concept-specific)
- F6: 3.5 → no change (already above floor; TBR is concept-specific)
- F7: 5.0 → no change (already above floor; BOP is mature)

**Revised function means with heritage credit**:
- F1: 3.5 (heritage floor)
- F2: 3.5 (heritage floor)
- F3: 3.5 (heritage floor)
- F4: 2.5 (no change)
- F5: 3.5 (no change)
- F6: 3.5 (no change)
- F7: 5.0 (no change)

**C7 (computed by Python)**: Mean of F1-F7 (after heritage) = (3.5 + 3.5 + 3.5 + 2.5 + 3.5 + 3.5 + 5.0) / 7 = 25.0 / 7 = **3.6** (rounded to nearest 0.5 = **3.5**)

**Function-level cap check**: F4 = 2.5 is the lowest function mean after heritage. Since 2.5 > 1.5, the function-level cap does NOT apply. C7 remains 3.5.

---

### Binary Risks Identified

1. **Target gain <200× at 60 km/s** (Function 1, Physics): If gain is below 200×, net electric power is negative at FLF's baseline rep rate (0.033 Hz) even with zero driver cost. Plant cannot produce electricity.

2. **Driver cannot reach 60 km/s** (Function 2, Physics): If EM launcher cannot achieve 60 km/s projectile velocity, gain falls below commercial threshold per FLF's claimed gain-vs-velocity scaling. Net electricity impossible.

3. **TBR <1.0** (Function 6, Physics): Standard D-T binary risk — if tritium breeding fails to achieve self-sufficiency, plant requires perpetual external tritium supply. At current global CANDU production (~20 kg/yr), fleet deployment impossible. (Note: FLF's TBR 1.8 validation makes this risk retired, but it is listed per mandatory framework rule.)

---

## YAML Scores Block

```yaml
---
scores:
  C1: 2.4
  C3: 2.9
  C4: 3.5
  C5: 1.7
  C8: 2.3
  F1: 3.5
  F2: 3.5
  F3: 3.5
  F4: 2.5
  F5: 3.5
  F6: 3.5
  F7: 5.0
  binary_risks:
    - "Target gain below 200× at 60 km/s projectile velocity prevents net electricity production at baseline rep rate (0.033 Hz)"
    - "EM launcher failure to reach 60 km/s causes gain to fall below commercial threshold, making net electricity impossible"
    - "Tritium breeding ratio below 1.0 prevents self-sufficiency and blocks fleet deployment (note: FLF's TBR 1.8 validation retires this risk, but listed per D-T framework rule)"
---
```
