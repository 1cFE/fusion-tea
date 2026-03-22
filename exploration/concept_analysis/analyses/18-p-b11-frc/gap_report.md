Now I have everything I need. Let me write the assessment.

---

# Gap Assessment: p-B11 FRC

## Overall Readiness
**Rating**: Mostly Ready (with significant quantitative constraints)
**Summary**: TAE Technologies is unusually transparent for a private fusion company — public press releases, a 2025 Nature Communications paper, multiple New Atlas interviews, and a detailed FAQ provide solid coverage of concept architecture and physics strategy. The qualitative write-up can be produced at high quality. However, the quantitative LCOE model will be severely constrained: no plant cost study exists, no Q value or power balance has been published, and the physics gap between current experiments (~1 keV electrons, 40 ms lifetimes) and Da Vinci targets (~250 keV ions, sustained) is multi-order-of-magnitude and not publicly bridged. LCOE modeling will require heavy use of analogues and explicit assumptions about parameters that are either proprietary or genuinely unknown.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate

**Available**:
- Machine architecture and concept physics: well-covered by Grokipedia summary, Nature Comm 2025 paper, TAE FAQ, and C-2W machine details
- Development roadmap and timeline: DJT merger announcement provides construction (2026), first plasma (2029), net energy (2030), power ops (2031)
- Plant size targets: 50 MWe initial, 350–500 MWe at scale (ANS Nuclear Newswire, DJT merger)
- Company financials: $1.2–1.3B raised, DJT merger >$6B valuation, 2,500+ patents
- NBI system: eight-injector spec, 13 MW at 15–40 keV (C-2W), formation breakthrough in Nature Comm 2025
- Energy conversion pathway: thermal/steam confirmed for Da Vinci (TAE FAQ); ICC patents documented (US7459654, US6628740, US6888907)
- p-B11 fuel cycle: physics well-known; 2023 first magnetically-confined p-B11 fusion (with NIFS Japan)

**Missing**:
- Peer-reviewed engineering or plant design papers (only one physics paper; no system code publications)
- Published cost estimates or techno-economic analysis for Da Vinci
- Investor technical presentations (likely contain more detail; not publicly available)
- Engineering design documents for Da Vinci (none published)

**Gaps**:
- No published plant study — `proprietary` — **blocking** for quantitative LCOE; must rely on analogues
- No peer-reviewed papers on Da Vinci engineering design — `proprietary/not-yet-sourced` — **important** for subsystem TRL assessment
- No published system code or power balance study — `proprietary` — **blocking** for recirculating power and net efficiency

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- High-level identification of novel subsystems: NBI-only formation (new), ICC direct conversion (patented but not deployed), X-ray capture (early research)
- Known physics challenge: p-B11 requires ~100–250 keV plasma temperatures; C-2W achieves ~1 keV electrons — a ~2-order-of-magnitude gap
- Energy conversion tension: steam turbine (Da Vinci baseline) vs. ICC (future) — sources resolve this clearly
- NBI as quadruple-duty system (formation, heating, current drive, stabilization) is well-documented

**Missing**:
- Recirculating power fraction: NBI wall-plug efficiency at reactor scale (~10–30% typical for NBIs; critical for p-B11 power balance) — not in any source
- Q value target for Da Vinci: nowhere stated publicly; C-2W is orders of magnitude below Q=1
- Alpha particle confinement efficiency in FRC geometry at reactor temperatures
- Soft X-ray energy fraction: p-B11 produces significant bremsstrahlung and synchrotron losses; how these are handled in Da Vinci's heat balance is not discussed
- Detailed power flow model (NBI in → plasma heating losses → fusion alpha energy → thermal/steam extraction → net electricity)

**Gaps**:
- Q value (fusion gain) for Da Vinci — `proprietary` — **blocking** for any LCOE model; must assume or bracket
- NBI wall-plug efficiency at reactor-relevant energies — `not-yet-sourced` — **blocking** for recirculating power calculation; NBI literature exists but TAE specifics are proprietary
- Recirculating power fraction — `derivable` from NBI efficiency assumptions + power balance — **blocking** if not derived
- X-ray/bremsstrahlung losses at 250 keV — `derivable` from p-B11 physics — **important**; this is the key loss channel for aneutronic p-B11 and substantially degrades effective Q
- Alpha particle confinement in FRC at burn temperatures — `truly-unknown` (open physics question) — **blocking** for high-fidelity analysis; use TBD/range approach

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- NBI system (experimental scale): well-characterized at 13 MW, 15–40 keV; TRL ~6 for current implementation
- FRC plasma formation (NBI-only): demonstrated on Norm (2025); TRL ~4–5 for NBI-only approach
- p-B11 fusion in magnetically confined plasma: first demonstration 2023 (with NIFS); TRL ~2–3
- Steam turbine BOP: commercial technology, TRL ~9
- Copper/resistive coil magnets for FRC equilibrium: demonstrated on C-2W/Norman; TRL ~6

