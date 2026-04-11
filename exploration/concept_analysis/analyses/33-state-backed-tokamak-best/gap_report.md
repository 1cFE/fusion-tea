Now I have everything I need. Let me write the gap assessment.

---

# Gap Assessment: State-Backed Tokamak - BEST

## Overall Readiness
**Rating**: Mostly Ready (with important framing caveat)

**Summary**: The BEST Research Plan v1.1 is an unusually comprehensive public document that resolves nearly all device-level parameters at high confidence. However, BEST is an experimental device — not a power plant — which creates a structural challenge for LCOE analysis: all five D1+ sections must be framed around the BEST→CFEDR→PFPP technology lineage rather than BEST itself. The qualitative sections (1–4) are well-supported; the quantitative LCOE section requires analogues and explicit assumptions because no commercial plant design yet exists.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good (device level) / Partial (power plant level)

**Available**:
- **BEST Research Plan v1.1** (EUROfusion/ASIPP, Nov 2025) — a 100+ page public document covering all major technical parameters, subsystem designs, timeline, and strategic positioning. This is an exceptionally transparent publication for a state-backed Chinese program.
- **Neo Fusion company profile** — ownership structure (CNPC ~20%, CAS), funding ($214M raised, registered capital expanded to 14.5B yuan / ~$2B USD), corporate identity.
- **CFETR power conversion studies** — three published papers (2021, 2024, 2025) on sCO2 Brayton cycle for the downstream CFEDR/PFPP reactors.
- All 11 differentiation table columns resolved; 9/11 at high confidence.

**Missing**:
- Detailed CFEDR/PFPP reactor design parameters (the commercial step that BEST feeds into).
- BEST construction cost data (typical for state-backed programs under construction).
- Chinese-language ASIPP internal reports on CFEDR system design.

**Gaps**:
- CFEDR/PFPP plant-level design parameters — `not-yet-sourced` — **important** (LCOE analysis must project to a power plant, and CFEDR studies likely exist in Chinese literature)
- BEST construction cost — `proprietary/state-classified` — **nice-to-have** (useful for cost scaling but not blocking; ITER analogues can substitute)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- The fundamental modeling challenge is clearly identifiable from sources: **BEST is explicitly experimental**, with no power conversion system, no tritium breeding, and no commercial plant configuration.
- Physics parameters are well-defined: R=3.6m, B=6.15T, Q targets (≥1 by 2030, ~5 by 2032-2035), Ip up to 7 MA, 50 MW auxiliary heating.
- Multiple candidate blanket designs for TBM testing (COOL, WCCB, WCLL, HCPB, WLCB) — no committed blanket for a power reactor.
- sCO2 Brayton cycle identified as preferred power conversion for the lineage, but BOP for CFEDR/PFPP is not finalized.

**Missing**:
- Plasma performance projections with uncertainty bounds (burn fraction, confinement scaling from BEST to CFEDR).
- How BEST experimental results will gate CFEDR design decisions.
- Cost uncertainty propagation from technology variants (5 candidate blankets = 5 cost scenarios).

**Gaps**:
- Multi-blanket cost uncertainty (5 candidate TBM concepts → which one CFEDR adopts is unknown) — `truly-unknown` — **important** (creates branching cost scenarios)
- Confinement quality assumptions for extrapolation to CFEDR power plant — `derivable` (use ITER/ARIES tokamak scaling) — **important**
- Plasma exhaust / divertor heat flux solutions at power plant scale — `not-yet-sourced` — **nice-to-have**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **TF/PF magnets (Nb₃Sn/NbTi)**: ITER-heritage conductors. TRL 8–9 — largest supply chain in fusion, mature manufacturing.
- **CS YBCO HTS sub-coils**: HTS used only in high-field CS region (peak 18.8T). TRL 6–7 — higher than full-HTS designs; ITER-adjacent manufacturing. Limited quantity relative to full-HTS concepts.
- **Heating systems** (ECRH 170 GHz, ICRH, LHCD, NBI): All established technologies at TRL 7–8. JET-heritage NBI. Gyrotrons at 170 GHz proven at ITER scale.
- **PFCs** (full-W first wall, W-monoblock divertor): TRL 8 — ITER-heritage design, 240 modules, remote-handling-compatible.
- **Remote handling**: ITER-derived approach confirmed; TRL 6–7 for D-T operational scale.

