# Gap Assessment: Muon-Catalyzed Fusion (D-T)

## Overall Readiness
**Rating**: Insufficient Data
**Summary**: The source base is extremely thin — three short company-generated or physics-background documents totaling ~6 KB. Acceleron has published no plant study, no cost breakdown, and no independent system-level analysis. The sole quantitative LCOE figure ($0.025/kWh) comes from a single slide claim with assumptions stated but no supporting model. The concept is in early R&D (energy breakeven targeted ~2030), and the most critical physics parameters (300 fusions/muon, 3 GeV/muon production cost) are undemonstrated targets, not validated measurements.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Poor

**Available**:
- Company-generated materials: ARPA-E BETHE presentation (July 2025) and company overview provide system-level intent, energy balance diagram, LCOE target, and roadmap
- Physics background: Wikipedia-derived summary of muon catalysis mechanism, historical experiments (PSI, TRIUMF, RAL), and key parameters (alpha-sticking, fusions/muon at conventional conditions)
- Experimental milestone: Oct 2024 PSI run with compressed D-T — 28 hours continuous fusion (proof-of-concept beam physics, not energy-positive)
- Funding context: ARPA-E BETHE grants + $24M Series A (Dec 2024)

**Missing**:
- Peer-reviewed papers from Acceleron (none identified; company founded 2023)
- Published plant studies or techno-economic analyses from any source
- Independent analysis from national labs or academic groups
- ARPA-E BETHE technical progress reports (may exist but not sourced)
- Historical μCF plant studies from 1980s–90s literature (Soviet, LANL, TRIUMF groups did publish some)

**Gaps**:
- Academic and historical μCF TEA literature — `not-yet-sourced` — **blocking**: would provide the only independent LCOE baseline
- ARPA-E BETHE progress reports — `proprietary/not-yet-sourced` — **important**: may contain engineering detail beyond the slide deck
- Any independent system-level analysis — `not-yet-sourced` — **blocking**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Energy balance structure is documented: 3 GeV/muon → 300 fusions/muon → 25 MeV/fusion → 47% recirculating power fraction (from ARPA-E slide)
- Key physics problem identified: alpha-sticking limits fusions/muon; historical ceiling 100–150, theoretical limit ~300
- Accelerator design concept described: ML-optimized active-target with GEANT4 simulation, 64% assumed electrical-to-beam efficiency
- Heat recycling concept noted (2.5 GeV recovered per muon)
- Fusion cell concept: high-density D-T at 500–1000°C under compression

**Missing**:
- Mechanism for heat recycling is not described — how 2.5 GeV is recovered from the muon source/accelerator exhaust is unspecified
- Fusion cell physics at commercial density: pressure, temperature, geometry, and fusion rate per unit volume are not documented
- How 300 fusions/muon is achieved: what conditions reduce alpha-sticking below the current ~0.5% minimum is not described beyond stating it is the goal
- Revenue from heat sales in LCOE: the slide assumes this as an offset but provides no basis — what heat is being sold, at what temperature, to whom?
- Accelerator efficiency (64%) is assumed; basis not stated

**Gaps**:
- Alpha-sticking reduction mechanism — `proprietary` — **blocking**: this is the central unsolved physics problem; the analysis must bound it
- Heat recycling subsystem design — `proprietary` — **important**: affects recirculating power fraction significantly
- Commercial fusion cell design (pressure vessel, geometry, material) — `proprietary` — **important**: no cost analogue can be built without this
- Revenue-from-heat-sales assumption basis — `proprietary` — **important**: affects apparent LCOE significantly and is non-standard

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- Muon source (accelerator): GEANT4 simulations at R&D stage; active-target concept novel; superconducting version planned for commercial — TRL ~2–3
- Fusion cell: PSI experiments demonstrate proof-of-concept μCF in compressed D-T; commercial-scale cell entirely undesigned — TRL ~3–4 for physics, ~1–2 for engineering
- Balance of plant (Brayton cycle): mature commercial technology — TRL 8–9
- Experimental validation: Oct 2024 PSI run (28 hours) — demonstrates muon-catalyzed fusion in compressed D-T but at beam intensity orders of magnitude below commercial scale

