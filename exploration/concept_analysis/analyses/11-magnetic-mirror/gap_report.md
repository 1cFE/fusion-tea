Now I have everything I need. Let me write the assessment.

---

# Gap Assessment: Magnetic Mirror (D-T)

## Overall Readiness
**Rating**: Significant Gaps

**Summary**: Realta Fusion is unusually transparent for a private fusion startup, and the physics basis for confinement is reasonably well-documented. However, no plant-level cost study exists for Hammir or any successor design — Realta has not published capital cost estimates, blanket specifications, thermal cycle details, or operating cost projections. The LCOE model will depend heavily on historical analogues (MARS study) and engineering extrapolations, with large parametric uncertainty on the most cost-relevant subsystems. Sufficient data exists to produce a credible first-pass model with clearly bounded uncertainty, but it cannot be anchored to Realta's own design.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate

**Available**:
- Physics basis paper (arXiv 2411.06644): Q > 5 modeling, 50m center cell, confinement predictions, design parameter optimization via ML
- APS DPP 2025 (Sutherland): development timeline, Hammir performance targets (Qe > 1, >50 MWe, 3-hour continuous), Anvil purpose
- Fusion Hub spotlight: heating systems, magnets, DEC architecture, stabilization schemes
- Fusion Report interview: performance scaling (~7 MW/m), dual-channel energy conversion, lithium tritium breeding confirmation
- WHAM experiment details: 17 T REBCO magnets, ECH/NBI/HHFW, first plasma July 2024
- SVB funding release: market focus (industrial heat, data centers), CoSMo branding — no technical depth
- Historical analogue: MARS study (1980s) — LiPb blanket, TBR 1.15, ~36% plant efficiency, gridless direct converters (~54% DEC efficiency) — available in dossier citations but not in extracted source documents

**Missing**:
- Pre-conceptual design paper for Hammir (Realta stated expected 2026, not yet published as of research cutoff)
- Any published plant study or system code output with cost estimates
- Detailed engineering specifications for blanket, shield, DEC hardware

**Gaps**:
- Hammir design paper — `not-yet-sourced` (pending publication) — **blocking** for anchored cost estimates
- Published plant cost study — `truly-unknown` at this stage; no one has done a full MARS-equivalent for a modern tandem mirror — **blocking** for capital cost model
- Peer-reviewed journal paper expanding on arXiv preprint — `not-yet-sourced` — **important**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Confinement physics uncertainties identified: DCLC and AIC instability management, classical radial transport quantified as a significant factor (arXiv 2411.06644)
- DEC mechanism described (venetian blinds, axisymmetric, for escaping charged particles); MARS analogue gives ~54% efficiency as a reference
- Performance scaling law is explicit: ~7 MW/m center cell addition at constant input power (Fusion Report interview)
- Stabilization mechanisms described: sloshing ions (DCLC/AIC), vortex stabilization via sheared azimuthal flows, expanders with good curvature (Fusion Hub)
- End-plug sustainment is undemonstrated — Anvil is the device to prove this

**Missing**:
- Validation of DCLC/AIC suppression under D-T relevant density and temperature (WHAM is deuterium-only, sub-breakeven physics)
- End-plug physics demonstration at commercial-scale field and density (Anvil device not yet built)
- Quantification of classical transport degradation in longer center cells
- Thermal cycle selection and system efficiency breakdown (steam vs. sCO2 unconfirmed)
- DEC efficiency for Realta's venetian blind design vs. MARS gridless converters
- Any modeling of recirculating power fraction (critical for Qe calculation)

**Gaps**:
- DCLC/AIC stability at reactor-relevant parameters — `truly-unknown` experimentally — **blocking** for physics confidence
- End-plug sustainment validation — `proprietary` (Anvil will test this, ~2028) — **important** for model credibility
- Recirculating power fraction and overall plant efficiency — `derivable` from Q, DEC efficiency, and thermal cycle assumptions — **important**
- Thermal cycle type — `proprietary` — **important** for efficiency estimates (sCO2 would be ~45-50% vs steam ~35%)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- HTS mirror magnets (REBCO, 17 T): demonstrated at WHAM with CFS-built magnets — TRL ~6 for magnet hardware at WHAM scale; TRL ~3-4 for a full Hammir-scale magnet array
- ECH (110 GHz gyrotron): mature technology, demonstrated at WHAM — TRL ~7-8
- NBI: mature technology, demonstrated at WHAM — TRL ~7-8
- HHFW (High Harmonic Fast Wave): demonstrated at WHAM — TRL ~6
- Mirror physics / tandem mirror concept: WHAM first plasma July 2024 validates basic confinement; tandem mirror physics is at TRL ~3 (sub-scale, no end-plug demonstration)
- WHAM cost: $10M ARPA-E grant; WHAM++ mentioned at "$50M in REBCO tape alone" suggesting magnet-dominated cost