**Missing**:
- NBI at reactor-relevant energies: Da Vinci will need MeV-range beams for p-B11 (vs. 15–40 keV on C-2W); no sources address this upgrade path
- ICC direct conversion hardware: only patents and theoretical descriptions; no prototype demonstrated
- Da Vinci magnet design: unconfirmed whether resistive or superconducting at reactor scale
- First wall materials for high-X-ray aneutronic environment: not discussed in any source
- Divertor/exhaust system for FRC at reactor scale: FRC's open-field-line exhaust is a known challenge; not addressed in sources
- High-temperature plasma sustainment: C-2W achieves ~1 keV; Da Vinci needs ~250 keV — the intermediate steps are entirely unspecified

**Gaps**:
- High-energy NBI at reactor scale (MeV-range) — `not-yet-sourced` — **important**; ITER NBI and SNL neutral beam literature may provide analogues
- ICC prototype/TRL — `proprietary` — **important** for long-term cost modeling; treat as speculative future upgrade
- Da Vinci magnet design specification — `proprietary` — **important**; low impact given FRC's near-unity beta, but needed for completeness
- First wall materials spec — `proprietary` — **important**; X-ray and alpha bombardment environment differs substantially from D-T
- FRC divertor at reactor scale — `not-yet-sourced` — **important**; FRC open field line exhaust design is an active research area

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- Fuel: hydrogen (abundant) and boron-11; TAE notes fuel is "virtually inexhaustible"
- No tritium required — explicitly documented; eliminates Li-6, Li breeding blanket
- No heavy neutron shielding — documented; hands-on maintenance possible
- Copper coils for current machines (standard, no special supply chain)
- TAE holds 2,500+ patents, suggesting significant proprietary manufacturing IP

**Missing**:
- Boron-11 enrichment: natural boron is ~80% B-11 / ~20% B-10; reactor-grade enrichment requirements, supply chain, and cost not discussed in any source
- NBI injector materials at high energy: ion source grids, accelerator electrodes subject to erosion; reactor-scale replacement cycle
- ICC electrode materials: segmented electrodes operating in 5 MHz / 0.6 T fields; no materials specification exists publicly
- First wall material for soft X-ray and alpha environment
- Any manufacturing bottleneck analysis

**Gaps**:
- B-11 enrichment supply chain and cost — `not-yet-sourced` — **important**; this is a recurring gap in p-B11 concept analyses; IAEA/DOE boron isotope reports likely exist
- NBI injector longevity and replacement schedule — `not-yet-sourced` — **important** for O&M cost; ITER NBI maintenance data may provide analogues
- ICC materials and manufacturing — `proprietary/truly-unknown` — **nice-to-have** for baseline Da Vinci (steam BOP), **important** if modeling long-term direct conversion path
- First wall erosion lifetime — `truly-unknown` — **important** for capacity factor and O&M; p-B11 alpha bombardment of vessel walls is a novel environment

---

