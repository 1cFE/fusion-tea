# Gap Assessment: Spherical Tokamak - CS-free p-B11 (ENN Energy)

## Overall Readiness
**Rating**: Significant Gaps

**Summary**: ENN Energy has published two peer-reviewed papers on its concept (arXiv:2401.11338 in *Phys. Plasmas* 31, 062507, 2024; and the EHL-2 physics design overview in *Plasma Science and Technology*), plus EXL-50 ECRH current drive results in arXiv:2104.14844. Experimental devices (EXL-50U operating; EHL-2 in design) provide concrete plasma-physics-program data. However, the published material describes a *physics verification* program — EHL-2 targets Ti ≈ 30 keV, ~10× below the >100 keV needed for net p-B11 fusion power. No commercial plant design point exists. Two fundamental physics gates remain unresolved by published evidence: (1) whether p-B11 ignition is achievable in a thermal tokamak at all, with a quantified critique by Li (2024) finding that the required hot-ion-mode Ti/Te = 4 is "far from accessible" under self-heating (would require external heating ~20× fusion power output); and (2) whether direct energy conversion of the alpha products to electricity — central to the economic case — is engineerable for a tokamak geometry (TRL 1–2, no engineering design published). Without these, an LCOE model is speculative.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial

**Available**:
- arXiv:2401.11338 / *Phys. Plasmas* 31, 062507 (2024) — ENN's flagship roadmap paper covering EXL-50U parameters, EHL-2 mission, and the commercial vision.
- EHL-2 physics design paper (doi:10.1088/2058-6272/ad981a) — device parameters (R₀ ≈ 1.05 m, A ≈ 1.85, B₀ ≈ 3 T, Ip ≈ 3 MA), heating design (17 MW NBI + 6 MW ECRH), target conditions (Ti ≈ 30 keV, Ti/Te ≥ 2).
- arXiv:2104.14844 — EXL-50 ECRH current drive with ~1 A/W efficiency.
- arXiv:2406.15495 — Li (2024) comment paper critiquing the hot-ion-mode feasibility.
- ENN English-language website — high-level commercial strategy statement (direct energy conversion, aneutronic).
- Adjacent concept: 21-spherical-tokamak-hts (Tokamak Energy ST-E1) provides D-T spherical-tokamak analog for geometry and ECRH efficiency.

**Missing**:
- Commercial plant design point — no Q value, no fusion power target, no net electric output, no capital cost.
- Direct energy converter engineering design — no electrostatic decelerator geometry, no inertial collector design, no efficiency target supported by hardware.
- EHL-2 magnet conductor type (resistive copper inferred for EXL-50U; EHL-2 type not stated).
- Independent TEA or plant study of ENN's concept.

**Gaps**:
- **No commercial plant design point published** — `truly-unknown` — **blocking** (LCOE inputs are entirely absent; the published material is a physics-verification roadmap, not a plant study).
- **Direct energy conversion design** — `truly-unknown` — **blocking** (the central economic-case dependency; TRL 1–2).
- **EHL-2 magnet engineering design** — `not-yet-sourced` — important (PST paper full text not yet ingested).

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial — physics is well-discussed in the literature; commercial economics absent.

**Available**:
- Rider 1997, Nevins 1998, and the Frontiers (2026) paper on p-B11 Lawson criterion establish that net energy production at Te = Ti is impossible across the full 75–500 keV range; net-energy windows exist only for Ti/Te > 1 hot-ion modes.
- Updated Tentori-Belloni (2023) cross-sections place the minimum Lawson triple product at ~1.5 × 10²² m⁻³s at Ti ≈ 270 keV (Te = 0.25 Ti).
- Li (2024) quantitatively critiques ENN's Ti/Te = 4 requirement: achievable Ti/Te < 1.5 at Ti = 150 keV under self-heating; external maintenance would cost ~20× fusion power.
- EHL-2 challenges identified: divertor heat flux >20 MW/m² at low density.
- Tokamak Energy ST-E1 D-T analog for the geometry and ECRH wall-plug efficiency assumption (~50–55%).