**Missing**:
- TRL for DEC (venetian blinds): no experimental demonstration at any scale — TRL ~2-3
- TRL for tritium breeding blanket: no Realta-specific blanket design published — TRL ~2 for Realta's concept specifically
- TRL for end-plug sustainment in tandem configuration: Anvil is the first test — TRL ~2-3
- Stability of longer center cells (>50m) has no experimental validation
- No data on first wall lifetime or replacement schedule under 14 MeV neutron flux

**Gaps**:
- DEC (venetian blinds) technology readiness — `truly-unknown` at pilot scale — **blocking** for Qe and LCOE calculation
- Tritium breeding blanket TRL — `not-yet-sourced` (MARS study exists; Realta-specific design pending 2026 paper) — **important**
- First wall lifetime under D-T neutron flux — `truly-unknown` for this geometry — **important**
- End-plug sustainment (Anvil) — `truly-unknown` until ~2028 — **important** for technical credibility statement

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- REBCO tape: identified as critical; "$50M in REBCO tape alone for WHAM++" (Fusion Hub) — signals significant magnet cost driver
- HTS magnet supply chain: CFS partnership confirmed for WHAM; CFS is a credible supplier
- Lithium for tritium breeding: confirmed as blanket feedstock (Fusion Report interview); Li-6 enrichment likely required for adequate TBR
- D-T fuel: tritium startup inventory not discussed anywhere in sources

**Missing**:
- REBCO tape quantity for Hammir (not in any source — only WHAM++ estimate available)
- Li-6 enrichment requirements and supply availability
- Tritium startup inventory requirement and source (CANDU reactors, DOE reserve)
- Beryllium: not mentioned, but may be relevant for neutron multiplication depending on blanket design
- Manufacturing scalability of venetian blind DEC electrodes
- Cryogenic system requirements for HTS magnet cooling at Hammir scale

**Gaps**:
- REBCO tape volume for Hammir — `derivable` (scale from WHAM++ estimate using magnet volume) — **important**
- Li-6 enrichment requirements — `derivable` from TBR modeling (needs blanket design) — **important**
- Tritium startup inventory — `not-yet-sourced` (industry-standard D-T startup analysis applies; search OSTI/NRC) — **important**
- DEC electrode manufacturing — `truly-unknown` — **nice-to-have** for first pass
- No supply chain analysis published by Realta — `proprietary` — **nice-to-have**

---

