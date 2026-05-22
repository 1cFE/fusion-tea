# Fusion Concept Scoring Framework

This framework defines eight criteria (C1-C8) for evaluating the long-term LCOE
reduction potential and technical feasibility of fusion concepts. Claude scores
C1, C3, C4, C5, C8 and fills the C7 risk matrix. Python computes C2, C6, and C7.

**All scores use a 1-5 scale where 5 = most favorable.**

---

## C1: Modularization (scored by Claude)

How much of the plant can be factory-manufactured as standardized, repeatable modules.

**Sub-factors:**

1. **Construction mode classification per CAS account** — For each major CAS account
   (CAS21-CAS27 at minimum), classify the construction mode:
   - Factory-manufactured module (score 5)
   - Site-assembled from factory sub-assemblies (score 3)
   - Stick-built / field-erected (score 1)

2. **Module repetition boost** — If 10-49 identical modules per plant: +1.0 to the
   cost-weighted average. Diminishing returns above 49 units.

**Computation:** C1 = cost-weighted average of mode scores + module repetition boost,
clamped to [1, 5].

Provide per-CAS mode classifications and the resulting weighted average in your
justification.

---

## C2: Scalability (DO NOT SCORE — assigned by Python)

Deterministic lookup based on confinement type. Claude does NOT score this criterion.

Reference table (for context only):
| Category | Score | Concepts |
|----------|-------|----------|
| Conventional Tokamak | 2.5 | 01, 21, 28, 29, 33, 34 |
| Stellarator | 2.5 | 05, 09, 10, 20a, 20b, 36 |
| Mirror | 3.5 | 06, 11 |
| FRC / Compact Pulsed MFE | 3.5 | 08, 15, 18 |
| Laser IFE | 3.5 | 03, 04, 17a, 17b, 26, 30, 31, 32 |
| Pulsed MIF (liner/target) | 3.0 | 07, 14, 22 |
| Levitated Dipole | 2.0 | 12, 19 |
| Exotic/Novel | 4.0 | 02, 13, 16, 24, 25, 27, 35 |

---

## C3: Supply Chain Learning (scored by Claude)

Three equally-weighted sub-factors:

### Sub-factor A: Component learning rates (1-5)
Cost-weighted average across CAS accounts. For each major cost component, estimate
the learning rate category:
- 5 = Commodity component with established manufacturing (e.g., steel structures, pumps)
- 4 = Industrial component with growing production base (e.g., standard superconducting wire)
- 3 = Specialty component with limited but existing supply chain (e.g., beryllium multiplier)
- 2 = Fusion-specific component with no current market (e.g., breeding blanket modules)
- 1 = Novel material or component never manufactured at scale

### Sub-factor B: Supply chain bottleneck count (1-5)
Start at 5.0 and subtract penalties:
- Hard constraint (no known path to required quantity): -1.0 each
- Scaling constraint (exists but must scale 10x+): -0.5 each
- Sole-source dependency: -0.25 each
- Helium-3 fuel dependency: -1.5

Clamp to [1, 5].

### Sub-factor C: External demand pull (1-5)
What fraction of capital cost is in components with >$1B/yr external market?
- >60%: score 5
- 40-60%: score 4
- 20-40%: score 3
- 10-20%: score 2
- <10%: score 1

**C3 = (A + B + C) / 3**

---

## C4: Plant Complexity (scored by Claude)

Equally-weighted sub-factors:

### Sub-factor A: Operational coupling density (1-5)
Rate failure cascades and maintenance dependencies. Focus on OPERATIONAL coupling
(if component X fails, what else stops working?) — NOT physics coupling chains.

- 5 = Highly decoupled; subsystems can be maintained independently
- 4 = Mostly decoupled; few critical interdependencies
- 3 = Moderate coupling; several failure cascade paths
- 2 = Highly coupled; many maintenance dependencies
- 1 = Extreme coupling; single-point failures cascade to full plant shutdown

