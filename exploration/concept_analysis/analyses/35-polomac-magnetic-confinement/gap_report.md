# Gap Assessment: PoloMac Magnetic Confinement

## Overall Readiness
**Rating**: Insufficient Data

**Summary**: PoloMac (Deutelio) is a pre-prototype concept with an extremely thin published record — two technical papers (available only as abstract-level summaries in Phase 1a), a startup company profile, and competition materials. The source documents contain no cost data, no plant study, no heating or power conversion specifications, and no performance validation. A D1+ analysis is possible only as a highly speculative, analogy-driven exercise with most parameters flagged as unknown or assumed. The quantitative LCOE model required for D1+ would rest almost entirely on assumptions borrowed from other MFE concepts with no concept-specific grounding.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Poor

**Available**:
- *Elio 2014 FED*: Foundational physics paper — basic geometry (dipole radius 5.4 m, plasma volume ~1300 m³), beta 20-30%, B-field 1.4–1.8 T, steady-state operation. Available only as an abstract-level summary; full paper content was not extracted.
- *2024 JTSP paper*: Updated concept description — magnetic tunnels, revised beta claim (70-80%), D-T and D-D operating regimes, prototype specs (0.2-0.3 T copper coils). Again, summary-level only.
- *Deutelio company profile*: Development roadmap, team, seed round stage, Innosuisse support, 2030 energy vision.
- *Boldbrain 2024*: Placement (4th), prize (10,000 CHF) — no technical content.
- *Fusion company tier list*: Rated C− (kunimune.blog 2024) — editorial only.

**Missing**:
- Full text of either technical paper (full methodology, assumptions, derivations)
- Any plant study or reactor design study
- Any peer-reviewed or independent validation of the concept
- Conference presentations, poster materials, or preprints beyond the two papers

**Gaps**:
- Full paper content for 2014 FED and 2024 JTSP — `not-yet-sourced` — **blocking**: the extracted summaries omit the technical derivations needed for any assessment beyond the abstract
- Beta inconsistency (20-30% in 2014 vs. 70-80% in 2024) is unexplained — `not-yet-sourced` — **important**: this is a 3-5x discrepancy in a key performance parameter
- No independent validation or review of the concept — `truly-unknown` — **important**: Deutelio is the only source for all technical claims

---

### 2. Challenges in Capturing System Function
**Coverage**: Poor

**Available**:
- High-level concept description: poloidal confinement, magnetic tunnel supports for internal dipole coil, steady-state D-D operation claimed
- Qualitative design intent distinguishing PoloMac from levitated dipole (LDX) and tokamaks

**Missing**:
- Plasma heating method: completely unspecified. D-D requires plasma temperatures of ~500 keV (roughly 10× D-T ignition temperature), making heating the most critical undefined subsystem.
- Plasma confinement time and energy confinement scaling: no published confinement data, no scaling law derived for this geometry
- Stability analysis: no published MHD stability results for the magnetic tunnel configuration
- Power balance / Q projections: no fusion gain estimates in available sources
- Energy conversion pathway: no specification of thermal cycle type, coolant, or BOP design
- Magnetic tunnel physics: the core innovation is described conceptually but no detailed field topology, plasma boundary, or coil geometry is published in the extracted summaries

**Gaps**:
- Plasma heating specification — `proprietary` or `truly-unknown` — **blocking**: without knowing the heating approach, the plasma physics and plant energy balance cannot be assessed
- Plasma confinement scaling — `truly-unknown` — **blocking**: no experimental data exists for this geometry at any scale
- Beta inconsistency resolution — `not-yet-sourced` — **blocking**: the two papers report fundamentally different beta values with no explanation available
- Power balance / Q — `truly-unknown` — **blocking**: no Q estimate exists in any available source

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Poor

**Available**:
- Prototype plan: small device with water-cooled copper coils (0.2-0.3 T) to validate magnetic tunnel concept — hydrogen plasma only, no fusion
- Commercial path described: step from prototype → D-D heat generators → SC-magnet electrical plants
- Company founded ~2022, seed round stage as of 2024

