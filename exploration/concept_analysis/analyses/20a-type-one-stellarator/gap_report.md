# Gap Assessment: QI Modular HTS Stellarator - Infinity Two

## Overall Readiness
**Rating**: Mostly Ready (with sourcing gap)

**Summary**: Type One Energy is unusually transparent for a private fusion company — six peer-reviewed J. Plasma Physics papers published in 2025 provide a documented physics basis that most competitors cannot match. The primary gap is that none of these papers have been extracted into the knowledge base, meaning the detailed numerical content from the primary sources is unavailable for parameter extraction. Physics parameters and system architecture are well-characterized from dossier-level research; the major substantive gap is techno-economic data (capital costs, component replacement costs, recirculating power breakdown), which is likely absent from the physics papers and may require analogue estimation.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good (physics/architecture); Poor (economics)

**Available**:
- 6 peer-reviewed J. Plasma Physics papers (2025 Physics Basis collection), including a "comprehensive unified baseline physics design" paper (E65) and a blanket/tritium feasibility paper (E86). This is the strongest published physics basis of any private stellarator concept.
- Published plant-level design targets: 800 MWf / 350 MWe net, Q > 40, R = 12.5 m, A = 10, 9 T on-axis, HCPB blanket, Rankine cycle with reheat (>30% thermal efficiency), TBR = 1.30 (OpenMC verified with 300M particles).
- Maintenance schedule: 2-year continuous power cycle, 30-day planned outages (press release, May 2025).
- Company design review completion announcement — implies internal design maturity beyond what's publicly released.
- CFS partnership for HTS magnet development.
- W7-X lineage provides substantial analogue physics and engineering data (publicly available separately).

**Missing**:
- No extracted source documents in the Phase 1a knowledge base — the 6 papers exist but their numerical content has not been ingested.
- No published cost estimates, plant study with cost breakdown, or system code output (e.g., PROCESS-equivalent).
- No detailed recirculating power breakdown (cryoplant, ECRH, tritium systems, pumping).
- No divertor design specification published (island divertor implied by QI configuration, but not documented at the level of blanket design).

**Gaps**:
- Primary sources not ingested — `not-yet-sourced` — **blocking** for LCOE parameter extraction from primary literature
- Cost/economic data from company — `proprietary` — **important** (central analysis need)
- System code (PROCESS-equivalent for stellarator) outputs — `not-yet-sourced` — **important**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Energy flow skeleton is known: D-T fusion → neutron/alpha energy → HCPB blanket thermalization → Rankine steam → turbine. Standard enough to model at first pass.
- Plasma physics basis is documented: Q > 40 burning plasma, alpha-dominated, ECRH only for startup/trim.
- Steady-state operation with no disruption risk and no current drive power — simplifies recirculating power modeling compared to tokamaks.
- TBR = 1.30 gives tritium self-sufficiency margin and feeds tritium processing load.
- 2-year / 30-day maintenance cycle gives a basis for capacity factor and scheduled outage cost modeling.

**Missing**:
- Recirculating power breakdown: HTS magnets at 9 T require cryoplant at ~20 K; cryoplant parasitic load for a R=12.5 m machine is a significant cost driver that has not been published.
- First wall and divertor heat loads: Power handling for an island divertor in QI geometry at 800 MWf is not publicly characterized at engineering design level.
- Blanket-to-electricity efficiency chain: Stated ">30% thermal efficiency" but the gross electrical output, blanket energy multiplication factor (M_E, expected ~1.1–1.25 for HCPB/Be), and recirculating fraction needed to reconcile to 350 MWe net are not extracted from papers.
- Engineering Q (Q_eng): Net electrical / recirculating electrical is not published; needed for LCOE.
- Divertor design details: Island divertor for stellarator geometry adds non-trivial cost and maintenance complexity not captured in available data.

**Gaps**:
- Gross electrical / recirculating power breakdown — `proprietary` likely, may be `not-yet-sourced` in E65 — **blocking** for quantitative LCOE
- Blanket energy multiplication M_E — `not-yet-sourced` (likely in E86) — **important**
- Island divertor heat load and design — `not-yet-sourced` or `proprietary` — **important**
- Cryoplant parasitic load — `derivable` from first principles (scaling from W7-X or HELIAS studies) but unverified — **important**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- QI stellarator physics: TRL 4–5. W7-X has demonstrated QI confinement and island divertor operation at low fusion-relevant parameters. Infinity Two configuration is optimized via 70,000+ DOE Frontier simulations — high design confidence but no plasma experiments at power-relevant parameters.
- HCPB blanket: TRL 4–5. EU DEMO and ITER Test Blanket Module heritage. Li₄SiO₄/Li₂TiO₃ pebble bed with Be multiplier is reasonably well-characterized from European programs. The adaptation to stellarator geometry (non-cylindrical blanket segments) adds uncertainty.
- Rankine steam cycle: TRL 9. Fully commercial technology. No maturity concern.
- HTS REBCO magnets (wound): TRL 6–7 for tokamak geometry (CFS SPARC basis). TRL 4–5 for 3D stellarator coil geometry — this is the primary manufacturing bet.
- Tritium systems: TRL 4–5 (no D-T facility at the scale needed has been built, though ITER will advance this).

