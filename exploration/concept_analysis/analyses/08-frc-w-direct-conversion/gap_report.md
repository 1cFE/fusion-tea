Now I have everything I need. Let me write the assessment.

---

# Gap Assessment: FRC w/ Direct Conversion

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: Helion has unusually high public transparency for a private fusion company — the working principle, prototype history, fuel cycle, and energy recovery mechanism are all well-documented. All 12 differentiation columns are filled at high confidence. The main gaps are in LCOE-critical parameters: no published capital cost breakdown, D-He3 gain not yet demonstrated (D-T only as of Feb 2026), and net electricity production not yet confirmed. A qualitative D1+ analysis can proceed confidently; the quantitative LCOE model will require explicit assumptions for several key parameters.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate (Rich for physics/concept, Limited for economics)

**Available**:
- **Company website** (`helion-website-technology.md`): comprehensive narrative on working principle, fuel cycle, energy recovery, prototype history, power targets
- **ARPA-E presentation** (`docslib-helion-arpa-e-presentation.md`): quantitative plasma parameters (density, temperature, field, FRC velocity), 50 MW / 2 Hz design point, early energy balance (η·Gain = 0.2×1.2)
- **Wikipedia** (`helion-prototype-generations.md`): full prototype history with measured parameters per generation (Venti triple product, Trenta densities/temperatures/confinement times), funding history, JASON/MITRE criticism summary
- **Contrary Research** (`contrary-research-helion.md`): third-party synthesis including supply chain risk identification and business terms
- **Helion Feb 2026 press release** (`helion-milestones-feb2026.md`): latest performance milestone (150M°C D-T, tritium regulatory approval), confirms D-He3 not yet demonstrated
- **Peer-reviewed literature**: Nuclear Fusion 2011 (Kirtley et al., IPA plasmoid merging) referenced in ARPA-E source — not yet extracted
- **Expert commentary**: PPPL critic (Jassby), DOE's Allain, Ryan McBride (Sandia), Alan Hoffman (FRC)

**Missing**:
- Independent technical assessments beyond JASON/MITRE 2018 summary
- Peer-reviewed publications on Trenta or Polaris performance (most data is company press releases)
- Published plant/system studies (no equivalent of a PROCESS run or system code output)
- Cost analysis from any public source

**Gaps**:
- No peer-reviewed Trenta/Polaris data publications — `not-yet-sourced` — **important** (all performance claims are company-reported)
- JASON/MITRE 2018 technical report — `not-yet-sourced` — **important** (provides independent technical assessment; referenced in Wikipedia but not yet extracted)
- No published plant study for Orion — `proprietary` — **blocking** for quantitative LCOE

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Direct inductive energy recovery mechanism clearly described: expanding plasma pushes back on coils via Faraday induction, no steam cycle (`helion-website-technology.md`)
- 95% round-trip energy recovery claimed on Grande (1M pulses) and required for net electricity (`contrary-research-helion.md`, `helion-website-technology.md`)
- FRC formation, acceleration (>300 km/s), merging, and compression sequence described (`docslib-helion-arpa-e-presentation.md`)
- He3 breeding pathway (DD→T→He3, t½=12.3 yr) described; patent held by Helion
- Key physics challenge identified: simultaneous high compression and plasma stability (`helion-prototype-generations.md`, citing JASON report)
- D-He3 fusion requires ~750M°C; only 150M°C (D-T) demonstrated — gap explicitly flagged in sources
- Pulsed RLC circuit architecture described; capacitor bank as fundamental driver

**Missing**:
- Electrical subsystem modeling: circuit parameters, inductance, discharge timescales — none published
- FRC stability scaling from prototype to commercial field strengths (40 T vs. 15 T demonstrated)
- Wall loading quantification under 1 Hz sustained operation
- He3 capture and recirculation subsystem: no design details published
- Coil and capacitor failure modes under sustained high-rep-rate operation
- Net electricity demonstration: explicitly not yet achieved (not achieved by Dec 2025 per Wikipedia)

