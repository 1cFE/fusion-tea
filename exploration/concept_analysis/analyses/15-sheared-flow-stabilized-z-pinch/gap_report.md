Now I have everything I need. Let me write the gap assessment.

---

# Gap Assessment: Sheared-Flow Stabilized Z-Pinch

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: The qualitative picture is well-supported — Zap Energy has published a reactor concept paper (Engineering Paradigms, FST 2023) and maintains an active public communications cadence, providing solid coverage of physics, architecture, and subsystem design intent. However, both key technical papers (FST 2023 and Physics of Plasmas 2023) are paywalled with only snippets captured in Phase 1a, and no capital cost estimates or quantitative plant studies have been published. The quantitative LCOE model will require substantial derivation and analogues, with Q value and recirculating power fraction being the critical unknowns.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate

**Available**:
- Zap Energy website explains the concept clearly and publicly (`zap-energy-website-how-it-works.md`)
- Engineering Paradigms paper (FST 2023) provides reactor-level specs: 190 MWt, 10 Hz, LiPb blanket, TBR ~1.1, ~70% driver efficiency, steam Rankine, ~3 m reactor height — captured via search snippets and a third-party summary (`engineering-paradigms-paper-summary.md`)
- Physics of Plasmas 2023 overview paper exists but is paywalled (no extracted content in Phase 1a)
- Century paper (FST 2025) published — paywalled, but press releases and APS DPP abstract provide operational details (`century-and-fuze-a-updates-2025.md`)
- FuZE-3 results confirmed via ScienceDaily summary (`fuze-3-gigapascal-results-2025.md`) and direct press release
- ARPA-E project page confirms DOE-funded electrode development program
- IEEE Spectrum article available for context

**Missing**:
- Full text of Engineering Paradigms paper (FST 2023) — contains the most complete reactor design details
- Full text of Physics of Plasmas 2023 overview paper
- Any published power plant study with cost breakdown or economic projections
- Zap Energy investor materials or company-published cost projections

**Gaps**:
- Full Engineering Paradigms paper (FST 2023) — `not-yet-sourced` — **important**: snippets provide the key parameters but reactor design details (electrode geometry, blanket thickness, component masses) may be in the full paper
- Full Physics of Plasmas 2023 overview — `not-yet-sourced` — **important**: likely contains confinement scaling and plasma parameter projections
- Any cost or economic analysis — `truly-unknown` (no published estimates identified) — **blocking for quantitative model**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Core physics understood: ohmic heating via axial current, self-generated B-field, sheared-flow stabilization mechanism
- Driver architecture clear: pulsed power capacitor bank + pulse-forming networks, passive design
- Energy flow pathway clear: driver → plasma → neutrons + alphas → LiPb → steam cycle
- Recirculating power pathway partially understood: wall-plug to cathode efficiency ~70%, but end-to-end Q and net electrical output not published
- Rep rate scaling challenge explicitly documented: 0.2 Hz (Century) → 10 Hz (commercial), with power requirement scaling from 39 kW to ~10 MW average input
- Electrode engineering is an active open problem (dedicated ARPA-E project)

**Missing**:
- Q value — FuZE-Q is designed for Q=1 but has not yet demonstrated breakeven; actual current Q is unquantified from available sources
- Plasma scaling laws from current experiments to reactor conditions (1.5 MA FuZE-Q → commercial reactor current requirements)
- Recirculating power fraction at commercial rep rate — this directly determines whether the concept is economically viable
- Confinement time scaling with current and plasma conditions
- Plasma-wall interaction details at high rep rate (electrode erosion, impurity injection)

**Gaps**:
- Q value / fusion gain demonstrated — `truly-unknown` (not yet achieved experimentally) — **blocking**: LCOE depends critically on Q
- Recirculating power fraction at 10 Hz commercial scale — `proprietary` — **blocking**: determines net electrical output
- Plasma scaling from FuZE-3/FuZE-Q to reactor current levels — `not-yet-sourced` (likely in Physics of Plasmas 2023 paper) — **important**
- Electrode erosion/impurity injection rates — `truly-unknown` at the required rep rate — **important**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **Plasma physics / sheared-flow stabilization**: FuZE demonstrated D-T fusion neutrons (confirmed by LLNL, 2021); FuZE-3 achieved 1.6 GPa total pressure — TRL ~4
- **Pulsed power driver**: Century operating at 39 kW average, 500 kA per pulse, 0.2 Hz; passive PFN design is mature at single-shot scale — TRL ~4 at current rep rate, TRL ~2 at 10 Hz target
- **Liquid metal wall system**: Century demonstrates liquid bismuth circulation with thermal management at 100 kW scale; vertically-oriented design validated at engineering level — TRL ~4 for Bi, TRL ~2-3 for LiPb with D-T plasma
- **Steam Rankine energy conversion**: fully mature technology, applicable directly — TRL ~9
- **Electrode technology**: ARPA-E project underway, explicitly described as needing development — TRL ~2-3

