# Gap Assessment: Compact Spherical Tokamak - India

## Overall Readiness
**Rating**: Insufficient Data

**Summary**: Pranos Fusion is an extremely early-stage company (founded May 2024, $417K seed) that has published essentially no technical specifications. The two available sources together total ~5 KB of usable content, covering company background and high-level architecture confirmation but zero subsystem details, plasma parameters, or cost data. The data situation is structurally limited by the company's development stage — not by a gap in source collection effort.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Poor

**Available**:
- Company profile: founding date, location, funding (~$417K seed), founders' backgrounds (`pranos-fusion-overview.md`)
- High-level architecture: confirmed D-T fuel, compact spherical tokamak geometry, steady-state operation (`iaea-fuse-pranos-profile.md`)
- Staged experimental roadmap: three device configurations named Ragya, Pragya, PraniQ — no specifications for any
- Engineering milestone: TF coil engineering designs completed (stress analysis + CAD), but material choice not disclosed
- Digital twin platform: "Jenga" integrates MHD, transport, neutronics, thermal-structural, PMI, and plant systems modules — confirms scope of physics being simulated, not performance targets
- India fusion context: IPR's SST-1, Aditya-U, SS-ST (Dec 2025 first plasma) — institutional backdrop only, not directly applicable to Pranos

**Missing**:
- Any technical papers, preprints, or conference presentations (none found as of March 2026)
- Any patents
- Plasma parameters (temperature, density, confinement time, Q target)
- Machine dimensions or aspect ratio
- Power output basis beyond marketing claim (50 MW per module)
- No company publications; website is JS-rendered and extractable content was minimal

**Gaps**:
- Technical publications — `truly-unknown` (company has not published anything) — **blocking**
- Transparent technical disclosures (patents, preprints) — `proprietary` (likely internal only at this stage) — **blocking**
- Expanded IAEA FUSE portal content — `not-yet-sourced` (portal may have more detail than the one-page profile captured) — **important**

---

### 2. Challenges in Capturing System Function
**Coverage**: Poor

**Available**:
- Confinement approach confirmed (compact spherical tokamak, D-T), which establishes the gross physics regime
- Existence of a digital twin platform (Jenga) suggests they are modeling the full system, but outputs are not public
- General spherical tokamak physics literature (external to these sources) can inform the analysis by analogy to Tokamak Energy, Commonwealth Fusion, ST40, etc.

**Missing**:
- Heating scheme — unknown; cannot assess heating power requirements, recirculating power fraction, or cost
- Magnet type — unknown; this is the single largest cost uncertainty for a compact tokamak. HTS vs. LTS vs. resistive determines capital cost structure dramatically
- Blanket architecture — unknown; determines tritium breeding ratio, neutron multiplication, thermal output, and first-wall replacement schedule
- Plasma scenario assumptions — unknown; Q, beta, confinement time determine whether the 50 MW claim is plausible
- Claimed performance basis — the 50 MW / 2,500 module vision appears to be a marketing concept, not a physics-validated design point

**Gaps**:
- Heating system architecture — `truly-unknown` — **blocking**
- Magnet type — `truly-unknown` (or `proprietary`) — **blocking**
- Blanket/tritium system architecture — `truly-unknown` — **blocking**
- Plasma scenario parameters (Q, beta, tau_E) — `truly-unknown` — **blocking**
- Validation of 50 MW design point — `proprietary` (Jenga may have outputs, not published) — **blocking**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Poor

**Available**:
- TF coil: engineering designs (stress analysis + CAD) completed — confirms design activity at early engineering level, but material not disclosed
- Digital twin: Jenga platform covers the right physics domains (neutronics, transport, thermal-structural, PMI, plant systems) — computational capability exists, but no validation data published

**Missing**:
- TRL for every major subsystem: magnets, heating systems, blanket, vacuum vessel, tritium handling, energy conversion, control systems
- Any experimental plasma results (the "glass globe" plasma mentioned in sources is a benchtop demo, not a fusion device)
- First device (Ragya) specifications or timeline
- Any analogue to published TRL assessments available for comparable concepts (Tokamak Energy, Spherical Tokamak at Culham)

**Gaps**:
- Magnet TRL and material — `proprietary` — **blocking**
- Heating system TRL — `truly-unknown` — **blocking**
- Blanket TRL — `truly-unknown` — **blocking**
- First device (Ragya) specifications — `proprietary` — **important**
- Experimental results from any plasma device — `truly-unknown` (company appears pre-plasma) — **blocking**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- D-T fuel confirmed → tritium supply chain dependency exists by definition (tritium scarcity, CANDU sourcing or future breeding, ~$30K/g)
- D-T → 14.1 MeV neutrons → heavy shielding or integrated blanket required (structural fact, not specific to Pranos)
- Indian industrial context: India has fusion infrastructure at IPR but no domestic HTS magnet manufacturing capability at scale; HTS tape is primarily sourced from US/Japan/EU/South Korea

**Missing**:
- Magnet material → cannot assess HTS tape supply chain (REBCO vs. BSCCO), cryogenic plant requirements, or cost
- Blanket material → cannot assess Li-6 enrichment needs, beryllium or alternative multiplier needs
- First-wall material → unknown
- Any supply chain analysis or manufacturing partnership disclosures

