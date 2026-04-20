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