**Gaps**:
- FRC stability at 40 T compression not demonstrated — `truly-unknown` — **blocking** (core physics risk)
- D-He3 ignition/gain (requires 4× higher temperature than D-T demonstrated) — `truly-unknown` — **blocking** for commercial concept validation
- Direct energy recovery efficiency at commercial pulse rate (1-2 Hz sustained) — `proprietary/truly-unknown` — **important** (95% is required threshold; only demonstrated at low rate)
- He3 recirculation system design and efficiency — `proprietary` — **important** (unique to Helion; no published data)
- Circuit parameters for quantitative efficiency modeling — `proprietary` — **important**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **FRC formation and merging**: Demonstrated across 7 prototype generations; IPA experiments from 2005-2012; Polaris operating (TRL ~5-6)
- **Magnetic compression**: >8 T on Trenta, 15 T+ on Polaris; 40 T commercial target; TRL ~4-5 for full-scale compression
- **Plasma temperature**: 100M°C (Trenta), 150M°C D-T (Polaris); D-He3 requires ~750M°C — TRL ~2-3 for commercial fuel cycle
- **Capacitor bank**: >50 MJ on Polaris; in-house manufacturing; TRL ~4 at current scale
- **Aluminum pulsed coils**: Fabricated in-house; demonstrated on all prototypes; TRL ~4-5
- **Repetition rate**: Trenta ~1 pulse/10 min; Polaris target 1 Hz (not confirmed achieved); commercial 2 Hz
- **Energy recovery**: 95% claimed at Grande scale (1M pulses); TRL ~4 at small scale, much lower at commercial scale

**Missing**:
- TRL assessments for He3 separation/recirculation (novel; no published data)
- Coil/capacitor replacement schedule and lifetime quantification under commercial rep rate
- Plasma-facing component design for commercial neutron flux
- Power conditioning and grid integration subsystem design
- Tritium handling system TRL (regulatory approval received, but scale details unknown)

**Gaps**:
- He3 separation and recirculation TRL — `proprietary` — **important** (unique subsystem, critical for fuel economics)
- Direct energy recovery at sustained 1-2 Hz commercial rep rate — `proprietary/truly-unknown` — **blocking** (95% efficiency not measured at target rate)
- Long-duration coil/capacitor lifetime (10^9 commercial shot count) — `truly-unknown` — **important** (no analogous pulsed system at this scale)
- Plasma-facing component design for 2.45 MeV neutron flux — `proprietary` — **important**
- Tritium system TRL at commercial throughput — `proprietary` — **nice-to-have** (Helion minimizes external tritium need)

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **Deuterium**: From water; abundant, low-cost — no supply risk
- **He3**: Self-bred via DD→T→He3 decay; no external supply required (key competitive advantage); patent held (`helion-prototype-generations.md`)
- **Aluminum coils**: Standard material, commodity supply; not superconducting — no exotic material requirement (`contrary-research-helion.md`)
- **Coaxial cables**: Copper, aluminum, and "custom-metal alloys" (~720 miles total per Polaris) — custom alloys unspecified
- **High-voltage pulsed capacitors**: In-house manufacturing; Helion itself identified this as "main potential risk" (`contrary-research-helion.md`)
- **No exotic superconductors**: Major advantage vs. tokamak/stellarator approaches — no REBCO or Nb3Sn supply chain dependency

**Missing**:
- Capacitor technology specification: dielectric type, voltage rating, energy density — not published
- Manufacturing scale-up roadmap for capacitors: current production capacity vs. Orion requirements
- "Custom-metal alloys" specification for coaxial cables
- Borated polyethylene and concrete shielding quantities (mentioned but not quantified)
- Neutron-activated component disposal and replacement cost

**Gaps**:
- Capacitor scale-up manufacturing: production volume, cost per unit, replacement rate — `proprietary` — **blocking** (company-identified risk; drives a large fraction of capital and O&M cost)
- Custom alloy specification for cables — `proprietary` — **nice-to-have**
- Component activation and replacement logistics for commercial plant — `not-yet-sourced/derivable` — **important**

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor for quantitative modeling; Partial for structural understanding

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Plant electrical output (Orion) | 50 MWe | Helion website, Wikipedia | H |
| Plant electrical output (future) | 500 MWe | Wikipedia (Nucor agreement) | M |
| Target repetition rate (commercial) | 2 Hz (ARPA-E design point) | ARPA-E presentation | M |
| Target repetition rate (Polaris) | 1 Hz | Helion website | M |
| Direct energy recovery efficiency (claimed) | 95% | Helion website, Contrary | M |
| Energy conversion pathway | Direct inductive (no steam) | All sources | H |
| Fuel input | Deuterium only (He3 self-bred) | All sources | H |
| Compression magnetic field (commercial target) | 40 T | ARPA-E presentation | M |
| Compression magnetic field (Polaris demonstrated) | 15 T+ | Helion website | H |
| Early energy balance (ARPA-E) | η·Gain = 0.2 × 1.2 | ARPA-E presentation | L (old/conceptual) |
| Input energy cost target | <$0.03/MJ | ARPA-E presentation | L (target only) |
| Capacitor bank energy (Polaris) | >50 MJ | Helion website | H |
| Plasma temperature (D-T achieved) | 150M°C (13 keV) | Feb 2026 press release | H |
| Plasma temperature (D-He3 required) | ~750M°C | Contrary Research | M |
| Neutron fraction (claimed, D-He3) | 5% | Helion website | M |
| Operation start target (Orion/Microsoft) | 2028 | Wikipedia, press release | H |
| Pulsed operation mode | Yes; ~24/7 at commercial scale | All sources | H |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost breakdown (Orion) | proprietary | blocking | No published cost; Orion under construction but no price disclosed |
| Fusion gain Q (D-He3) | truly-unknown | blocking | D-He3 not yet demonstrated; D-T only as of Feb 2026 |
| Net electricity demonstrated | truly-unknown | blocking | Explicitly not achieved as of Dec 2025; required before LCOE meaningful |
| O&M cost structure | proprietary | blocking | No public data; capacitor/coil replacement dominates |
| Capacitor replacement cost and schedule | proprietary | blocking | Helion's self-identified main risk; no data |
| Coil replacement cost and lifetime | proprietary | blocking | Critical for O&M; no lifetime data at commercial rep rate |
| Capacity factor / availability | derivable | important | Could estimate from rep rate × pulse duration; no published target |
| Commercial fusion gain Q (design point) | not-yet-sourced | important | ARPA-E gives early design point (Q~1.2 × η=0.2); outdated |
| Thermal waste fraction | derivable | important | ~5% neutrons deposited in shield; can estimate from D-He3 spectrum |
| Plant construction cost (Orion) | proprietary | blocking | Microsoft PPA terms with "significant penalties" suggest real commitment, but cost undisclosed |
| He3 recirculation energy cost | proprietary | important | Parasitic load from He3 capture system unknown |
| Deuterium fuel cost | derivable | nice-to-have | ~$1,000/kg, consumption rate derivable from Q and shot energy |
| Regulatory/licensing cost | not-yet-sourced | nice-to-have | State license obtained; federal NRC pathway unclear |

