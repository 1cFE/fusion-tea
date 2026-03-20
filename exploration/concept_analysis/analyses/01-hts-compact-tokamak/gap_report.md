Now I have everything I need. Let me write the gap assessment.

---

# Gap Assessment: HTS Compact Tokamak

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: The HTS Compact Tokamak (CFS/ARC) is among the best-documented fusion concepts in the public domain. Phase 1a sources cover the engineering architecture, performance targets, and power conversion pathway at sufficient depth to write the qualitative sections and a parameterized LCOE skeleton. The primary gaps are economic: no published capital cost breakdowns by subsystem, no component replacement schedules, and no explicit capacity factor targets. These are derivable or analogizable — they do not block analysis, but they require explicit flagging of assumptions.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**:
- Full conceptual plant design: Sorbom et al. 2015 (ARC) — dimensions, field, power, heating, blanket, materials, cycle
- SPARC experimental baseline: Creely et al. 2020 (overview), Lin & Wright et al. 2020 (ICRF physics)
- Power conversion trade study: Colliva et al. 2024 (Rankine vs. Brayton vs. He), Segantin et al. 2020
- Current construction status and commercial commitments: cfs-2025-2026-updates.md — ARC site, PPAs (400 MWe subscribed), SPARC first plasma 2027
- Multiple independent synthesis sources (Grokipedia, Wikipedia SPARC, IEEE Spectrum)
- ~$2B+ funding transparency and investor-level updates from CFS blogs

**Missing**:
- A second-generation ARC plant study incorporating post-2020 design evolution (the 270→400 MWe upgrade is mentioned but no updated paper cited)
- CFS-authored engineering cost disclosures

**Gaps**:
- Updated ARC plant study (270 MWe → 400 MWe evolution) — `not-yet-sourced` — important (affects scaling assumptions and power block sizing)
- CFS internal cost-of-electricity projections — `proprietary` — nice-to-have (public analogues exist)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Core physics uncertainties: I-mode confinement regime, Q~13.6 target, beta limits (β_N = 3.3) — from arc-reactor-specifications.md
- LHCD/ICRF coupled heating and current drive architecture described — sources clarify LHCD is for steady-state current drive, not primary heating
- FLiBe blanket as thermal buffer enabling continuous grid output despite pulsed plasma — documented in cfs-2025-2026-updates.md
- Operation mode ambiguity (quasi-steady vs. true steady-state) — resolved with citations in dossier
- Heating power budget (25 MW LHCD + 13.6 MW ICRF = 38.6 MW recirculating power for ARC)

**Missing**:
- Bootstrap current fraction quantification (critical for steady-state LHCD requirement scaling)
- FLiBe corrosion/compatibility data at operating temperatures (900–1200 K)
- Tritium permeation rates through FLiBe and structural materials
- Demountable joint performance under neutron fluence
- Disruption frequency and impact on availability at high field
- Remote maintenance strategy and downtime model for ARC

**Gaps**:
- Bootstrap current fraction for ARC operating scenario — `not-yet-sourced` — important (drives LHCD power requirement and recirculating fraction); search: J. Plasma Physics SPARC series 2020, particularly the transport/confinement paper
- FLiBe corrosion and tritium permeation: engineering challenge literature — `not-yet-sourced` — important; search OSTI for molten salt blanket tritium permeation studies (unverified — confirm existence before searching)
- Disruption management and availability model — `truly-unknown` (no published ARC-specific availability analysis found) — nice-to-have
- Demountable joint neutron hardness data — `proprietary` — nice-to-have

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **HTS magnets (REBCO)**: TRL ~7 — 20 T large-bore magnet demonstrated September 2021; first TF coil installed in SPARC January 2026. This is the most mature novel subsystem.
- **SPARC tokamak** (burning plasma demonstrator): TRL ~5 — under construction, first plasma 2027. Validates physics basis for ARC.
- **ICRF heating system**: TRL ~6 — well-established technology on other tokamaks; SPARC system uses standard fast-wave approach (Lin & Wright 2020)
- **Power conversion (Rankine)**: TRL ~9 — mature industrial technology; FLiBe-coupled HX is the integration challenge, not the turbine