**Missing**:
- TRL assessment for energy recovery system (heat recycling)
- TRL for tritium breeding blanket (design unspecified)
- TRL for high-density D-T fuel handling/circulation at scale
- No accelerator cost scaling or design maturity documentation
- No demonstration of any integrated system (all subsystems tested independently or not at all)

**Gaps**:
- Breeding blanket design and TRL — `proprietary/not-yet-sourced` — **important**: determines tritium self-sufficiency
- Muon source cost and engineering readiness — `proprietary` — **important**: dominant capital cost driver
- Energy recovery subsystem existence and TRL — `truly-unknown` — **blocking**: without this the energy balance claimed cannot be evaluated
- Integrated system test results — `truly-unknown` — **blocking**: no integrated system has been built

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- D-T fuel: standard D-T supply chain challenge (tritium production, handling)
- Lithium-6 for breeding: implied by D-T concept; standard breeder material
- 14.1 MeV neutron flux: requires heavy shielding — standard D-T challenge
- Superconducting accelerator: mentioned as commercial design direction but magnet type unspecified

**Missing**:
- Muon source target material: what the proton beam hits is not specified (tungsten? liquid metal? exotic target?)
- Fusion cell material and pressure vessel specifications: operates at 500–1000°C under compression — material is unspecified
- Superconducting magnet type for accelerator (NbTi, Nb3Sn, REBCO): cost and supply chain implications differ significantly
- Diamond anvil cell used in PSI experiments — this technology is not scalable; what replaces it at commercial scale is not stated
- Tritium inventory estimate for 100 MW plant

**Gaps**:
- Muon source target material — `proprietary` — **important**: may involve exotic or limited-supply materials
- Commercial fusion cell material — `proprietary` — **important**: must survive neutron flux + high pressure at elevated temperature
- SC accelerator magnet type — `proprietary` — **important**: REBCO vs. conventional SC has major cost implications
- Scalable replacement for diamond anvil cell — `truly-unknown` — **blocking**: PSI experiments use lab-scale pressure apparatus; no commercial analog identified

---

### 5. LCOE Parameter Extraction

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| LCOE target | $0.025/kWh | ARPA-E presentation (slide 21) | Low — aspirational claim, no model |
| Recirculating power fraction | 47% | ARPA-E presentation (slide 5) | Low — derived from unvalidated targets |
| Energy per D-T fusion | 17.6 MeV + ~4.8 MeV breeding = ~22–25 MeV | Physics source + ARPA-E | Medium — physics well-established |
| Muon production energy target | 3 GeV/muon | ARPA-E presentation | Low — GEANT4 simulation target, not demonstrated |
| Conventional muon production energy | 5–6 GeV/muon | Physics source | High — experimentally established |
| Fusions per muon (experimental) | 100–150 | Physics source | High — experimentally measured |
| Fusions per muon (target) | 300 | ARPA-E presentation | Low — theoretical limit, not demonstrated |
| Alpha-sticking probability (measured) | ~0.3–1% | Physics source | High — experimentally measured |
| Plant size target | 100 MW (electrical) | Company overview | Low — target only |
| Energy conversion | Brayton cycle | ARPA-E presentation | Medium — mentioned but unspecified |
| Accelerator efficiency (assumed) | 64% | ARPA-E presentation | Low — basis unstated |
| Heat recycled per muon | 2.5 GeV | ARPA-E presentation | Low — mechanism not described |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost breakdown (any subsystem) | proprietary | Blocking | No cost model published; no plant study exists |
| Accelerator capital cost ($/muon/s or $/MW) | proprietary | Blocking | Dominant cost driver; no analog cost data provided |
| Fusion cell capital cost | proprietary | Blocking | No design exists at commercial scale |
| Thermal efficiency of Brayton cycle | derivable | Important | Type unspecified; sCO2 vs. air vs. He — can range 40–55% |
| Capacity factor / availability | truly-unknown | Blocking | No maintenance model; accelerator uptime not discussed |
| O&M cost estimates | truly-unknown | Blocking | No staffing, replacement schedule, or maintenance model |
| Tritium handling cost | derivable | Important | Can be estimated from D-T plant analogs (ITER, DEMO studies) |
| Plant lifetime assumption | truly-unknown | Important | Not stated; affects capital cost amortization |
| Fuel cost (D-T, Li-6) | derivable | Important | Tritium market price well-characterized |
| Revenue from heat sales | proprietary | Important | Included in LCOE claim; basis and magnitude not stated |
| Fusion power density (MW/m³ in cell) | proprietary | Blocking | Required to size fusion cell and derive capital cost |
| Neutron wall loading | truly-unknown | Important | Determines blanket/shield replacement schedule |