**Missing**:
- Whether the prototype has been built or operated (no experimental results in any source)
- TRL of any subsystem beyond the coil concept (design on paper)
- Superconducting magnet path (HTS vs. LTS) for commercial scale — completely unspecified
- Plasma-facing component design: no wall material, geometry, or heat flux specification
- D-D plasma heating hardware: no technology selected
- Shielding design: D-D neutron shielding differs from D-T but specific design absent

**Gaps**:

| Subsystem | Estimated TRL | Gap Type | Criticality |
|-----------|--------------|----------|-------------|
| Magnetic tunnel concept | TRL 2–3 (concept/paper design) | `not-yet-sourced` (prototype status) | blocking |
| Internal dipole coil (resistive) | TRL 3–4 (prototype planned) | `proprietary` | important |
| SC magnets for commercial | TRL 1–2 (not yet specified) | `truly-unknown` | important |
| Plasma heating | TRL 1 (not selected) | `truly-unknown` | blocking |
| D-D plasma physics | TRL 1 (no experiments) | `truly-unknown` | blocking |
| Vacuum vessel / first wall | TRL 1–2 (conceptual) | `not-yet-sourced` | important |
| Power conversion | TRL 1 (not specified) | `truly-unknown` | important |

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial (some inferences possible; no concept-specific data)

**Available**:
- D-D fuel: deuterium is abundant, commercially available, no supply concern
- No tritium breeding blanket required (D-D cycle) — eliminates Li-6, tritium handling, and breeding infrastructure costs
- Resistive copper coils for prototype: no supply concern

**Missing**:
- SC magnet material path: if HTS (REBCO tape) is chosen for commercial scale, supply chain constraints are the same as for HTS tokamaks — but Deutelio has not specified this
- Internal coil cooling and support structure materials: unique geometry may require novel structural materials in a high-radiation environment
- Shielding material specification: D-D neutron flux is lower energy than D-T but still significant at commercial scale
- First wall and plasma-facing component materials: not specified

**Gaps**:
- SC magnet material selection — `proprietary` — **important**: REBCO vs. LTS vs. resistive determines a major cost driver and supply chain exposure
- Radiation-tolerant structural materials for internal coil support — `truly-unknown` — **important**: the magnetic tunnel geometry places structural supports inside the plasma volume — a novel engineering challenge with no published design
- First wall material — `truly-unknown` — **nice-to-have** at this stage

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Plasma volume | ~1300 m³ | Elio 2014 FED | medium |
| Dipole radius | 5.4 m | Elio 2014 FED | medium |
| Magnetic field (D-T) | 1.4–1.8 T | Elio 2014 FED | medium |
| Beta | 20-30% (2014) / 70-80% (2024) | Both papers | low (inconsistent) |
| Operation mode | Steady-state | Both papers | high |
| Fuel | D-D | Both papers | high |
| Tritium breeding needed | No | D-D physics | high |
| Magnet type (prototype) | Resistive copper | 2024 JTSP | high |
| Prototype B-field | 0.2–0.3 T | 2024 JTSP | high |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Fusion power output (MW) | `truly-unknown` | blocking | No plant power target published |
| Fusion gain Q | `truly-unknown` | blocking | No Q estimate in any source |
| Plasma heating power and method | `truly-unknown` | blocking | No heating approach specified |
| Recirculating power fraction | `derivable` | blocking | Requires Q and heating method first |
| Thermal conversion efficiency | `truly-unknown` | blocking | Power cycle not specified |
| Net electrical output (MWe) | `truly-unknown` | blocking | Requires Q, heating, conversion |
| Capital cost (any subsystem) | `truly-unknown` | blocking | No cost data published anywhere |
| First wall lifetime / replacement cost | `truly-unknown` | blocking | No design exists |
| Operating costs (O&M, fuel, staffing) | `truly-unknown` | blocking | No plant study |
| Capacity factor | `derivable` | important | Steady-state claimed; can assume ~85% as generic MFE proxy |
| Magnetic field (commercial D-D) | `not-yet-sourced` | important | 2024 paper implies same field as tokamak for D-D; ~5–7 T possible |
| SC magnet cost (commercial) | `derivable` | important | Requires material choice; analogy to HTS tokamak possible |
| Blanket/shielding cost | `derivable` | important | D-D neutron shielding — analogy to D-T with scaling factor |

