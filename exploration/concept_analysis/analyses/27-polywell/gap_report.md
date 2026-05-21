Now I have all the source material. Let me write the gap assessment.

# Gap Assessment: Polywell (D-T)

## Overall Readiness
**Rating**: Significant Gaps

**Summary**: The Polywell D-T concept has a single credible reactor-scale physics study (Park et al. 2025) and a handful of experimental records, but no engineering plant study, no capital cost estimates, and no specified thermal cycle or blanket design. The physics model rests on an unvalidated free parameter (γ=0.1 loss reduction factor). An LCOE analysis is possible but will be almost entirely analogy-based and assumption-driven — the error bars will be enormous. Two potentially relevant sources from the dossier (Rogers 2018, Sporer 2022) were not extracted and may partially close gaps.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Limited

**Available**:
- Park et al. 2025 (arXiv:2508.06761): The only EMC2-authored reactor design study. Provides physics scaling to Q=10.5, 980 MW fusion power, and some qualitative engineering observations. This is a preprint, not a full engineering design report.
- Park et al. 2015 (Phys. Rev. X): Peer-reviewed experimental result demonstrating high-beta electron confinement in WB-X. No reactor extrapolation.
- EMC2 website: High-level technology description, FPNS program overview, broad performance claims (100 MW–1 GW).
- FPNS/SHINE DOE proposal (2023–2024): FPNS hardware parameters at neutron source scale (350 kW fusion power, 8.5 cm radius). Real engineering constraints but not a power plant.
- Experimental history (WB-1 through WB-X): Documented via secondary sources. Resistive-coil pulsed devices only; no sustained fusion burn.

**Missing**:
- No published plant study or system code analysis for a D-T power plant
- No EMC2 engineering white paper or techno-economic report
- Rogers 2018 (J. Fusion Energy) covers p-B11, not D-T, but may contain engineering cost structure useful as analogue — **not extracted in Phase 1a**
- Sporer 2022 ("Analysis of Two Fusion Reactor Designs Based on Magnetic Electrostatic Plasma Confinement") likely contains engineering/cost analysis of Polywell-type designs — **not extracted in Phase 1a**
- Lynceans/EMC2 "Fork in the Road" document may contain economic framing — **not extracted in Phase 1a**

**Gaps**:
- No power plant engineering design study — `proprietary` (unlikely to exist even internally at current stage) / `not-yet-sourced` (Rogers 2018, Sporer 2022 may provide analogues) — **blocking for LCOE**
- Thermal cycle specification — `truly-unknown` (EMC2 has not published this) — **blocking**
- Blanket design — `truly-unknown` at this stage — **blocking for tritium self-sufficiency assessment**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial (challenges are well-characterized; resolutions are not)

**Available**:
- The γ=0.1 loss reduction factor is explicitly flagged by Park et al. 2025 as a free parameter derived from 2D PIC simulations extrapolated to 3D. Authors acknowledge "several optimistic projections."
- Electron confinement scaling: WB-X demonstrated high-beta electron confinement at small scale; extrapolation to reactor scale is theoretically justified but experimentally unvalidated.
- Steady-state operation: Park et al. 2025 models it explicitly; WB-series devices were all pulsed. No demonstrated steady-state plasma.
- Electron beam injection at 60 keV, 1.3 kA: Park et al. notes "off-the-shelf availability" of such injectors, which is the strongest engineering grounding in any source.
- Neutron shadowing by polyhedral coils: acknowledged in Park et al. 2025 as a novel blanket engineering challenge.

**Missing**:
- No experimental demonstration of Q > 0 (net fusion gain)
- No validated confinement scaling law — the critical physics bet is unresolved
- No PIC simulation results for reactor-scale parameters
- No thermal-hydraulic or neutronics analysis of the polyhedral geometry