---

## Source Recommendations

1. **JASON/MITRE 2018 Helion Assessment** — search OSTI or DTIC for the full report (Wikipedia references: "Helion requires 40 T for commercial viability; 8 T in prototype; projected 2023 breakeven") — `not-yet-sourced` — *unverified: confirm existence before searching*

2. **Kirtley et al. (2011), Nuclear Fusion 51(5)** — "Creation of a high-temperature plasma through merging and compression of supersonic FRC plasmoids" — foundational peer-reviewed paper on IPA experiments — `not-yet-sourced` — confirmed cited in ARPA-E source

3. **ARPA-E ALPHA program final reports** — Helion received ARPA-E ALPHA contract (2015) for "Staged Magnetic Compression of FRC Targets"; final technical report may contain design-point parameters — search OSTI for ARPA-E ALPHA Helion final report — `not-yet-sourced` — *unverified: confirm existence before searching*

4. **Alan Hoffman FRC review literature** — quoted as expert in Helion press release (40+ years FRC experience); UW Madison FRC publications may provide scaling law context for compression stability — search Google Scholar for Hoffman FRC reviews — `not-yet-sourced`

5. **Slough et al. IPA papers (2012-2014)** — John Slough (Helion co-founder) published on FRC plasmoid merging pre-commercialization; contains pre-commercial plasma parameters — `not-yet-sourced`

6. **Contrary Research full report** — the sourced file appears to be a summary; the full report may contain more detail on Orion construction cost and timeline — `not-yet-sourced` — *unverified: confirm whether full report is accessible*

7. **DOE Fusion Energy Sciences press coverage of Polaris results** — Jean Paul Allain (DOE FES) quoted in press release; DOE FES may have published a supporting technical summary — search energy.gov/science — `not-yet-sourced` — *unverified*

---

## Summary

**Proceed to full qualitative analysis.** The data is sufficient to write a high-quality D1+ qualitative write-up. The physics mechanism, fuel cycle, prototype progression, maturity gaps, and supply chain risks are all well-documented — primarily from Helion's own communications but with enough external corroboration (ARPA-E, Wikipedia prototype table, expert quotes) to report with appropriate confidence levels.

**For quantitative LCOE modeling**, be explicit that several critical inputs require assumptions rather than extracted values:
- D-He3 fusion gain Q: not yet demonstrated; use ARPA-E early design point (Q~1.2 × η=0.2) with wide uncertainty range
- Capital cost: no public data; must build bottom-up estimate from component descriptions or use cost-per-watt analogues from other pulsed power systems
- Capacitor/coil O&M: structurally the dominant cost driver (company-identified), but completely opaque — flag as the primary LCOE uncertainty

The concept is unusual in that **the binding uncertainty is not the energy conversion system** (well-described and plausible) **but the core plasma physics** — D-He3 fusion has not been demonstrated, and reaching 750M°C from 150M°C demonstrated represents a 5× temperature increase. Any LCOE model should treat fusion gain Q as the primary sweep parameter and back-solve to what Q is needed for commercial viability.
