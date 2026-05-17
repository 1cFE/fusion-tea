# Synthesis: Laser ICF (p-B11)

You are producing an editorial synthesis for the fusion concept **Laser ICF (p-B11)**
(hb11). Your role is to INTERPRET, JUDGE, and PRIORITIZE — not to document.

The underlying analysis has been reviewed and verified. You may trust its factual
claims. Your job is to synthesize them into decision-support guidance.

## Required Reading

### 1. Reviewed Analysis
`C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\analysis.md`

### 2. Model Setup and Output

`C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\model_setup.py`


Model output (user-generated): `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\model_output.txt`


### 3. Approved Prior Syntheses
- `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\22-spherical-tokamak-hts\synthesis.md`

## Writing Instructions

### Voice and Style
- **Be opinionated.** State what you think, not just what the data shows.
- **Be direct.** "This concept is unlikely to achieve commercial LCOE" is better
  than "There are significant uncertainties regarding commercial viability."
- **Quantify.** "Eliminates ~20% of direct capital" is better than "Significantly
  reduces capital cost."
- **Use model output.** Reference specific LCOE numbers, CAS breakdowns, and
  sensitivity elasticities from the model setup.

### Mandatory Sections

Write to: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\synthesis_body.md`

#### 1. Executive Summary (3-5 bullets)
- The single most important risk
- The single most important advantage
- LCOE ballpark from the model (or "no model available" with reasoning)
- Confidence verdict: High / Medium / Low with one-sentence justification

#### 2. What Matters Most for LCOE
Rank the top 3-5 parameters by LCOE sensitivity. For each:
- The assumed value and its source
- The sensitivity magnitude (elasticity from model, or qualitative if no model)
- What change in this parameter would flip the economic conclusion

#### 3. Risk Verdicts
For each major challenge from the analysis Section 2:
- **Verdict:** Likely resolvable | Unlikely resolvable | Genuinely uncertain
- **Rationale:** One sentence
- **What would retire this risk:** Specific evidence or milestone

#### 4. Structural Advantages and Disadvantages
Compare against the conventional D-T tokamak cost structure baseline.
Quantify eliminated or added cost items where possible.

#### 5. Cross-Concept Positioning
Where does this concept sit in the landscape? What concepts share similar
economics? What makes this one fundamentally different?

#### 6. Modeling Confidence
Rate: High / Medium / Low
- How many parameters are data-anchored vs. speculative?
- What is the dominant source of LCOE uncertainty?

#### 7. What Would Change My Mind
2-3 specific future developments or data releases that would materially
change the LCOE estimate (in either direction).

#### 8. LCOE Downselect Scoring

Score this concept using the scoring framework below. You score C1, C3, C4, C5,
and C8. You also fill the C7 risk matrix (7 functions x 2 subcategories = 14 cells).

**You do NOT score C2, C6, or C7.** These are computed deterministically by Python.
Do not include them in your score table or YAML block.

For each scored criterion, provide:
- The **score** (1-5, where 5 = most favorable)
- **Sub-scores** where the framework defines them
- **2-3 sentences of justification** citing specific data from the analysis,
  model output, CAS breakdown, or gap report. Do not score without evidence.

**Do not double-count between criteria.** C4 measures operational complexity of
the built plant, not physics feasibility. C7 is the sole place where "this might
not work at all" is scored.

Present C1, C3, C4, C5, C8 as a table with sub-factor breakdowns, then fill the
complete 7-function x 2-subcategory risk matrix with all required per-cell fields.
Report function-level means (F1-F7). End with the YAML scores block.

### Gap Report

`C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\gap_report.md`


### Scoring Framework

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

### Thermal-to-electric conversion efficiency (η_th)

Look up the canonical η_th for the concept's energy-capture category:

| Energy Capture (per `table.csv`) | Canonical η_th | Reasoning |
|----------------------------------|----------------|-----------|
| Thermal (steam) — saturated cycle | 0.32 | Coal-plant baseline; modest temperature |
| Thermal (steam) — superheated, ≤500°C | 0.35 | Standard fusion baseline (most concepts) |
| Thermal (steam) — supercritical, ~600°C | 0.42 | ARC-class advanced steam |
| Thermal (sCO₂ Brayton) | 0.48 | High-T closed-loop, demonstrated 10 MWe pilots |
| Thermal (helium Brayton) | 0.45 | GT-MHR-class design point |
| Thermal (combined cycle, Brayton-Rankine) | 0.50 | Best thermal achievable |
| Thermal (unspecified) | 0.35 | Default to superheated steam unless concept specifies |
| Hybrid (thermal + direct) | 0.55 | Partial DEC; partial thermal |
| Direct (inductive / EM compression) | 0.85 | Helion-style compressed-FRC EM recovery |
| Direct (charged particle, ICC, alpha collection) | 0.70 | TAE ICC, mirror DEC; patent-stage but consistent target |
| Pulsed power implosion | 0.30 | Inertial pulse loss; conservative |
| Projectile impact | 0.30 | Same |
| TBD / Unknown | 0.35 | Default to superheated steam |

**Justified deviations**: A concept may use a non-canonical η_th if (a) the
underlying physics forces derating (e.g. a p-B11 plasma whose bremsstrahlung
heat is partially absorbed by walls and contributes thermally — 06-magnetic-mirror's
η_th=0.20 reflects this), or (b) the concept's published design specifies a
specific cycle parameter from peer-reviewed sources. In both cases, the model
file must include a comment identifying the deviation, the source, and the
deviation magnitude vs. the canonical value.

### Why standardize

Cross-concept LCOE comparisons are only meaningful when all concepts in the
same conversion category use the same η_th. A 0.32 vs. 0.46 spread within
"steam Rankine" produces a 30–40% LCOE difference for identical fusion power —
swamping legitimate architectural advantages between concepts. Use the canonical
value to isolate the architectural signal.

### Helper

The Python helper `lib.scoring.canonical_eta_th(energy_capture)` returns the
canonical value for a given energy-capture string (matching the `table.csv`
column). Import it in `model_setup.py`:

```python
from lib.scoring import canonical_eta_th
ETA_TH = canonical_eta_th("Thermal (steam)")  # → 0.35
```

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