**Gaps**:
- Confinement scaling validity (γ extrapolation) — `truly-unknown` — **blocking for any credible performance projection**
- Stability of high-density plasma (~10²¹/m³) in the potential well — `truly-unknown` — **important**
- First-wall/PFC heat flux management at reactor scale — `not-yet-sourced` (FPNS has some PFC data; Sporer 2022 may have more) — **important**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **Polyhedral cusp coils (resistive)**: TRL ~4–5. WB-X demonstrated high-beta confinement. WB-8 (0.8 T) achieved 6× higher plasma density. No superconducting version demonstrated.
- **Electron beam injectors**: TRL ~7–8. Park et al. 2025 states "off-the-shelf availability of steady-state electron beam injectors" at 60 keV. FPNS uses similar technology.
- **Ion beam injectors (for FPNS mode)**: TRL ~5–6. FPNS specifies 150–200 keV, 5–6 MW ion beams — not demonstrated at this scale for Polywell specifically.
- **Superconducting polyhedral coils**: TRL ~2–3. EMC2 reportedly began superconducting Polywell work in 2012; no published results. Required for reactor-scale steady-state operation at 4.5 T.
- **Vacuum vessel**: Not described specifically. Conventional technology; TRL ~8–9 for analogous confinement systems.

**Missing**:
- **Tritium breeding blanket**: TRL ~1 (concept only; coil-shadowing challenge acknowledged but unresolved). No material or geometry specified.
- **First wall/PFC for reactor scale**: TRL ~2–3 (FPNS data at 350 kW fusion power only; 980 MW reactor is 2800× more powerful)
- **Energy conversion system (thermal cycle)**: TRL unknown — not specified anywhere in available sources
- **Tritium handling and processing**: TRL ~5–6 by analogy to D-T fusion community; Polywell-specific challenges not documented

**Gaps**:
- Superconducting polyhedral coil design — `proprietary` (EMC2 may have internal work from 2012+) / `truly-unknown` — **blocking**
- Tritium breeding blanket design and TRL — `truly-unknown` — **blocking**
- Thermal conversion system — `truly-unknown` for this concept specifically; **important** (derivable by analogy)

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- **Tritium**: General D-T supply challenge applies. No Polywell-specific tritium consumption rate published; derivable from Park et al. 2025 fusion power (980 MW → ~56 g/day tritium burn at 100% burnup, TBR unknown).
- **Magnet conductor**: All demonstrated devices use copper (resistive). Reactor requires superconducting coils at 4.5 T — LTS (NbTi/Nb₃Sn) or HTS (REBCO) unspecified. Both are available commercially.
- **Electron beam system components**: Relatively standard accelerator technology per Park et al. 2025; no supply chain concerns flagged.
- **Neutron shielding materials**: Standard; no concept-specific challenge beyond polyhedral geometry.

**Missing**:
- Blanket material (Li₂TiO₃, Li₄SiO₄, LiPb, etc.) — unspecified; cannot assess Li-6 supply implications
- Coil conductor specification (LTS vs HTS) — unspecified
- PFC material (W, CFC, etc.) — not addressed
- Manufacturing complexity of the polyhedral coil geometry — noted as advantageous (non-interlocking) but not costed

**Gaps**:
- Blanket material and lithium supply chain — `truly-unknown` at this stage — **important** (for D-T self-sufficiency)
- Superconductor type and quantity — `derivable` from coil geometry once specified, but geometry not specified — **important**
- PFC material specification — `not-yet-sourced` — **nice-to-have** for first pass

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion power | ~980 MW | Park et al. 2025 | m |
| Input (driver) power | 78 MW (60 keV, 1.3 kA e-beam) | Park et al. 2025 | m |
| Q value | 10.5 | Park et al. 2025 | l (γ=0.1 unvalidated) |
| Device size | 1.6 m cube (coil-to-coil) | Park et al. 2025 | m |
| Magnetic field | 4.5 T boundary | Park et al. 2025 | m |
| Plasma volume | ~4.1 m³ | Park et al. 2025 | m |
| Thermal efficiency (rough) | ~40% | polywell-technical-details.md | l (no primary source cited) |
| FPNS R&D cost | $20M / 24 months | EMC2/SHINE proposal | l (neutron source only; not power plant) |
| Navy program cost | ~$12M total | polywell-technical-details.md | h (historical) |
| Operation mode | Steady-state (design intent) | Park et al. 2025 | m |
| Electron beam "off-the-shelf" | Implies moderate cost | Park et al. 2025 | l (no $ cited) |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost by subsystem | truly-unknown | Blocking | No plant study; analogy to accelerator/magnet costs required |
| Total plant capital cost (overnight) | truly-unknown | Blocking | No published estimate |
| Thermal cycle type and efficiency | truly-unknown | Blocking | Not specified anywhere; Rankine/sCO2 analogy required |
| Blanket cost and design | truly-unknown | Blocking | No blanket design; standard tokamak breeding blanket costs not applicable due to polyhedral geometry |
| Superconducting coil cost | derivable | Blocking | Coil geometry compact (1.6 m), non-interlocking; cost derivable once conductor type assumed |
| O&M cost rate | truly-unknown | Blocking | No published O&M estimate |
| Capacity factor / availability | derivable | Important | No published value; analogy to steady-state MFE concepts (~80–90%) is reasonable |
| Component replacement schedule | truly-unknown | Important | First wall lifetime at 980 MW fusion power not addressed |
| Tritium breeding ratio (TBR) | truly-unknown | Important | Blanket unspecified; TBR < 1 unless novel blanket designed for polyhedral shadowing |
| Electrical output (gross/net) | derivable | Blocking | Derivable from 980 MW fusion × ~40% thermal eff. × recirculating power; ~320–350 MWe estimated |
| Scaling assumptions / plant size | derivable | Important | Only one reactor design point; scaling not explored |