**Missing**:
- TRL for **tritium breeding blankets** (under TBM test; none committed) — currently TRL 3–5 depending on concept.
- TRL for **sCO2 power conversion at fusion scale** — only CFETR studies exist, no built prototype.
- TRL for **CFEDR divertor** at power plant heat loads.

**Gaps**:
- Tritium breeding blanket maturity for power plant application — `truly-unknown` (depends on which TBM concept CFEDR selects) — **important**
- sCO2 Brayton cycle at fusion scale — `not-yet-sourced` (gen-IV fission sCO2 analogues exist; search DOE/NGNP literature) — **important**
- Tritium processing and handling at commercial scale — `not-yet-sourced` — **important**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **Nb₃Sn**: ITER supply chain established; ~2000 tons total magnet mass in BEST. No supply bottleneck at this scale.
- **NbTi**: Mature commercial supply. No concern.
- **YBCO (REBCO) tape**: Used only in CS HTS sub-coils — limited quantity. Less critical than full-HTS designs. Supply is tighter than LTS but manageable at this scale.
- **Tungsten**: Mature supply (PFC coatings and monoblock divertors); ITER-heritage specification.
- **Tritium**: 110g inventory sourced externally — standard dependency for any D-T device. Sources identify this as external supply, not bred. CANDU/fission supply chain assumed.
- **TBM breeding materials under test**: PbLi (liquid), Li₂TiO₃/Li₄SiO₄ (ceramic), Be₁₂Ti (neutron multiplier) — all at R&D/pilot scale, not yet commercial.

**Missing**:
- Lithium-6 enrichment requirements and supply chain for power plant blanket.
- Be₁₂Ti neutron multiplier manufacturing scale-up assessment.
- PbLi corrosion/activation materials qualification at commercial scale.
- Tritium supply chain for CFEDR-scale operations (many grams/day tritium throughput).

**Gaps**:
- Li-6 enrichment supply chain for commercial blanket — `not-yet-sourced` (OSTI/IAEA tritium supply studies likely exist) — **important**
- Beryllium/Be₁₂Ti scale manufacturing (if HCPB/ceramic breeder selected) — `not-yet-sourced` — **important**
- Tritium throughput at power plant scale (CFEDR) — `derivable` (from TBR × fusion power) — **important**
- PbLi corrosion materials qualification — `not-yet-sourced` — **nice-to-have**

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor (as expected for an experimental device)

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion power target (BEST) | >50 MW (Q≥1), Q~5 burning plasma | BEST Research Plan v1.1, p.20 | high |
| Magnetic field | 6.15 T | BEST Research Plan v1.1, p.16 | high |
| Plasma current | Up to 7 MA | BEST Research Plan v1.1, p.16 | high |
| Plasma volume | 142 m³ | BEST Research Plan v1.1, p.16 | high |
| Auxiliary heating power | ~50 MW nominal, ~71 MW upgrade | BEST Research Plan v1.1, p.18-19 | high |
| Power conversion cycle (lineage) | sCO2 Brayton | CFETR power conversion studies (2021, 2024, 2025) | medium |
| Thermal efficiency (CFETR studies) | 34–40% | CFETR Energy papers (2021, 2024) | medium |
| COOL blanket operating conditions | 8 MPa, 350°C inlet | CFETR COOL Blanket (2024) | medium |
| Company funding | $214M raised; ~$2B registered capital | Neo Fusion company profile | medium |
| Construction timeline | 2023–2027 (first plasma 2027/28) | BEST Research Plan v1.1, p.20 | high |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Plant electrical output (CFEDR/PFPP) | not-yet-sourced | blocking | CFEDR targeted ~1 GWe; CFETR studies suggest ~200–1000 MWe range — search CNKI/OSTI for CFEDR system design |
| Capital cost breakdown (by subsystem) | proprietary / not-yet-sourced | blocking | No public cost estimate for BEST or CFEDR; ITER scaling analogues required |
| O&M costs | not-yet-sourced | blocking | No published O&M estimate; ITER/DEMO analogues needed |
| Capacity factor / availability (power plant) | derivable | blocking | Tokamak availability assumptions derivable from ITER DEMO studies (~75–85%) |
| First wall replacement schedule | not-yet-sourced | important | ITER assumes ~5-year FW lifetime; BEST dossier doesn't specify |
| Blanket replacement interval | truly-unknown (design not committed) | important | Depends on which TBM concept CFEDR selects |
| Tritium breeding ratio (TBR) | derivable | important | TBM testing active but no published TBR for any BEST TBM yet |
| Net electric output (recirculating power fraction) | derivable | important | 50 MW aux heating is large recirculating load; wall-plug efficiency of H&CD systems needed |
| Magnet system cost | derivable | important | Scale from ITER cost data (similar Nb₃Sn technology); ~$1–2B analogue |
| Target Q / fusion gain for power plant | not-yet-sourced | important | CFEDR likely targets Q~10–20; BEST data doesn't specify CFEDR performance |