### Sub-factor B: Subsystem count (1-5)
Count CAS22 sub-accounts that represent >1% of total capital:
- 5 = Fewer than 5 significant subsystems
- 4 = 5-7 significant subsystems
- 3 = 8-10 significant subsystems
- 2 = 11-14 significant subsystems
- 1 = 15+ significant subsystems

**"Magic wand" test:** If the physics were proven tomorrow, would this plant still
be hard to build and operate? If the answer is NO, the complexity belongs in C7
(Technical Risk), not C4.

**C4 = (A + B) / 2**

---

## C5: Customization Needs (scored by Claude)

Equally-weighted sub-factors:

### Sub-factor A: Thermal rejection (1-4)
- 4 = No thermal cycle or air-cooled (e.g., direct energy conversion only)
- 3 = Hybrid power conversion (partial DEC + partial thermal)
- 2 = Large cooling towers required (standard thermal cycle)
- 1 = Exceptional thermal rejection needs (multiple cooling systems)

### Sub-factor B: Fuel safety profile (1-4)
- 4 = p-B11 (aneutronic, no tritium)
- 3 = D-He3 (low neutron fraction, no tritium breeding)
- 2 = D-D (neutrons but no tritium handling)
- 1 = D-T (full tritium handling and breeding infrastructure)

**IMPORTANT:** Site-specific advantages (named sites, brownfield reuse, proximity
to water) must NOT inflate C5. Score only the intrinsic concept characteristics.

**C5 = (A + B) / 2**, then scale to [1, 5] range: C5 = 1 + (raw - 1) * (4/3)

---

## C6: Upper Capacity Factor (DO NOT SCORE — assigned by Python)

Deterministic lookup based on fuel type and operation mode. Claude does NOT score
this criterion.

Reference table (for context only):
| Fuel | Steady-State | Pulsed |
|------|-------------|--------|
| D-T | 2.5 | 2.0 |
| D-D | 3.5 | 3.0 |
| D-He3 | 4.0 | 3.5 |
| p-B11 | 4.5 | 4.0 |

Pulsed penalty is a flat -0.5 across all fuel types.

---

## C7: Technical Risk Evidence (risk matrix scored by Claude, C7 computed by Python)

Claude fills a **7-function x 2-subcategory = 14-cell risk matrix**. Python then
computes C7 from the function-level means.

### 7 Functions

1. **Plasma Performance** — Density, temperature, confinement sufficient for net energy gain
2. **Driver / Energy Input** — Heating, compression, or catalytic species delivery
3. **Instability Control** — Suppression or tolerance of intrinsic plasma instabilities
4. **Plasma-Wall Interaction** — Erosion, heat flux management, surface damage
5. **Neutron/Particle Handling** — Activation, shielding, displacement damage
6. **Fuel Cycle Closure** — Breeding, extraction, purification, recycling
7. **Power Conversion & BOP** — Technical risk of the energy conversion scheme.
   This category primarily captures risk from **novel direct energy conversion (DEC)**
   methods (magnetic expansion, charged-particle collection, MHD, inductive coupling,
   photovoltaic conversion of bremsstrahlung, etc.). Conventional thermal cycles
   (Rankine, Brayton, sCO₂) are mature analogues — score them at the operating-regime
   tier their cycle has demonstrated commercially, regardless of the fusion concept
   coupling to them. Score concepts that rely on novel DEC against the demonstrated
   regime of that specific DEC method, not against thermal-cycle baselines.

### 2 Subcategories per function

- **Physics risk** — Scaling, regime extrapolation, cross-section uncertainty
- **Hardware risk** — Materials AND engineering risks combined. Must name specific
  materials AND components with quantitative limits.

**AVOID DOUBLE COUNTING RISKS** between physics and hardware subcategories.

### Per-cell fields (all required)

For each of the 14 cells, provide:

| Field | Description |
|-------|-------------|
| Plant requirement | Quantitative target the commercial plant must achieve |
| Best demonstrated | Cited experimental result, or "never demonstrated" |
| Gap ratio | requirement / demonstrated (or "N/A" if never demonstrated) |
| Closure mechanism | How the proponent claims to close the gap |
| Classification | **Binary** (zero net electricity if unmitigated) or **Degrading** (worse economics) |
| Evidence tier | 1-5 scale (see below) |