---

## Source Recommendations

1. **Rogers 2018** — J. Fusion Energy 37, 1-17: "A Polywell Fusion Reactor Designed for Net Power Generation." This is explicitly about net power generation, not just physics. Even though it's p-B11, it likely contains cost structure, BOP assumptions, and scaling that can inform D-T analogues. Listed in dossier citations but **not extracted**. Priority: **high** — `not-yet-sourced`.

2. **Sporer 2022** — "Analysis of Two Fusion Reactor Designs Based on Magnetic Electrostatic Plasma Confinement" (Michigan plasma lab). The title suggests capital cost / engineering analysis of Polywell-type designs. Listed in dossier citations but **not extracted**. Priority: **high** — `not-yet-sourced`. `unverified — confirm existence before searching`.

3. **Lynceans/EMC2 "Fork in the Road" PDF** — EMC2 internal/presentation document. May contain economic framing or cost comparisons. Listed in dossier but **not extracted**. Priority: **medium** — `not-yet-sourced`. `unverified — confirm existence before searching`.

4. **Park 2015 Phys. Rev. X (full paper)** — Peer-reviewed; may contain more detail on plasma parameters useful for loss rate derivation than the summary captured. `not-yet-sourced` — priority: **low** (physics, not cost).

5. **OSTI / DOE search for FPNS final report** — The FPNS DOE report was anticipated March 2025. If published, it may contain engineering design detail (PFC heat loads, coil design, tritium handling) that provides a scaling bridge to a power reactor. Search: OSTI.gov for "Fusion Prototypic Neutron Source EMC2 SHINE 2025." `not-yet-sourced`. Priority: **medium**.

6. **APS-DPP conference proceedings (2025)** — Park et al. 2025 was presented at APS-DPP. Supplementary slides may contain cost or engineering detail not in the preprint. `not-yet-sourced`. Priority: **low**. `unverified — confirm existence before searching`.

---

## Summary

**Proceed to full analysis with flagged assumptions**, but extract Rogers 2018 and Sporer 2022 first if time permits — these are the most likely to partially fill capital cost and BOP gaps.

The Park et al. 2025 paper gives sufficient reactor design parameters (power, gain, device geometry, input power) to anchor a first-pass LCOE model, but virtually every cost parameter must be derived by analogy or assumption:

- **Capital costs**: Use coil geometry (small, non-interlocking) + superconductor technology cost analogues; no primary estimate exists
- **Thermal cycle**: Assume Rankine or sCO2 at 40% efficiency (rough literature cite available from polywell-technical-details.md, though sourcing is weak)
- **BOP**: Analogy to compact tokamak or stellarator of similar electrical output
- **Blanket**: Acknowledge as a blocking unknown for tritium self-sufficiency; assign a cost range from tokamak breeding blanket analogues with a large uncertainty multiplier for the polyhedral geometry challenge
- **O&M**: Analogy to other steady-state MFE concepts

The critical caveat for the entire analysis: the reactor design's viability rests on γ=0.1, an unvalidated free parameter. The LCOE model should treat Q (and by extension, gross electrical output and recirculating power fraction) as a highly uncertain input and show sensitivity sweeps. A Q significantly below 10 rapidly makes the concept nonviable for power production.

## Structured summary (machine-readable)

```yaml
overall_rating: "Significant Gaps"
blocking_count: 7
important_count: 4
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Limited"
  system_function:            "Partial (challenges are well-characterized; resolutions are not)"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Poor"
  lcoe_parameter_extraction:  "Poor"
```
