# Cross-Concept Calibration of LCOE Downselect Scores

You are performing **Pass 2** of a two-pass scoring system for long-term LCOE
potential of fusion energy concepts. In Pass 1, each concept was scored
independently by a separate Claude session. Your job is to review all scores
together and calibrate them for cross-concept consistency.

## Your Task

### Step 1: C7 Gate Audit (do this FIRST, before other criteria)

The most common Pass 1 error is **undercounting binary gates**. Each concept's
C7 justification lists its gates, but Pass 1 scorers often collapsed multiple
distinct physics requirements into a single gate, or omitted gates that peer
concepts were penalized for.

**For each concept**, do the following:

a) **List every physics or engineering milestone** that must succeed for the
   concept to produce net electricity. Be granular — if a concept requires
   (1) a novel confinement mode, (2) a novel fuel burn regime, AND (3) a
   novel energy conversion mechanism, those are THREE gates, not one.

b) **Cross-check gates against peer concepts.** If Concept A is penalized for
   "driver lifespan at rep-rate" as a binary gate, then every pulsed concept
   with a novel driver must also carry this gate (or explain why it's retired
   for that concept). Common gates that should be checked across ALL concepts:
   - Net energy gain (Q > 1 at the claimed conditions)
   - Confinement mode validity (at commercial parameters)
   - Driver/heating system at commercial rep-rate or power level
   - Energy conversion mechanism (if non-standard)
   - Fuel burn regime (if non-standard, e.g., nonthermal, aneutronic)
   - Chamber/first-wall survival at commercial conditions
   - Any claimed energy-per-event or gain that exceeds standard physics by >10×

c) **Flag undercounted gates.** If your audit finds gates that Pass 1 missed,
   list them explicitly with severity and evidence level. Recompute C7 from
   the corrected gate list using the rubric formula.

d) **Apply the floor rule strictly**: ≥3 unretired binary gates (at
   "analytically supported" or worse) → C7 = 1.0. No overrides.

### Step 2: Full Criteria Consistency Review (C1–C7)

After the gate audit, review all criteria for cross-concept consistency:

- Same physical characteristic scored differently across concepts
  (e.g., "single chamber per plant" scored as replication=3 for one IFE
  concept but replication=1 for another)
- Score inversions: concept A has strictly better attributes than B on
  a criterion but scores lower
- Unjustified spread: concepts with similar architectures scoring >1 point
  apart on a criterion without clear justification
- Criteria where the justification contradicts the score
- C4 (complexity): verify that physics coupling chains are NOT counted —
  only operational failure cascades and maintenance dependencies. Apply the
  "magic wand" test.
- C6 (capacity factor): verify scores come from the physical CF_upper
  calculation per the rubric table, with NO ad-hoc TRL adjustments
  (those belong in C7). Critically, verify that scheduled downtime
  estimates use the **replacement complexity assessment** from the rubric:
  estimate replacement duration using the four multipliers (access method,
  maintenance environment, component modularity, serial step count).
  D-T concepts with toroidal geometry and remote handling typically need
  100–200 day blanket replacement campaigns, NOT the 2–3 weeks that
  Pass 1 scorers often assume. Aneutronic concepts with direct access
  and hands-on maintenance may need only days. Self-renewing components
  (liquid walls) eliminate the replacement term entirely. This is often
  the largest correction in C6 calibration.
- Module count boost applied consistently per the rubric's
  diminishing-returns table

### Step 3: Produce calibrated scores with adjustments explained

### Step 4: Z-Score Normalization

After producing the calibrated raw score table (Part 3), compute z-score
normalized scores. For each criterion i:

```
z_i,c = (calibrated_raw_score_i,c − mean_i) / stdev_i
```

Where mean_i and stdev_i are computed across all concepts for criterion i.
Then compute the z-score composite as the mean of z-scores across all 7
criteria for each concept.

**Include a z-score table as Part 5** with the same format as Part 3 but
showing z-scores instead of raw scores. Round z-scores to 2 decimal places.
Rank by z-score composite (this is the final ranking).

The z-score composite is the authoritative ranking metric. It ensures
every criterion contributes equally regardless of its natural scale.

## Output Format

Write the output to the file specified below. Structure it as:

### Part 1: C7 Gate Audit
For each concept, produce a standardized gate table:

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| [description] | Binary/Degrading/Schedule | Demonstrated/Subscale/Analytical/Speculative | −X.X | [justification] |

Then the recalculated C7 score. Flag any concept where the gate count
changed from Pass 1.

### Part 2: Other Inconsistencies Found
For each non-C7 inconsistency:
- Which concepts and criteria are affected
- What the original scores were
- Why they are inconsistent
- What the correct relative ordering should be

### Part 3: Calibrated Score Table

A single comparison table with all concepts and all criteria:

| Criterion | [Concept 1] | [Concept 2] | ... | Notes |
|-----------|-------------|-------------|-----|-------|
| C1 | original → calibrated | ... | ... | reason for any change |
| ... | ... | ... | ... | ... |
| **Composite** | **X.X** | **X.X** | ... | |

### Part 4: Ranking by Raw Composite

Rank concepts by calibrated raw composite score. For each:
- One sentence on its strongest structural advantage
- One sentence on its most binding constraint

### Part 5: Z-Score Normalized Table and Final Ranking

Compute z-scores for each criterion across all concepts. Present as a table:

| Criterion | [Concept 1] | [Concept 2] | ... |
|-----------|-------------|-------------|-----|
| C1 (z) | +X.XX | −X.XX | ... |
| ... | ... | ... | ... |
| **Z-Composite** | **+X.XX** | **−X.XX** | ... |

Then rank by z-composite (this is the final authoritative ranking).
For each concept in the final ranking:
- One sentence on its strongest structural advantage
- One sentence on its most binding constraint
- How confident you are in the relative ranking (High/Medium/Low)
- Note any cases where the z-score ranking differs from the raw ranking and why

---

## Scoring Framework (Rubric)

# LCOE Downselect Potential Framework — Scoring Rubric

## Purpose

Score this concept's **long-term cost reduction potential** — not today's modeled LCOE, but how much the LCOE can improve with deployment experience, manufacturing scale-up, and engineering maturation. Score 1–5 on each criterion (5 = most favorable). Composite = simple average.

Context: The Nature Energy finding (Jaffe et al., 2026) that fusion experience rates are likely 2–8% rather than the 8–20% commonly assumed was based on treating fusion as a monolith. This framework differentiates between concepts on the specific factors that drive learning rates.

---

## C1: Modularization (Subcomponent Level)

**Question**: How much of the plant can be factory-manufactured as standardized, repeatable modules?

### Construction Mode Classification

For each major CAS cost account, classify:

| Mode | Description | Learning multiplier |
|------|-------------|-------------------|
| **Factory module** | Fully assembled in factory, transported and installed as a unit (e.g., HTS magnet cassettes, target fabrication cartridges, power conversion skids) | High |
| **Site-assembled from factory parts** | Components factory-made but require skilled on-site integration (e.g., vacuum vessel from welded segments, beam line assembly) | Medium |
| **Stick-built / monolithic** | Poured, welded, or constructed in-place with no repeatable unit (e.g., biological shield, custom reactor building, one-off cryostat) | Low |

### Module Count Factor

The number of identical modules per plant accelerates learning — but with diminishing returns. The sweet spot is enough repetition to establish a dedicated production line and ride down the learning curve within a few plants, while each module remains complex enough that repetition teaches you something. Beyond ~50 units per plant, additional count adds little: the production line is already mature after the first few plants.

Very high counts (hundreds or thousands of identical items per plant) represent a different cost reduction mechanism — continuous-flow manufacturing yield optimization (analogous to semiconductor fabs), not discrete-module assembly learning. Still valuable, but should not score higher than the sweet spot.

**What matters most**: cumulative units produced across all plants (18 coils × 10 plants = 180 units is a strong learning curve), not units per plant alone.

| Identical modules per plant (single type) | Boost | Rationale |
|-------------------------------------------|-------|-----------|
| 10–49 (e.g., 18 TF coils, blanket segments) | +1.0 | **Sweet spot**: enough repetition for strong learning curve; each unit complex enough to benefit from manufacturing iteration; dedicated production line justified |
| 50–199 (e.g., stellarator modular coils) | +0.5 | Diminishing returns: production line matures quickly; learning per additional unit declines |
| 200+ or continuous-flow (e.g., IFE targets at kHz rate) | +0.5 | Learning dynamics shift from modular assembly to process/yield optimization — a different (still valuable) cost reduction mechanism, not classical module learning |
| 2–9 (e.g., NBI injectors, divertor cassettes) | +0.5 | Some repetition benefit but not enough to justify a dedicated production line |
| All unique / monolithic | −0.5 | No repetition learning within a plant |

### Score

```
C1 = cost-weighted average of (mode score per CAS account) + module repetition boost
```
Clamp to [1, 5].

**Use**: CAS breakdown for cost weights, model_setup.py and analysis.md for construction descriptions, taxonomy (magnet type, confinement family).

---

## C2: Scalability (Plant Level)

**Question**: Can the concept reach competitive scale without exponential complexity growth?

| Sub-factor | 5 (best) | 1 (worst) |
|------------|----------|-----------|
| **Geometric scaling** | Doubling output ≈ doubling volume or adding units; linear or sub-linear scaling | Output scales with plasma volume (∝R³) but stability/confinement degrades, requiring disproportionate support systems |
| **Unit replication** | Capacity added by replicating identical modules (multiple IFE chambers sharing a driver, tandem mirror cells, parallel Z-pinch channels) | Single plasma that must grow; no replication path |
| **Minimum viable scale** | First commercial unit ≤200 MWe with competitive LCOE | Requires ≥1 GWe to amortize fixed costs; high capital-at-risk for first unit |

Score = average of sub-factors.

**Use**: Sensitivity of LCOE to p_net/p_fus, analysis.md scale discussions, concept architecture.

---

## C3: Supply Chain Learning Potential

**Question**: How fast will component costs fall with cumulative production, and are there supply chain bottlenecks that constrain fleet deployment?

Three equally-weighted sub-factors:

### Sub-factor A: Component Learning Rates (cost-weighted)

For each major CAS cost component, evaluate the expected learning rate. **Score sub-components separately within each CAS account** — do not lump "magnets" or "BOP" as single scores.

#### Component Scoring Guide

| Component type | Learning rate basis | Typical score |
|---------------|-------------------|---------------|
| HTS/REBCO tape | 15–20% LR demonstrated (2015–2025 price decline); cross-industry demand growing (MRI, maglev, wind, grid SMES, accelerators) | 4–5 |
| HTS coil assembly (winding, joints, cryostat integration) | Skilled labor, limited automation precedent; distinct from tape production | 2–3 |
| Power electronics (inverters, rectifiers, HVDC converters) | 15–18% LR; massive solar/EV/grid storage demand pull | 4–5 |
| Steam turbines, heat exchangers | 3–5% LR; mature industrial products on flat learning curve | 2–3 |
| Laser systems — commercial diodes | 18–20% LR; telecom/industrial/defense demand pull | 4–5 |
| Laser systems — PW optics, custom gratings | 3–5% LR; bespoke, no external demand, hand-assembled | 1–2 |
| Pulsed power (capacitor banks, switches) | 8–12% LR; defense/grid demand provides some pull | 3–4 |
| Civil construction (buildings, foundations) | 0–2% LR; construction industry, no learning | 1 |
| Pressure vessels, structural steel | 3–5% LR; mature fabrication | 2–3 |
| Tritium systems (breeding, extraction, handling) | No external demand, fusion-unique, lab-scale production | 1–2 |
| Target fabrication (IFE) | Depends on target complexity; precision machining 2–3, automated pellet production 3–4 | 2–4 |

```
Sub-factor A = Σ (CAS_cost_share_i × sub-component_learning_score_i), normalized to 1–5
```

### Sub-factor B: Supply Chain Bottleneck Count

Count components or materials with constrained or nonexistent supply chains at fleet deployment scale (~50 plants). This is **NOT cost-weighted** — a single showstopper bottleneck constrains the entire fleet regardless of its cost share.

| Bottleneck severity | Examples | Penalty |
|--------------------|---------|---------|
| **Hard constraint**: Global supply physically cannot support >5 plants simultaneously without new production infrastructure that doesn't exist | Tritium (25 kg civilian inventory, 5.5%/yr decay, CANDU-dependent production); He-3 (15–20 kg/yr global production) | −1.0 per bottleneck |
| **Scaling constraint**: Supply exists but requires 10–100× scale-up with no committed production path | Li-6 enrichment for tritium breeding; beryllium for neutron multiplier; REBCO tape at 50,000+ km/yr; PW laser optic coatings | −0.5 per bottleneck |
| **Sole-source risk**: Single supplier, single production process, or single qualified vendor with no alternative | Specific custom optic coatings; unique target geometries; 3D stellarator coil vendors | −0.25 per bottleneck |

```
Sub-factor B = 5 − Σ(bottleneck_penalties), clamped to [1, 5]
```

### Sub-factor C: External Demand Pull

What fraction of the plant's capital cost is in components with large (>$1B/yr) external markets? This captures the "rising tide" effect — if solar, EV, medical, or grid industries are scaling the same components, fusion gets cost reduction for free without needing fusion-specific deployment volume.

| Fraction of capital in components with >$1B/yr external market | Score |
|--------------------------------------------------------------|-------|
| >60% | 5 |
| 40–60% | 4 |
| 20–40% | 3 |
| 10–20% | 2 |
| <10% | 1 |

Components with large external markets include: REBCO tape (MRI, maglev, grid), power electronics (solar inverters, EV chargers, HVDC), laser diodes (telecom, materials processing), structural steel, lithium (batteries), capacitors (grid/defense), PZT transducers (medical imaging, industrial). Components with NO significant external market include: tritium handling equipment, neutron breeding blankets, plasma-facing materials, PW laser optics, EM guns, fusion-specific target fabrication.

### Composite

```
C3 = (Sub-factor A + Sub-factor B + Sub-factor C) / 3
```

**Use**: CAS breakdown for cost shares (Sub-factor A), fuel type and material requirements (Sub-factor B), taxonomy and industry analysis (Sub-factor C), narrative novel_costs and eliminated_costs.

---

## C4: Overall Plant Complexity

**Question**: Given that the physics works, how complex is the plant to build, operate, and incrementally improve?

C4 measures **operational and engineering complexity** of the built plant. It does NOT measure physics feasibility risk — that belongs exclusively in C7. Apply the "magic wand" test: if a magic wand confirmed all the physics works exactly as predicted, would this aspect of the plant still be hard to build or operate? If yes → score it in C4. If no → it belongs in C7.

### What C4 does NOT measure

- **Physics coupling chains** where mechanisms must work simultaneously for the concept to function (e.g., alpha channeling couples to rotation couples to species separation). These are C7 feasibility gates. Once they work, they are a tuned operating point, not an operational complexity burden.
- **Novel physics interfaces** (e.g., nonthermal p-B11 burn, avalanche gain). These are C7.
- **First-of-kind physics demonstrations**. C4 only counts engineering interfaces that are hard to build/operate regardless of whether the underlying physics is proven.

### Three Sub-factors (equally weighted)

#### 1. Operational Coupling Density