**Missing**:
- ENN's published response to the Li (2024) critique.
- Engineering path for a tokamak-geometry direct energy converter.
- Recirculating-power fraction at commercial plant scale (depends on undisclosed commercial plasma current and coil system).
- Divertor design for all-charged-particle heat flux.

**Gaps**:
- **p-B11 ignition feasibility in a thermal spherical tokamak** — `truly-unknown` — **blocking** (the most fundamental gap; Li 2024 quantitatively challenges the proposed hot-ion-mode path).
- **Hot-ion-mode maintenance power** — `truly-unknown` — **blocking** (Li 2024: ~20× fusion power for Ti/Te = 4 at Ti = 150 keV → Q_engineering deeply negative).
- **Direct energy converter design and efficiency** — `truly-unknown` — **blocking** (central economic-case dependency; no published design).
- **ECRH recirculating power at commercial scale** — `truly-unknown` — **blocking** (depends on commercial plasma current; ~30–50% of gross plausible).
- **Divertor solution for all-charged-particle heating** — `truly-unknown` — important (p-B11 puts 100% of fusion energy into the divertor as charged-particle heat — qualitatively more severe than D-T).
- **Fallback thermal-cycle scenario** — `derivable` from D-T MFE analogs — important (the DEC-failure economic case is the primary go/no-go test the LCOE model should evaluate).

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- TRL assessments by subsystem: p-B11 plasma at reactor conditions TRL 1–2; direct energy conversion TRL 1–2 (Venetian-blind LLNL 1970s, mirror-machine geometry); CS-free non-inductive current drive TRL 3–4 (EXL-50 demonstrated, EHL-2 will scale); ST plasma confinement at Ti/Te >> 1 TRL 2–3; divertor at p-B11 conditions TRL 3–4; ECRH/NBI heating TRL 5–7 (mature at EHL-2 scale); ST vacuum vessel + resistive copper magnets TRL 5–6 (EHL-2 level).
- EXL-50U operates at 1 MA / 1.2 T with 150 kA TF coil current — concrete data point for resistive-magnet ST engineering.

**Missing**:
- Any ST plasma data at Ti > 30 keV.
- DEC hardware for tokamak geometry.
- HTS magnet transition for ENN's commercial plant (not announced; resistive copper has prohibitive recirculating power at reactor scale).

**Gaps**:
- **Direct energy conversion at tokamak scale** — `truly-unknown` — **blocking** (no hardware, no engineering design, no efficiency demonstration).
- **Commercial-scale magnet conductor decision** — `truly-unknown` — important (resistive copper → ~300 MW ohmic loss at ITER-scale current; HTS transition unannounced).
- **Divertor materials for combined alpha + radiation heat flux** — `not-yet-sourced` — important.

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Good

**Available**:
- Boron-11: natural boron is ~80% ¹¹B, global production ~10 Mt/yr. Isotopic enrichment to >95% ¹¹B is industrially feasible (¹⁰B enrichment is mature for fission control rods).
- No tritium / FLiBe / Li-6 / beryllium required — major structural supply-chain advantage relative to D-T MFE concepts.
- Copper coils: unconstrained supply.
- ECRH gyrotrons at ITER class (1 MW CW): commercially available.
- HTS REBCO (if ENN transitions): same supply chain as 21-spherical-tokamak-hts (Tokamak Energy); production capacity is the bottleneck for any HTS-based fusion fleet.

**Missing**:
- Quantitative ¹¹B enrichment demand at plant scale.
- HTS supply commitment from ENN (none announced; concept currently uses resistive copper).

**Gaps**:
- ¹¹B enrichment demand at plant scale — `derivable` once plant design exists — nice-to-have.
- ENN HTS supply agreement — `not-yet-sourced` (and may not exist; copper magnets unrealistic at reactor scale) — important.

---

### 5. LCOE Parameter Extraction
**Available Parameters**:

| Parameter | Value | Source | Confidence |
|---|---|---|---|
| EHL-2 R₀ | ~1.05 m | dossier, roadmap paper | high |
| EHL-2 A (aspect ratio) | ~1.85 | dossier | high |
| EHL-2 B₀ | ~3 T | dossier | high |
| EHL-2 Ip | ~3 MA | roadmap paper | high |
| EHL-2 heating | 17 MW NBI + 6 MW ECRH | dossier | high |
| EHL-2 target Ti | ~30 keV | roadmap paper | high |
| EHL-2 Ti/Te target | ≥2 | roadmap paper | high |
| EXL-50U Ip / B₀ | 1 MA / 1.2 T | dossier | high |
| ECRH current drive efficiency (EXL-50) | ~1 A/W | dossier | medium |
| p-B11 peak cross-section energy | ~650 keV CM (~ 10× D-T) | nuclear physics | high |
| p-B11 minimum Lawson (Te = 0.25 Ti) | ~1.5 × 10²² m⁻³s at Ti ≈ 270 keV | Frontiers (2026) | high |
| Hot ion mode Ti/Te achievable under self-heating | < 1.5 at Ti = 150 keV | Li (2024) | high |
| Theoretical DEC efficiency | 70–90% | DEC literature (upper bound) | low |
| Operation mode | Steady-state | dossier | high |

**Missing Parameters**:

| Parameter | Gap Type | Criticality |
|---|---|---|
| Commercial plant Q | truly-unknown | blocking |
| Fusion power (gross), net electric output | truly-unknown | blocking |
| Capital cost (any subsystem) | truly-unknown | blocking |
| Direct energy converter efficiency (achieved) | truly-unknown | blocking |
| Direct energy converter capital cost | truly-unknown | blocking |
| Commercial plasma current | truly-unknown | blocking |
| ECRH recirculating power at commercial scale | truly-unknown | blocking |
| Hot-ion-mode maintenance power | truly-unknown | blocking |
| Capacity factor | truly-unknown | important |
| Power conversion cycle thermal efficiency (DEC failure case) | not-yet-sourced | important |
| Commercial magnet type | truly-unknown | important |

---

## Source Recommendations

1. **EHL-2 PST paper full text** (doi:10.1088/2058-6272/ad981a) — should be ingested to confirm magnet conductor and detailed engineering design.
2. **ENN response (if any) to Li (2024) critique** — would clarify ENN's position on the hot-ion-mode feasibility.
3. **Rider (1997) and Nevins (1998) papers** — the foundational analyses of p-B11 Lawson criterion; should be formally ingested as sources.
4. **ARIES-ST plant study** — D-T spherical-tokamak commercial design analog; provides geometry and BoP cost-structure baselines.
5. **Comparable Chinese state fusion program filings** — ENN is a private subsidiary of a state-adjacent conglomerate; if ENN files for national R&D program funding, milestone details may enter the public domain.
6. **Tokamak Energy ST-E1 analysis** (21-spherical-tokamak-hts) — the most direct D-T cross-reference for ECRH efficiency, ST geometry, and HTS supply chain.

---

## Summary

**Proceed to full analysis**: Yes, with significant caveats.

ENN's concept is the only p-B11 spherical tokamak in the catalog, and its published material is enough to define the device geometry, fuel cycle, and high-level commercial strategy. A *speculative-placeholder* LCOE model is buildable: 500 MWe / 1 GWe scaling cases under the assumption that p-B11 ignition and direct energy conversion are achievable, producing rough $/MWh estimates (analyst placeholder ~96 $/MWh at 500 MWe, ~61 $/MWh at 1 GWe). These should be reported as best-case bounds, not forecasts.

The dominant LCOE-relevant gaps are not engineering uncertainties — they are physics go/no-go gates: (1) can a thermal spherical tokamak achieve p-B11 ignition at all, given Li (2024)'s analysis that the required hot-ion mode is infeasible under self-heating? and (2) can direct energy conversion at the tokamak geometry actually be engineered? If either gate fails, the entire LCOE case collapses regardless of magnet type or BoP cost. The model should explicitly include a DEC-failure scenario (alpha power routed through a fallback thermal cycle at η ≈ 0.35) and a hot-ion-mode-heating-multiplier scenario (1× → 20×) to characterize the boundary of viability.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Significant Gaps"
blocking_count: 8
important_count: 3
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Partial"
  system_function:            "Partial — physics is well-discussed in the literature; commercial economics absent."
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Good"
  lcoe_parameter_extraction:  "Unknown"
```