### 5. LCOE Parameter Extraction

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion gain Q | >5 (50m), >10 (longer) | arXiv 2411.06644 | medium |
| Net electric output | >50 MWe (Hammir pilot) | APS DPP 2025 | medium |
| Electric gain Qe | >1 (Hammir target) | APS DPP 2025 | medium |
| Performance scaling | ~7 MW/m center cell | Fusion Report interview | medium |
| Operation mode | Steady-state, 3+ hr demonstrated | APS DPP 2025 | high |
| Center cell length | 50m for Q>5 | arXiv 2411.06644 | medium |
| DEC efficiency (analogue) | ~54% (MARS historical) | Dossier (MARS citation) | low |
| Plant efficiency (analogue) | ~36% (MARS historical) | Dossier (MARS citation) | low |
| TBR (analogue) | 1.15 (MARS, LiPb blanket) | Dossier (MARS citation) | low |
| Magnet field strength | 17 T (WHAM) | WHAM experiment details | high |
| REBCO tape cost signal | "$50M for WHAM++" | Fusion Hub | low |
| Heating technologies | ECH + NBI + HHFW | WHAM, Fusion Hub | high |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost by subsystem (magnets, blanket, BOP, DEC, vacuum vessel) | `truly-unknown` | Blocking | No plant study exists; must use MARS analogues scaled to HTS costs |
| Thermal cycle type and efficiency | `proprietary` | Blocking | sCO2 vs steam changes plant efficiency by ~10 pp; contact Realta or use range |
| Recirculating power fraction | `derivable` | Blocking | Needed to go from Q to Qe; depends on heating power, DEC efficiency |
| Operating costs (maintenance, staffing, component replacement) | `truly-unknown` | Blocking | No Realta data; use tokamak analogues with mirror-specific adjustments |
| First wall replacement schedule | `truly-unknown` | Important | Neutron fluence limits drive O&M cost; no Hammir-specific data |
| Capacity factor target | `derivable` | Important | Steady-state design, but availability TBD; use ~80-90% as analogue assumption |
| Tritium startup inventory and cost | `not-yet-sourced` | Important | Industry standard ~1-2 kg; search NRC/OSTI |
| Blanket type and TBR | `not-yet-sourced` | Important | Realta unspecified; MARS LiPb TBR=1.15 available as analogue |
| DEC capital cost | `truly-unknown` | Important | No commercial DEC hardware exists; pure R&D extrapolation |
| Plant footprint / modular unit size | `not-yet-sourced` | Important | CoSMo brand implies modularity; MARS geometry can bound estimate |
| REBCO tape quantity for Hammir | `derivable` | Important | Scale from WHAM++ $50M signal + magnet geometry |

---

## Source Recommendations

1. **MARS study full text** (Logan 1984, LLNL): OSTI biblio 5981974 — best available analogue for blanket design (LiPb, TBR 1.15), direct conversion efficiency (36% thermal + DEC), and plant layout. Listed in dossier but not extracted as a source document. **Priority: high** — `not-yet-sourced`, confirmed in dossier citations.

2. **Hammir pre-conceptual design paper** (Realta, expected 2026): This is the single highest-value missing document. Will specify blanket type, shielding architecture, plant layout, and performance targets. Monitor arXiv (`tandem mirror`, `Realta`, `Hammir`). **Priority: high** — `not-yet-sourced`, expected soon.

3. **DCLC instability suppression papers**: The arXiv 2411.06644 preprint references prior work on sloshing ions and DCLC management. Search arXiv for Sutherland et al. follow-on papers or related UW-Madison publications on drift cyclotron loss cone stabilization. **Priority: medium** — `not-yet-sourced`, existence plausible but `unverified — confirm existence before searching`.

4. **Direct energy conversion literature (mirror-specific)**: George Miley and/or post-MARS mirror DEC papers. Search OSTI for "direct energy conversion mirror fusion" or "venetian blind direct converter." **Priority: medium** — `not-yet-sourced`, MARS-era papers likely on OSTI; modern Realta-specific DEC unpublished.

5. **Tritium startup inventory studies**: NRC/DOE reports on tritium supply for D-T fusion programs give industry-standard startup inventory estimates (~1-2 kg). Search OSTI or NRC for "tritium supply fusion startup." **Priority: medium** — `not-yet-sourced`.

6. **REBCO tape market and cost**: Search for HTS wire cost studies (e.g., ARPA-E SUMMIT program outputs, or CFS public filings) to anchor the magnet cost component. The $50M/WHAM++ signal is a single weak data point. **Priority: medium** — `not-yet-sourced`, `unverified — confirm existence before searching`.

---

## Summary

**Proceed to full analysis with caveats.** The concept is well-enough understood to produce a first-pass LCOE model, but the model will be heavily analogue-driven. The physics layer (confinement, Q targets, DEC principle) is sufficiently documented. The cost layer is essentially empty — no plant study, no subsystem cost estimates, no thermal cycle specification. 

The recommended approach: (1) extract the MARS study (it's in the dossier citations and on OSTI) as the primary cost analogue, applying scaling corrections for HTS magnets vs. copper coils and modern NBI vs. 1980s beamlines; (2) treat the DEC efficiency and thermal cycle efficiency as the two highest-sensitivity parameters and run sweeps; (3) treat the entire capital cost estimate as ±50% and document this explicitly. The back-solve to $0.01/kWh will be particularly illuminating here given the DEC pathway — the concept has a structural advantage in Q threshold that doesn't apply to thermal-only designs, but DEC cost and reliability are completely unvalidated.