**Missing**:
- TRL assessment for tritium breeding loop (LiPb processing, extraction, reinjection)
- Tritium breeding has no experimental validation in this system
- High-rep-rate electrode lifetime data
- Capacity factor projections (maintenance intervals, component replacement schedules)

**Gaps**:
- Electrode lifetime under commercial conditions (500 kA+ at 10 Hz) — `truly-unknown` — **important**: drives replacement cost and availability
- LiPb tritium breeding validation — `truly-unknown` (Century uses Bi, no D-T testing) — **important**
- Rep rate scaling path from 0.2 Hz to 10 Hz — `proprietary` (internal roadmap) / `not-yet-sourced` — **important**
- Capacitor bank lifetime and replacement at commercial rep rate — `truly-unknown` — **important**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- Tritium supply dependency confirmed (D-T fuel); TBR ~1.1 from LiPb blanket, marginally self-sufficient
- LiPb composition confirmed (17% Li, 83% Pb by mass); Li-6 enrichment likely needed for adequate TBR but not explicitly stated
- No superconducting magnets, cryogens, or beryllium — eliminates several common critical material concerns
- No target fabrication requirement (unlike ICF) — eliminates that supply chain challenge
- Lead (Pb): abundant, no supply concerns
- Bismuth: used only for Century (engineering demo), not commercial concept

**Missing**:
- Whether Li-6 enrichment is required (Li-6 fraction in natural Li is ~7.5%; enrichment affects blanket cost significantly)
- Electrode material specifications and supply (high-current-density cathodes at 10 Hz)
- Capacitor bank component supply chain at required scale (large pulsed-power capacitors)
- LiPb total inventory requirement and lead activation concerns
- Tritium inventory requirements and permeation through liquid metal

**Gaps**:
- Li-6 enrichment requirement — `derivable` from TBR analysis — **important**: cost driver if enrichment needed
- Electrode material specification and supply — `proprietary` — **nice-to-have**
- High-rep-rate capacitor bank supply chain — `not-yet-sourced` — **nice-to-have**: analogues from pulsed power industry exist
- Tritium inventory and permeation — `not-yet-sourced` (likely in FST 2023 paper or D-T fusion literature) — **important**

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Reactor thermal power | 190 MWt | Engineering Paradigms, FST 2023 | m (snippet only) |
| Repetition rate (target) | 10 Hz | FST 2023; Zap website | h |
| Current rep rate (Century) | 0.2 Hz | Century press releases | h |
| Drive efficiency (wall-plug → cathode) | ~70% | Engineering Paradigms, FST 2023 | m |
| Energy conversion pathway | Steam Rankine | FST 2023; Ben Bridger blog | h |
| Tritium breeding ratio | ~1.1 | Engineering Paradigms, FST 2023 | m |
| Blanket material | LiPb (17% Li, 83% Pb) | FST 2023; Zap website | h |
| Reactor footprint | ~3 m tall | Engineering Paradigms, FST 2023 | m |
| No external magnets | Confirmed | Multiple sources | h |
| Plasma current range | 650 kA – 1.5 MA | FuZE-Q specs | h |
| Driver bank energy (FuZE-Q scale) | ~1 MJ | fuze-q-and-fuze-3.md | h |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q value (fusion gain) | truly-unknown | blocking | FuZE-Q targets Q=1, not yet demonstrated; current devices likely Q << 1 |
| Net electrical output (MWe) | derivable | blocking | Requires Q and recirculating power fraction; ~63 MWe if 33% thermal efficiency, but recirculating power could dominate |
| Recirculating power fraction at 10 Hz | proprietary | blocking | At 10 MW avg input and 190 MWt output, this is ~5% — but unconfirmed |
| Capital cost by subsystem | truly-unknown | blocking | No published estimates; no analogues cited in sources |
| Pulsed power system specific cost ($/kWe or $/J) | not-yet-sourced | blocking | Analogues from NIF, Z Machine, ICF drivers may exist |
| Electrode replacement cost and lifetime | truly-unknown | important | ARPA-E project active — no data yet |
| Capacity factor / availability | truly-unknown | important | No published maintenance schedule; pulsed systems can achieve high availability in principle |
| Thermal efficiency of steam cycle | derivable | important | ~30-35% for steam Rankine at LiPb temperatures; LiPb operating temperature not published |
| LiPb operating temperature | not-yet-sourced | important | Needed for steam cycle efficiency; likely in full FST 2023 paper |
| Blanket capital cost | not-yet-sourced | important | Liquid metal system analogues (FNSF, tokamak blankets) may provide rough bounds |
| O&M cost fraction | truly-unknown | important | No published estimates; comparable pulsed concepts (Z Machine) are research tools, not commercial analogues |
| Plant electrical output target | proprietary | important | 190 MWt × efficiency − recirculation; Zap hasn't published a MWe target |