**Missing**:
- FLiBe blanket TRL: no explicit TRL assessment in sources. MSRE (molten salt reactor experiment, 1960s) provides chemistry precedent, but fusion-specific TRL is not stated.
- First wall (W) lifetime under ARC neutron flux: not addressed
- TiH2 neutron shielding performance at ARC-relevant fluence: not addressed
- LHCD system for ARC: TRL assessment not in sources (precedent from other tokamaks, but ARC-geometry coupling not validated)
- Tritium handling and processing system: TRL ~4-5 (being built for ITER), not discussed in Phase 1a sources

**Gaps**:
- FLiBe blanket TRL and fusion-relevant test data — `not-yet-sourced` — important; search OSTI/IAEA for molten fluoride salt blanket test loop experiments (unverified — confirm existence before searching)
- First wall W lifetime under ARC neutron flux (~3 MW/m²) — `not-yet-sourced` — important; search: fusion materials irradiation database, IFMIF data, FNSF design studies
- Tritium processing system TRL relative to ARC requirements — `not-yet-sourced` — important; ITER TPBAR studies are the closest analogue

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- REBCO HTS tape identified as the critical enabling material (high-field magnets); CFS has demonstrated large-scale winding capability (dossier, IEEE Spectrum source)
- Tungsten first wall (1 cm W) — established material for fusion PFCs
- Inconel 718 vacuum vessel — mature aerospace/industrial material
- FLiBe (LiF-BeF2) blanket — chemistry well-characterized from MSRE; no supply/cost data in sources
- TiH2 neutron shielding — mentioned in design; no supply data

**Missing**:
- REBCO tape production capacity vs. ARC demand (estimated meters of tape per TF coil × 18 coils): not in sources
- Beryllium supply for FLiBe (BeF2 component): BeF2 requires Be, which is a controlled critical material with limited global supply
- Li-6 enrichment requirements for tritium breeding at TBR ≥ 1.1: not addressed
- Helium-3 (not applicable — D-T fuel cycle, not D-He3)
- Tritium initial inventory sourcing: not addressed (CFS will need ~1–2 kg to start ARC)
- REBCO tape cost trajectory ($/kA-m): mentioned as "dramatically decreasing" in industry context but no data in sources

**Gaps**:
- REBCO tape production capacity and cost trajectory — `not-yet-sourced` — important; search: SuperPower, Faraday Factory Japan, Bruker HTS supply chain reports (unverified — confirm existence before searching)
- Li-6 enrichment supply chain for ARC FLiBe inventory — `not-yet-sourced` — important; search DOE isotope program reports
- Beryllium supply constraints for FLiBe BeF2 — `not-yet-sourced` — important; search USGS critical minerals reports
- Tritium startup inventory sourcing strategy — `proprietary`/`truly-unknown` — blocking for full fuel cycle cost model; no company has solved this publicly

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electrical output | 400 MWe (current plan); 270 MWe (original ARC) | cfs-2025-2026-updates.md; arc-reactor-specifications.md | h |
| Fusion thermal power | ~525 MW (up to ~1 GW in latest estimates) | arc-reactor-specifications.md | m |
| Fusion gain Q | ~13.6 (ARC); ~11 (SPARC) | arc-reactor-specifications.md; dossier | h |
| Thermal-to-electric efficiency | 30–40% (Rankine ~30%, sCO2 potentially 40%+) | arc-power-conversion-studies.md | m |
| Recirculating power (heating) | ~38.6 MW (25 MW LHCD + 13.6 MW ICRF) | arc-reactor-specifications.md | h |
| FLiBe blanket outlet temperature | ~900 K (up to 1200 K) | arc-reactor-specifications.md | h |
| TBR | ≥1.1 (up to 1.22 with optimization) | arc-reactor-specifications.md | h |
| Magnet operating temperature | ~20 K | arc-reactor-specifications.md | h |
| First plasma date (SPARC) | 2027 | cfs-2025-2026-updates.md | h |
| ARC grid connection | early 2030s | cfs-2025-2026-updates.md | m |
| Aspect ratio / major radius | 3.3 m / AR~3 | arc-reactor-specifications.md | h |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost (total plant, $/kWe) | `proprietary` | blocking | No published estimate; ITER analogues exist but poor comparator for compact design |
| Capital cost by CAS subsystem | `proprietary` | blocking | No subsystem breakdown published; derivable from first principles with large uncertainty |
| Magnet system cost ($/coil, $/kA-m) | `not-yet-sourced` | blocking | REBCO tape cost data exists in HTS industry; winding cost must be estimated |
| First wall replacement schedule (years) | `truly-unknown` | blocking | Depends on neutron fluence; ARC-relevant test data does not yet exist |
| FLiBe blanket replacement schedule | `truly-unknown` | important | No published estimate; activation and tritium retention drive this |
| Capacity factor target | `derivable` | important | Quasi-steady + FLiBe thermal buffer suggests high CF; no explicit target stated |
| Plant lifetime (years) | `derivable` | important | Typically assumed 30–40 years; no CFS statement found |
| O&M cost ($/MWh or $/year) | `proprietary`/`not-yet-sourced` | important | ITER-scale tokamak analogues could bound this |
| Tritium startup inventory cost | `truly-unknown` | important | ~$30M/kg × 1–2 kg required; tritium price trajectory uncertain |
| Construction cost learning rate | `truly-unknown` | nice-to-have | Needed for fleet economics; no data |
| Cryogenic system power parasitic | `derivable` | important | ~20 K HTS magnets require substantial cryo plant; estimable from coil mass |

