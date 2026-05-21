I now have enough to write the full gap assessment. Let me compile it.

---

# Gap Assessment: Levitated Dipole (D-T)

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: OpenStar has published one of the most detailed first-principles power plant study of any private fusion startup (arXiv 2602.20564), providing comprehensive physics, engineering, and reactor parameter data for two design points (208 MWe and 75 MWe). The primary gaps are: (1) no dollar-denominated cost data — the paper explicitly defers this to a future publication; (2) no balance-of-plant thermal cycle specification; and (3) plasma confinement scaling is genuinely unknown, leaving Q=15 unvalidated at any fusion-relevant device scale. These gaps are real but do not block a D1+ analysis — enough data exists to structure a quantitative LCOE model with transparent assumptions, with clearly flagged unknowns.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Rich

**Available**:
- arXiv 2602.20564 (Simpson et al., 2026): Full peer-reviewed power plant study with two FOAK design points, 0D power balance, plasma equilibrium, neutron transport (OpenMC), coil FEA, material mass inventories, and quantified duty cycle. Most detailed published plant study of any MFE startup.
- arXiv 2508.17691 (Chisholm et al., 2026): Detailed Junior prototype paper: HTS coil specs, flux pump results, plasma heating systems, first plasma results.
- OpenStar website / news coverage (IEEE Spectrum, Bloomberg, RNZ, NucNet): Company milestones, roadmap (Junior → Tahi → Maui → Tama Nui), funding (~NZD 35M + USD 21M), headcount (~80).
- Wikipedia / LDX heritage literature: Physics heritage and experimental record from MIT LDX (2004–2014).

**Missing**:
- No published LCOE estimates or overnight capital cost values — paper explicitly states it is "in the process of developing" this model and will publish it as future work.
- No published balance-of-plant design (thermal cycle, cooling water systems, power conversion unit).
- No detailed blanket engineering design (beyond Li₂O baseline with TBR 1.1).
- No Tahi design paper (planned, per §5 of 2602.20564).