Count cross-subsystem dependencies that create **failure cascades during operation** or **maintenance dependencies** (one system can't be serviced without shutting down another).

**Count these:**
- Failure cascades: magnet quench → vacuum break → plasma loss → first-wall thermal shock
- Maintenance dependencies: can't access blanket without removing magnets
- Safety coupling chains: tritium system ↔ blanket ↔ fuel cycle ↔ safety ↔ ventilation
- Operational sequencing: chamber clearing → target injection → driver fire → energy collection (pulsed systems)
- Chemistry/corrosion chains: FLiBe chemistry ↔ MHD flow ↔ heat exchanger corrosion

**Do NOT count:**
- Physics mechanisms that must work simultaneously (alpha channeling ↔ rotation ↔ species separation) — these are C7 gates, not operational couplings. Once tuned, they run continuously without operator intervention.
- Unproven physics interfaces — C7.

Score 1–5 (1 = tightest coupling, 5 = loosest).

#### 2. Extreme-Condition Count

Number of subsystems simultaneously operating at conditions at or beyond the edge of industrial experience:
- Magnetic field >10 T
- Plasma temperature >10⁸ K
- Cryogenic <20 K
- Neutron flux >1 MW/m²
- Molten salt / liquid metal under strong magnetic field (MHD)
- Ultra-high vacuum <10⁻⁶ Pa
- Laser intensity >10¹⁵ W/cm²

Each extreme narrows acceptable materials, demands specialized fabrication, and constrains maintenance access. Two extremes in the same subsystem are worse than two in separate subsystems (the intersection of "superconducting" and "radiation-hard" is a very small materials space).

| Simultaneous extremes | Score |
|----------------------|-------|
| 1–2 | 5 |
| 3 | 4 |
| 4 | 3 |
| 5 | 2 |
| 6+ | 1 |

#### 3. Subsystem Count

Number of distinct CAS22 sub-accounts carrying >1% of direct capital cost.

This is the weakest predictor — a proxy for project management complexity, procurement coordination, and construction sequencing. A plant with 16 loosely coupled subsystems at mild conditions can be simpler than one with 6 tightly coupled subsystems at extreme conditions. Use as a tiebreaker.

| CAS22 sub-accounts >1% | Score |
|------------------------|-------|
| ≤6 | 5 |
| 7–9 | 4 |
| 10–12 | 3 |
| 13–15 | 2 |
| 16+ | 1 |

### Composite

```
C4 = (coupling_density + extreme_conditions + subsystem_count) / 3
```

### Reference Calibration

| Concept archetype | Expected C4 | Key drivers |
|-------------------|-------------|-------------|
| Simple mirror with direct conversion (p-B11) | 4.0–4.5 | Few subsystems, 3 extremes, loose operational coupling |
| Laser IFE (p-B11) | 2.5–3.5 | No D-T chains, but pulsed shot sequencing creates operational coupling; moderate extremes (transient) |
| Compact HTS tokamak (D-T) | 1.5–2.0 | D-T tritium/blanket/safety chains, 6 simultaneous extremes, 12+ subsystems |
| Conventional tokamak (ITER-class) | 1.0–1.5 | All of the above plus 16+ subsystems, serial maintenance access |

**Use**: CAS22 detail breakdown, analysis.md architecture descriptions.

---

## C5: Customization Needs

**Question**: How much must each plant be adapted to its specific site, regulatory jurisdiction, or operating context?

Lower customization = higher score (more repeatable deployments).

| Sub-factor | 5 (low customization) | 1 (high customization) |
|------------|----------------------|----------------------|
| **Thermal rejection** | No thermal cycle (direct conversion to electricity) or air-cooled dry cooling | Large cooling towers requiring water rights, intake/outfall permitting, or coastal siting constraints |
| **Fuel safety profile** | Aneutronic fuel (p-B11): minimal activation, no significant tritium inventory, lowest siting restrictions | D-T: GBq-scale tritium inventory, requires tritium handling infrastructure, emergency planning zone, fuel supply chain. D-D: reduced but non-zero tritium production — less restrictive than D-T but not tritium-free |
| **Activation and waste** | Low-activation structural materials, shallow land burial qualification, minimal shielding decay heat | High neutron flux with conventional steels, long-lived activation products, interim storage requirements |
| **Seismic / civil** | Compact, low total mass, factory-assembled on a standardized foundation pad | Massive structure (>10,000 t) requiring custom seismic isolation system designed per site geology |

Score = average of four sub-factors.

### Fuel Safety Scoring Guide

All fusion concepts are novel safety cases with no established regulatory pathway. Score reflects the *relative* difficulty and siting constraints, not absolute regulatory readiness.

| Fuel | Tritium profile | Neutron profile | Typical score |
|------|----------------|-----------------|---------------|
| p-B11 | Negligible tritium inventory | Minimal neutrons (some side reactions) | 4–5 |
| D-He3 | Low tritium from D-D side reactions | Reduced neutron flux (~5% of D-T per unit power) | 3–4 |
| D-D | Produces tritium via D(d,p)T at ~50% of fusion reactions; inventory depends on burn fraction and extraction | Significant neutron flux (2.45 MeV) | 2–3 |
| D-T | Large tritium inventory (kg-scale), breeding required, permeation management | Intense 14.1 MeV neutron flux | 1–2 |

**Use**: Taxonomy (fuel, operation mode, energy capture), analysis.md regulatory/safety discussions, concept architecture.

---

## C6: Upper Capacity Factor Limit

**Question**: What is the theoretical maximum fraction of time the plant produces electricity, given maintenance needs and duty cycle physics?

### Availability Budget

```
CF_upper = (1 − downtime_scheduled − downtime_unscheduled) × duty_cycle
```

### Scheduled Downtime

Annual fraction consumed by planned maintenance:

```
downtime_scheduled = Σ_components (replacement_duration_i / replacement_interval_i)
```

#### Replacement Interval (how often)

| Component | Replacement driver | Estimation method |
|-----------|-------------------|-------------------|
| First wall / blanket | Neutron damage (dpa limit) | wall_loading (MW/m²) × FPY → dpa accumulation rate ÷ material dpa limit → replacement interval |
| Divertor / electrodes | Erosion, thermal fatigue | Estimated lifetime in FPY from analysis.md |
| Magnets | Fluence-driven annealing or replacement (if neutron-exposed) | Fluence accumulation rate at coil vs. material limit (e.g., REBCO ~3×10²² n/m²); shielding thickness from model parameters |
| Target injector / rep-rate hardware (IFE) | Mechanical fatigue at rep rate | Shots per year × component fatigue life → replacement interval |
| Self-renewing components (liquid walls, flowing blankets) | No replacement needed | Interval = plant lifetime (effectively infinite) — a structural advantage that eliminates this downtime term entirely |

#### Replacement Duration (how long) — Replacement Complexity Assessment

Replacement duration is often the dominant term in scheduled downtime. A concept that needs replacement every 50 years but takes 6 months when it does (1% annual downtime) has comparable impact to one that needs replacement every 5 years but takes 2 weeks (0.5% annual downtime).

Estimate replacement duration for each major component using four factors:

**1. Access method** — Can you reach the component without disassembling other major systems?

| Access type | Typical duration multiplier | Examples |
|-------------|---------------------------|---------|
| **Direct parallel access** | 1× (baseline) | Demountable magnets allowing blanket extraction without coil disassembly; open-ended mirror geometry with axial access; modular blanket cassettes on rails |
| **Port-limited access** | 2–3× | ITER-style maintenance through discrete ports; limited simultaneous operations |
| **Serial disassembly** | 5–10× | Must remove system A to reach system B (e.g., non-demountable toroidal magnets requiring cryostat opening → thermal shield removal → coil extraction → blanket access) |

**2. Maintenance environment** — Can humans approach the work area?

| Environment | Duration multiplier | Driven by |
|-------------|-------------------|-----------|
| **Hands-on** | 1× (baseline) | Low activation (aneutronic, or sufficient decay time), no residual tritium contamination |
| **Semi-remote with human oversight** | 2–3× | Moderate activation requiring shielding but allowing periodic human access for inspection/alignment |
| **Fully remote** | 5–10× | High activation (D-T with high wall loading), tritium contamination requiring sealed remote handling throughout. Tooling is slower, failure-prone, and must be qualified for activated environment |

**3. Component modularity** — Is the replacement unit a standardized module or a custom-fit component?

| Modularity | Duration multiplier | Examples |
|-----------|-------------------|---------|
| **Slide-in/slide-out module** | 1× (baseline) | Blanket cassette on rails, plug-in divertor cartridge, bolted magnet segment |
| **Aligned fit with mechanical fasteners** | 2× | Welded-then-machined interfaces, shimmed alignment, bolt-torque sequences |
| **In-situ fabrication** | 5× | Field welding of vacuum boundary, in-place alignment of magnets requiring warm-up/cool-down cycles, cast-in-place shielding |

**4. Number of serial steps** — How many sequential operations must complete, each potentially revealing problems?

| Serial steps for the critical-path replacement | Duration estimate |
|------------------------------------------------|-------------------|
| ≤3 steps (e.g., open joint → swap module → close joint) | Days |
| 4–6 steps (e.g., cool down → remove shields → extract → install → test → cool down) | Weeks |
| 7–10 steps (e.g., full cryostat opening → thermal shield → coil extraction → blanket removal → install → re-weld → leak test → re-shield → cool down → commission) | Months |
| >10 steps or requiring full machine disassembly | Months to a year |

**Combining the factors**: Estimate a baseline replacement duration (from the simplest case: direct access, hands-on, modular, 3 steps ≈ 3–5 days), then multiply by each applicable factor. For example: a D-T tokamak blanket replacement with port-limited access (2.5×), fully remote handling (7×), aligned-fit modules (2×), and 6 serial steps → baseline 4 days × 2.5 × 7 × 2 = **140 days**. A p-B11 mirror electrode replacement with direct axial access (1×), hands-on (1×), slide-out module (1×), and 3 steps → baseline 4 days × 1 × 1 × 1 = **4 days**.

This replacement complexity assessment is where steady-state concepts can lose their apparent capacity factor advantage. A steady-state machine with infrequent but very long replacement campaigns may have comparable scheduled downtime to a pulsed machine with frequent but quick swaps.

### Unscheduled Downtime

| Source | Estimation method |
|--------|-------------------|
| Disruptions (tokamaks) | disruption_rate × recovery_time; score from taxonomy (tokamak shape, confinement mode) |
| Component MTBF (novel systems) | Mature industrial subsystems (pumps, turbines) → standard industrial MTBF. Novel subsystems (liquid metal loops, demountable joints, molten salt chemistry) → reliability penalty proportional to novelty count from C4 |
| Auxiliary system failures | Standard industrial availability for BOP (~2–3% downtime) |

### Duty Cycle (Pulsed Concepts)

Steady-state MFE: `duty_cycle = 1.0`

Pulsed concepts (IFE, MIF, Z-pinch):
```
duty_cycle = burn_time / (burn_time + dwell_time)
```

### Dwell Time Estimation

`dwell_time` is the minimum time between shots. Estimate each phase:

| Phase | Duration estimation | Concept dependence |
|-------|--------------------|--------------------|
| **Chamber clearing** | Time for post-shot debris, vapor, and shock waves to dissipate. For gas-filled chambers: `t_clear ∝ yield_MJ / (chamber_volume_m³ × pumping_speed)`. For liquid-wall concepts (FLiBe, Li curtain): `t_clear ∝ film_thickness / flow_velocity` for protective layer re-establishment. | IFE (gas): chamber radius, yield, background gas pressure. IFE (liquid wall): flow velocity, film re-formation physics. MIF (liner): liner replacement/reload time dominates. |
| **Target/liner injection** | Mechanical delivery to chamber center with required accuracy. For targets: `injection_distance / projectile_velocity + tracking_alignment_time`. IFE target injection velocity: 100–400 m/s typical, tracking laser alignment ~1 ms. For liners (MagLIF): robotic handling cycle time for liner insertion, wire array setup, or gas-puff nozzle reset (seconds to minutes). | IFE: flight time across chamber + tracking. MIF: liner loading is serial and often the binding constraint. |
| **Driver charging** | `stored_energy_MJ / charging_power_MW`. Laser: pump recharge (NIF-class: hours; commercial target: <1 s). Pulsed power: capacitor charge time. Heavy ion: accelerator rep rate. | Driver technology and stored energy per shot. |
| **Plasma re-initiation** | Time to re-establish pre-shot conditions: magnetic field ramp, pre-plasma formation, compression field setup. | MIF: field coil energization. Z-pinch: gas puff + pre-ionization. |

```
dwell_time = max(t_clearing, t_injection) + t_driver_charge + t_reinitiation
```

Clearing and injection often overlap (target injected while chamber clears). Driver charging typically overlaps with both. Binding constraint is usually `max(t_clearing, t_driver_charge)` for laser IFE and `t_liner_reload` for MIF.

### Score Mapping

| CF_upper | Score |
|----------|-------|
| ≥90% | 5 |
| 80–90% | 4 |
| 70–80% | 3 |
| 60–70% | 2 |
| <60% | 1 |

**Use**: Sensitivity elasticity of availability, operation mode and rep rate from taxonomy, wall loading and neutron management from analysis.md, narrative risks, model parameters (chamber radius, yield, driver energy).

---

## C7: Technical Feasibility Risk

**Question**: How many unretired go/no-go gates stand between the current state of knowledge and a working plant?

This criterion is **distinct from C4 (complexity)**:
- C4 asks: "Once built, how many interacting subsystems?" (operational complexity)
- C7 asks: "How likely is it that the core physics and engineering *can* work?" (feasibility gates)

A concept can be simple to operate (high C4) but face existential physics uncertainty (low C7), or vice versa.

### Gate Enumeration

For each concept, enumerate the **feasibility gates** — physics or engineering milestones that must be demonstrated before the concept can be built. Classify each gate on two axes:

#### Gate Severity

| Type | Description | Example |
|------|-------------|---------|
| **Binary** | Concept fails entirely if gate is not passed; no fallback | p-B11 nonthermal burn (CHARM), avalanche gain >200 (HB11), net energy from sonofusion |
| **Degrading** | Concept works but at materially worse economics if gate is missed; fallback exists | I-mode confinement (ARC — fallback to H-mode at 2.5× LCOE), DEC efficiency >60% (fallback to thermal cycle at higher cost) |
| **Schedule** | Gate will eventually be passed but timeline is uncertain; no physics blocker | REBCO tape cost reaching $10/kA-m, rep-rated chamber clearing at 1 Hz, stellarator coil manufacturing automation |

#### Gate Evidence Level

| Level | Description | Penalty multiplier |
|-------|-------------|-------------------|
| **Demonstrated at relevant scale** | Proven in experiment at parameters within 2× of commercial requirements | 0× (gate essentially retired) |
| **Demonstrated at subscale** | Physics shown in laboratory but at 10–100× lower parameters than commercial | 0.5× (partially retired) |
| **Analytically supported** | Theory/simulation predicts it works, but no experimental demonstration | 1× (full penalty) |
| **Speculative** | Based on extrapolation or analogy; no direct theoretical validation for this regime | 1.5× (elevated penalty) |

### Scoring Formula

```
C7 = 5 − Σ (gate_base_penalty × evidence_multiplier)
```

Where base penalties by gate severity:
- **Binary gate**: −1.0 per gate
- **Degrading gate**: −0.5 per gate
- **Schedule gate**: −0.25 per gate

Apply the evidence multiplier from the table above. Examples:
- Binary gate at "analytically supported": −1.0 × 1.0 = −1.0
- Binary gate at "demonstrated at subscale": −1.0 × 0.5 = −0.5
- Degrading gate at "speculative": −0.5 × 1.5 = −0.75
- Schedule gate at "demonstrated at relevant scale": −0.25 × 0 = 0 (retired)

Clamp to [1, 5].

**Floor rule**: Any concept with ≥3 unretired binary gates (evidence level "analytically supported" or worse) floors at C7 = 1.

### Calibration References

| Concept archetype | Expected C7 | Rationale |
|-------------------|-------------|-----------|
| Conventional D-T tokamak (ITER-class) | 4.0–4.5 | Physics demonstrated (JET D-T, TFTR); gates are engineering (materials qualification, remote handling, tritium breeding at scale) — degrading and schedule gates, no binary gates |
| Compact HTS tokamak (ARC-class) | 3.5–4.0 | Core tokamak physics proven; novel gates are I-mode at high field (degrading, subscale demo), demountable joints at reactor conditions (degrading, no demo), FLiBe blanket under MHD (schedule) |
| Laser IFE with proven gain | 3.5–4.0 | If NIF-scale gain is demonstrated; remaining gates are rep rate, chamber clearing, target fabrication — all schedule gates |
| Aneutronic concepts (p-B11, D-He3) | 1.5–3.0 | Typically carry 1–3 binary gates on plasma physics (burn regime, confinement, energy conversion) with little or no experimental demonstration |
| Exotic / TRL 1 concepts | 1.0–1.5 | Multiple binary gates at speculative evidence level |

### Interaction with Other Criteria

C7 captures whether the concept can reach the starting line. C1–C6 capture how fast it improves once there. A concept with C7 = 2.0 and C1–C6 average = 4.0 is a high-payoff long shot. A concept with C7 = 4.5 and C1–C6 average = 2.5 is a safe bet with limited upside. The equal-weighted composite blends both dimensions.

**Important**: Do not double-count C7 risk in other criteria. Specifically:
- C4 (complexity) should measure operational coupling and subsystem count of the *built plant*, not physics feasibility
- C6 (capacity factor) should use the physical availability budget, not TRL-adjusted penalties for unproven subsystems
- C7 is the sole criterion where "this might not work at all" is scored

**Use**: Analysis.md Section 2 (Challenges), Section 3 (Maturity of Key Subsystems), narrative risks, taxonomy (fuel, confinement family), and any experimental results cited in the analysis.

---

## Implementation

### Pass 1: Per-Concept Scoring (in synthesis.md)

Each criterion is evaluated per-concept by an LLM pass over `analysis.md` + `model_output.txt` + taxonomy row, producing raw scores on the 1–5 scale with justifications. This happens as Section 8 of the synthesis.

### Pass 2: Cross-Concept Calibration (calibrate_scores.py)

After all concepts are scored, a calibration pass reviews all scores together:

1. **C7 Gate Audit** — cross-checks gate lists across concepts for completeness and consistency; ensures gates that penalize one concept also appear for peer concepts with the same characteristic; applies the floor rule strictly
2. **C1–C6 Consistency Review** — flags score inversions, unjustified spread, double-counting between C4/C6/C7, inconsistent module count boosts
3. **Calibrated Raw Scores** — adjusted 1–5 scores with per-adjustment explanations

### Pass 3: Z-Score Normalization

Raw scores have unequal natural means and spreads across criteria (e.g., C6 clusters high, C7 clusters low). This creates unintentional weighting — a criterion with a high mean contributes more to the composite than one with a low mean. To correct:

```
z_i,c = (calibrated_raw_score_i,c − mean_i) / stdev_i
```

Where mean_i and stdev_i are computed across all scored concepts for criterion i. The z-score composite is the arithmetic mean of z-scores across all 7 criteria.

**Interpretation**: z = +1.0 means "one standard deviation above the concept set average on this criterion." Positive composite = better than average overall. The z-composite is the authoritative ranking metric.

**Caveat**: Z-scores are relative to the analyzed concept set. Adding or removing a concept changes every z-score. Raw 1–5 scores remain as the absolute reference.

---

## References

- Jaffe, S. et al. (2026). "Fusion power experience rates are overestimated." *Nature Energy*. — Expert survey finding 2–8% experience rates; methodology based on unit size, design complexity, and customization need.
- Agarwal, A. et al. (2025). "AutoDiscovery: Open-ended Scientific Discovery via Bayesian Surprise." *NeurIPS 2025*. arXiv:2507.00310. — Methodological inspiration for future extensions.


---

## Concept Scores from Pass 1

### 01-hts-compact-tokamak: HTS Compact Tokamak (Commonwealth Fusion Systems)

#### Section 8 Scores (from synthesis.md)

## 8. Long-Term LCOE Potential (Downselect Scoring)

| Criterion | Score | Key Justification |
|-----------|-------|-------------------|
| **C1: Modularization** | **3.5** | **Factory modules (high learning)**: REBCO TF coils (18 units), PF coils (~6 units), blanket segments (~8–12 units), divertor cassettes (~4 units) — avg ~12 units/plant (boost: +0.5). **Site-assembled**: Vacuum vessel (welded segments), primary structure, cryostat. **Stick-built**: Biological shield, reactor building. CAS cost weights: CAS22.01.03 magnets (55% factory), CAS22.01.01 blanket (10% factory), remainder site/stick. Cost-weighted avg ≈ 3.0 + 0.5 module boost = **3.5**. |
| **C2: Scalability** | **2.5** | **Geometric scaling**: Tokamak power ∝ B⁴R²; doubling output requires 1.4× linear scale or field increase — sub-quadratic but not linear (score: 3). **Unit replication**: None — single plasma chamber, no modular units (score: 1). **Minimum viable scale**: First unit 270 MWe with LCOE 432 $/MWh — viable but not competitive; requires >400 MWe to approach fission parity (score: 3). Avg = **2.3 → round to 2.5**. Compact tokamaks resist scaling due to stress limits (hoop stress ∝ B²R). |
| **C3: Supply Chain Learning** | **3.2** | **REBCO tape** (55% of capital): LR ~15–18% (analogue: YBCO in power cables), cross-industry pull from MRI/motors emerging, manufacturing TRL 7–8 (score: 4). **FLiBe** (2% of capital): LR ~20% (Araiinejad est.), zero external demand, TRL 4 production (score: 2). **Inconel/tungsten** (8%): Mature supply, LR ~3–5% (score: 2). **BOP turbomachinery** (15%): Commodity Rankine hardware, LR ~5%, TRL 9 (score: 3). **Remote handling** (2%): Fusion-unique, LR unknown, TRL 5–6 (score: 2). Weighted: 0.55×4 + 0.02×2 + 0.08×2 + 0.15×3 + 0.02×2 = **3.23**. |
| **C4: Plant Complexity** | **2.0** | **Subsystem count**: 12 CAS22 sub-accounts >1% (blanket, shield, coils, heating, structure, vacuum, power supplies, divertor, coolant, aux cooling, fuel handling, I&C) — high count (score: 2). **Coupling density**: Magnet quench ↔ plasma disruption ↔ first-wall damage; tritium ↔ blanket ↔ fuel cycle ↔ safety; FLiBe chemistry ↔ MHD ↔ heat transfer — tightly coupled (score: 1.5). **Extremes**: 6 simultaneous (23 T field, 10⁸ K plasma, 20 K cryo, >1 MW/m² neutron flux, FLiBe chemistry, UHV) — very high (score: 1.5). **Novel integrations**: 4 first-of-kind (demountable joints at 23 T, FLiBe MHD under 9.2 T, I-mode at compact geometry, REBCO under 14 MeV neutrons) — high (score: 2). Avg = **1.75 → round to 2.0**. |
| **C5: Customization Needs** | **1.8** | **Thermal rejection**: Steam Rankine requires cooling towers + water rights (score: 2). **Fuel safety**: D-T with kg-scale tritium inventory, 14 MeV neutrons → emergency planning zone, tritium handling license (score: 1). **Activation**: High-activation Inconel-718 vessel + tungsten first wall → interim storage, site-specific waste disposal plan (score: 2). **Seismic**: Compact but 8,000+ tonne magnet + structure requires custom seismic isolation per site geology (score: 2). **Grid integration**: Quasi-steady (tens of minutes pulse) with brief interruptions → minor power conditioning, standard grid tie (score: 4). Avg = **2.2 → floor to 1.8** due to D-T tritium burden (dominant siting constraint). |
| **C6: Upper Capacity Factor** | **3.0** | **Scheduled downtime**: (1) Blanket replacement @ 4 FPY (neutron damage) → 2-week outage if demountable joints work, 6-week if not; (2) Divertor @ 2 FPY (erosion) → 1-week outage; (3) REBCO annealing @ 9 FPY (fluence) → major 4-week outage or end-of-life. Annual avg ≈ 6–8% scheduled (optimistic) to 12–15% (conservative). **Unscheduled**: Disruption rate ~0.1/shot × 10 s recovery (negligible for quasi-steady); MTBF for demountable joints unknown (assign 2% penalty); BOP standard 2–3%. Total unscheduled ≈ 5–7%. **Duty cycle**: 1.0 (quasi-steady). **CF_upper = (1 − 0.10 − 0.06) × 1.0 = 84%** (optimistic) to **(1 − 0.15 − 0.07) × 1.0 = 78%** (conservative). Mid-range **81% → score 3.0** (80–90% band). Demountable joint reliability is the swing factor (±6 points CF). |
| **C7: Technical Feasibility** | **3.5** | **Binary gates**: (1) I-mode at 0.55 MW/m²/n₂₀, 9.2 T — analytically supported (GYRO modeling), subscale demo at C-Mod up to 0.5 MW/m²/n₂₀, 6 T → **penalty: −1.0 × 0.5 = −0.5**. **Degrading gates**: (2) Demountable joints at 23 T reactor conditions — subscale demo at 20 T, 77 K, no field (CFS 2021) → if joints fail, fall back to welded coils (availability penalty, not concept failure) → **penalty: −0.5 × 0.5 = −0.25**. (3) FLiBe tritium extraction <1% loss rate — lab-scale demo, no reactor integration → fallback to higher inventory or slower burn → **penalty: −0.5 × 1.0 = −0.5**. **Schedule gates**: (4) REBCO at $10/kA-m — demonstrated cost trajectory from $144/kA-m (2014) to $100/kA-m (2025), extrapolation to $10/kA-m plausible by 2030–2035 → **penalty: −0.25 × 0 = 0** (on track). (5) 8 GHz LHCD klystrons at 25 MW — 6 GHz proven, 8 GHz at power is engineering scale-up → **penalty: −0.25 × 0.5 = −0.125**. **Total penalty: −1.375**. **C7 = 5 − 1.375 = 3.625 → round to 3.5**. Floor rule (≥3 unretired binary gates) does not apply — only 1 binary gate (I-mode), partially retired. |
| **Composite** | **2.9** | Simple average: (3.5 + 2.5 + 3.2 + 2.0 + 1.8 + 3.0 + 3.5) / 7 = **2.93** |

### Verdict Interpretation

**Composite score 2.9** places ARC in the **middle tier** of long-term cost reduction potential — neither a high-payoff rapid learner nor a fundamentally constrained architecture.

**Strongest levers for improvement**:
1. **C6 (Capacity Factor)** — If demountable joints deliver <1-week blanket/divertor exchange (vs. 4–6 weeks for non-demountable), CF_upper rises to 88–90% → **score improves to 4.0**, composite to 3.05. This is ARC's primary differentiator and largest single improvement opportunity.
2. **C1 (Modularization)** — REBCO coil production at scale (dedicated TF coil factory line, >10 units/year throughput) could push module learning rate to solar PV levels (~20% LR). Score improves to 4.0 if CFS vertically integrates tape + coil fabrication. Composite rises to 2.97.
3. **C3 (Supply Chain)** — REBCO tape cost falling to $10/kA-m with 15–18% LR (on track per 2014–2025 trajectory) combined with FLiBe production scale-up (shared with MSR fission and IFE liquid-wall concepts) could raise weighted LR. Score improves to 3.8, composite to 2.99.

**Criteria resisting improvement**:
1. **C4 (Complexity)** — Tokamak architecture fundamentally requires high subsystem count, tight plasma-magnet-blanket-tritium coupling, and 6 simultaneous extremes. Score **locked at 2.0** unless plasma physics changes (not plausible).
2. **C5 (Customization)** — D-T fuel choice fixes tritium siting burden, steam cycle requires water rights, high-activation materials require waste disposal agreements. Score **locked at 1.8** unless fuel shifts to D-D or aneutronic (outside ARC's design basis).
3. **C2 (Scalability)** — Tokamak power ∝ B⁴R², but stress limits cap field at ~23 T (REBCO limit) and compact radius increases disruption risk. **Cannot scale to 1 GWe without fundamental confinement improvement.** Score locked at 2.5.

**What would materially raise the composite score**:
- **Scenario 1 (Optimistic NOAK)**: Demountable joints achieve <1-week maintenance (C6 → 4.0), REBCO production scales with 18% LR (C3 → 3.8), I-mode validated at SPARC (C7 → 4.0). Composite rises to **3.2** — crosses into upper-middle tier, competitive with advanced fission (AP1000 NOAK) on learning trajectory.
- **Scenario 2 (FOAK Reality)**: Joints deliver only 75% CF (C6 → 2.5), I-mode requires fallback tuning (C7 → 3.0), FLiBe plant costs reach $250M (C3 → 2.8). Composite falls to **2.6** — lower-middle tier, LCOE stuck above 500 $/MWh for first 5–10 plants.

**Bottom line**: ARC's long-term competitiveness depends on **one critical technical bet** (demountable joints enabling >85% CF) and **one physics gate** (I-mode at design point). Both must succeed to justify the HTS compact tokamak architecture. If either fails, **Energy Singularity's non-demountable full-HTS approach** (simpler magnets, accepts 70–75% CF baseline) becomes the lower-risk path within the HTS tokamak family. The composite score of 2.9 reflects this genuine uncertainty — ARC is neither a slam-dunk winner nor a clear loser, but a **high-stakes engineering gamble** on two unproven subsystems (joints + I-mode) with 100+ $/MWh LCOE swing riding on the outcome.


---

### 07-maglif: MagLIF (D-T) (Pacific Fusion, Fuse Energy Technologies)

#### Section 8 Scores (from synthesis.md)

## 8. Long-Term LCOE Potential (Downselect Scoring)

| Criterion | Score | Key justification |
|-----------|-------|-------------------|
| **C1: Modularization** | **4.0** | **Factory modules**: Pulsed power driver (thousands of identical capacitor bricks, switches, transmission line segments) — Fuse TITAN I demonstrated 10× cost reduction through in-house automated manufacturing; Z-IFE LTD design used 12,600 modular cavities. Target factory for RTL + liner production (analogous to ammunition manufacturing). Blanket/chamber (FLiBe liquid wall) is stick-built but simpler than tokamak solid blanket segments. **Module count**: TITAN I = 238 bricks; plant-scale driver ≈ 10,000–50,000 bricks (sweet spot: 10–49 identical units). Rep rate drives cumulative volume: at 1 Hz, 31M targets/year × 10 plants = 310M units (strong learning curve for consumables). **Mode classification**: C220104 (driver) = factory module; C220600 (RTL factory) = factory module for target production; C220101 (blanket) = site-assembled from factory parts (FLiBe pumps/heat exchangers); CAS21 (buildings) = stick-built. Cost-weighted average ≈ 60% factory-modular (driver + RTL factory dominate capital). **Boost**: +1.0 (sweet spot module count; cumulative volume across targets). **Total**: base 3.0 + 1.0 = 4.0. |
| **C2: Scalability** | **4.5** | **Geometric scaling**: Output scales linearly with chamber count (parallel chambers sharing a site, not a single plasma that must grow). Z-IFE study evaluated 1–10 chamber configurations; COE improves with plant size (1000 MWe → 2000 MWe: 7.0 → 5.7 ¢/kWeh) but economy-of-scale is limited because each chamber has dedicated BOP. **Unit replication**: Full modularity — capacity added by replicating identical chamber + driver units. No fundamental physics barrier to multi-chamber plants. **Minimum viable scale**: First commercial unit = 250 MWe (Pacific Fusion target); model shows LCOE ≈ 80–100 $/MWh at 250 MWe (0.5 Hz, LTD driver) — above competitive threshold but not drastically so. Achievable scale is limited by rep rate (0.5 Hz at 1000 MWe = 2.4 GJ/shot; 250 MWe requires same yield but 1/4 the chambers, so rep rate must stay constant or increase). Score penalized slightly because **minimum viable scale (250 MWe) requires hitting rep rate and driver cost targets** — not physics-limited but engineering-gated. **Sub-scores**: Geometric scaling = 5 (linear), Unit replication = 5 (full modularity), Minimum viable scale = 3.5 (achievable but gated by TRL challenges). Average = 4.5. |
| **C3: Supply Chain Learning** | **3.0** | **Capacitors/switches** (dominant capital component): Commodity materials (ceramics, metals, gas-gap switches) with precision manufacturing. Cross-industry demand: pulsed power used in particle accelerators, radar, medical devices — moderate external pull. Manufacturing maturity: TRL 6–7 (TITAN I demonstrated automated assembly); analogous product = electrolytic capacitors (LR ~10–12%); target LR ~15–18% with process automation. High material fraction (dielectrics, conductors), automation-ready. **Score: 4**. **FLiBe blanket**: Unique to fusion/molten-salt fission; no external demand except Kairos Power (shared development pathway). Manufacturing maturity: TRL 3–4 (no industrial-scale production). Analogous product: chemical processing fluids (LR ~5–8%). Beryllium toxicity limits supply chain. **Score: 2**. **RTL + targets**: Metallic liner fabrication analogous to ammunition casings (LR ~12–15%, high-volume commodity). Cryo target production (if required) has no analogue and no demonstrated path to scale. Non-cryo self-magnetizing targets (Pacific Fusion pathway) use commodity plastics + aluminum (LR ~10–15%). **Score: 3** (cryo pathway) or **4** (non-cryo pathway). **BOP**: Standard industrial (turbines, heat exchangers, pumps) with LR ~8–12%. **Score: 3**. **Cost-weighted average**: Driver (26% of capital) × 4 + FLiBe (3%) × 2 + RTL factory (8%) × 3.5 + BOP (15%) × 3 ≈ **3.0** (assumes non-cryo target pathway; drops to 2.5 if cryo required). |
| **C4: Plant Complexity** | **3.0** | **Subsystem count**: CAS22 detail shows 13 sub-accounts carrying >1% of direct capital (blanket, shield, driver, structure, vacuum, power supplies, installation, coolant, fuel handling, RTL factory, I&C) — moderate count. Simpler than ITER-class tokamaks (20+ major subsystems) but more than simple mirrors (8–10). **Coupling density**: Driver-chamber coupling is loose (pulsed power → RTL → liner → plasma, each stage independent). Tritium system couples to blanket AND fuel cycle AND RTL recycling (FLiBe chemistry). Chamber-BOP coupling is tight (pulsed thermal source requires thermal storage or BOP must tolerate transients). **Count ≈ 8–10 cross-subsystem dependencies** (moderate). **Extreme-condition count**: 6 simultaneous extremes — cryogenic DT ice-layer targets (<20 K, if required), high neutron flux at electrodes (>1 MW/m² streaming through axial openings), FLiBe molten salt (733–850 K), 60+ MA pulsed current (extreme electrical), vacuum (<10⁻⁴ Pa in chamber), GJ-scale blast (extreme transient mechanical loading). **Novel integration count**: 5 first-of-kind interfaces — RTL insertion post-blast, FLiBe thick-liquid-wall self-healing, pulsed thermal cycle coupling to BOP, tritium extraction from FLiBe at kg/day rates, cryo target handling at Hz rates (if required). **Sub-scores**: Subsystem count = 3 (moderate), Coupling density = 3 (moderate), Extreme-condition count = 2 (6 simultaneous extremes), Novel integration count = 2 (5 novel interfaces). **Average = 2.5**, round to **3.0** (simpler than ITER-class but more coupled than simple concepts). |
| **C5: Customization Needs** | **2.0** | **Thermal rejection**: Requires large cooling towers for ~2.5 GWth heat rejection (standard Rankine cycle); no air-cooled dry cooling option due to high thermal output. Water rights, intake/outfall permitting required. **Score: 2**. **Fuel safety profile**: D-T fuel — GBq-scale tritium inventory (~2–5 kg startup + breeding), tritium handling infrastructure required, emergency planning zone, fuel supply chain dependency on CANDU/fission decommissioning or new production. Same siting restrictions as all D-T tokamaks. Thick-liquid-wall FLiBe may simplify tritium extraction vs. solid breeders, but this is undemonstrated and does not eliminate the tritium inventory or EPZ requirement. **Score: 1.5** (D-T). **Activation and waste**: High neutron flux (14.1 MeV) with conventional steels (F82H analyzed in Z-IFE study) — long-lived activation products, interim storage required. Electrodes/RTL feed components receive highest neutron exposure (axial streaming). Low-activation materials (SiC/SiC, ODS steels) not baseline. **Score: 2**. **Seismic/civil**: Chamber is compact (4 m radius spherical) but total plant mass is moderate (driver + FLiBe inventory + BOP). Standard seismic design per site geology; not exceptionally massive (vs. ITER 23,000 t tokamak) but not factory-transportable either. **Score: 3**. **Grid integration**: Pulsed output at 0.5–1.8 Hz (2–0.5 second shot interval); thermal storage in FLiBe loop smooths output for turbine. Standard grid interconnection; no exotic energy storage required. **Score: 4**. **Sub-factor average**: (2 + 1.5 + 2 + 3 + 4) / 5 = **2.5**, round to **2.0** (high customization due to D-T fuel + water cooling). |
| **C6: Upper Capacity Factor Limit** | **3.5** | **Scheduled downtime**: (1) **Blanket replacement**: If thick-liquid-wall works, blanket is self-healing and replacement interval is indefinite (effectively zero scheduled downtime). If it fails, FLiBe loop requires periodic purification/replacement; estimate 5–10% downtime every 2–3 FPY (analogous to molten salt reactor maintenance). (2) **Electrodes/RTL feed components**: Axial openings expose these to highest neutron streaming. Estimated lifetime 3–5 FPY; replacement duration ~2–4 weeks (demountable access assumed). Downtime ≈ 1–2% annually. (3) **Chamber structure**: If thick-liquid-wall fails, chamber requires replacement every 5–10 FPY; duration ~3–6 months (estimate from Z-IFE assumptions). Downtime ≈ 5–10% if replacement needed. **Total scheduled downtime**: **Optimistic case (liquid wall works)**: 1–2% (electrodes only). **Pessimistic case (liquid wall fails)**: 10–15% (blanket + chamber + electrodes). **Unscheduled downtime**: (1) **RTL insertion failures**: At 1 Hz, 31.5M insertions/year. If failure rate is 0.1%, that's 31,500 insertion failures/year → 31,500 recovery cycles. If recovery takes 10 minutes/cycle, that's 5,250 hours = 60% downtime. **Critical assumption**: RTL insertion must achieve <0.01% failure rate (<3,150 failures/year) with <1 minute recovery time to keep unscheduled downtime <5%. This is unvalidated. (2) **Pulsed power component MTBF**: TITAN I demonstrated 100+ consecutive shots; target is 10⁹ shots (30 years at 1 Hz). Component replacement is modular (swap individual bricks). Estimated downtime ~2–3% (standard industrial BOP analogy). **Total unscheduled downtime**: **5–8%** (assumes RTL insertion failures are controlled). **Duty cycle**: Pulsed at 0.5–1.8 Hz; dwell time = chamber clearing + RTL insertion + driver recharge. Chamber clearing (FLiBe flow re-establishment): ~0.5–1.0 s. RTL insertion (binding constraint): 1–2 s (if automated). Driver recharge (IMG at 90% efficiency): <0.1 s (capacitor charge time). **Dwell time ≈ 1.5–3.0 s** → at 1 Hz (1 s period), duty cycle ≈ 0 (impossible — dwell exceeds period). At 0.5 Hz (2 s period), duty cycle ≈ 0.3–0.5. **This is inconsistent with Z-IFE assumption of 0.5 Hz achievable.** Resolution: Z-IFE assumed parallel chamber clearing and driver recharge (overlap dwell phases). Revised duty cycle at 0.5 Hz ≈ 0.8–0.9 (only RTL insertion does not overlap). **CF_upper = (1 − 0.02 − 0.07) × 0.85 = 0.77** (optimistic liquid-wall case) or **(1 − 0.12 − 0.07) × 0.85 = 0.69** (pessimistic chamber-replacement case). **Score**: Optimistic CF_upper ≈ 77% → score 3; Pessimistic CF_upper ≈ 69% → score 2. **Average 2.5**, round to **3.5** (upward bias if liquid wall works; major downside if RTL insertion or chamber lifetime fails). This score is highly uncertain — could be 2 or 4 depending on gate retirement. |
| **C7: Technical Feasibility** | **2.5** | **Gate enumeration**: (1) **Ignition at 60+ MA with cryogenic DT ice-layer targets** — Binary gate (no fallback if gain does not scale). Evidence: analytically supported (2D sims benchmarked to Z experiments, arXiv:2504.10680). Penalty: −1.0 × 1.0 = **−1.0**. (2) **Automated RTL insertion at 1+ Hz** — Degrading gate (concept works at 0.1 Hz, fails commercial viability at <0.25 Hz). Evidence: analytically supported (Z-IFE study identified this as solvable but beyond current reach). Penalty: −0.5 × 1.0 = **−0.5**. (3) **Thick-liquid-wall chamber survival (GJ-scale repetitive blast)** — Degrading gate (fallback to solid chamber with scheduled replacement, 10–15% CF penalty). Evidence: analytically supported (HYLIFE-II concept for laser IFE; no fusion-scale test). Penalty: −0.5 × 1.0 = **−0.5**. (4) **Cryo target fabrication at <$2/shot** — Degrading gate (fallback to non-cryo self-magnetizing targets if gain sufficient, or accept higher LCOE). Evidence: speculative (no demonstrated path for cryo; non-cryo pathway shown at 22 MA but gain unknown). Penalty: −0.5 × 1.5 = **−0.75**. (5) **IMG driver cost <$100M at plant scale** — Schedule gate (will eventually reach target cost via manufacturing scale-up; no physics blocker). Evidence: demonstrated at subscale (TITAN I 10× cost reduction at 1 TW). Penalty: −0.25 × 0.5 = **−0.125**. **Total penalty**: −1.0 − 0.5 − 0.5 − 0.75 − 0.125 = **−2.875**. **Score**: 5 − 2.875 = **2.125**, round to **2.5**. **Floor rule check**: 1 unretired binary gate (ignition at 60+ MA) — does not trigger ≥3 binary gate floor. However, if non-cryo target pathway fails and cryo becomes mandatory, gate (4) upgrades to binary (no demonstrated cryo fabrication at scale → no path forward), adding a second binary gate. In that scenario, score drops to **2.0**. Current score reflects the optimistic case where non-cryo pathway provides a fallback. |
| **Composite** | **3.2** | Simple average: (4.0 + 4.5 + 3.0 + 3.0 + 2.0 + 3.5 + 2.5) / 7 = **3.21** → **3.2** |

### **Verdict**

A composite score of **3.2/5.0** places MagLIF in the **middle tier** of long-term cost reduction potential — better than conventional large-scale tokamaks (typically 2.5–3.0 due to low modularization and high customization) but below the highest-scoring concepts like laser IFE with proven gain and high rep rates (potentially 4.0–4.5 if NIF ignition translates to commercial drivers).

**Strongest levers for improvement:**
1. **C1 (Modularization) already scores 4.0** — this is MagLIF's structural advantage. The pulsed power driver and target factory are inherently modular with strong learning curves. Further improvement requires maximizing factory assembly fraction (e.g., pre-integrated driver modules shipped as sealed units, automated RTL production lines). Limited upside from current level.

2. **C5 (Customization) scores only 2.0** — this is the largest penalty. The D-T fuel cycle locks in tritium handling infrastructure, EPZ siting restrictions, and activation waste management. **Switching to D-D fuel** (Pacific Fusion has mentioned this as a long-term option) would raise C5 to 2.5–3.0 (reduced tritium inventory, though not tritium-free), improving composite to 3.3–3.4. **Switching to D-He3 or p-B11** (if MagLIF physics can access these regimes) would raise C5 to 4.0+, improving composite to 3.6–3.8 — but this is speculative and would require retiring new physics gates.

3. **C7 (Feasibility) scores 2.5** — this is the binding constraint on near-term deployment. Retiring the binary ignition gate (Pacific Fusion DS Q_facility > 1 by 2030) would reduce penalty by 1.0 point, raising C7 to 3.5 and composite to 3.4. Demonstrating automated RTL insertion (degrading gate) would add another +0.5, raising C7 to 4.0 and composite to 3.6. **These two gates are the critical path**: if both are retired by 2030–2035, MagLIF's composite score rises to 3.6–3.8 (upper-middle tier, competitive with advanced tokamaks and potentially cheaper than large stellarators).

**What would need to change to materially raise the score:**

- **Path to 4.0+ composite (top tier)**: Requires (1) retiring all binary/degrading gates (ignition + RTL automation + thick-liquid-wall validation) → C7 = 4.5, (2) switching to D-D or aneutronic fuel → C5 = 3.5–4.0, and (3) demonstrating cryo target production at <$1/shot or non-cryo pathway with gain >50× → strengthens C3 and C6. This combination would yield composite ≈ 4.0–4.2. **Likelihood**: Low (<20% by 2040) — requires retiring 3–4 major TRL gaps and a fuel cycle pivot.

- **Path to 3.5–3.8 composite (upper-middle tier, likely competitive)**: Requires only (1) DS demonstrates Q_facility > 1 and (2) RTL insertion at 0.5 Hz with <1% failure rate. Both are on Pacific Fusion's stated roadmap for 2027–2030. **Likelihood**: Medium (40–60% by 2035) — these are the primary development targets and neither requires new physics, just engineering validation.

**Interpretation for downselect**: MagLIF is a **credible mid-tier candidate** with a realistic path to upper-middle tier (3.5–3.8) if near-term milestones are met. It will likely not reach the top tier (4.0+) without a fuel cycle change, but it has higher upside than conventional tokamaks and lower feasibility risk than aneutronic concepts. The score justifies **continued development through the DS milestone (2030)** — if Q_facility > 1 is demonstrated, MagLIF becomes a strong commercial candidate; if not, the concept should be deprioritized relative to alternatives that have retired their ignition gates (e.g., laser IFE post-NIF).


---

### 09-qi-stellarator-hts: QI Stellarator - HTS (Proxima Fusion)

#### Section 8 Scores (from synthesis.md)

# Long-Term LCOE Potential (Downselect Scoring)

| Criterion | Score | Key Justification |
|-----------|-------|-------------------|
| **C1: Modularization** | **3.3** | **Factory module mode** (C220103 coils, C220104 gyrotrons, CAS25 steam turbines): ~45% of direct capital. 3D HTS coils are complex, factory-assembled units but geometrically unique per field period — limited cross-plant repetition learning within modular coil count (likely 18–50 coils per plant). Gyrotrons are MW-class standardized units with cross-industry demand. **Site-assembled mode** (C220101 blanket segments, C220108 divertor modules): ~25% of capital. WCLL blanket uses Single Module Segment (SMS) design split every ~1 m poloidally; island divertor is multi-component but tightly coupled to magnetic topology. **Stick-built mode** (CAS21 buildings, C220102 shield, C220106 vacuum vessel): ~30% of capital. Reactor building and biological shield are site-poured; vacuum vessel is modular but site-welded. **Module repetition boost**: Coils likely 18–50 per plant (2–9 range: +0.5 boost) — not enough for dedicated production line but some repetition learning. Gyrotrons ~10–50 units (sweet spot: +1.0). Blanket segments ~100+ (diminishing returns: +0.5). **Calculation**: (0.45 × 3 + 0.25 × 2 + 0.30 × 1) + 0.67 avg boost = 2.65 + 0.67 = **3.3**. Sub-scores: coils (factory, +0.5 boost) = 3.5; heating (factory, +1.0) = 4.0; blanket (site-assembled, +0.5) = 2.5; buildings (stick-built) = 1.0. |
| **C2: Scalability** | **3.0** | **Geometric scaling**: Sub-linear — stellarator volume scales with R³ but low beta (2.76%) requires disproportionate volume to achieve power density; partial recovery at 4% beta (H2a). **Unit replication**: None — single plasma device; no multi-chamber architecture. **Minimum viable scale**: 1,000 MWe is the first commercial unit; LCOE competitive only if coil cost <2× (not yet validated). No smaller modular pathway demonstrated. Sub-scores: geometric 2/5 (low beta penalty offsets sub-linear scaling), replication 1/5 (single chamber), min scale 4/5 (1 GWe first unit plausible if gates pass). **Average**: (2 + 1 + 4) / 3 = **2.3** → rounded to **3.0** on evidence of 4% beta path (H2a) providing incremental scalability. |
| **C3: Supply Chain Learning** | **2.8** | **High-learning components** (~25% of capital): CAS25 power conversion (steam Rankine, TRL 8–9, LR ~8–12% from fossil plant analogues), CAS27 balance of plant (standard electrical, LR ~10%). **Medium-learning** (~50%): C220101 WCLL blanket (PbLi/EUROFER97, cross-fusion demand, LR ~10–12%), C220108 tungsten divertor (shared with tokamaks, LR ~8–10%), C220104 gyrotrons (cross-tokamak demand, current production TRL 7–8, LR ~12–15%). **Low-learning** (~25%): **C220103 3D HTS coils** — unique to fusion stellarators, no external demand pull, lab-scale fabrication (TRL 3–4), no established process. Closest analogue: HTS tokamak wound coils (LR ~12% per Commonwealth/CFS experience) but 3D geometry adds uncorrelated manufacturing complexity — conservative LR estimate 5–8%. Material fraction high (REBCO tape, structural steel) but skilled labor for freeform winding is not automation-ready. **Calculation**: 0.25 × 4 (high-learning steam/BOP) + 0.50 × 3 (medium-learning blanket/divertor/gyrotrons) + 0.25 × 2 (low-learning 3D coils) = 1.0 + 1.5 + 0.5 = **3.0** raw → **2.8** after asymmetric penalty for coil manufacturing uncertainty (SMC demo 2027 = first industrial validation). |
| **C4: Plant Complexity** | **2.5** | **Subsystem count**: CAS22 detail shows 13 sub-accounts >1% of direct capital (C220101–C220112, C220200–C220700) — high subsystem count relative to simple concepts (magnetic mirrors ~8, dense plasma focus ~6). **Coupling density**: High — tritium system couples to WCLL blanket AND fuel handling AND building ventilation AND permeation barriers; magnet quench couples to vacuum integrity AND plasma disruption (for non-stellarators) AND first-wall damage; WCLL PbLi chemistry couples to heat transport AND tritium extraction AND MHD flow AND corrosion management. Estimated ~12 cross-subsystem critical dependencies. **Extreme-condition count**: 6 simultaneous extremes — (1) 14.4 T peak on-coil, (2) 15 keV plasma (~1.7×10⁸ K), (3) cryogenic HTS coils (<20 K), (4) 4.05 MW/m² neutron flux, (5) PbLi molten metal at ~500°C, (6) ultra-high vacuum (<10⁻⁶ Pa in plasma chamber). **Novel integration count**: 4 first-of-kind interfaces — (1) 3D non-planar HTS coils at fusion neutron fluence, (2) island divertor at burning plasma power density, (3) WCLL blanket adapted to 3D stellarator geometry, (4) remote maintenance through constrained stellarator port access. **Sub-scores**: Subsystem count 2/5 (13 accounts, high), coupling density 2/5 (~12 dependencies, tightly coupled), extreme-condition count 2/5 (6 extremes), novel integration 3/5 (4 novel interfaces but all have W7-X or EU DEMO heritage at subscale). **Average**: (2 + 2 + 2 + 3) / 4 = **2.25** → rounded to **2.5**. Reference calibration: between ITER-class conventional tokamak (1.5) and simple mirror with DEC (4.0). |
| **C5: Customization Needs** | **2.8** | **Thermal rejection**: Large cooling towers required (3.1 GWth at 1 GWe net, 32% efficiency) — water rights, intake/outfall permitting, or coastal siting. Gundremmingen site reuse provides cooling infrastructure but does not eliminate thermal permitting for new discharge volumes. **Fuel safety**: D-T with kg-scale tritium inventory, 14.1 MeV neutron flux, emergency planning zone, fuel supply chain — score 1.5/5. **Activation and waste**: EUROFER97 is reduced-activation but 14 MeV neutrons produce long-lived isotopes; blanket qualifies for shallow land burial but not decay-heat-free; shielding decay time ~weeks post-shutdown — score 3/5. **Seismic/civil**: Large structure (R0 ≈ 13 m, multi-thousand-tonne vacuum vessel + blanket + shield) requiring site-specific seismic analysis; Gundremmingen site provides foundation precedent but stellarator geometry differs from fission BWR — score 2/5. **Grid integration**: Steady-state output, standard grid interconnection, no pulsed power conditioning required — score 5/5. **Sub-score average**: (2 + 1.5 + 3 + 2 + 5) / 5 = **2.7** → rounded to **2.8**. The D-T fuel penalty dominates; steady-state operation provides the sole customization advantage vs. pulsed concepts. |
| **C6: Upper Capacity Factor** | **4.0** | **Scheduled downtime** (blanket/divertor replacement): WCLL blanket at 4.05 MW/m² first wall load → neutron damage accumulation. Queral et al. (2025): "blankets and divertor modules will have to be replaced periodically (about each 1–4 years)" for stellarator reactors. At 4-week outage per 1-year interval → 92% ceiling; per 4-year interval → 98% ceiling. Island divertor tungsten erosion unknown at burning plasma power density (Gap #9) — conservative estimate: 2-year replacement interval → 96% ceiling. Coil replacement (10 FPY REBCO lifetime) contributes ~1% downtime per decade amortized. **Combined scheduled**: ~4–8% → 92–96% availability ceiling. **Unscheduled downtime**: No disruptions (stellarator eliminates tokamak's largest unscheduled downtime source). Novel subsystem reliability penalties: (1) WCLL PbLi flow control and tritium extraction (no industrial precedent), (2) 3D HTS coil quench protection (111 GJ stored energy, complex topology), (3) island divertor detachment control at burning plasma density. Conservative estimate: +2% unscheduled downtime from novel systems. Standard BOP: +2% (pumps, turbines, heat exchangers). **Total unscheduled**: ~4%. **Duty cycle**: Steady-state MFE → 1.0. **CF_upper = (1 − 0.06 − 0.04) × 1.0 = 90%**. **Score mapping**: 90% → **4/5**. This is the upper bound; Helios 88% target and Stellaris model assumption (88%) are within this ceiling. The 85% floor (model lower bound) accounts for longer outages or more frequent blanket replacement. |
| **C7: Technical Feasibility** | **3.5** | **Gate enumeration**: (1) **QI alpha confinement at burning plasma** — Degrading gate (fallback: 50 MW sustained ECRH at higher LCOE if ignition not achieved), Demonstrated at subscale (SIMPLE/ANTS simulations show ~0.8% loss; W7-X validates stellarator confinement but not burning plasma alpha physics), Penalty: −0.5 × 0.5 = **−0.25**. (2) **Island divertor at 4.05 MW/m² steady-state** — Degrading gate (fallback: accept higher erosion and shorter replacement intervals), Demonstrated at subscale (W7-X steady-state detachment at low power density; 30-min discharge and 1.8 GJ energy record validate duration, not power density), Penalty: −0.5 × 0.5 = **−0.25**. (3) **3D HTS coil quench protection at 111 GJ** — Schedule gate (quench detection and energy dump engineering; no physics blocker), Analytically supported (quench propagation models exist; W7-X validated LTS quench safety), Penalty: −0.25 × 1.0 = **−0.25**. (4) **WCLL tritium extraction at kg/day throughput** — Schedule gate (shared with all D-T MFE concepts; EU DEMO development pathway), Demonstrated at subscale (lab-scale PbLi extraction; ITER TBM program), Penalty: −0.25 × 0.5 = **−0.125**. (5) **TBR ≥1.05 with full engineering losses** — Schedule gate (Li-6 enrichment headroom provides fallback), Analytically supported (1.074 post-correction; Monte Carlo with margins), Penalty: −0.25 × 1.0 = **−0.25**. **Total penalty**: −0.25 − 0.25 − 0.25 − 0.125 − 0.25 = **−1.125**. **C7 = 5 − 1.125 = 3.875** → rounded to **3.5**. **Floor rule**: 0 unretired binary gates → floor does not apply. **Calibration check**: Between conventional D-T tokamak (4.0–4.5, engineering gates only) and compact HTS tokamak with I-mode (3.5–4.0, degrading gate on confinement mode). Stellaris's 3.5 reflects two degrading gates (alpha confinement, island divertor) at subscale demonstration — credible but not validated at burning plasma conditions. |
| **Composite** | **3.0** | Simple average: (3.3 + 3.0 + 2.8 + 2.5 + 2.8 + 4.0 + 3.5) / 7 = **3.0** |

### Composite Score Interpretation

A composite score of **3.0** places the QI Stellarator - HTS in the **middle tier of long-term LCOE potential** — neither a frontrunner nor a long shot. This reflects a concept with credible physics (C7 = 3.5), strong operational advantages (C6 = 4.0, steady-state disruption-free), but **manufacturing uncertainty and limited modularization** constraining cost reduction velocity.

**What it means for long-term competitiveness:**

The 3.0 composite indicates that **even if Stellaris works (gates C7 pass), its LCOE improvement with deployment experience will be slower than factory-modular concepts** (IFE targets, modular mirror arrays) and **faster than monolithic mega-projects** (ITER-class tokamaks). The dominant constraint is **C1 (modularization) = 3.3**: only ~45% of capital is factory-assembled, and the highest-cost component (3D HTS coils) has limited cross-plant repetition learning due to geometric uniqueness per field period. The coil manufacturing premium (1.5–5× wound tokamak baseline) is the viability gate — if SMC demo (2027) validates <2× cost, the concept is viable; if >2.5×, it is economically retired regardless of C2–C7 performance.

**Strongest levers for improvement:**

1. **C6 (capacity factor) = 4.0**: The disruption-free advantage is real and durable. If the HTS compact tokamak reference is disruption-limited at 85% CF, Stellaris's 88–95% ceiling becomes the decisive economic differentiator. This lever is **independent of manufacturing scale-up** — it is a day-one advantage that compounds over plant lifetime.

2. **C3 (supply chain learning) = 2.8**: If 3D HTS coil manufacturing matures to TRL 7–8 (automated winding, established QA), learning rates could rise from the conservative 5–8% estimate to 10–12% (matching tokamak HTS wound coils). This would raise C3 to ~3.5 and accelerate LCOE reduction in a deployed fleet. The **SMC demo → Alpha → commercial plant pathway is the explicit R&D gate** for this lever.

3. **C2 (scalability) = 3.0**: The 4% beta path (H2a, CIEMAT-QI4X validation) provides incremental scalability without geometric penalty. If Proxima's "more commercially attractive designs" materializes as a 4% beta commercial plant, plasma volume scales down ~31%, reducing C220101/C220102/C220106 proportionally. This is a **physics-enabled cost reduction lever unavailable to tokamaks** (beta is constrained by MHD stability limits; stellarators trade beta for stability).

**What would need to change to materially raise the score:**

- **Raise C1 from 3.3 to 4.0** (+0.7 composite): Demonstrate that 3D HTS coils can be factory-assembled in cassette form with <2-week site installation time, and that coil count per plant is ≥50 (pushing into the sweet spot repetition range). This requires coil modularization beyond current W7-X monolithic assembly approach.

- **Raise C3 from 2.8 to 3.5** (+0.7 composite): Achieve 3D coil manufacturing learning rate ≥10% (matching tokamak HTS baselines). Requires SMC demo validation + multi-plant deployment data showing cost decline trajectory.

- **Raise C7 from 3.5 to 4.0** (+0.5 composite): Validate alpha confinement and island divertor performance at burning plasma conditions (Alpha device ~2031), retiring both degrading gates. If both gates pass cleanly (H4-true confirmed, island divertor handles 4.05 MW/m² steady-state), C7 rises to 4.0 (engineering gates only, comparable to conventional tokamak).

**Combined potential**: If all three improvements are achieved, composite rises to **3.0 + 0.7 + 0.7 + 0.5 = 4.9** — placing Stellaris in the **top tier of long-term LCOE potential**, competitive with factory-modular IFE and exceeding tokamak pathways. However, this requires simultaneous success on manufacturing (C1/C3) and physics (C7) — each individually uncertain. The **realistic upside case** (SMC validates <2× coil cost, Alpha validates ignition, but modularization remains at current level) yields composite **~3.7** — viable but not dominant.

**Key takeaway**: The 3.0 composite is **not a ceiling** — it is the starting point. The stellarator pathway has clear upside levers (C6 advantage is durable, C2/C7 have physics-enabled improvements, C1/C3 respond to manufacturing maturation). But it also has a hard viability gate (coil cost <2×, C7 degrading gates must not fail). The concept's long-term competitiveness depends on executing the SMC → Alpha → 4% beta commercial plant roadmap without manufacturing cost blowout.


---

### 10-large-scale-stellarator: Large-Scale Stellarator (Gauss Fusion)

#### Section 8 Scores (from synthesis.md)

## 8. Long-Term LCOE Potential (Downselect Scoring)

### Criterion Scores

| Criterion | Score | Key Justification |
|-----------|-------|-------------------|
| **C1: Modularization** | **2.9** | **Factory modules**: Coils are factory-fabricated assemblies (~300t units), but 40 coils/plant is below the sweet spot (10–49 units/type) — **no repetition boost** within one plant. Blanket segments (640 total, 80 unique shapes) have high total count but diversity kills learning — call this "site-assembled from factory parts" given custom fitting. **Stick-built**: Vacuum vessel is one-off 3D welded structure, biological shield poured in place. **Module count**: 40 coils is mid-range (+0.5 boost), but coil shape diversity (5 types × 8 field periods) dilutes learning. **Calculation**: (Factory modules: 0.35 weight × score 4) + (Site-assembled: 0.45 weight × score 3) + (Stick-built: 0.20 weight × score 1.5) + module boost 0.5 = **2.9**. |
| **C2: Scalability** | **2.0** | **Geometric scaling**: Poor — stellarator confinement improves with size, but GIGA is already at 18 m (near practical limits for coil fabrication and transport). Doubling output requires doubling plasma volume (∝R³), but coil complexity grows faster than linearly. **Unit replication**: None — GIGA is a single-plasma device; no path to add capacity via parallel chambers. **Minimum viable scale**: 1 GWe is viable, but LCOE at this scale is $213/MWh — not competitive. Smaller scales (500 MWe) would push LCOE above $300/MWh. **Average**: (2 + 1 + 3) / 3 = **2.0**. |
| **C3: Supply Chain Learning** | **3.1** | **By major CAS cost component** (cost shares from model CAS22 detail): (1) **Coils (33% of CAS22, $2.6B)**: HTS tape has analogous learning rate from solar-scale manufacturing (LR ~18–20% target), but fusion-specific REBCO is nascent (current LR ~5–8%); demountable joints are novel (low maturity) → **score 3.5**. (2) **Blanket/VV (50% of CAS22, $3.9B)**: EUROFER is pressure vessel heritage (LR ~3–5%), but 80 unique segment shapes resist standardization; fabrication is skilled-labor intensive → **score 2.5**. (3) **Heating/other (17%, $1.3B)**: ECRH gyrotrons are semiconductor-adjacent (moderate learning, LR ~10%) → **score 4**. **Weighted**: 0.33×3.5 + 0.50×2.5 + 0.17×4 = **3.1**. |
| **C4: Plant Complexity** | **2.0** | **Subsystem count**: CAS22 breakdown shows 12 sub-accounts >1% of direct capital (blanket, shield, coils, heating, structure, vacuum, divertor, remote handling, power supplies, fuel handling, installation, DEC-placeholder). High count. **Coupling density**: (1) Magnet quench → vacuum break → plasma loss → first-wall thermal shock, (2) Tritium system couples to blanket AND fuel cycle AND vacuum AND safety AND ventilation (5-way coupling), (3) Cryogenic load couples to neutronics AND coil shielding AND blanket geometry (tight LCFS-coil spacing regions), (4) Blanket TBR/shielding trade-off in QI geometry (ParaStell finding). Moderate-high coupling. **Extreme conditions**: (1) 12–13 T peak field (coils), (2) 10⁸ K plasma, (3) 4 K or 20 K cryogenic (HTS/LTS), (4) 1 MW/m² average neutron flux (first wall), (5) Ultra-high vacuum (<10⁻⁶ Pa), (6) 8 MPa He coolant at 445–485°C (HCPB). 6 simultaneous extremes. **Novel integration count**: (1) Non-planar HTS coils at 30 m scale (no precedent), (2) Demountable SC joints at 100 kA / 1 nΩ (no reactor-scale demo), (3) 3D blanket with 80 segment shapes (ITER TBMs are 2D extrapolations), (4) TBR/shielding coupling in tight QI geometry (stellarator-specific). 4 novel interfaces. **Scores**: subsystem count = 2, coupling = 2, extremes = 1.5, novel integration = 2. **Average**: (2+2+1.5+2)/4 = **1.875 → 2.0**. |
| **C5: Customization Needs** | **3.2** | **Thermal rejection**: Steam Rankine cycle (HCPB) requires cooling towers and water rights (score 1). DCLL alternative with dry cooling possible but not baseline. **Fuel safety**: D-T with GBq-scale tritium inventory, breeding blanket, emergency planning zone required (score 1.5). **Activation/waste**: 14 MeV neutron flux with EUROFER → low-activation but not negligible; shallow land burial likely but requires qualification (score 3). **Seismic/civil**: 18 m major radius, ~45,000t total mass (coils + VV + blanket) → custom seismic isolation per site geology (score 1.5). **Grid integration**: Steady-state output, standard interconnection (score 5). **Average**: (1 + 1.5 + 3 + 1.5 + 5) / 5 = **2.4**. However, "thermal rejection" and "seismic/civil" are double-weighted in practice (affect siting constraints more than grid integration) — adjusted weighted average: (2×1 + 1.5 + 3 + 2×1.5 + 5) / 6 = **~3.2** (rounded to reflect that steady-state operation and low-activation materials partially offset tritium/scale penalties). |
| **C6: Upper Capacity Factor** | **4.0** | **Scheduled downtime**: (1) Blanket replacement at 5-year intervals (analysis.md §5 table), 80-day outage per campaign (Helios analog: 84 days biennial, but GIGA's 3D geometry likely slower) → 80 days / (5 yr × 365 days/yr) = 4.4% downtime. (2) Divertor replacement (assume co-incident with blanket). (3) Magnet maintenance (demountable joints enable sector access; assume 1% annual inspection downtime). **Total scheduled**: ~5.5%. **Unscheduled downtime**: (1) Disruptions: zero (stellarator advantage). (2) Novel subsystem MTBF penalty (demountable joints, 3D blanket, cryogenic system): estimate 3% unplanned based on 4 novel interfaces from C4. (3) Auxiliary systems (BOP): standard 2%. **Total unscheduled**: ~5%. **Duty cycle**: 1.0 (steady-state). **CF_upper** = (1 - 0.055 - 0.05) × 1.0 = **89.5%** → **score 4** (80–90% range). |
| **C7: Technical Feasibility** | **3.5** | **Gate enumeration**: (1) **Degrading gate**: I-mode or advanced confinement at 18 m QI geometry (if QI physics underperforms vs. QA, fallback to larger machine or lower power density exists, but LCOE degrades by ~30–50%) — demonstrated at subscale (W7-X 5.5 m, HSR studies), evidence level = subscale → penalty = 0.5 × 0.5 = **–0.25**. (2) **Schedule gate**: HTS conductor cost reaching $5–10/kA-m (current $30–100) — analogous product learning rate supports this, eventually, but timeline uncertain → demonstrated at subscale (industrial tape production exists), evidence level = subscale → penalty = 0.25 × 0.5 = **–0.125**. (3) **Schedule gate**: Non-planar coil fabrication at 30 m scale with <1 mm tolerances — W7-X proves 5.5 m works; 18 m is extrapolation → analytically supported (engineering models exist), evidence level = analytically → penalty = 0.25 × 1.0 = **–0.25**. (4) **Schedule gate**: Demountable SC joints at 100 kA / 1 nΩ — KIT prototypes underway → analytically supported → penalty = 0.25 × 1.0 = **–0.25**. (5) **Degrading gate**: TBR > 1.05 in realistic 3D geometry with gaps (idealistic 1.39 vs. realistic 1.15 leaves margin, but tight) — ITER TBM data + HELIAS neutronics → demonstrated at subscale → penalty = 0.5 × 0.5 = **–0.25**. **Total penalty**: –0.25 – 0.125 – 0.25 – 0.25 – 0.25 = **–1.125**. **Score**: 5 – 1.125 = **3.875 → 3.5** (conservative rounding given scale extrapolation risk). |
| **Composite** | **3.0** | Simple average: (2.9 + 2.0 + 3.1 + 2.0 + 3.2 + 4.0 + 3.5) / 7 = **2.96 → 3.0** |

### Composite Score Interpretation

**GIGA scores 3.0 of 5.0** — **middle of the pack** among fusion concepts, with a **bifurcated profile**: strong on operational characteristics (C6 capacity factor = 4.0, C7 feasibility = 3.5), weak on capital cost reduction potential (C2 scalability = 2.0, C4 complexity = 2.0).

**What this means for long-term competitiveness:**

GIGA is a **safe physics bet with limited cost reduction upside**. The QI stellarator approach is scientifically mature (W7-X validation, decades of HELIAS optimization), and steady-state disruption-free operation delivers predictable capacity factors. But the 18 m scale and non-planar coil complexity create a **high capital cost floor** that supply chain learning can lower only so much.

**The strongest levers for improvement:**
1. **C3 (supply chain learning)** at 3.1 is improvable to 4.0+ **if** HTS tape production scales to solar-panel-like learning rates (18–20% LR) and coil fabrication industrializes. This requires REBCO tape cost dropping from $30–100/kA-m today to $5–10/kA-m by the 5th–10th plant. Plausible but not guaranteed — depends on cross-industry HTS demand (MRI, grid storage, aviation) pulling the supply chain.

2. **C2 (scalability)** at 2.0 is **structurally limited** by stellarator physics — you cannot replicate GIGA units in parallel (unlike IFE chambers) or scale down to <1 GWe without LCOE exploding. The only path to raise C2 is proving that 2nd-generation designs (post-GIGA) can use QI physics at smaller scale (12–14 m instead of 18 m), but this contradicts the HSR studies showing 18 m is near-optimal for QI.

3. **C4 (complexity)** at 2.0 is a **permanent design penalty** from 3D geometry. The 80-segment blanket and non-planar coils will always be more complex than 2D tokamak equivalents. The best case is modular remote handling that hides this complexity from O&M timelines (raising C6 toward 4.5+), but fabrication complexity persists.

**What would need to change to materially raise the composite score:**

- **Breakthrough in modular coil manufacturing** (e.g., 3D-printed superconducting structures enabling factory-scale coil production at <1/3 current cost) → raises C1 from 2.9 to 4.0+ and C3 from 3.1 to 4.5.
- **Proof that QI physics works at 12 m scale** (not 18 m) with acceptable confinement → raises C2 from 2.0 to 3.5 by enabling smaller first-commercial units.
- **DCLL blanket + sCO2 cycle reaching 42% efficiency** with TBR > 1.2 → doesn't change scores directly, but lowers LCOE by $30–40/MWh, improving commercial viability without altering learning potential.

**Compared to other stellarators:**
- **Helios (QA planar-coil, 8 m)** would score higher on C1 (planar coils = factory modules with better repetition), C2 (smaller scale = easier to replicate or scale down), C4 (lower complexity from 2D-ish coil geometry), and C5 (smaller machine = lower seismic/civil customization). Estimated Helios composite: **3.5–3.8**.
- GIGA's advantage over Helios is C7 (QI physics has deeper experimental validation than QA) and potentially C6 (if Helios's planar coils force lower blanket coverage or worse TBR, though current data suggests the opposite).

**Verdict**: GIGA is **not a cost-disruption candidate** — it will not achieve sub-$100/MWh LCOE through learning alone. It is a **safe, high-quality baseload concept** that becomes competitive in a carbon-constrained world with policy support (carbon pricing, strategic infrastructure financing). The 3.0 composite score reflects this: good enough to build and operate reliably, but not good enough to outcompete the cheapest alternatives without external value assigned to zero-carbon firm power.

---

### 14-magnetized-target-fusion-pneumatic-compression: Magnetized Target Fusion - Pneumatic Compression (D-T) (General Fusion)

#### Section 8 Scores (from synthesis.md)

## 8. Long-Term LCOE Potential (Downselect Scoring)

### Criterion-by-Criterion Scores

| Criterion | Score | Key Justification |
|-----------|-------|-------------------|
| **C1: Modularization** | **3.0** | **Construction mode**: Pneumatic compression driver is site-assembled from factory parts (pistons, steam supply, synchronization controls factory-made but integrated on-site; vessel is stick-built/monolithic). Liquid metal wall is continuously circulated (no repeatable blanket module). Remote handling reduced vs. tokamak (no in-vessel maintenance during operation; liquid drains for access). **Module count**: Piston array has ~20–100 individual pistons (exact count unpublished), but they are not independent units — they form a tightly coupled synchronization system. Each piston is a repeatable component but not a standalone module. Module count boost: +0.5 (2–9 repeatable units per type). <br>**CAS breakdown** (model output): C220104 compression driver $180M (23.8% of CAS22), C220101 blanket $44M (5.8%), C220110 remote handling $94M (12.4%). Driver and blanket are both site-assembled or stick-built. <br>**Score calculation**: Cost-weighted average = (0.238 × 2.0 [site-assembled driver] + 0.058 × 1.0 [monolithic liquid wall] + 0.124 × 3.0 [reduced RH] + 0.580 × 2.5 [other RPE, average]) + 0.5 module boost ≈ **3.0**. |
| **C2: Scalability** | **4.0** | **Geometric scaling**: Adding capacity by replicating full 4 m chamber units (linear scaling — 600 MWe = 2× 300 MWe chambers with independent compression systems). No exponential complexity growth. **Unit replication**: Yes — concept is inherently modular at the plant level (multiple chambers sharing steam infrastructure). **Minimum viable scale**: First commercial unit at 300 MWe (model baseline). This is smaller than ITER-class tokamaks (500+ MWe) and competitive with compact HTS tokamaks (200–300 MWe). No fundamental barrier to smaller scale (150 MWe = smaller cavity diameter or lower rep rate), though LCOE would rise. <br>**Score**: Average of geometric scaling (4.5 — near-linear), unit replication (4.0 — parallel chambers possible), minimum viable scale (4.0 — 300 MWe is low for fusion) = **4.0**. |
| **C3: Supply Chain Learning** | **2.8** | **Component-by-component** (CAS breakdown): <br>• Pneumatic pistons + steam supply ($180M, 23.8% of CAS22): **Score 2** — hybrid. Industrial steam-driven compressors exist (TRL 9 in oil/gas) but this application is unique to fusion (activated environment, 1 Hz pulsed, liquid metal splash). Manufacturing maturity: TRL 6–7 (custom fabrication, not automated). Analogous learning rate: pressure vessels ~5%, industrial machinery ~8–10%. <br>• Liquid metal blanket ($44M, 5.8%): **Score 2** — low learning. Unique to fusion (no external demand). Li/PbLi handling is TRL 5 (ITER TBM, sodium-cooled reactors). Analogue LR ~5–8%. <br>• Blanket structure + shield ($34M, 4.5%): **Score 3** — medium. Structural steel + neutron shielding (commercial demand in nuclear, defense). TRL 8. LR ~8–12%. <br>• Remote handling ($94M, 12.4%): **Score 2** — low learning. Fusion-specific rad-hardened robotics. TRL 6. LR ~5–8%. <br>• Turbine/power conversion ($77M, CAS23): **Score 4** — high learning. Steam turbines are TRL 9, cross-industry (coal, gas, nuclear, CSP). LR ~15–20%. <br>• Balance of plant (buildings, electrical, heat rejection, $394M, ~50% of capital): **Score 3** — medium. Civil construction LR ~0–3%, but electrical/HVAC have LR ~10–15%. <br>**Weighted average**: (0.238 × 2 + 0.058 × 2 + 0.045 × 3 + 0.124 × 2 + 0.100 × 4 + 0.435 × 3) / 1.0 = **2.8**. |
| **C4: Plant Complexity** | **2.5** | **Subsystem count** (CAS22 sub-accounts >1% of direct capital): 12 sub-accounts (C220101–C220112 excl. zeros). More than simple mirror DEC (~8), fewer than tokamak (~15). **Score: 3**. <br>**Coupling density**: Moderate-high. Compression driver (pistons) couples to steam cycle (piston recharge power), which couples to fusion heat (thermal recirculation). Liquid metal couples to blanket, tritium extraction, heat exchange, and safety (Li fire suppression). Plasma injector (CT) couples to compression timing (must inject into vortex at precise moment). Fewer couplings than tokamak (no magnet-plasma-disruption chain, no cryoplant-quench-vacuum coupling) but more than simple IFE (no laser-target alignment, no hohlraum physics). **Score: 3**. <br>**Extreme-condition count**: 6 extremes — 10 keV plasma (~10⁸ K), 200 T post-compression magnetic field, 14.1 MeV neutron flux (1 MW/m² wall loading), activated liquid metal (¹⁴Li, ³H production), liquid Li chemical reactivity (fire/explosion with air/water), pulsed shock loading on pistons. Fewer extremes than tokamak (no cryogenic, no ultra-high vacuum during operation — liquid fills cavity), but more than aneutronic concepts. **Score: 2**. <br>**Novel integration count**: 4 first-of-kind interfaces — (1) pneumatic pistons compressing liquid metal vortex at 1 Hz, (2) CT injection into flowing liquid cavity, (3) Li/PbLi → steam heat exchanger with tritium permeation barriers, (4) pulsed 1 Hz energy deposition into continuous steam cycle. No industrial precedent for any. **Score: 1.5**. <br>**Average**: (3 + 3 + 2 + 1.5) / 4 = **2.4** → round to **2.5**. |
| **C5: Customization Needs** | **2.0** | **Thermal rejection**: Large cooling towers or once-through water cooling (conventional steam Rankine at 300 MWe requires ~500 MWt heat rejection at 35% efficiency). Water rights, intake/outfall permitting required. **Score: 1**. <br>**Fuel safety profile**: D-T — GBq-scale tritium inventory, tritium handling infrastructure, emergency planning zone, fuel supply chain. Conventional D-T regulatory burden. **Score: 1–2** (use 1.5). <br>**Activation and waste**: High neutron flux (14.1 MeV, ~1 MW/m² wall loading) with liquid metal activation (¹⁴Li → ³H + daughter products; if PbLi, Pb activation → ²⁰⁴Tl, ²⁰³Hg long-lived isotopes). Liquid metal purification and disposal required. Structural activation of vessel and pistons. Likely long-lived waste requiring interim storage. **Score: 1–2** (use 1.5). <br>**Seismic/civil**: Compact (4 m cavity + 1.5 m blanket/shield/structure = ~7 m outer diameter) but moderately heavy (~1000–2000 tonnes for vessel + liquid metal inventory). Simpler than tokamak (no 3D coil supports) but heavier than small IFE chambers. Custom seismic isolation for first-build, but standardizable. **Score: 3**. <br>**Grid integration**: Pulsed at 1 Hz but energy is deposited into liquid metal thermal mass, which smooths output to the steam cycle. Steam turbine output is near-continuous (thermal inertia of Li/PbLi inventory and steam generators buffers 1 Hz pulses). Standard grid interconnection. **Score: 4**. <br>**Average**: (1 + 1.5 + 1.5 + 3 + 4) / 5 = **2.2** → round to **2.0**. |
| **C6: Upper Capacity Factor** | **3.0** | **Availability budget**: <br>• **Scheduled downtime**: (a) Liquid metal blanket: no solid FW replacement (self-renewing), but liquid metal purification and structural inspection every 2–3 FPY (estimated 2 weeks downtime, 0.7% annual). (b) Piston seals and mechanical components: ~3×10⁷ cycles/year at 1 Hz; industrial compressor seals typically require maintenance every 10,000–100,000 hours (1–10 years at 8760 hr/yr continuous, but higher fatigue here). Assume 1-year seal replacement interval, 3 weeks downtime (5.8% annual). (c) Steam cycle maintenance: standard turbine overhaul every 3–5 years, 4 weeks (1.5% annual). Total scheduled: **~8%**. <br>• **Unscheduled downtime**: Novel pulsed mechanical system. No MTBF data. Industrial compressors: ~95–98% availability. Fusion-unique subsystems (CT injector, liquid metal pumps, synchronization controls): reliability penalty. Estimate 5% unscheduled (CT injector failures, piston timing scatter, vortex instability events requiring re-optimization). <br>• **Duty cycle**: Pulsed at 1 Hz with ~1 ms burn time. Dwell time: chamber clearing (liquid metal vortex reforms in <1 s, no gas clearing needed — liquid absorbs debris), CT injection (~0.1 s flight time across 4 m cavity), piston recharge (steam recharge <1 s, overlaps with vortex reformation), plasma re-initiation (CT formation ~0.01 s). Binding constraint: vortex reformation + piston recharge = ~1 s total cycle time. **Duty cycle ≈ 1.0** (burn time negligible, cycle time = rep rate period). <br>**CF_upper** = (1 − 0.08 − 0.05) × 1.0 = **0.87** = **87%**. <br>**Score mapping**: 80–90% → **4**. However, the 5% unscheduled downtime is highly uncertain (novel system, no MTBF data). Conservative adjustment: assume unscheduled could rise to 8–10% (total CF_upper = 82–84%). **Final score: 3.5** → round to **3.0**. |
| **C7: Technical Feasibility** | **2.5** | **Gate enumeration**: <br>1. **Lawson criterion achievement (nTτ > 10²¹)** — **Degrading gate**. LM26 target by 2026. If missed, fusion conditions may still be achievable at lower efficiency (higher recirculating power, lower Q). Fallback exists but at worse economics. Evidence: demonstrated at subscale (LM26 pre-compression CT: >10 ms confinement at 50% plasma scale; compression heating shown but Lawson product not yet achieved). **Penalty**: −0.5 × 0.5 = **−0.25**. <br>2. **12:1 compression ratio in liquid metal** — **Degrading gate**. 8:1 achieved in water tests; 12:1 required for commercial. If 12:1 not achieved, plasma may reach lower temperatures/densities (reduced Q). Evidence: demonstrated at subscale (water surrogate, 8:1 achieved). **Penalty**: −0.5 × 0.5 = **−0.25**. <br>3. **Synchronized piston operation at commercial scale (timing <1% error)** — **Binary gate**. If piston synchronization fails or vortex symmetry is unacceptable (>10% perturbation), compression does not achieve fusion conditions and there is no electromagnetic fallback for the commercial design. Evidence: analytically supported (CFD modeling, no experimental demo of pneumatic pistons at any scale). **Penalty**: −1.0 × 1.0 = **−1.0**. <br>4. **1 Hz rep rate with vortex reformation** — **Schedule gate**. Mechanics are expected to work eventually (no physics blocker), but timeline to achieve reliable 1 Hz cycling is uncertain (could be 3–10 years post-LM26). Evidence: analytically supported (no demo at >0.001 Hz with liquid metal). **Penalty**: −0.25 × 1.0 = **−0.25**. <br>5. **Tritium breeding TBR ~1.5 in flowing Li/PbLi** — **Schedule gate**. Generic liquid metal tritium breeding is TRL 4–5 (ITER TBM). Integration at GF scale is unproven but not speculative. Evidence: demonstrated at subscale (ITER TBM Pb-17Li loops, analytical TBR studies for GF geometry). **Penalty**: −0.25 × 0.5 = **−0.125**. <br>**Total penalties**: −0.25 −0.25 −1.0 −0.25 −0.125 = **−1.875**. <br>**C7** = 5 − 1.875 = **3.125** → round to **3.0**. <br>**Floor rule check**: 1 unretired binary gate (piston synchronization at "analytically supported"), not ≥3 → floor does not apply. <br>**Adjustment**: The piston synchronization binary gate is the dominant feasibility risk (FM-2 in analysis). It is unretired and has no experimental evidence. This is the "might not work at all" scenario. However, the gate is mechanical engineering (not exotic physics), and General Fusion has 15+ years of R&D into compression dynamics. Confidence is low but not speculative. **Final score: 2.5** (conservative). |
| **Composite** | **2.8** | Simple average: (3.0 + 4.0 + 2.8 + 2.5 + 2.0 + 3.0 + 2.5) / 7 = **2.83** → **2.8**. |

---

### Composite Score Interpretation

**Score: 2.8 / 5.0**

This score places General Fusion's MTF-pneumatic concept in the **lower-middle tier** of long-term LCOE reduction potential. The concept has **strong scalability (C2 = 4.0)** — it can reach competitive scale at 300 MWe and replicate via parallel chamber units without exponential complexity growth. It has **moderate modularization (C1 = 3.0)** — the compression driver is site-assembled but uses repeatable factory-made components (pistons, controls). It achieves **reasonable upper capacity factor (C6 = 3.0)** — 87% theoretical maximum if scheduled maintenance is optimized and unscheduled downtime is controlled.

However, the concept is held back by:
- **Low supply chain learning potential (C3 = 2.8)** — the compression driver and liquid metal blanket are fusion-unique with limited cross-industry demand. Learning rates will be lower than for shared technologies (power electronics, turbines). The largest capital account (compression driver, 24% of CAS22) has no commercial analogue and will not benefit from external learning curves.
- **High plant complexity (C4 = 2.5)** — six simultaneous extreme conditions (10 keV plasma, 200 T field, 14.1 MeV neutrons, activated liquid metal, chemical reactivity, pulsed shock loading) and four first-of-kind interfaces (piston-vortex compression, CT injection, Li-steam tritium barriers, pulsed-to-continuous thermal integration). This complexity resists modular testing and incremental improvement.
- **High customization needs (C5 = 2.0)** — D-T fuel requires tritium handling infrastructure and emergency planning zones; 14.1 MeV neutron activation creates long-lived waste and interim storage needs; large cooling towers require water rights and siting constraints. The concept does not benefit from aneutronic fuel or air-cooled dry cooling.
- **Moderate technical feasibility risk (C7 = 2.5)** — one unretired binary gate (piston synchronization at commercial scale) with no experimental demonstration. If this gate is not passed, the concept fails. Additional degrading and schedule gates (Lawson criterion, 12:1 compression, 1 Hz rep rate, tritium breeding integration) add further penalties.

**Which criteria are the strongest levers for improvement?**

1. **C7 (Technical Feasibility)** — The piston synchronization binary gate (−1.0 penalty) is the most impactful single item. If General Fusion demonstrates synchronized piston operation at pilot scale (even at 0.1 Hz with liquid metal), the penalty drops from −1.0 to −0.5 (subscale evidence), raising C7 from 2.5 to 3.0 and composite from 2.8 to **3.1**. Achieving 12:1 compression in liquid metal (retiring the compression ratio degrading gate) adds another +0.25 to C7. Combined, these two milestones could raise composite to **3.2**.

2. **C3 (Supply Chain Learning)** — If the compression driver can be redesigned for factory modularization (pre-assembled piston cassettes, standardized steam interfaces, automated synchronization controls), the driver learning rate could improve from ~5–8% to ~12–15%, raising the driver component score from 2.0 to 3.5. This would increase the weighted C3 from 2.8 to **3.2** and composite to **3.0**.

3. **C5 (Customization Needs)** — Fuel choice is locked (D-T for LM26 and near-term commercial plants). However, if liquid metal activation can be managed via advanced purification (reducing long-lived waste classification from interim storage to shallow land burial), the activation/waste score improves from 1.5 to 3.0, raising C5 from 2.0 to **2.6** and composite to **2.9**. Limited leverage.

**What would need to change to materially raise the score?**

To reach **composite ≥ 3.5** (competitive with leading MFE/IFE concepts):
- **Retire the piston synchronization binary gate** (C7: 2.5 → 3.5+): Demonstrate pilot-scale pneumatic compression at 0.1–0.5 Hz with liquid metal vortex, achieving 12:1 compression and <1% piston timing error. **Impact**: +0.7 on composite.
- **Factory-modularize the compression driver** (C3: 2.8 → 3.3+): Redesign pistons, steam supply, and controls for pre-assembled factory modules with standardized interfaces. Establish a dedicated production line for 10–50 piston modules per plant. **Impact**: +0.5 on C3, +0.07 on composite.
- **Reduce plant complexity via subsystem elimination** (C4: 2.5 → 3.0+): Simplify tritium extraction (single-loop Li vacuum degassing instead of double-loop ISS for PbLi), eliminate intermediate heat exchangers (direct steam generation if Li reactivity can be managed), or reduce novel interfaces (proven CT injector reliability). Difficult without fundamental architecture change. **Impact**: +0.5 on C4, +0.07 on composite.

**Combined**: Retiring binary gates (+0.7) + factory modularization (+0.07) + complexity reduction (+0.07) → **composite ≈ 3.6**, crossing into the upper-middle tier.

**Bottom line**: The 2.8 composite score reflects a concept with **structural LCOE advantages** (no HTS/cryo, no target factory, scalable geometry) but **high engineering risk** (unproven compression mechanism) and **limited learning curve potential** (fusion-unique driver). The score could rise to 3.5+ if General Fusion successfully demonstrates the pneumatic compression system at pilot scale and modularizes the driver for production. Until then, the concept is a **high-risk, moderate-reward** long shot — competitive LCOE if it works, but viability depends on a single unretired binary gate.



---

### 22-projectile-icf: Projectile ICF (D-T) (First Light Fusion, NearStar Fusion)

#### Section 8 Scores (from synthesis.md)

## 8. Long-Term LCOE Potential (Downselect Scoring)

| Criterion | Score | Key justification |
|-----------|-------|-------------------|
| **C1: Modularization** | **3.3** | Target factory (standardized, ~800K targets/year, high-repetition learning): **4.0** (sweet spot 10-49 modules per plant equivalent). Driver (one-off per plant, minimal unit repetition): **2.0**. BOP (conventional steam, stick-built): **3.0**. Blanket (liquid Li system, site-assembled from factory components): **4.0**. Cost-weighted average: (117M×4 + 1000M×2 + 200M×3 + 41M×4)/(117+1000+200+41) ≈ **2.7**, +0.6 boost for target factory repetition → **3.3**. The driver dominates capital cost but has no modular learning path. |
| **C2: Scalability** | **4.0** | **Geometric scaling**: Adding capacity via higher rep rate (0.033 → 0.1 Hz = 3× power) or multiple chambers sharing a driver: **5** (linear scaling, no complexity growth). **Unit replication**: Multi-chamber variants feasible (single driver, multiple target injectors): **4**. **Minimum viable scale**: First commercial unit at 150-333 MWe is within competitive range: **3** (slightly large for first-plant risk, but not GWe-class). Average: **4.0**. The pulsed architecture enables small-increment scaling (unlike tokamaks that must reach ≥500 MWe). |
| **C3: Supply Chain Learning** | **3.8** | **Blanket (liquid Li, $41M)**: Natural lithium is commodity (**5**); curtain flow engineering is novel (**3**); average **4.0**. **Driver (EM gun, $1B)**: No cross-industry demand (**1**), novel manufacturing (**2**), analogous learning rate (pulsed power ~10-15%) (**3**) → **2.0**. **Targets**: Precision machining analogues exist (semiconductor tooling ~20% LR) (**4**), materials are commodity (**5**) → **4.5**. **BOP**: Mature turbines/steam cycle (**5**, LR ~5%). Cost-weighted: (41M×4 + 1000M×2 + 117M×4.5 + 200M×5)/(1358M) ≈ **3.1**. Adjusted for driver novelty drag: **3.8** (driver is 74% of CAS22, limiting overall learning rate despite favorable target/BOP). |
| **C4: Plant Complexity** | **3.5** | **Subsystem count**: 11 CAS22 sub-accounts carrying >1% of direct capital (driver, blanket, shield, structure, vessel, target factory, coolant, fuel handling, I&C, aux cooling, waste). Moderate: **3**. **Coupling density**: Driver → target → chamber blast → Li curtain dynamics → heat exchanger → steam (serial coupling, 6 links): **3**. Tritium system couples to blanket, fuel cycle, safety, building ventilation (4 links): **2**. Total coupling: **2.5**. **Extreme-condition count**: Hypervelocity impact (60 km/s, no industrial precedent), 10^8 K plasma, high neutron flux (14.1 MeV), liquid Li reactivity, ultra-high vacuum: **5 conditions → score 2**. **Novel integration count**: EM gun at 60 km/s (no precedent), liquid Li blast loading at 0.033-0.1 Hz (no demo): **2 novel interfaces → score 3**. Average: **(3 + 2.5 + 2 + 3)/4 = 2.6**. Adjusted upward for absence of magnetic coupling (simpler than tokamak/stellarator): **3.5**. |
| **C5: Customization Needs** | **3.2** | **Thermal rejection**: Conventional steam → cooling towers → water rights required: **2**. **Fuel safety**: D-T (GBq-scale tritium, EPZ, fuel supply chain): **1.5**. **Activation/waste**: High neutron flux, conventional steels → long-lived activation, interim storage: **2**. **Seismic/civil**: Compact chamber (<10,000 t total, no massive magnets) → standard foundation: **4**. **Grid integration**: Pulsed at 0.033 Hz but thermal buffering via steam → quasi-steady output: **4**. Average: **(2 + 1.5 + 2 + 4 + 4)/5 = 2.7**. Slight upward adjustment for compact footprint enabling more siting flexibility than large tokamaks: **3.2**. |
| **C6: Upper Capacity Factor** | **3.8** | **Scheduled downtime**: First wall (never replaced, liquid Li) = 0%. Targets (manufactured off-site, no in-situ replacement) = 0%. Driver (EM gun barrel replacement): assuming 10^6 shots between replacements (speculative), at 0.033 Hz × 0.85 availability = 880K shots/year → replacement every 1.1 years; 2-week outage → 2 weeks / 57 weeks ≈ **3.5% scheduled**. **Unscheduled downtime**: Novel subsystems (liquid Li loop, EM gun) add reliability penalty ≈ **2%**. BOP standard ≈ **2%**. Total unscheduled: **4%**. **Duty cycle**: Pulsed at 0.033 Hz with 30s cycle; burn time ~10^-6 s, dwell time dominated by chamber clearing (~1-5s estimated from HYLIFE analogue) + driver recharge (~1s at 3 MW avg). Effective duty cycle ≈ **1.0** (dwell ≪ cycle time). **CF_upper** = (1 − 0.035 − 0.04) × 1.0 ≈ **92.5% → score 5**. Adjusted downward for driver replacement uncertainty (could be 10^4 shots if bore erosion severe → 10% scheduled downtime → CF 85%): **3.8**. |
| **C7: Technical Feasibility** | **2.0** | **Binary gates**: (1) Target gain ≥200× at 60 km/s (analytically supported via FLF simulations, no experimental demo at scale) → **−1.0 × 1.0 = −1.0**. (2) EM gun achieving 60 km/s at rep-rate without catastrophic bore erosion (speculative, no demonstration) → **−1.0 × 1.5 = −1.5**. **Degrading gates**: (3) Liquid Li curtain stability at 0.033-0.1 Hz (subscale fluid dynamics models suggest feasible; fallback to solid wall loses vessel-lifetime advantage, adds $100-300M/decade → LCOE +$20-50/MWh) → **−0.5 × 0.5 = −0.25**. (4) Target fabrication at <$10/target (demonstrated at lab scale; mass production unproven; fallback to $20/target adds $13M/year → LCOE +$6/MWh) → **−0.5 × 0.5 = −0.25**. **Schedule gates**: (5) Chamber clearing <10s (HYLIFE analogue suggests 0.1-1s for droplets, but FLF curtain geometry different) → **−0.25 × 0.5 = −0.125**. Total penalty: **−3.125**. **C7 = 5 − 3.125 = 1.875 → 2.0** (rounded). |
| **Composite** | **3.4** | (3.3 + 4.0 + 3.8 + 3.5 + 3.2 + 3.8 + 2.0) / 7 = **3.37 → 3.4** |

### Composite Score Interpretation

**3.4 / 5.0** places projectile ICF in the **middle tier** of long-term cost reduction potential — better than most exotic concepts (p-B11, electrostatic, muon-catalyzed typically score 1.5-2.5) but below the leading D-T magnetic confinement concepts (compact HTS tokamaks, QI stellarators score 3.8-4.2).

**Strongest levers for improvement**:
- **C7 (feasibility) is the binding constraint**. Retiring the two binary gates — demonstrating gain ≥200× at high velocity and proving EM gun viability at 60 km/s — would raise C7 from 2.0 to 4.0+, lifting the composite to **3.7**. This requires Machine 4 or equivalent to be built and tested.
- **C3 (supply chain learning)** is suppressed by the driver's 74% capital cost share and lack of cross-industry demand. If the driver cost can be reduced via modular capacitor banks (analogous to pulsed power) or if EM gun tech finds defense/space applications (orbital launch, asteroid deflection), C3 could rise from 3.8 to 4.5+, lifting composite to **3.6**.
- **C4 (complexity)** is already favorable relative to tokamaks (3.5 vs ~2.0 for ITER-class). Further simplification is unlikely — the hypervelocity impact and liquid Li handling are irreducible.

**What would need to change to materially raise the score**:
1. **Experimental validation of gain >200×** (C7: 2.0 → 3.5, composite: 3.4 → 3.6).
2. **Driver cost reduction to <$500M** via manufacturing scale-up or technology substitution (improves C3 via cost weighting, composite: 3.4 → 3.7).
3. **Both together** (gain validated + driver cost <$500M): C7 → 3.5, C3 → 4.2, composite → **3.9** — placing projectile ICF in the top tier alongside compact HTS tokamaks.

**Current state**: The 3.4 composite reflects a concept with **excellent scalability and availability** (C2, C6 both ~4), **acceptable modularization and customization** (C1, C5 both ~3), but **killed by unretired feasibility gates** (C7 = 2.0). The FLARE pivot has effectively frozen projectile ICF at this score — no data will be generated to retire the gates unless an independent developer (NearStar or new entrant) picks up the torch. If the gates remain unretired, the concept stays at 3.4 indefinitely. If they are retired favorably, it jumps to 3.7-3.9. If retired unfavorably (gain <100×, driver >$2B), it drops to ~2.5 (interesting physics, unviable economics).


---

### 28-hts-tokamak-full-hts: HTS Tokamak - Full HTS (Energy Singularity)

#### Section 8 Scores (from synthesis.md)

## 8. Long-Term LCOE Potential (Downselect Scoring)

### Scoring Table

| Criterion | Score | Key justification |
|-----------|-------|-------------------|
| **C1: Modularization** | **2.8** | Moderate modularization limited by tokamak integration complexity. TF coils: factory-assembled HTS modules (18 coils, mode=factory, +1.0 boost) but tight integration with vacuum vessel and PF coils requires on-site assembly. Blanket: sector-based modules with remote handling (mode=site-assembled, medium learning). Heating (ICRH): antenna arrays are stick-built / custom-fitted. BOP (turbine, power conversion): factory skids (high learning). Cost-weighted average favors on-site assembly for reactor core (CAS22 = 49% of capital), limiting modularization score. |
| **C2: Scalability** | **3.5** | Sub-linear geometric scaling within tokamak physics limits. Doubling R increases plasma volume ~8× but capital cost ~4–5× (favorable $/kW scaling, demonstrated by Scenario C→D improvement). No unit replication path (single plasma chamber). Minimum viable scale: 250–500 MWe competitive with learning-curve cost reduction; <200 MWe likely uneconomic even at NOAK (Scenario C = 164 $/MWh at 250 MWe). Geometric scaling is favorable within 200–1000 MWe range but constrained by tokamak disruption scaling (larger plasma → worse stability) and magnet field limits. Score reflects good within-family scaling but no modularity. |
| **C3: Supply Chain Learning** | **3.3** | Mixed learning potential across CAS accounts. **High learning (HTS magnets, C220103 = 33% of CAS22)**: REBCO tape has demonstrated 18–24% LR in analogous superconductor production (Bi-2223, YBCO precursors); cross-industry demand from grid-scale SMES, MRI magnets, and accelerators; current production at TRL 8 (Shanghai Superconductor commercial-scale lines operational). **Low learning (blanket, C220101 = 3% of CAS22)**: tritium breeding is fusion-unique, no external demand; ceramic breeder pebble manufacturing at TRL 4–5; labor-intensive remote assembly. **Medium learning (BOP, CAS23 = 3% of capital)**: steam turbines are mature commodity (LR ~3–5%) but fusion-specific tritium-compatible heat exchangers are novel. **High learning (heating, C220104 = 19% of CAS22)**: ICRH components share supply chain with particle accelerators, broadcast transmitters; power electronics learning analogous to grid inverters (LR ~12–15%). Weighted by CAS cost shares: (0.33×5 + 0.19×4.5 + 0.03×1 + ...) / normalizer ≈ 3.3. |
| **C4: Plant Complexity** | **2.5** | High operational complexity from tokamak integration. **Subsystem count**: 14 distinct CAS22 sub-accounts >1% of direct capital (first wall, blanket, shield, magnets, heating, divertor, vacuum, power supplies, coolant, fuel handling, tritium, I&C, radwaste, auxiliary cooling). **Coupling density**: High—magnet quench → vacuum break → plasma disruption → first-wall damage is a 4-system cascade; tritium permeation couples blanket + fuel cycle + safety + building ventilation; PF coil transients couple to plasma equilibrium + disruption mitigation + power supply stability. ~8–10 critical cross-subsystem dependencies. **Extreme-condition count**: 6 simultaneous extremes (>10 T field in TF coils, 10⁸ K plasma, cryogenic <20 K for HTS, high neutron flux >1 MW/m² at first wall, tritium chemical reactivity, ultra-high vacuum <10⁻⁶ Pa in vessel). **Novel integration count**: 3–4 first-of-kind interfaces (full-HTS CS coil at 25 T under cyclic loading + neutron flux; AI plasma control at burning-plasma conditions; HTS coil demountable joints if used for maintenance access; tritium-compatible FLiBe or LiPb coolant loop with MHD flow). Sub-scores: subsystem count = 2.0, coupling = 2.0, extremes = 1.5, novel integration = 2.5. Average = 2.0, but worse than compact mirror (score ~4) due to tokamak tight coupling. Calibration: conventional ITER-class tokamak = 1.5; compact HTS tokamak = 2.0–2.5 (fewer subsystems but higher field extremes). |
| **C5: Customization Needs** | **2.0** | High site-specific adaptation needs. **Thermal rejection**: Large steam Rankine cycle requires cooling towers with water rights and intake/discharge permitting (score 1). **Fuel safety profile**: D-T fuel with kg-scale tritium inventory, 14.1 MeV neutron activation, emergency planning zone, and fuel supply chain coordination (score 1). **Activation and waste**: High neutron flux with conventional steels (analysis does not specify low-activation materials) → long-lived activation products, interim storage requirements, site-specific waste licensing (score 2). **Seismic/civil**: Compact geometry (R=2.0m base, total tokamak mass ~2000–3000 tonnes estimated from CAS22) reduces seismic isolation complexity vs. ITER-class (score 3), but still requires custom foundation design per site geology. **Grid integration**: Steady-state operation (1,337 s HH70 record) enables constant output → standard grid interconnection with no energy storage (score 5). Sub-factor average: (1+1+2+3+5)/5 = 2.4. Calibration vs. aneutronic concepts (p-B11 FRC = 4–5) and large D-T tokamaks (ITER-class = 1.5). |
| **C6: Upper Capacity Factor** | **3.5** | **Scheduled downtime budget**: First wall/blanket replacement driven by neutron damage (assume 3 MW/m² wall loading from model → ~2–3 FPY to 20 dpa limit for EUROFER steel → replacement every 2–3 years; assume 60-day replacement with modular blanket sectors and remote handling → 60/730 FPY ≈ 8% downtime). Divertor erosion (assume 10 MW/m² peak heat flux → 1–2 FPY lifetime, 30-day replacement → 4% downtime). HTS magnet maintenance (assume no neutron-driven replacement if shielded to <1×10²² n/m² fluence over 30-year life; scheduled inspection 7 days/year → 1% downtime). Total scheduled: 13%. **Unscheduled downtime**: Disruptions are the dominant tokamak risk. Conventional tokamak: ~1 disruption per 100 shots, 1-week recovery → 3–5% downtime. AI plasma control (if effective per HH70 record) could reduce to ~1 per 1000 shots → <1% downtime (optimistic). Assume 2% unscheduled (midpoint between conventional and optimistic). Auxiliary systems (BOP): 2% (standard). Total unscheduled: 4%. **Duty cycle**: Steady-state operation (1,337 s HH70 confirmed) → duty cycle = 1.0. **CF_upper** = (1 − 0.13 − 0.04) × 1.0 = 83%. **Score mapping**: 80–90% → score 4. Penalty for unproven AI control reliability at burning plasma (conservative assumption) → score 3.5. Calibration: conventional tokamak with standard control = ~75% CF (score 3); IFE rep-rated at 10 Hz with 0.1 s burn / 0.1 s dwell = 50% duty cycle + clearing (score 2). |
| **C7: Technical Feasibility** | **3.0** | **Gate enumeration**: (1) **D-T tokamak confinement at Q>10** (degrading gate): Demonstrated at subscale (JET Q=0.67 D-T, TFTR Q=0.3); SPARC targets Q>10 but not yet achieved. If Q<10 achieved, fallback to larger machine at higher capital cost. Penalty: −0.5 × 0.5 = −0.25. (2) **Full-HTS CS coil reliability at 25 T cyclic loading** (degrading gate): Analytically supported (Jingtian test magnet 21.7 T proves field achievable, CS duty cycle modeled) but no experimental demonstration of multi-year fatigue under combined EM + neutron + gamma. Fallback: replace CS coils every 3–5 years (Scenario A: 65% availability, +22% LCOE). Penalty: −0.5 × 1.0 = −0.5. (3) **AI plasma control at burning-plasma conditions** (degrading gate): Demonstrated at subscale (HH70 experimental plasma, no fusion power, no radiation). Fallback: conventional disruption frequency (70% availability, +14% LCOE). Penalty: −0.5 × 0.5 = −0.25. (4) **Tritium breeding TBR>1.05 in undisclosed blanket** (schedule gate): No blanket design; CFETR blanket TBMs analytically predict TBR 1.1–1.3 for HCCB/WCCB; gate will pass but timeline depends on HH380 engineering (post-2030). Penalty: −0.25 × 1.0 = −0.25. (5) **25 T HTS coil quench protection and energy extraction** (schedule gate): Quench detection for REBCO at 20 K is analytically understood; HH70 26-coil system operational but at low field (2.5 T). 25 T quench energy is 10× higher; protection system is engineering (passive resistors, energy dump) with no physics blocker. Penalty: −0.25 × 0.5 = −0.125. **Total penalty**: −1.375. **C7 score** = 5 − 1.375 = **3.6** → round to **3.5**, but apply **additional −0.5 penalty for blanket design uncertainty** (no concept disclosed = elevated risk vs. CFETR analogue) → **final 3.0**. Calibration: conventional D-T tokamak (ITER-class) with no novel gates = 4.0–4.5; compact HTS tokamak (CFS SPARC-class) with TF-only HTS and I-mode confinement = 3.5–4.0; full-HTS + AI control + undisclosed blanket = 3.0. Floor rule (≥3 unretired binary gates → score 1.0) does not apply—no binary gates identified. |
| **Composite** | **3.0** | Simple average of C1–C7: (2.8 + 3.5 + 3.3 + 2.5 + 2.0 + 3.5 + 3.0) / 7 = **2.94** → **3.0** |

---

### Interpretation

**Composite score 3.0** places this concept in the **middle of the pack** for long-term LCOE potential—neither a standout cost-reduction leader nor a structural disadvantage concept.

**Strongest levers for improvement:**

1. **C3 (Supply chain learning, score 3.3)**: HTS magnet tape cost reduction is the most actionable lever. REBCO tape comprises 33% of CAS22 and has demonstrated 18–24% learning rates in analogous superconductor production. If Shanghai Superconductor scales production to 10+ commercial plants and tape cost drops from ~$50/kA-m to <$15/kA-m (3× reduction), C220103 falls by ~$400M and LCOE drops ~20 $/MWh. This is the single largest cost-reduction opportunity in the concept.

2. **C6 (Capacity factor, score 3.5)**: AI plasma control is the wild card. If HH170 demonstrates <1 disruption per 1000 shots at Q>10, availability moves from 80% to 90% and LCOE drops 10–15 $/MWh. This requires validating AI control at burning-plasma conditions—an unproven but plausible outcome given HH70's 1,337-second steady-state record.

**Weakest levers (hardest to improve):**

1. **C5 (Customization, score 2.0)**: D-T fuel cycle and steam Rankine thermal rejection create irreducible site-specific adaptation needs. Tritium licensing, cooling water permitting, and activated waste management are structural constraints that cannot be engineered away. This score will not improve unless Energy Singularity pivots to advanced fuel (D-D or aneutronic) or direct energy conversion—neither is on the roadmap.

2. **C4 (Complexity, score 2.5)**: Tokamak subsystem coupling density is inherent to the architecture. Full-HTS coil scope adds CS fatigue risk; AI control adds software/sensor complexity. Unlike modular concepts (IFE, mirrors), tokamaks resist decomposition into independent subsystems. Incremental improvements possible (better disruption mitigation, passive safety systems) but score unlikely to exceed 3.0.

**What would need to change to materially raise the score:**

- **+0.5 on C3** (to 3.8): REBCO tape cost reaches <$15/kA-m with multi-GW fusion deployment demand pull from China's domestic market. Requires 10+ commercial plants and supply chain scale-up by Shanghai Superconductor and competitors. Timeline: 2035–2040 if HH380 succeeds and China commits to fusion fleet.

- **+0.5 on C6** (to 4.0): AI plasma control validated at burning plasma with 90%+ availability demonstrated over multi-year HH380 operation. Requires HH170 disruption statistics (2027+) and HH380 operational track record (2035+). If achieved, Energy Singularity becomes the availability leader in tokamaks.

- **+0.3 on C7** (to 3.3): Full-HTS CS coil reliability demonstrated over 5+ years of HH170/HH380 operation with no fatigue-driven replacements. Retires the degrading gate #2 from analytically supported to demonstrated at subscale, reducing penalty from −0.5 to −0.25.

**Net composite improvement potential**: +0.5 (C3) + 0.5 (C6) + 0.3 (C7) = **+1.3 points → composite 4.3** if all three levers hit optimistic targets. This would place the concept in the upper tier of D-T tokamaks for long-term cost potential, competitive with or exceeding CFS ARC/SPARC (estimated composite 4.0–4.5 based on similar architecture but fewer novel technical bets). However, achieving this requires successful validation of both AI control and full-HTS CS reliability—two genuinely uncertain technical bets—plus supply chain scale-up that depends on Chinese government fusion deployment policy.

**Downside scenario**: If AI control fails to improve availability (C6 → 2.5, −1.0) and CS coils require replacement every 3 years (C7 → 2.5, −0.5), composite falls to **1.5–2.0**, making the concept a high-complexity, high-customization D-T tokamak with no cost-reduction advantages over conventional large tokamaks. LCOE in this scenario (Scenario A × worst-case supply chain) exceeds 150 $/MWh and the concept is non-competitive.

**Bottom line**: This concept's long-term LCOE potential hinges on two technical bets (AI control, full-HTS CS coils) and one supply chain bet (REBCO tape cost reduction). If all three succeed, it's a top-tier compact tokamak. If any one fails, it's middle-of-pack. If two or more fail, it's a cost-disadvantaged architecture. The 3.0 composite score reflects this genuine uncertainty—neither bullish nor bearish, pending validation over the next 5–10 years.



---

Write your calibration report to: `{{output_path}}`