### Evidence tier scale

Tiers are anchored to **actual operation**, not design status. Paper designs,
preliminary design reviews (PDRs), and conceptual studies do **not** themselves
move evidence above tier 2 — only operating hardware does. Apply this rule
uniformly across concepts: ITER, GT-MHR, sCO₂ pilot scale-up plans, and
sub-2 GeV muon-cost projections all count as tier 2 until the corresponding
system actually operates in the relevant regime.

| Tier | Definition | Examples |
|------|------------|----------|
| 5 | **Operating-regime demonstrated at commercial scale** in the same fuel / temperature / pressure / neutron flux / duty cycle as the plant requirement. The cited demonstration must be operating hardware (current or historical), not a design. | Commercial steam Rankine cycle for thermal-cycle BOP at 100+ MWe; PWR pressure-vessel steel for ~40 dpa over decades; HV electrical switchyard equipment. |
| 4 | **Near-regime demonstrated** — operated at ≥50% of the plant requirement OR transiently at full scale. Extrapolation from demonstrated operation must be ≤2× on the limiting parameter. | JET D-T plasma performance (transient, near-scale) cited for steady-state D-T tokamaks; ITER tungsten divertor mock-ups qualified at full heat flux for short cycles; W7-X long-pulse stellarator plasmas cited for steady-state stellarators. |
| 3 | **Subscale or partial demonstration** — operated at <50% of the plant requirement, or operated at full scale in an *adjacent* environment (different fuel/coolant but same physics regime). | TFTR/JET D-T at <1 MW/m² wall loading cited for 2 MW/m² compact STs (4× gap); MSRE FLiBe operation at 650°C cited for 900–1200°C fusion HX (~2× temperature gap, fission neutron spectrum); sCO₂ Brayton at 10 MWe pilots cited for 200 MWe commercial. |
| 2 | **Simulation, design study, or non-adjacent analogue** — paper designs, MCNP/Serpent neutronics, scaling laws, or analogues in a meaningfully different environment (different fuel, very different flux/temperature, fission vs. fusion). | ITER tritium plant cited before ITER operates; GT-MHR design cited as evidence; ARIES/STEP studies; computational TBR predictions; fission-reactor sodium-loop steam generators cited for fusion Li/PbLi; ENDF/B cross-section libraries for unbuilt geometries. |
| 1 | **Asserted, absent, or novel** — no demonstrated analogue, no experimental basis, or company claim without supporting publication. | "γ = 0.1 in polywell" with no measurement; muon-cost projection below current TRIUMF/RIKEN demonstrated values; novel DEC scheme with no operating prototype; "we will use advanced materials" without naming specific tested candidates. |

**Required citation format**: every tier ≥3 score must name the specific
experiment/facility/operating regime cited (e.g., "JET 1997 D-T at 11 MW peak,"
"WEST 1000+ tungsten-divertor pulses at 5 MW/m²"). Generic phrases like "tokamak
analogues" or "ITER design" without the operating-regime qualifier default to
tier 2.

**Adjacent-environment rule** (for tier 3): an analogue is "adjacent" only if it
shares the limiting physics or materials regime. Fission steel under fast-spectrum
neutrons is adjacent to fusion steel under 14 MeV neutrons (similar dpa, different
He production); commercial Rankine cycle is adjacent to fusion FLiBe-Rankine HX
(same thermodynamics, different chemistry). When uncertain, default to tier 2.

### Mandatory binary classifications (cannot be overridden)

These risks are ALWAYS classified as **binary**, regardless of claimed mitigation:
- TBR < 1.0 for any D-T concept
- Tritium extraction failure
- He-3 self-breeding at scale
- He-3 extraction/purification
- External tritium or He-3 purchase is NOT a valid fallback for reclassification

### Anti-leniency rule

When evidence is absent or limited to non-peer-reviewed sources for a cell, score
it at Tier 1-2. Do NOT infer favorable performance from silence. "No data" means
Tier 1 (asserted/absent), not Tier 3 (partial demonstration). The burden of evidence
is on the concept to demonstrate capability, not on the scorer to assume it.