---

## Source Recommendations

1. **Full text of Engineering Paradigms for SFS Z-Pinch Fusion Energy (FST 2023)** — `not-yet-sourced` — institutional library access to Fusion Science & Technology would unlock blanket geometry, electrode design, and possibly cost discussion. Search: tandfonline.com DOI 10.1080/15361055.2023.2209131. *Flag: paper confirmed to exist; content beyond snippets unverified.*

2. **Full text of "The Zap Energy approach to commercial fusion" (Physics of Plasmas 2023)** — `not-yet-sourced` — AIP open access check or institutional access. DOI: pubs.aip.org/aip/pop/article/30/9/090603. *Flag: confirmed to exist; AIP PoP articles are sometimes open access after a year.*

3. **Full text of Century paper (FST 2025)** — `not-yet-sourced` — same journal; details on power handling architecture would inform rep-rate scaling and pulsed power cost modeling. *Flag: confirmed to exist; paywalled.*

4. **Pulsed power system cost analogues from ICF or defense literature** — `not-yet-sourced` — search OSTI for pulsed power driver cost studies (e.g., from Z Machine, NIF pulsed power, or NNSA driver technology reports). Z pinch pulsed power is architecturally similar to Z Machine drivers. *Flag: unverified — confirm existence before searching.*

5. **ARPA-E project reports on electrode technology development** — `not-yet-sourced` — ARPA-E project page links are indexed; final technical reports may be on OSTI. Search ARPA-E DE-AR0001554 or similar project number for electrode development deliverables. *Flag: unverified — ARPA-E project confirmed, but final reports may not be public.*

6. **Ben Levitt APS DPP 2025 presentation slides or proceedings** — `not-yet-sourced` — APS DPP proceedings sometimes have extended abstracts with quantitative data. The abstract cited mentions "progress towards commercial fusion." *Flag: abstract confirmed; full slides unverified.*

7. **Tritium permeation and inventory literature for LiPb systems** — `not-yet-sourced` — large body of work from ITER TBM programs, FTF studies. Tritium behavior in flowing LiPb is well-studied in the tokamak context and could provide bounds for SFS Z-pinch. Search OSTI for "LiPb tritium permeation" or "flowing liquid metal tritium inventory."

---

## Summary

**Proceed to full analysis.** The qualitative write-up is well-supported: physics rationale, architecture, device lineage, and the reactor concept's major design choices are all documented from public sources. The Engineering Paradigms paper (FST 2023) provides sufficient anchors (190 MWt, 10 Hz, LiPb, TBR ~1.1, steam Rankine, ~70% driver efficiency) for a first-pass quantitative model.

The quantitative LCOE model will require explicit `derivable` assumptions for most economic parameters, since no capital cost estimates exist in the literature. The critical path is: assume Q=1 (FuZE-Q target, not yet achieved), assume recirculating power from the 10 Hz pulsed power system, estimate thermal efficiency from LiPb operating temperatures, and apply pulsed-power cost analogues for the driver system. The analysis should clearly flag that these are model assumptions, not published data, and the back-solve to $0.01/kWh will be highly informative precisely because no one has published whether this concept can plausibly reach that target.

The two most critical data gaps — **Q value** and **capital cost structure** — are endemic to the current state of the technology (pre-breakeven, no plant study), not sourcing gaps. The qualitative uncertainty section should feature both prominently.