---

## Source Recommendations

1. **Full text of Elio 2014 FED paper** (DOI: 10.1016/j.fusengdes.2014.04.013) — `not-yet-sourced` — This is paywalled on ScienceDirect. The Phase 1a extraction only captured abstract-level content. Obtaining the full paper may clarify the beta derivation, reactor geometry details, and any power balance analysis. *Search ScienceDirect or request via institutional access.*

2. **Full text of 2024 JTSP paper** (DOI: 10.31281/med9bh43) — `not-yet-sourced` — Licensed CC-BY 4.0, so it should be freely accessible. The Phase 1a extraction captured only a summary. Full text may contain more detailed specifications, prototype design, and any power estimates. *Direct download from jtsp.eu.*

3. **Swiss Startup Association interview with Francesco Elio (2025-03-03)** — `not-yet-sourced` — The company profile references this URL. May contain roadmap details, funding status, and technology descriptions in lay language that could resolve some gaps. *Fetch directly; URL is in company profile.*

4. **Boldbrain 2024 competition materials** — `not-yet-sourced` — `unverified — confirm existence before searching`. Competition slide decks sometimes contain more technical detail than company websites. May be on the Boldbrain website.

5. **Levitated dipole / LDX literature** — `not-yet-sourced` — Since PoloMac is a variant of levitated dipole, published work on LDX (MIT/Columbia) provides the closest physics analogues: confinement scaling, beta behavior, heating approaches. These can ground LCOE parameter estimates where Deutelio-specific data is absent. *Search OSTI or Google Scholar for "levitated dipole" or "LDX" fusion.*

6. **Dipole confinement cost analogues** — `derivable` — No plant study exists for PoloMac or any levitated dipole concept. The 2014 FED paper may discuss reactor size parameters that allow rough capital cost estimation by analogy with tokamak ARIES studies, scaled for the different geometry. Flag all such estimates as first-order analogues with ±50% uncertainty.

7. **Direct contact with Deutelio** — For a company this early-stage and this opaque, direct outreach may be the only path to heating method, prototype status, and commercial design intent. Not a research search — a stakeholder engagement question.

---

## Summary

**Do not proceed to full D1+ analysis with current sources alone.**

The two extracted source documents are abstract-level summaries; the full papers — particularly the CC-BY 2024 JTSP paper — should be retrieved first. The 2024 JTSP full text is freely available and is the single highest-priority action before analysis. The 2014 FED full text would be the second priority.

Even with full papers in hand, PoloMac will be a "Limited/Opaque" rated concept. The quantitative LCOE model will necessarily be an analogy exercise borrowing from LDX and generic MFE plant studies, with the following parameters entirely assumed: Q, heating power, net electrical output, thermal efficiency, capital costs by subsystem, and O&M. All must be flagged explicitly as assumed, with broad uncertainty ranges (±50–100%). The concept's primary analytic value at D1+ stage is characterizing *what would need to be true* for the concept to be viable, not producing a grounded cost estimate.

## Structured summary (machine-readable)

```yaml
overall_rating: "Insufficient Data"
blocking_count: 9
important_count: 4
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Poor"
  system_function:            "Poor"
  subsystem_maturity:         "Poor"
  materials_supply_chain:     "Partial (some inferences possible; no concept-specific data)"
  lcoe_parameter_extraction:  "Poor"
```