### Heritage credit (D-T fuel only)

Apply a heritage credit to concepts with good traceability to previous public fusion
experiments or mature reactor designs. The heritage credit provides a FLOOR on
**all seven function scores (F1–F7)** — it overrides any F_n score only if the
computed value falls below the floor.

The rationale: heritage doesn't only help with plasma physics. A tokamak-lineage
concept inherits decades of engineering work on divertors (F4), neutron-handling
materials (F5), tritium fuel cycles (F6), and steam-cycle BOP integration (F7).
A muon-catalyzed concept gets no such inheritance for its compact-cell engineering.
Applying the floor only to F1–F3 systematically rewards less-mature concepts that
cite generic analogues for their back-half (F4–F7) without the corresponding
heritage debt.

| Heritage lineage | Floor (F1–F7) |
|-----------------|---------------|
| Tokamak (ITER, JET, EAST, etc.) | 4.0 |
| Stellarator (W7X, LHD, HSX, TJ-II, etc.) | 4.0 |
| Laser IFE (HYLIFE, NIF, etc.) | 3.5 |
| Mirror (MFTF, TMX) | 2.5 |
| FRC | 2.5 |
| Spherical Tokamak (STEP) | 3.0 |
| Z-pinch (ZETA) | 2.5 |
| magLIF (Sandia Z-machine) | 3.0 |

**Heritage credit only applies to D-T fuel.** Alternate fuels get no heritage credit.

### Function-level means

After filling all 14 cells, compute the function-level mean as the **symmetric
arithmetic mean** of the two subcategory tiers:

```
F_n = (Physics_tier + Hardware_tier) / 2
```

Do NOT use cost-weighted averages, "weighted toward" the higher-uncertainty
subcategory, capital-share weighting, or any other aggregation method within a
function. Round each F_n to the nearest 0.5 and report as F1 through F7.

If you believe one subcategory should dominate, raise that subcategory's *tier*
in the cell itself (with explicit evidence), not by weighting the mean.

### C7 computation (done by Python, not Claude)

1. Read F1-F7 function-level means from the YAML block
2. Apply heritage credit floor to **all of F1-F7** (D-T concepts only)
3. C7 = mean of F1-F7 (after heritage), rounded to nearest 0.5
4. Function-level cap: if any function mean <= 1.5 (after heritage), C7 is capped
   at that function's actual value

---

## Standard LCOE Modeling Parameters

These canonical values **must** be used in `model_setup.py` for every concept,
unless concept-specific evidence justifies a deviation. **Document any deviation
explicitly** in the model file and in synthesis Section 2 (Modeling Approach),
including the source of the alternative value.

### Energy capture efficiencies (η_th, η_de)

costingfe's physics layer distinguishes two efficiency channels and adds them:

```
p_the = eta_th * p_th                  # thermal-cycle heat load → electric
p_dee = f_dec * eta_de * p_transport   # DEC end-loss channel → electric
p_et  = p_the + p_dee                  # total useful electric power
```