**Gaps**:
- Magnet material supply chain — `derivable` only after magnet type determined — **important**
- Tritium breeding blanket material — `truly-unknown` — **important**
- First-wall / PFC material — `truly-unknown` — **important**
- India-specific manufacturing constraints for fusion components — `not-yet-sourced` (IAEA country reports, IPR publications on Indian fusion industrial base may exist) — **nice-to-have**

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Target electrical output | 50 MW per module | `pranos-fusion-overview.md` | low (marketing claim) |
| Operation mode | Steady-state | Dossier (inferred) | medium |
| Fuel type | D-T | `iaea-fuse-pranos-profile.md` | high |
| Energy capture pathway | Thermal (cycle unspecified) | Dossier (inferred from D-T) | medium |
| Fleet vision | 2,500 × 50 MW modules | `pranos-fusion-overview.md` | low (aspirational) |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost estimates (any subsystem) | truly-unknown | blocking | No plant study; no cost disclosures |
| Magnet system cost | truly-unknown | blocking | Material unknown; dominant cost driver for compact tokamak |
| Blanket system cost | truly-unknown | blocking | No blanket architecture disclosed |
| Balance of plant cost | truly-unknown | blocking | Thermal cycle not specified |
| First wall / PFC cost and replacement schedule | truly-unknown | blocking | No first-wall material disclosed |
| O&M cost structure | truly-unknown | blocking | No operational parameters |
| Tritium handling cost | derivable | important | Can use ITER/CANDU analogues once scale known |
| Thermal efficiency | truly-unknown | blocking | Cycle not specified; sCO2 vs steam Rankine has meaningful efficiency difference |
| Capacity factor / availability | derivable | important | Can assume ~85% for steady-state tokamak by analogy; no Pranos-specific basis |
| Fusion gain Q | truly-unknown | blocking | No plasma parameters disclosed; cannot validate 50 MW output claim |
| Plasma heating power (recirculating fraction) | truly-unknown | blocking | Heating method unknown |
| Net electric output (gross – recirculating) | truly-unknown | blocking | Requires Q and heating scheme |
| Plant lifetime | truly-unknown | important | No design specifications to inform lifetime |
| Construction cost (overnight) | truly-unknown | blocking | No cost data exists |
| LCOE (published or analogous) | truly-unknown | blocking | No plant study exists for this concept |

---

## Source Recommendations

1. **IAEA FUSE Portal full entry** — The captured profile may be a subset of a longer portal page. Check if additional technical tabs exist. — `not-yet-sourced` — *unverified, confirm before searching*

2. **arXiv / ResearchGate — Shaurya Kaushal author search** — The co-founder has 11 publications (per LinkedIn/Fusion Energy Base); check if any post-2024 papers relate to compact spherical tokamak design or the Jenga platform. — `not-yet-sourced` — *unverified — PhD work was NOT in plasma physics, so post-founding output is uncertain*

3. **OSTI / NTI / IPR publications on Indian spherical tokamak** — IPR's SS-ST (first plasma Dec 2025) may have associated design papers that inform generic compact spherical tokamak parameters in the Indian context. — `not-yet-sourced`

4. **FIA 2025 Supply Chain Survey** — Pranos is listed among 22 responding companies. The survey may contain company-submitted technical parameters. — `not-yet-sourced` — *unverified — check if survey data is published or restricted*

5. **Fusion Energy Base extended profile** — The Fusion Energy Base entry may have been updated since iter-01 capture (particularly following the Dec 2024 stealth exit). — `not-yet-sourced`

6. **Analogous compact spherical tokamak plant studies** — For LCOE modeling, use analogues from Tokamak Energy (ST40/ST80 published parameters), STEP programme (UKAEA spherical tokamak power plant study), and SPARC/ARC (compact HTS tokamak) as proxy cost structures. These are external references, not Pranos-specific, but are the only viable path to a quantitative model. — `derivable` basis

---

## Summary

**Do not proceed to a Pranos-specific quantitative LCOE analysis as though it reflects Pranos's actual design.** The data is structurally insufficient: Pranos Fusion has disclosed no plasma parameters, no magnet specifications, no blanket architecture, no heating scheme, no cost data, and no experimental results. Every LCOE parameter would require assumption without Pranos-specific basis.

**Recommended path**:
1. Attempt one additional source sweep (IAEA FUSE full portal, arXiv Kaushal search, FIA survey) to confirm no technical publications have been missed.
2. Write the qualitative D1+ sections using available information — the data supports a candid assessment of a very early-stage concept with high uncertainty, which is itself analytically informative.
3. For the quantitative model, build it as a **generic compact spherical tokamak** parameterized by HTS tokamak analogues (STEP, ST40/ST80, SPARC), clearly labeled as analogue-based rather than Pranos-specific. This is the honest and useful framing given the data situation.
4. The back-solve to $0.01/kWh exercise can still be performed meaningfully using the generic compact tokamak model.

## Structured summary (machine-readable)

```yaml
overall_rating: "Insufficient Data"
blocking_count: 12
important_count: 3
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Poor"
  system_function:            "Poor"
  subsystem_maturity:         "Poor"
  materials_supply_chain:     "Poor"
  lcoe_parameter_extraction:  "Poor"
```