**Missing**:
- No published TRL assessment from Type One Energy for their specific subsystems.
- HTS coil manufacturing readiness: wound REBCO on complex 3D forms at R=12.5m scale has no direct precedent. W7-X used LTS (NbTi/Nb₃Sn). CFS experience is with planar D-coils.
- Island divertor at power-relevant heat loads: W7-X divertor operated at kW-level. Infinity Two requires handling O(100 MW) heat flux.
- First wall materials qualification: no specific material selection documented publicly.
- Remote maintenance system: Not documented in public sources. Complex 3D coil geometry complicates remote handling.

**Gaps**:
- HTS 3D stellarator coil manufacturing TRL — `not-yet-sourced` / `proprietary` — **important**
- Island divertor at power-relevant conditions — `truly-unknown` (no experiment has approached this) — **important** (flags as risk rather than blocking analysis)
- First wall material selection and lifetime — `not-yet-sourced` or `proprietary` — **important**
- Remote maintenance architecture — `proprietary` — **nice-to-have** for cost modeling

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- REBCO tape identified as magnet conductor — global supply chain is a known bottleneck. CFS partnership implies access, but tonnage requirements for 3D stellarator coil geometry at R=12.5m are not published.
- HCPB materials (Li₄SiO₄ or Li₂TiO₃ pebbles, Be/Be₁₂Ti neutron multiplier): EU DEMO program has characterized supply requirements. Beryllium is a controlled, hazardous material with limited qualified suppliers.
- Li-6 enrichment: Required for HCPB breeding. TBR = 1.30 implies sufficient breeding margin. Enrichment to 60–90% Li-6 needed. Supply chain exists but capacity-limited for fusion-scale deployment.
- Tritium: Initial startup inventory required; TBR > 1 enables self-sufficiency after burnin period.

**Missing**:
- Tape length / total REBCO quantity estimate for Infinity Two coil set — not published.
- Beryllium sourcing plan — no public documentation.
- Specific Li-6 enrichment fraction and total Li inventory required — not extracted from E86.
- Manufacturing process for complex 3D coil winding at scale — no public roadmap.
- First wall material choice — not published (will determine activation and replacement supply chain).

**Gaps**:
- REBCO tape quantity for 3D coils at R=12.5m — `not-yet-sourced` / `proprietary` — **important** (major cost driver)
- Beryllium quantity and supplier plan — `not-yet-sourced` (may be in E86) — **important**
- Li-6 enrichment requirements — `not-yet-sourced` (likely in E86) — **important**
- First wall material — `not-yet-sourced` or `proprietary` — **nice-to-have**

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor (parameters known at concept level; quantitative values not extracted from papers)

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion power | 800 MW | J. Plasma Phys. E65 | high |
| Net electrical output | 350 MWe | J. Plasma Phys. E65 | high |
| Thermal efficiency | >30% (Rankine w/ reheat) | J. Plasma Phys. 2025 | high |
| Major radius | 12.5 m | J. Plasma Phys. E65 | high |
| Aspect ratio | 10 | J. Plasma Phys. E65 | high |
| Field strength (on-axis) | 9 T | J. Plasma Phys. E65 | high |
| Plasma gain (Q) | >40 | J. Plasma Phys. E65 | high |
| TBR | 1.30 | J. Plasma Phys. E86 | high |
| Planned outage schedule | 30 days / 2-year cycle | Press release May 2025 | high |
| Capacity factor (planned only) | ~96% (730/760 days) | Derived from above | medium |
| Blanket type | HCPB (Li₄SiO₄/Li₂TiO₃ + Be) | J. Plasma Phys. E86 | high |
| Energy conversion | Rankine steam cycle | J. Plasma Phys. 2025 | high |
| Field periods | 4 | J. Plasma Phys. E65 | high |
| Plasma heating at steady-state | ECRH (small fraction at Q>40) | J. Plasma Phys. E65 | high |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost by subsystem (magnets, blanket, vessel, BOP) | proprietary | blocking | No published cost estimates exist |
| Gross electrical output | not-yet-sourced | blocking | Need to reconcile 350 MWe net; likely in E65 |
| Recirculating power fraction | not-yet-sourced / proprietary | blocking | Cryoplant + ECRH + pumping; needed for Q_eng |
| Blanket energy multiplication M_E | not-yet-sourced | important | Likely in E86; needed for thermal power calc |
| First wall / blanket replacement interval | proprietary | important | Drives operating cost (major component) |
| Coil set mass and cost estimate | proprietary | important | Primary capital cost driver; no analogue published at this scale |
| ECRH system power and cost | not-yet-sourced | important | Small power fraction at burn but capital cost non-trivial |
| Staffing / O&M cost analogues | derivable | important | Use ITER/DEMO O&M models as analogue |
| Tritium startup inventory required | not-yet-sourced | important | Likely in E86 |
| Unplanned outage rate | truly-unknown | important | No operating history; use conservative analogue (~85% availability) |
| Cryoplant size and cost | derivable | important | Scaleable from W7-X with engineering assumptions |
| Plant footprint / construction cost | proprietary | nice-to-have | R=12.5m stellarator will be very large; construction cost non-trivial |

