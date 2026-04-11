# Gap Assessment: Magnetized Target Fusion - Pneumatic Compression (D-T)

## Overall Readiness
**Rating**: Mostly Ready (with significant LCOE-specific gaps)

**Summary**: General Fusion is unusually transparent about physics and architecture for a private fusion company — the concept's operating principle, system configuration, liquid metal roles, and commercial targets are well-documented in peer-reviewed literature and company materials. However, essentially no cost data (capital, operating, or performance-economic parameters) has been published, and several critical commercial-scale subsystems (pneumatic piston array, liquid metal handling at 1 Hz, recirculating power fraction) have no public analogues or estimates. A first-pass LCOE model can be constructed with stated assumptions, but the capital cost side will require analogue-based estimation throughout.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate

**Available**:
- Peer-reviewed physics results from LM26 compression experiments (Nuclear Fusion journal, 2025 — cited in dossier sources)
- FST 2025 paper (Fuel Cycles, doi:10.1080/15361055.2025.2526266): confirms pneumatic pistons, ~4 m cavity diameter, liquid metal composition candidates (Li vs. PbLi), tritium inventory analysis
- IAEA FEC 2025 abstract: 50% scale confirmation, milestone targets (10 keV by 2025, Lawson by 2026)
- Company website: concept description, tritium breeding role, liquid metal wall function, commercial target (300 MWe, ~1 Hz)
- APS 2018 overview: compression parameter ranges (density 10²²→10²⁵ m⁻³, temp 0.1→10 keV, B-field 2→200 T)
- 34 peer-reviewed publications and 210 patents (per company, though most not ingested)

**Missing**:
- Published plant/power study (no equivalent of ARIES, DEMO, or STARFIRE-style plant report)
- Techno-economic assessment or pre-FEED study
- System code outputs (no PROCESS or equivalent published)
- Independent third-party technical reviews

**Gaps**:
- No plant study or system code output — `proprietary` — **blocking** (no structured cost baseline exists)
- 34 peer-reviewed publications largely uninspected — `not-yet-sourced` — **important** (technical details on piston design, liner dynamics, and plasma performance may exist)
- No independent techno-economic analysis published — `truly-unknown` — **important** (academic groups have not yet published MTF cost models)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Clear description of energy flow: fusion neutrons → liquid metal heating → heat exchanger → steam → turbine + piston power
- Understanding of pulsed nature: ~1 Hz, ~1 ms compression, discrete burn events
- Liquid metal triple function (compression medium, neutron absorber, tritium breeder) is well documented
- Plasma formation via Marshall gun (compact toroid) is described

**Missing**:
- **Recirculating power fraction**: Steam from the thermal cycle powers the pistons. The fraction of gross power consumed by piston recharging is undisclosed and could be 20–50%+ — this is the dominant LCOE driver after capital cost.
- **Gain (Q) assumptions**: No commercial Q target has been published. Without Q, net electrical output cannot be calculated.
- **Piston synchronization and reset time**: The pistons must fire, retract, and recharge within 1 second. Whether this is achievable with steam at commercial scale is undocumented.
- **Plasma formation energy cost**: The Marshall gun consumes energy each pulse; no estimate available.
- **Energy balance at 1 Hz**: No published analysis of whether the energy balance (power in from steam to pistons vs. power out from fusion) closes at the commercial scale.

**Gaps**:
- Recirculating power fraction for piston system — `proprietary` — **blocking** (drives net electrical efficiency; cannot close energy balance without it)
- Commercial Q target — `proprietary` — **blocking** (cannot estimate gross fusion power or energy gain)
- Piston reset feasibility at 1 Hz — `not-yet-sourced` — **important** (mechanical engineering papers may exist; search OSTI/Google Scholar for "magnetized target fusion piston repetition" or General Fusion patent filings)
- LM26 → commercial scale-up physics fidelity — `truly-unknown` — **important** (LM26 uses electromagnetic compression, not pneumatic; pneumatic system at commercial scale never tested)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **Plasma injector (Marshall gun / compact toroid)**: Demonstrated at LM26 scale (50% of commercial plasma size). >10 ms confinement time confirmed (peer-reviewed). TRL ~4.
- **Electromagnetic compression (LM26 surrogate)**: Operational. 18 MJ coils, 2 m diameter. Ion temperature increase and 190× density compression confirmed. TRL ~4 for this configuration.
- **Liquid metal handling (basic)**: General Fusion demonstrated liquid lithium contact with plasma (2019). TRL ~3.
- **Steam Rankine BOP**: Mature commercial technology. TRL 9.