---

## Source Recommendations

1. **CFEDR/PFPP system design studies** — search OSTI, CNKI, ASIPP publications for "CFEDR design" or "Chinese fusion demonstration reactor" parameters (fusion power, electric output, capital cost projections). *Not-yet-sourced — unverified — confirm existence before searching.*

2. **ARIES / Starfire / EUROfusion DEMO cost studies** as tokamak power plant analogues for capital cost scaling. These are well-documented and directly applicable. `derivable` path.

3. **ITER cost breakdown** (official ITER Organization cost reports) as direct LTS magnet system cost analogue. Publicly available. `derivable` path.

4. **Tokamak availability studies** (EU DEMO, ITER Long-Pulse) for capacity factor and maintenance interval assumptions. Search EUROfusion publications. `not-yet-sourced — unverified — confirm existence before searching.*

5. **Li-6 enrichment supply chain assessments** — search IAEA, DOE fusion fuel cycle reports for tritium/lithium supply chain analyses applicable to commercial tokamak scale. `not-yet-sourced — unverified.*

6. **sCO2 Brayton cycle at industrial scale** — search DOE/NGNP or Sandia National Labs sCO2 pilot plant data for efficiency and cost analogues. Well-documented outside fusion context; fission-sector data directly applicable.

7. **Auxiliary heating H&CD wall-plug efficiency** — published for ITER (NBI ~28% wall-plug, gyrotrons ~50–55%). Search ITER design documents for recirculating power fraction benchmarks.

---

## Summary

**Proceed to full analysis with framing caveats.** BEST is the best-documented concept in this cohort from a device physics standpoint, thanks to the publicly released BEST Research Plan v1.1. The qualitative sections (Data Availability, System Function Challenges, Subsystem Maturity, Materials) can be written thoroughly with high confidence.

The structural constraint is that **BEST is an experimental device**, so the D1+ analysis must explicitly adopt a two-layer framing: (a) what BEST itself tells us about technology readiness, and (b) what the CFEDR/PFPP downstream reactor would look like from an LCOE perspective. The quantitative model will rely on ITER/ARIES analogues for capital cost and should clearly flag this extrapolation. The blanket design uncertainty (5 candidate TBMs, no selection made) creates irreducible branching in cost scenarios that should be modeled explicitly.

No blocking data gaps prevent a D1+ write-up from proceeding. The LCOE model will be analogue-based but defensible — which is appropriate for a pre-CFEDR concept at this stage of development.