---

## Source Recommendations

1. **Ingest all 6 J. Plasma Physics (2025) Physics Basis papers** — `not-yet-sourced`. These are the primary sources and almost certainly contain gross electrical, blanket energy multiplication, recirculating power fractions, and detailed geometry. The Cambridge collection URL is in the dossier. Priority: **critical before writing the analysis**.

2. **HELIAS reactor studies (Beidler et al., IPP Garching)** — `not-yet-sourced`. HELIAS-5B and similar large-stellarator plant studies provide cost analogue data (coil system, cryoplant, vacuum vessel) for QI stellarators at similar scale. Search: OSTI or Fusion Engineering and Design for "HELIAS reactor study" or "HELIAS-5" — `unverified — confirm existence before searching`.

3. **ARIES-CS compact stellarator study** — `not-yet-sourced`. Published ~2008, ARIES-CS is the most complete public techno-economic study for a modular stellarator. Has CAS cost breakdowns. Different geometry (A=4.5) but provides scaling basis. Search: "ARIES-CS" on OSTI — likely findable.

4. **EU DEMO HCPB blanket cost data** — `not-yet-sourced`. EU DEMO preliminary design studies include HCPB blanket cost estimates per unit area. Relevant for Infinity Two blanket cost modeling. Search: EUROfusion reports or Fusion Engineering and Design for "DEMO HCPB blanket cost" — `unverified — confirm existence before searching`.

5. **W7-X construction cost reports** — `not-yet-sourced`. W7-X (LTS) is the heritage machine. Construction costs (€1B+) provide a scaling anchor for stellarator coil complexity, even though HTS changes the conductor cost curve. Search: public IPP reports or peer-reviewed cost-of-construction analyses — `unverified — confirm existence before searching`.

6. **CFS HTS tape cost projections** — `not-yet-sourced`. CFS has published some HTS tape cost roadmap estimates ($/kA-m) in investor and conference materials. These set the conductor cost floor for any HTS stellarator. Search: CFS white papers, IAEA FEC proceedings.

---

## Summary

**Proceed to full analysis, but extract the 6 J. Plasma Physics papers first.**

Infinity Two is the best-documented private fusion concept for qualitative analysis — the physics basis is peer-reviewed and detailed, the system architecture is clear, and the key engineering bets are identifiable. The qualitative write-up can be written now with high confidence.

For the quantitative LCOE model, the immediate blocker is that the six primary papers have not been ingested. Many of the "missing" parameters (gross electrical, blanket energy multiplication, recirculating power, tritium inventory) are likely present in E65 and E86 and can be extracted with one ingestion pass. Once extracted, the remaining gaps are primarily capital cost estimates, which must be derived from analogues (ARIES-CS, W7-X, HELIAS studies) with transparent uncertainty bounds — the `proprietary` classification applies to company-internal cost estimates, but public analogue estimation is viable and appropriate for a first-pass LCOE.

The most significant substantive uncertainty (not a sourcing gap) is the HTS 3D stellarator coil manufacturing cost at R=12.5m scale. No machine of this type has been built with HTS. This is a genuine `truly-unknown` / `derivable-with-wide-uncertainty` parameter that will dominate the capital cost sensitivity analysis.

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready (with sourcing gap)"
blocking_count: 3
important_count: 8
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Good (physics/architecture); Poor (economics)"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Poor (parameters known at concept level; quantitative values not extracted from papers)"
```