### 5. LCOE Parameter Extraction

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Plant electrical output (initial) | 50 MWe | DJT merger announcement / ANS Newswire | h |
| Plant electrical output (mature) | 350–500 MWe | DJT merger announcement | m |
| Construction start | 2026 | DJT merger announcement | h |
| First plasma | 2029 | DJT merger announcement | h |
| Net energy capability | 2030 | DJT merger announcement | h |
| Power operations | 2031 | DJT merger announcement | m |
| Energy conversion type | Thermal/steam (Da Vinci baseline) | TAE FAQ, New Atlas | h |
| Thermal efficiency (steam) | ~30–35% (analogue, not stated) | Standard steam cycle | m (analogue) |
| Fusion reaction energy per event | 8.7 MeV (3 alphas) | p-B11 physics | h |
| Target plasma temperature | ~250 keV (~3 billion °C) | Grokipedia (Da Vinci target) | m |
| Fuel cost (H, B-11) | Very low (order: negligible) | General knowledge | m |
| No tritium breeding blanket cost | N/A (eliminated) | Multiple sources | h |
| No heavy shielding cost | Minimal (eliminated) | TAE website | h |
| Operation mode | Steady-state | Multiple sources | h |
| Magnet type (experimental) | Copper/resistive | C-2W machine details | h |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q value / fusion gain (Da Vinci) | proprietary | blocking | No public statement; C-2W is far sub-breakeven; must bracket (e.g., Q=2–10) |
| NBI wall-plug efficiency at reactor scale | not-yet-sourced | blocking | Determines recirculating power; current C-2W NBI is 13 MW input; Da Vinci NBI scale/efficiency unknown |
| Recirculating power fraction | derivable | blocking | Must derive from Q + NBI efficiency assumptions; dominates net LCOE for beam-driven concepts |
| Total plant capital cost | proprietary | blocking | No estimate published; no plant study exists; will need analogue-based estimate |
| Capital cost by subsystem (CAS breakdown) | proprietary | blocking | No published breakdown; rough analogues only |
| O&M cost estimate | proprietary | blocking | No published data; must estimate from fusion plant analogues |
| NBI system capital cost at reactor scale | not-yet-sourced | important | ITER NBI cost data may provide analogue (unverified — confirm existence before searching) |
| Capacity factor / availability | truly-unknown | important | Steady-state is favorable, but first wall and NBI maintenance schedules unknown |
| NBI injector replacement schedule | not-yet-sourced | important | Drives O&M; ITER injector maintenance literature may help (unverified) |
| ICC capital cost (if modeled) | proprietary/truly-unknown | nice-to-have | Only relevant if modeling long-term direct conversion path |
| B-11 fuel cost (enriched) | not-yet-sourced | important | Enrichment cost largely unknown; natural boron is cheap but reactor-grade B-11 may not be |
| Plant construction cost (Da Vinci) | proprietary | blocking | Only "smaller and less expensive" claims; no dollar figure |
| Bremsstrahlung/synchrotron loss fraction | derivable | important | Physics is known; p-B11 at 250 keV loses significant energy to radiation; quantifiable from first principles |
| Alpha particle confinement fraction in FRC | truly-unknown | blocking | Required for effective Q calculation; open physics research question |

---

## Source Recommendations

1. **B-11 enrichment costs and supply chain** — search IAEA Nuclear Data Section, DOE isotope program reports, or ORNL stable isotope production literature — `not-yet-sourced`
2. **High-energy NBI capital and O&M cost analogues** — ITER NBI system cost estimates from ITER Organization project documentation or F4E procurement reports — `not-yet-sourced` — *unverified — confirm existence before searching*
3. **p-B11 plasma physics: bremsstrahlung losses and effective Q ceiling** — published plasma physics literature (e.g., Nevins & Swain, Nuclear Fusion 2000, on p-B11 reactivity; Rider critique papers) — `not-yet-sourced` — these papers are well-known in the fusion community and likely exist; search Google Scholar for "proton boron-11 reactivity bremsstrahlung"
4. **FRC power plant conceptual studies** — search OSTI for "field-reversed configuration power plant" or "FRC reactor study"; older DOE system studies (1980s–1990s) may give rough cost analogues even if based on different FRC physics — `not-yet-sourced` — *unverified — confirm existence before searching*
5. **TAE engineering publications** — IAEA Fusion Energy Conference proceedings (FEC) often include TAE contributions (Gota et al.); these may contain more detailed machine parameters than press materials — `not-yet-sourced`; dossier cites "IAEA FEC papers (Gota et al.)" as a source type but none are extracted
6. **Da Vinci reactor design details** — likely in TAE investor presentations or technical roadmap documents; not public — `proprietary`; no search strategy will resolve this

---

## Summary

**Proceed to full analysis**, with explicit acknowledgment of quantitative constraints. The qualitative write-up (data availability, system function challenges, subsystem maturity, materials) can be produced at high quality with available sources — TAE is more communicative than most private fusion companies and the physics architecture is well-documented.

The quantitative LCOE model is feasible but will be built almost entirely on assumptions and analogues for the cost-driving parameters. The two binding constraints are: **(1) Q value** — must be assumed; literature on p-B11 physics suggests a ceiling well below tokamak-class D-T concepts due to bremsstrahlung losses, and this should be quantified using published reactivity data rather than TAE's aspirational claims; and **(2) NBI recirculating power** — for a beam-driven concept, this is the dominant factor in net LCOE and is essentially unknown at reactor scale. Before running the model, sourcing the Nevins & Swain (or equivalent) p-B11 reactivity analysis would substantially improve the Q-ceiling estimate and is likely the highest-value pre-analysis data acquisition step.