The canonical lookup therefore returns a **(η_th, η_de) pair** per Energy Capture
category — η_th is the thermal-cycle efficiency only (NOT an overall plant
efficiency); η_de is the DEC channel efficiency. Conflating them under a single
value (the pre-2026-05 shape) double-counted the DEC contribution and silently
under-stated LCOE for hybrid and direct concepts by 1-31%. See
[issue #30](https://github.com/1cFE/fusion-tea/issues/30) and
`.project/active/eta_th-double-count-fix/` for the fix details.

| Energy Capture (per `table.csv`) | Canonical (η_th, η_de) | Reasoning |
|----------------------------------|-------------------------|-----------|
| Thermal (steam) | (0.35, 0.0) | Superheated-steam Rankine; no DEC channel |
| Thermal (sCO₂) | (0.48, 0.0) | High-T closed-loop Brayton; no DEC channel |
| Thermal (unspecified) | (0.35, 0.0) | Default to superheated steam; no DEC channel |
| Hybrid (thermal + direct) | (0.35, 0.54) | Steam cycle on neutrons/wall load + MARS-class gridless DEC on charged-particle end loss |
| Direct (inductive) | (0.0, 0.85) | Helion-style compressed-FRC EM recovery; no thermal cycle |
| Direct (charged particle) | (0.0, 0.70) | TAE ICC, mirror DEC, alpha collection; no thermal cycle |
| TBD / Unknown | (0.35, 0.0) | Default to superheated steam |

**Removed categories** (no longer in `table.csv`, no canonical defined):
`Thermal (steam) saturated`, `Thermal (steam) superheated`, `Thermal (steam) supercritical`,
`Thermal (helium Brayton)`, `Thermal (combined cycle)`, `Pulsed power implosion`,
`Projectile impact`. If a concept lands in `table.csv` with one of these labels, decide
whether to fold it into one of the canonical-table rows above or to add a new row here.

**Justified deviations**: A concept may use a non-canonical (η_th, η_de) pair —
**on either axis independently** — when one of the following holds:
- (a) The underlying physics forces a derating on one channel only. Worked
  example: `06-magnetic-mirror` is Direct (charged particle), canonical
  `(0.0, 0.70)`. Bremsstrahlung is partially absorbed by walls and contributes
  thermally (~15-25% of fusion power), so the concept legitimately raises
  η_th above zero (`eta_th=0.20`) while keeping η_de canonical. The model
  file annotates the η_th line with `# DEVIATION:` and cites both
  `scoring_framework.md §"Justified deviations"` and the original physics
  derivation (`feedback_eta_th/06-magnetic-mirror.md §F-1`).
- (b) The concept's published design specifies a specific cycle parameter
  from peer-reviewed sources (e.g. an MARS-class gridless DEC measurement
  citing 0.54 from `MARS 1983` for a concept that explicitly uses MARS as a
  point of comparison).

In both cases, the model file must mark the deviating line with
`# DEVIATION: <one-line rationale>. Source: <file/url>. Canonical: <axis>=<value>.`
The `# DEVIATION:` annotation is detected by the standardization script and is
the only thing that protects the line from being rewritten to the canonical.
Deviations on η_th do not affect standardization of η_de on the same file
(and vice versa) — the regex passes are independent.

### Plant availability

Look up the canonical availability for the concept's operating-mode category
(combine the `Confinement Family` and `Operation Mode` columns from `table.csv`):

| Operating-mode category (D-T fuel) | Canonical availability | Reasoning |
|------------------------------------|------------------------|-----------|
| MCF — steady-state or quasi-steady (tokamak, stellarator, mirror, ST, FRC steady) | **0.85** | Midpoint of Araiinejad & Shirvan (2025) 75–90% commercial-target band for D-T MCF |
| Pulsed MCF — short pulses, no quasi-steady claim | 0.75 | Pulse + dwell + recharge floor |
| Pulsed IFE — rep-rated laser / heavy-ion / direct or indirect drive | 0.75 | Shot-rate × target-factory × optics-maintenance composite |
| Pulsed MIF — mechanical compression, MagLIF-class | 0.75 | Mechanical-system MTBF dominates duty cycle |
| Single-shot demo (NIF-class) | use sourced value, flag non-commensurable | These are not commercial plants; their reported availability is not directly comparable to commercial targets |
| D-D / D-³He / p-¹¹B | 0.85 | Same MCF basis; no fuel-specific operations data in literature yet |

**Justified deviations**: A concept may use a non-canonical availability **only**
when its own design literature (peer-reviewed paper, company technical
disclosure, or comparable external publication) commits to a specific
availability number with an articulated basis (e.g., maintenance schedule,
duty-cycle calculation). Author-reasoned values within a published range, or
midpoint picks within a band, are **not** sufficient — they must move to the
canonical value. In the deviation case, the `model_setup.py` comment must:

1. Quote or paraphrase the externally-published number
2. Name the source (paper, slide deck, company technical report)
3. State the basis the source gives (e.g., "biennial 84-day maintenance cycle")

Examples of *accepted* deviations:
- `05-planar-coil-stellarator` / `10-large-scale-stellarator` — Helios/Thea
  Energy published **88%** with biennial 84-day maintenance cycle.
- `20b-renaissance` — Renaissance Fusion disclosed **92%** target (flagged uncertain).

Examples of *not-accepted* deviations (must move to canonical):
- "Mid-range of published 80–85% band" without a specific cited target.
- "Conservative central estimate" without external publication of that estimate.
- Citing only the Araiinejad & Shirvan range without a concept-specific commitment.

### Blanket energy multiplication (mn)

Look up the canonical blanket energy multiplication factor for the concept's fuel:

| Fuel | Canonical `mn` | Reasoning |
|------|----------------|-----------|
| D-T  | **1.1** | costingfe framework default for a generic Li-bearing blanket without a dedicated neutron multiplier |
| D-D / D-³He / p-¹¹B | not standardized | concept-specific; cite per design |

Unlike η_th and availability, `mn` is not a free policy lever — it is a function of the blanket technology chosen. The canonical here is the framework default. Concepts that specify a particular blanket design (HCPB+Be, FLiBe with a stated TBR, etc.) will legitimately differ.

**Justified deviations**: A concept may use a non-canonical `mn` **only** when one of the following holds:

1. The model specifies a named blanket technology with a published multiplication factor (e.g., HCPB+Be reported in the EU-DEMO HCPB design literature; FLiBe with a stated TBR from a peer-reviewed neutronics study).
2. The model has a physics-coupling argument that requires a non-default value (e.g., the Li exothermic boost is already embedded in `eta_th`, so `mn` must drop to 1.0 to avoid double-counting).

Author-guessed values without a blanket-technology cite must move to canonical. The `model_setup.py` comment must:

1. Name the blanket technology or physics argument
2. Cite the source (paper, design report, in-repo derivation)
3. State the value the source gives (or, for coupling arguments, the equation being avoided)

Examples of *accepted* deviations:
- `20b-renaissance` — `mn=1.07`, JNM 599 (2024) blanket-design source.
- `29-negative-triangularity-tokamak` — `mn=1.11`, MANTA FLiBe TBR=1.15 design (`manta-reference-design.md` §5.1).
- `31-laser-icf-oec` — `mn=1.0`, physics-coupling: Li boost already embedded in `eta_th` upstream of the framework call.

### Plant lifetime (`lifetime_yr`)

Look up the canonical plant lifetime:

| Concept scope | Canonical `lifetime_yr` | Reasoning |
|---------------|-------------------------|-----------|
| All D-T concepts | **30 yr** | Standard commercial-plant finance / depreciation horizon; consistent with the WACC-based LCOE convention used across the framework |

Plant lifetime drives the annualization of overnight capital cost (Fixed Charge Rate ∝ 1/lifetime in the limit of zero discount). A 30→40 yr extension reduces capital-driven LCOE by ~10–15%, so the choice is LCOE-material and must be defensible.

**Justified deviations**: A concept may use a non-canonical `lifetime_yr` **only** when its own published design literature commits to a specific plant or major-component (magnet, vacuum vessel, blanket structure) design life with a stated basis. Author-judged values, conservative round numbers, or "standard fusion plant assumption" without a citation are **not** sufficient.

The `model_setup.py` comment must:

1. Quote or paraphrase the externally-published design-life number
2. Name the source (paper, slide deck, company technical report)
3. State the component scope (magnet, VV, plant) the source commits to

Examples of *accepted* deviations:
- `05-planar-coil-stellarator` — `lifetime_yr=40`, Helios/Thea Energy QA stellarator preconceptual design: "Magnet design lifetime: 40+ years".
- `10-large-scale-stellarator` — `lifetime_yr=40`, Gauss Fusion GIGA technical summary: "Magnet and vacuum vessel design life: 40 years".

### Why standardize

Cross-concept LCOE comparisons are only meaningful when all concepts in the
same conversion category use the same η_th and the same availability. A 0.32
vs. 0.46 spread within "steam Rankine" produces a 30–40% LCOE difference for
identical fusion power. A 0.75 vs. 0.88 availability spread is similarly
LCOE-driving (LCOE scales as 1/availability for capital-dominated concepts).
Use the canonical values to isolate the architectural signal; sensitivity-sweep
when an availability question is the focus of the analysis.

### Helpers

The Python helpers in `lib.canonical_params` return canonical values for the
strings that appear in `table.csv`. Import them in `model_setup.py`:

```python
from lib.canonical_params import (
    canonical_eta_th, canonical_eta_de, canonical_availability, canonical_mn, canonical_lifetime_yr,
)
ETA_TH       = canonical_eta_th("Thermal (steam)")                   # → 0.35  (thermal-cycle only)
ETA_DE       = canonical_eta_de("Thermal (steam)")                   # → 0.0   (no DEC channel)
# Hybrid example — both axes nonzero:
ETA_TH_H     = canonical_eta_th("Hybrid (thermal + direct)")         # → 0.35
ETA_DE_H     = canonical_eta_de("Hybrid (thermal + direct)")         # → 0.54
# Direct (charged particle) example — DEC carries the entire useful-electric channel:
ETA_TH_D     = canonical_eta_th("Direct (charged particle)")         # → 0.0
ETA_DE_D     = canonical_eta_de("Direct (charged particle)")         # → 0.70
AVAILABILITY = canonical_availability("MCF", "Steady-state", "D-T")  # → 0.85
MN           = canonical_mn("D-T")                                   # → 1.1
LIFETIME_YR  = canonical_lifetime_yr("D-T")                          # → 30.0
```

`canonical_availability(confinement_family, operation_mode, fuel)` accepts the
`Confinement Family`, `Operation Mode`, and `Fuel` columns directly from
`table.csv` (case- and whitespace-insensitive).

---

## C8: Data Adequacy (scored by Claude)

Four equally-weighted sub-factors:

### Sub-factor A: Source diversity & independence (1-5)
- 5 = Multiple independent public-domain sources (academic papers, government reports)
- 4 = Mix of independent and company sources with public peer review
- 3 = Primarily company publications with some independent validation
- 2 = Almost exclusively company publications
- 1 = No public-domain architecture literature available

Must survey public-domain architecture literature, not just company publications.

### Sub-factor B: Reactor design specification (1-5)
- 5 = Complete plant design with detailed engineering specifications
- 4 = Comprehensive conceptual design with major subsystems specified
- 3 = Partial design with key subsystems defined but gaps in integration
- 2 = Preliminary design with significant specification gaps
- 1 = No reactor design beyond basic concept description

### Sub-factor C: LCOE parameter coverage (1-5)
Based on blocking gap count from the concept's **gap_report.md**:
- 5 = 0 blocking gaps — all LCOE-critical parameters have data
- 4 = 1-2 blocking gaps
- 3 = 3-4 blocking gaps
- 2 = 5-7 blocking gaps
- 1 = 8+ blocking gaps or no gap report available

### Sub-factor D: Commercialization pathway clarity (1-5)
- 5 = Detailed commercialization plan with milestones, funding, and timeline
- 4 = Clear pathway with identified steps but some gaps
- 3 = General pathway described but lacking specifics
- 2 = Vague or aspirational commercialization narrative
- 1 = No commercialization pathway articulated

**C8 = (A + B + C + D) / 4**

---

## YAML Output Block Format

At the end of Section 8, include a YAML block with the following exact format.
Include ONLY the scores listed below — C2, C6, and C7 are computed by Python
and must NOT appear in this block.

```yaml
---
scores:
  C1: X.X
  C3: X.X
  C4: X.X
  C5: X.X
  C8: X.X
  F1: X.X
  F2: X.X
  F3: X.X
  F4: X.X
  F5: X.X
  F6: X.X
  F7: X.X
  binary_risks:
    - "description of binary risk 1"
    - "description of binary risk 2"
---
```

All numeric scores must be rounded to one decimal place. The binary_risks list
must include every risk classified as "binary" in the risk matrix.