**Missing**:
- **Pneumatic piston array at commercial scale**: LM26 uses electromagnetic compression as a surrogate — the commercial pneumatic system has not been tested at any scale representative of the 4 m commercial cavity. This is the most critical undemonstrated subsystem.
- **Liquid metal vortex formation at commercial rep rate**: Whether the liquid metal can form a stable vortex cavity, accept a plasma, be compressed, and be re-established 1×/second is undemonstrated.
- **Tritium extraction system**: Li and PbLi extraction are analyzed in FST 2025 but no experimental demonstration cited.
- **First wall / structural materials**: The liquid metal wall eliminates solid first-wall issues, but the pressure vessel and piston ports must survive radiation and thermal cycling.

**Gaps**:
- Pneumatic piston compression at any scale — `not-yet-sourced` — **blocking** (critical to TRL assessment; patent literature may contain design details; search USPTO/Google Patents for General Fusion piston patents)
- Liquid metal vortex stability at commercial repetition rate — `truly-unknown` — **blocking** (no experiment approaching this has been reported)
- Tritium extraction system TRL — `not-yet-sourced` — **important** (FST 2025 paper covers inventory but not extraction technology maturity)
- Radiation damage to piston actuators/ports — `truly-unknown` — **important** (neutron streaming through piston channels is a unique challenge with no clear analogue)

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- Liquid metal identified as Li or PbLi (FST 2025 — both under evaluation)
- TBR target ~1.5 (Fusion Conclusion blog, dossier)
- Li-6 enrichment needed for tritium breeding from natural lithium is implicit (Li-6 is the active isotope)
- D-T fuel cycle confirmed (standard tritium supply chain issues apply)

**Missing**:
- **Li-6 enrichment requirement**: Li-6 is ~7.5% of natural lithium. Commercial tritium breeding requires enriched Li-6 (typically 30–90%). The commercial enrichment pathway (CECE process or other) is not discussed.
- **Lithium inventory for a 300 MWe plant**: The liquid metal volume at ~4 m cavity at 1 Hz operation is significant. Total plant lithium inventory not published.
- **Piston materials**: The commercial pistons must withstand steam pressure cycling, potentially neutron flux through piston ports, and thermal gradients. Material specifications are not published.
- **Structural materials**: Pressure vessel, piston housing — material choices not disclosed.
- **Lead supply (if PbLi)**: Lead-lithium eutectic is ~83% lead by mass. Large volume requirements; supply chain implications not analyzed.

**Gaps**:
- Li-6 enrichment pathway and cost — `not-yet-sourced` — **important** (standard fusion fuel cycle literature applies; ORNL and ITER documentation are authoritative)
- Plant lithium/PbLi inventory (and associated cost) — `derivable` from cavity geometry and density assumptions — **important**
- Piston material specifications — `proprietary` — **nice-to-have** (analogues from steam/pneumatic engineering exist)
- Tritium startup inventory — `derivable` from TBR target and fusion power assumptions — **important**

---