**Gaps**:
- Dollar-denominated cost model — `proprietary` (OpenStar has a preliminary model, per the paper) — **important** (needed for LCOE, can be estimated by analogy)
- Balance-of-plant specifics — `truly-unknown` (not published anywhere) — **important** (thermal efficiency can be assumed at 40% from the paper's Table 2)
- Confinement scaling validation — `truly-unknown` (no fusion-relevant dipole data exists) — **blocking** for verifying Q=15, but design can proceed with stated assumption

---

### 2. Challenges in Capturing System Function
**Coverage**: Good (challenges are well-articulated in the paper itself)

**Available**:
- Paper explicitly acknowledges the key physics unknown: energy confinement time scaling. No empirical dipole scaling law exists (unlike H-98 for tokamaks). The paper uses Bohm vs. gyro-Bohm scaling as bounding assumptions.
- The paper notes that alpha heating in the good-curvature region "is an ongoing area of active research" and its treatment in the power balance is approximate.
- Good-curvature alpha energy is assumed to be fully radiated — simplified assumption, explicitly flagged.
- Edge pedestal physics is unknown ("the physics defining viable conditions at the plasma edge is not well understood") — treated with tokamak I-mode upper bounds.
- Plasma edge conditions affect confinement and wall loading but are unbenchmarked.
- Duty cycle model is explicitly approximate (5-min dock time is an engineering target, not a demonstrated result).

**Missing**:
- No validated confinement scaling law for dipoles. The LDX data gives one data point at low temperature — extrapolation to 10 keV spans orders of magnitude.
- Alpha particle transport in good-curvature region is estimated, not modeled fully.
- No system code (e.g., PROCESS) output for this concept — the optimization is done in the paper's bespoke code.

**Gaps**:
- Confinement scaling law — `truly-unknown` — **blocking** for validating Q=15 (but stated assumption enables LCOE model construction)
- Good-curvature alpha transport — `truly-unknown` — **important** for power balance accuracy
- Edge pedestal physics — `truly-unknown` — **important** (bounded in the model, so tractable)
- No independent system code validation — `not-yet-sourced` — **nice-to-have** (PROCESS or similar has not been applied to this concept)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial (TRLs not formally stated, but implied by the published record)

**Available**:

| Subsystem | Status | TRL (Implied) | Source |
|-----------|--------|---------------|--------|
| HTS core magnet (REBCO, ~5.6 T) | Demonstrated (Junior, Feb 2026) | TRL 4 | arXiv 2508.17691 |
| On-board superconducting flux pump | Demonstrated at 170 kJ world record | TRL 4 | arXiv 2508.17691 |
| Magnetic levitation system | Demonstrated (Feb 2026) | TRL 4 | Bloomberg, IEEE Spectrum |
| Neon slush cryo reservoir | Conceptual design; no demonstration | TRL 2-3 | arXiv 2602.20564 §2.2.3 |
| 23 T REBCO coil (power plant scale) | Conceptual design; Tahi targets 20 T | TRL 1-2 | arXiv 2602.20564 |
| On-board neutron shield (W/B₄C) | Conceptual; OpenMC modeled | TRL 2 | arXiv 2602.20564 §4.3 |
| CICC REBCO cable (30 kA) | Design concept; not manufactured | TRL 2-3 | arXiv 2602.20564 §4.1 |
| Li₂O tritium breeding blanket | Baseline selection; no engineering design | TRL 2 | arXiv 2602.20564 §2.2.6 |
| Reinforced concrete vacuum vessel | Conceptual design; structural engineering feasible | TRL 2-3 | arXiv 2602.20564 |
| ICRH heating system (power plant) | Design target; Junior uses ECRH only | TRL 3 (in fusion context) | arXiv 2602.20564 §2.2.7 |
| Sacrificial coil replacement system | Conceptual; modular dock/undock design | TRL 2 | arXiv 2602.20564 §2.3.1 |

**Missing**:
- No formal TRL assessment published by OpenStar or any external reviewer.
- No engineering design for tritium extraction and processing system.
- No cryogenic system engineering at power-plant scale (neon slush infrastructure).
- Blanket cooling scheme is explicitly unspecified.

**Gaps**:
- Formal TRL assignments — `not-yet-sourced` — **nice-to-have** (can be inferred from published record)
- Tritium processing system design — `truly-unknown` — **important** (can borrow from ITER/ARC analogues)
- Neon supply/cryo infrastructure — `derivable` — **important** (paper flags hydrogen as an alternative if neon procurement is difficult)
- Blanket cooling scheme — `truly-unknown` — **important** but doesn't block first-pass analysis

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- REBCO tape: Paper gives full tape mass inventory. Reactor A requires **4,320 km** of REBCO tape; Reactor B requires 2,550 km. Paper cites current-generation SuperOx tape and upcoming Faraday Factory "Mirai" REBCO (~30% improvement in engineering current density). These figures allow direct comparison to current production volumes.
- Tungsten: Reactor A uses **1,760 tonnes** of W tiles. Large but commercially available; no fundamental scarcity issue.
- Li₂O: Reactor A blanket requires **3,490 tonnes** Li₂O. Requires enriched Li-6 (natural Li is ~7.5% Li-6). Li-6 enrichment is a supply chain concern — global enrichment capacity is limited and primarily defense-sector.
- B₄C shield: Reactor A requires **82.3 tonnes** — commercially available, no supply concern.
- Inconel 718 inner vessel: 325 tonnes — commercially available.
- Reinforced concrete outer vessel: 38,700 tonnes — no supply concern.
- Neon (cryogen): Paper acknowledges procurement risk and flags hydrogen as alternative. Neon is a byproduct of steel production; supply is geographically concentrated.

**Missing**:
- No analysis of REBCO tape production scale-up requirements. Current global REBCO production is estimated at ~1,000–2,000 km/year; Reactor A requires 4,320 km. This is a potentially severe manufacturing bottleneck. The paper does not address this.
- No Li-6 enrichment supply chain analysis.
- No tritium startup inventory analysis (initial tritium load, external supply from CANDU/ITER).

**Gaps**:
- REBCO tape production scale-up — `not-yet-sourced` — **blocking** for supply chain assessment (search OSTI/IEEE for REBCO market analyses; industry roadmaps from SuperOx, American Superconductor, Faraday Factory)
- Li-6 enrichment capacity — `not-yet-sourced` — **important** (search for fusion Li-6 supply studies; IAEA reports)
- Tritium startup inventory — `derivable` — **important** (can estimate from fusion power × breeding ratio × startup time using published methods e.g., Abdou et al.)
- D supply — `derivable` — **nice-to-have** (deuterium is abundant; not a practical constraint)

---

### 5. LCOE Parameter Extraction
**Coverage**: Good on physics/performance parameters; zero on dollar costs

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electric power (Reactor A) | 208 MW | arXiv 2602.20564, Table 5/9 | High |
| Net electric power (Reactor B) | 74.5 MW | arXiv 2602.20564, Table 5/9 | High |
| Fusion power (Reactor A) | 667 MW | arXiv 2602.20564, Table 9 | High |
| Fusion power (Reactor B) | 237 MW | arXiv 2602.20564, Table 9 | High |
| Thermal power (Reactor A) | 741 MW | arXiv 2602.20564, Table 9 | High |
| Thermal conversion efficiency (η_th) | 40% (assumed) | arXiv 2602.20564, Table 2 | Medium (assumed, not specified) |
| ICRH efficiency (η_aux) | 70% | arXiv 2602.20564, Table 2 | Medium |
| Cryogenic system efficiency (η_cryo) | 1.25% | arXiv 2602.20564, Table 2 | Medium |
| Auxiliary heating power (Reactor A) | 44.5 MW (electrical draw: ~63.6 MW) | arXiv 2602.20564, Table 9 | High |
| Sci Q | 15 (assumed target) | arXiv 2602.20564, §3.3 | Low (unvalidated) |
| Core magnet duty cycle (f_d) | 90.1% (Reactor A), 90.2% (Reactor B) | arXiv 2602.20564, Table 5 | Medium |
| Plant availability factor | 96% | arXiv 2602.20564, Table 5 | Medium |
| Annual maintenance downtime | <2 weeks/year | arXiv 2602.20564, §2.3 | Medium |
| Core magnet dock time | 5 min (design target) | arXiv 2602.20564, §3.2.5 | Low |
| Sacrificial coil lifetime | ~1 year (Reactor A), ~1.4 yr (Reactor B) | arXiv 2602.20564, Table 8 | Medium |
| Semi-permanent coil lifetime | ~12 years (Reactor A) | arXiv 2602.20564, Table 8 | Medium |
| First wall lifetime | ~1.3 yr outboard (W tiles) | arXiv 2602.20564, §4.3 | Medium |
| REBCO tape mass (Reactor A) | 4,320 km / 2,560 tonnes CM | arXiv 2602.20564, Table 5 | High |
| Outer VV mass | 38,700 tonnes reinforced concrete | arXiv 2602.20564, Table 5 | High |
| TBR | 1.1 | arXiv 2602.20564, §3.3 | Medium |
| Core magnet stored energy | 20.8 GJ (Reactor A) | arXiv 2602.20564, §4.1 | High |
| First wall radius | 20.6 m (Reactor A) | arXiv 2602.20564, Table 5 | High |
| Junior prototype cost | < $10M USD | arXiv 2508.17691 | High |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Overnight capital cost ($/kW or $total) | `proprietary` | Blocking | Paper explicitly defers to future publication; preliminary model exists at OpenStar |
| LCOE ($/MWh) | `proprietary` | Blocking | Same — OpenStar has preliminary model |
| REBCO tape unit cost ($/m at scale) | `not-yet-sourced` | Blocking | Key cost driver; current ~$50–100/m but scale matters; search SuperPower/American Superconductor pricing |
| Core magnet fabrication cost | `derivable` | Blocking | Can estimate from tape mass × unit cost + structural materials |
| Vacuum vessel construction cost | `derivable` | Important | Concrete VV is unusual — analogues from large civil engineering projects |
| Balance of plant cost | `not-yet-sourced` | Important | No BoP design exists; use generic fusion BoP fractions from ARIES/PROCESS |
| Tritium cycle operating cost | `not-yet-sourced` | Important | Annual T₂ consumption, breeding efficiency, processing cost — use ITER/ARC analogues |
| Thermal cycle specification | `truly-unknown` | Important | η_th=40% is assumed in model; no Rankine vs sCO₂ decision published |
| Blanket replacement cost & schedule | `truly-unknown` | Important | No engineering design; Li₂O blanket lifetime not specified |
| ICRH system capital cost | `not-yet-sourced` | Important | Use ITER ICRH analogues; ~44.5 MW installed, ~70% efficiency |
| First wall replacement cost | `derivable` | Important | Tungsten tiles ~1.3 yr outboard lifetime; can estimate from W mass × unit cost |
| Staffing/O&M cost | `not-yet-sourced` | Important | No published estimate; use fusion plant analogue (ARIES, DEMO studies) |
| Li-6 enrichment cost | `not-yet-sourced` | Nice-to-have | Annual tritium production; Li-6 is specialty enriched material |

---

## Source Recommendations

1. **REBCO tape unit cost and production roadmap**: Search for market analyses from SuperPower, American Superconductor, Faraday Factory, or academic studies on HTS tape economics. Relevant search terms: "REBCO tape cost learning curve", "2G HTS tape production capacity". `unverified — confirm existence before searching`

2. **Fusion BoP cost fractions**: ARIES and PROCESS/DEMO studies (e.g., Kovari et al., Franza et al.) provide generic BoP cost fractions (~25–40% of plant capital) that can be applied as analogues. These exist in the OSTI database. Search: "PROCESS fusion power plant cost model", "ARIES-ACT balance of plant".

3. **Li-6 enrichment supply chain**: IAEA reports on tritium and Li-6. Search IAEA PRIS or IAEA-TECDOC series. Also: Abdou et al. tritium self-sufficiency studies (several published in Nuclear Fusion journal). `unverified — confirm exact papers before citing`

4. **Tritium startup inventory**: Abdou et al. (2021), "Physics and technology considerations for the deuterium-tritium fuel cycle and conditions for tritium fuel self sufficiency," Nuclear Fusion — cited in the OpenStar paper as ref [58] (Sawan & Abdou 2006 version). Directly applicable for T inventory estimation.

5. **ICRH capital cost analogues**: ITER ICRH system documentation (ITER Design Report, CDA) provides costed subsystem breakdowns. Search ITER.org technical reports.

6. **Dipole confinement scaling**: No published empirical scaling law exists. The LDX papers (Boxer et al. 2010, Davis et al. 2014) are the closest available data — both cited in arXiv 2602.20564. These are the only external validation points for the confinement assumption.

---

## Summary

**Proceed to full analysis.** The OpenStar arXiv 2602.20564 paper is exceptional for a TRL 2–4 concept — it provides reactor-scale design points, detailed material inventories, quantified power balance, neutron transport, and explicit discussion of key unknowns. This is sufficient to support a D1+ analysis structured as:

1. **Qualitative narrative**: Well-supported. Physics, engineering design, prototype status, roadmap, and key challenges are all publicly documented.

2. **Quantitative LCOE model**: Requires analogue-based cost estimation for capital items. The key missing input is REBCO tape cost at scale (most sensitive parameter given 4,320 km for Reactor A). All performance/efficiency parameters needed for a 0D LCOE model are directly available from Table 2, Table 5, and Table 9 of the paper.

3. **Back-solve to $0.01/kWh**: Feasible. The largest sensitivities are: (a) REBCO tape cost learning curve, (b) annual sacrificial coil replacement cost, (c) whether η_th can exceed the assumed 40%, and (d) whether Q=15 is achievable under Bohm-like scaling. These can all be varied parametrically.

**The one structural caution**: the paper explicitly avoids quoting specific capital costs or LCOE values, and OpenStar's own cost model is described as preliminary and unpublished. Any dollar estimates in the D1+ model will be analyst-constructed analogues, not OpenStar-endorsed figures. This should be stated clearly in the analysis.

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 4
important_count: 8
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Rich"
  system_function:            "Good (challenges are well-articulated in the paper itself)"
  subsystem_maturity:         "Partial (TRLs not formally stated, but implied by the published record)"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Good on physics/performance parameters; zero on dollar costs"
```