---

## Source Recommendations

1. **SPARC physics series, J. Plasma Physics 2020** — ~10-paper special issue including transport, disruptions, current drive, blanket physics. Phase 1a captured only the ICRF paper. Remaining papers cover bootstrap current, disruption limits, and neutron handling. `not-yet-sourced` — these papers are confirmed published; search Cambridge Core for the full SPARC JPP 2020 special issue.

2. **Sorbom et al. 2015 full text** (MIT PSFC report) — The dossier cites this but only the specifications were extracted. The full paper contains a preliminary cost discussion and power balance. `not-yet-sourced` — available at the arXiv and MIT PSFC links already in the dossier.

3. **Updated ARC plant study (post-2022)** — The 270→400 MWe evolution and Virginia site selection suggest CFS has updated engineering parameters. Search: MIT News, CFS press releases, NIF/Fusion Industry Association reports for any updated ARC design disclosure. `unverified — confirm existence before searching`.

4. **HTS tape supply chain / cost projections** — Search: DOE fusion energy office HTS supply chain workshops, SuperPower/AMSC/Fujikura manufacturer data sheets, ARPA-E BETHE program reports. `not-yet-sourced` — `unverified — confirm existence before searching`.

5. **Molten fluoride salt blanket test loop data** — ORNL has historical MSRE data; more recent work at HFIR and EU (ITER TBM) may address corrosion and tritium permeation. Search OSTI for "FLiBe tritium permeation" and "molten salt blanket test loop." `not-yet-sourced` — `unverified — confirm existence before searching`.

6. **Fusion tokamak O&M cost analogues** — JET and ITER budget disclosures provide upper bounds; compact tokamak O&M may be lower. Search: IAEA fusion reactor economics studies, EPRI fusion assessment reports. `not-yet-sourced` — `unverified — confirm existence before searching`.

---

## Summary

**Proceed to full analysis**, but with explicit gap flags in the LCOE model.

The qualitative write-up (D1 sections 1–4) can be written now with high confidence. The HTS Compact Tokamak is the most data-rich concept in the shortlist — a published plant study, a precursor under construction, multiple independent power cycle analyses, and detailed plasma physics publications exist. Section 2 (system function challenges) will need to draw on the broader SPARC JPP 2020 series not yet ingested.

The quantitative LCOE model (D1 section 5) can be parameterized and run, but with important caveats: capital costs must be estimated from first principles or ITER analogues rather than published CFS figures; first wall and blanket replacement schedules must be treated as free parameters; and the capacity factor must be derived from the quasi-steady operational model rather than a stated target. The back-solve to $0.01/kWh is tractable — the compact high-field design has a credible pathway (smaller capital base, high power density, demountable maintenance) and the binding constraints are well enough understood to identify.

**Priority additional sourcing** before writing: pull the remaining SPARC JPP 2020 papers (especially transport/current drive), and skim the Sorbom 2015 full text for any cost discussion. Both are confirmed-existing sources already cited in the dossier.