### 5. LCOE Parameter Extraction

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Plant power output | 300 MWe | LM26 milestones, GF commercialization page | h |
| Repetition rate | ~1 Hz | Multiple sources | h |
| Cavity diameter | ~4 m | FST 2025 paper | h |
| Compression timescale | ~1 ms | APS 2018, technical details | h |
| Pre-compression density | 10²² m⁻³ | APS 2018 | m |
| Peak density | 10²⁵ m⁻³ | APS 2018 | m |
| Pre-compression temperature | ~0.1 keV | APS 2018 | m |
| Target temperature | 10 keV | LM26 milestones, IAEA FEC 2025 | h |
| Energy conversion pathway | Steam Rankine | Multiple sources | h |
| Tritium breeding ratio target | ~1.5 | Fusion Conclusion / dossier | m |
| Plasma scale (LM26) | 50% of commercial | IAEA FEC 2025 | h |
| Commercial deployment timeline | Early-mid 2030s | COMSOL, dossier | m |
| Fuel type | D-T | All sources | h |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Fusion gain Q (commercial target) | proprietary | blocking | Cannot close energy balance or derive gross fusion power |
| Recirculating power fraction (piston steam) | proprietary | blocking | Pistons powered by steam; fraction consumed could dominate net efficiency |
| Thermal efficiency of steam cycle | derivable | important | No steam parameters published; standard Rankine ~33–38% can be assumed |
| Capital cost (any subsystem) | proprietary | blocking | No plant cost study or breakdown published |
| Piston system capital cost | proprietary | blocking | No analogues for this specific system exist in literature |
| Liquid metal system capital cost | not-yet-sourced | important | Molten salt and LBE analogues from fission may provide bounds |
| Annual piston replacement rate | proprietary | important | Mechanical fatigue in pulsed service is the key lifetime driver |
| Liquid metal pump/handling opex | not-yet-sourced | important | Industrial analogues from sodium-cooled fission reactors may exist |
| Plasma injector replacement rate | proprietary | important | Marshall gun wear at 1 Hz × 8760 hr/yr ≈ 31M shots/yr |
| Capacity factor / availability | truly-unknown | important | No published estimate; piston maintenance cycles not disclosed |
| Net plant efficiency (gross to net) | derivable | important | Requires Q, recirculating power, and thermal efficiency |
| Tritium startup inventory cost | derivable | important | Standard D-T fusion economics; ~$30K/g current tritium price |
| Plant footprint / land cost | not-yet-sourced | nice-to-have | No published plant layout |

---

## Source Recommendations

1. **General Fusion patent portfolio** — `not-yet-sourced` — Search USPTO/Google Patents for "General Fusion" assignee. Piston design, synchronization control, and liquid metal vortex formation may be described in patents. Flag as `unverified — confirm existence before searching`.

2. **General Fusion's 34 peer-reviewed publications** — `not-yet-sourced` — The dossier cites company press releases about peer-reviewed publications; the actual papers are likely on Google Scholar under "General Fusion" OR "magnetized target fusion" OR "MTF piston." APS and Nuclear Fusion journal are most likely venues.

3. **OSTI search for MTF system studies** — `not-yet-sourced` — Search OSTI for "magnetized target fusion power plant" or "MTF economics." DOE-funded MTF work (e.g., LANL FRX-L program) may include system-level analyses. Flag as `unverified — confirm existence before searching`.

4. **Lead-lithium / sodium-cooled fission BOP analogues** — `not-yet-sourced` — For liquid metal handling cost analogues, sodium fast reactor (SFR) plant studies (e.g., ARC-100, EBR-II) and Gen IV designs provide documented liquid metal pump, heat exchanger, and piping cost estimates. IAEA and DOE have published these.

5. **ITER tritium systems documentation** — `not-yet-sourced` — For tritium extraction system costs and Li-6 enrichment chain, ITER's tritium breeding and processing documentation (published by ITER Organization) provides quantitative cost analogues usable with stated scale assumptions.

6. **MTF system code / conceptual design study** — `truly-unknown` — No academic MTF plant study equivalent to ARIES (tokamak) is known to exist. If one exists, it would be transformative for LCOE estimation. Consider a search of IAEA Nuclear Fusion and Fusion Engineering and Design for "magnetized target fusion power plant study." Flag as `unverified — confirm existence before searching`.

---

## Summary

**Proceed to full qualitative analysis now; quantitative LCOE requires explicit assumption documentation.**

The qualitative write-up (D1+ sections 1–3) can be completed at good quality with available data. General Fusion's concept is architecturally clear, the physics pathway is well-described, and subsystem TRLs can be assessed with moderate confidence. The key narrative gap — that the commercial pneumatic piston system has never been tested and represents the central unproven engineering bet — is itself well-evidenced and worth stating prominently.

For the quantitative LCOE model, proceed with the following posture:
- **Use 300 MWe output** as the fixed anchor.
- **Assume Q = 5–20** as a range (commercial D-T MTF targets; no published value — document this assumption explicitly).
- **Assume steam Rankine efficiency 33–35%** (standard, no GF-specific data).
- **Assume recirculating power 20–40%** (wide range; this is the single largest uncertainty and should be the primary sensitivity axis).
- **Capital cost**: Use a bottom-up analogue approach: BOP from fission analogues (~$1,000–1,500/kWe), piston/compression system as a novel cost item with wide uncertainty (±50%).
- The back-solve to $0.01/kWh will be informative precisely because the piston recirculating power and capital cost uncertainties are so large — those become the binding constraints to discuss.