---

## Source Recommendations

1. **Historical μCF plant studies (1980s–90s)** — `not-yet-sourced` — search OSTI or Google Scholar for "muon catalyzed fusion power plant" or "muon catalyzed fusion economics" (Petrov, Jones, Jändel, Rafelski). These groups published techno-economic analyses when μCF was seriously considered; they would provide the only published capital cost structure analog. `unverified — confirm existence before searching`

2. **ARPA-E BETHE program technical reports** — `not-yet-sourced` — ARPA-E publishes project-level technical reports for BETHE awards. Acceleron had two NK Labs BETHE grants (2020, 2023); search ARPA-E project database for "NK Labs" or "Acceleron muon" for any published deliverables. `unverified — confirm existence before searching`

3. **PSI experimental papers (2023–2025)** — `not-yet-sourced` — Acceleron ran experiments at PSI in 2024; any co-authored or PSI-authored papers describing fusion yields, pressures, or alpha-sticking at compressed conditions would provide the most current validated physics parameters. Search PSI publications database. `unverified — confirm existence before searching`

4. **Proton accelerator cost literature** — `not-yet-sourced` — SNS (Spallation Neutron Source), ESS (European Spallation Source), and similar GeV-class proton accelerators have published construction cost data. These provide order-of-magnitude analogs for the muon source cost (even if Acceleron's active-target design is more compact). Available from DOE/OSTI reports.

5. **Alpha-sticking experimental papers (RIKEN-RAL, PSI)** — `not-yet-sourced` — The most precise alpha-sticking measurements came from RIKEN-RAL and PSI. These are published in journals (e.g., *Physical Review Letters*, *Hyperfine Interactions*). They set the hard floor on fusions/muon and are needed to bound the "300 fusions/muon" claim. Author: Ishida, Matsuzaki, and collaborators. `unverified — confirm existence before searching`

---

## Summary

**Do not proceed to full analysis without additional sourcing.** The current source base — three short documents, all company-generated — is insufficient to support a credible D1+ analysis. The LCOE target ($0.025/kWh) is a slide-deck aspiration with no published cost model behind it. Every capital cost line item is missing. The two most critical physics parameters (300 fusions/muon, 3 GeV/muon production) are undemonstrated simulation targets, not validated measurements.

What a first-pass analysis *can* do with current sources:
- Build a parametric physics model (energy balance as a function of fusions/muon and muon cost) using the well-established experimental physics
- Bound the minimum requirements for energy breakeven (~300–500 fusions/muon depending on efficiency assumptions)
- Perform a back-solve to show what Acceleron's claimed parameters would need to deliver at $0.025/kWh vs. $0.01/kWh
- Use proton accelerator cost analogs and D-T plant cost analogs as order-of-magnitude capital cost proxies

What it cannot do: produce a defensible absolute LCOE estimate. The analysis should be framed explicitly as a parametric sensitivity study with all capital costs flagged as highly uncertain or missing, and the $0.025/kWh claim treated as a target to audit rather than a baseline to refine.
