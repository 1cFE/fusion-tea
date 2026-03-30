Now I have everything needed to write the assessment.

# Gap Assessment: Levitated Dipole (D-T)

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: OpenStar has published two peer-reviewed preprints (Junior prototype design and a detailed D-T power plant study) that provide unusually rich physics, magnet, shielding, and performance data for a TRL 4-5 concept. The primary gaps are in absolute capital costs and LCOE (explicitly deferred by the authors), energy conversion cycle selection, and tritium blanket cooling details — none of which block a high-quality qualitative analysis, and all of which can be handled with stated assumptions in LCOE modeling. The concept is well-suited for a D1+ analysis now, with clear flags on what Tahi (~2028) must validate.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**:
- Two substantial arXiv preprints: `arxiv-2508-17691` (Junior prototype design, test results) and `arxiv-2602-20564` (D-T power plant design study with two reactor variants). Both are detailed engineering papers, not press releases.
- IEEE Spectrum article (`openstar-prototype-roadmap.md`) providing program context and independent commentary
- Bloomberg article (`openstar-2026-funding-tahi-timeline.md`) covering funding, milestones, and CEO candor on risk
- Company roadmap milestones with dates and costs (Junior <$10M, Tahi $21M USD + NZ$35M, Maui ~2031, commercial "next decade")
- Plasma physics underpinned by LDX heritage (MIT experiment) — decades of academic literature available behind the current preprints

**Missing**:
- Peer-reviewed publication of the full power plant study (arXiv preprint status, not yet journal-reviewed)
- Any published systems code output or independent techno-economic study (no ARIES/PROCESS analogue exists yet for this concept)
- Independent academic critique of the power plant design assumptions

**Gaps**:
- No independent TCA/TEA study beyond OpenStar's own work — `not-yet-sourced` — important (needed for cross-check, but OpenStar paper is detailed enough for first-pass modeling)
- Journal review pending — `not-yet-sourced` — nice-to-have

---

### 2. Challenges in Capturing System Function
**Coverage**: Good

**Available**:
- Full 0D power balance for both reactor variants (Reactor A: 667 MW fusion → 208-230 MWe net)
- Detailed description of the levitate/dock cycle as the core operational rhythm: ~100+ hour levitation, ~15-20 min docking for cryogen swap, resulting in 96% duty cycle
- Physics basis for MHD stability (no disruptions; inherent stabilization by adiabatic compression) explicitly contrasted with tokamak behavior
- Bohm-like confinement scaling assumed (conservative, validated from LDX); paper explicitly flags gyro-Bohm alternative
- Power recirculation breakdown: ~500-600 MW auxiliary RF heating vs. 208-230 MWe net electric; very high recirculation fraction (~40-50% gross) is a key system-level challenge
- Flux pump operation during levitation (no physical connections to floating magnet) — novel subsystem with clear engineering description
- Neon slush cryogenic reservoir operation fully described (latent heat budget, reservoir sizing, thermal loads)
- Shield thermal reservoir (Al-Cu eutectic, phase-change heat store) described

**Missing**:
- Edge plasma physics at the separatrix: assumed I-mode-like pedestal (800 eV ions, ~10 Pa edge pressure), but dipole edge behavior is explicitly flagged by the authors as poorly understood
- RF coupling efficiency in closed-field-line geometry: ICRH in dipole topology is different from tokamak ICRH; no published experimental validation
- Plasma fueling scheme (gas injection, pellet fueling) — not described in power plant study
- Ash (helium-4) removal mechanism: critical for D-T operation; not addressed in sources

**Gaps**:
- Edge pedestal physics unknown — `truly-unknown` — **blocking** for confinement validation, but can proceed with Bohm-like assumption with explicit caveat
- ICRH coupling efficiency in dipole geometry — `not-yet-sourced` — important (search: conference papers on ICRH in dipole/mirror geometry; IAEA FEC proceedings)
- Alpha ash exhaust mechanism — `truly-unknown` — important (no divertor in dipole; open question how helium is removed; may be handled by natural outward convection but not analyzed)
- Pellet/gas fueling scheme — `truly-unknown` — nice-to-have

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Good

**Available**:
- Junior prototype build and initial plasma results documented (TRL 4-5 for full system)
- REBCO HTS magnet: 5.6 T at 550 kg demonstrated; non-insulated solder-impregnated coil design proven; 14-coil winding validated. Assessed TRL 7 for REBCO tape itself, TRL 5-6 for the specific non-insulated CICC configuration at power-plant scale
- On-board superconducting flux pump: 170 kJ demonstrated (world record); mV-level output confirmed. TRL 5-6. Scaling to higher voltage for large magnet charging described (semiconductor supplies when docked); identified as novel but not a fundamental blocker
- Neon slush cryogenics: selected for superior latent heat; laboratory-scale demonstrations exist; TRL 4-5 for full on-board reservoir at scale
- Tungsten neutron shield: ITER heritage (prototype blankets); creep modeling done; TRL 5-6
- Li₂O ceramic breeding blanket: ITER TBM baseline; TBR=1.1 confirmed by OpenMC modeling; TRL 5-6
- Roadmap explicitly sequences maturity: Junior (TRL 4-5) → Tahi (TRL 6-7, ~2028) → Maui neutron-producing (TRL 7-8, ~2031)

**Missing**:
- No published TRL table by the authors (TRL assessments in sources are inferred from descriptions)
- Tahi design details not yet public (same magnet volume as Junior but 4× field, 100+ MW auxiliary heating)
- Plasma heating system TRL for ICRH at power plant scale not analyzed

**Gaps**:
- Tahi design specs not published — `proprietary` — nice-to-have (will be known ~2028)
- Formal TRL matrix from OpenStar — `proprietary` — nice-to-have
- ICRH power plant system TRL — `not-yet-sourced` — important (ICRH is mature technology in tokamak context; TRL mapping to dipole application is straightforward with citation to tokamak ICRH literature)

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- REBCO HTS tape identified as critical material: ~450-500 km per reactor (Reactor A); 2nd-gen tape (Faraday "Mirai" class) with >1000 A/mm² Je target cited
- Tungsten for shield: ~500-600 tonnes per reactor; standard fusion-grade tungsten supply chain (ITER precedent)
- Neon (for slush): not rare, but large-scale cryogenic application is novel; no supply chain analysis published
- Lithium-6 enrichment: needed for Li₂O breeding blanket; mentioned only implicitly (Li₂O material chosen) — no enrichment fraction or supply chain discussed
- Helium-4: coolant; supply chain not discussed
- Structural materials: 316LN SS, Inconel 718 identified for vacuum vessel (~200+ tonnes)
- Annual REBCO sacrificial section replacement explicitly modeled as part of O&M (inner section >10-20 year lifetime; outer 20% section ~1 year)

**Missing**:
- No supply chain risk analysis published (no analogue to ITER supply chain studies)
- Lithium-6 enrichment fraction and annual Li consumption not calculated
- Neon supply chain for large-scale slush cryogenics not assessed
- REBCO production scale-up analysis: current global production capacity vs. fleet deployment demand not analyzed
- Tungsten tile manufacturing at scale (grain size control for creep resistance) not addressed

**Gaps**:
- Li-6 enrichment / annual lithium consumption — `derivable` — important (can be estimated from TBR=1.1, fusion power, burn fraction; standard tritium breeding calculation)
- REBCO production scale-up — `not-yet-sourced` — important (search: HTS tape market analyses, CFS supply chain publications; several exist in fusion economics literature — `unverified — confirm existence before searching`)
- Neon supply chain — `not-yet-sourced` — nice-to-have (industrial gas market reports)
- Tungsten supply chain at fusion scale — `not-yet-sourced` — nice-to-have (ITER supply chain documentation likely covers this)

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion power (Reactor A) | 667 MW | arXiv 2602.20564 | h |
| Net electrical output | 208-230 MWe (A); 50-80 MWe (B) | arXiv 2602.20564 | h |
| Plant availability / duty cycle | 96% | arXiv 2602.20564 | m |
| Thermal efficiency (assumed) | 45% | arXiv 2602.20564 | m |
| Auxiliary heating power | ~500-600 MW (A) | arXiv 2602.20564 | m |
| RF plant efficiency (assumed) | 70% | arXiv 2602.20564 | m |
| Cryogenic parasitic load | ~20-30 kW (total) | arXiv 2602.20564 | h |
| Annual magnet replacement (frequency) | 1 year (outer 20% of coil) | arXiv 2602.20564 | m |
| REBCO tape per reactor | ~450-500 km | arXiv 2602.20564 | m |
| Magnet stored energy | ~70-80 GJ | arXiv 2602.20564 | m |
| Docking downtime per cycle | ~15-20 min | arXiv 2602.20564 | m |
| Junior prototype cost | <$10M USD | openstar-roadmap; Bloomberg | h |
| Tahi prototype cost | $21M USD + NZ$35M | Bloomberg | h |
| Fuel (deuterium) | Low-cost commodity | — | h |
| Tritium breeding (on-site) | TBR = 1.1 | arXiv 2602.20564 | m |
| Reactor mass (approx.) | ~5,000-6,000 tonnes | arXiv 2602.20564 | l |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Overnight capital cost (absolute $/kWe) | proprietary | **blocking** | OpenStar explicitly deferred; "subject to change as model developed" |
| LCOE (absolute $/kWh or $/MWh) | proprietary | **blocking** | Same; only relative constraints published |
| Energy conversion cycle type (Rankine vs sCO2) | proprietary | important | Dossier notes 45% thermal efficiency assumed but cycle not selected |
| Specific capital cost by subsystem (CAS breakdown) | proprietary | important | No CAS-equivalent breakdown published |
| Annual REBCO replacement cost | derivable | important | Can estimate from REBCO tape $/m × 500 km × 20% fraction; market price ~$20-50/m |
| O&M cost (staffing, consumables) | not-yet-sourced | important | No analogue study; can adapt from tokamak O&M literature with assumptions |
| Magnet decommissioning / end-of-life costs | truly-unknown | nice-to-have | Not yet analyzed |
| Li-6 enrichment annual cost | derivable | important | From TBR, burn fraction, market price of enriched Li |
| Learning curve / nth-of-a-kind cost factors | truly-unknown | nice-to-have | FOAK concept; no fleet experience |
| Construction schedule / interest during construction | not-yet-sourced | important | Can adapt from analogous small modular designs |

---

## Source Recommendations

1. **REBCO replacement cost basis**: Search for published HTS tape cost projections from CFS, SuperPower, or SuNAM. The key variable is $/m at scale. CFS published estimated REBCO tape costs for SPARC — `unverified — confirm existence before searching`. Otherwise, use current market pricing (~$20-50/m for 4mm tape) as a range.

2. **O&M cost analogue**: Adapt tokamak O&M cost models from ARIES-AT or PROCESS outputs. EPRI nuclear O&M benchmarks may also apply given similar staffing structure. These are published — search ARIES reports on OSTI.

3. **Thermal cycle (Rankine vs sCO2) efficiency range**: Use published supercritical steam / sCO2 cycle literature for fusion applications (e.g., Abdalla et al. or ITER-era thermal cycle studies on OSTI). Difference at 45% is small; bracket 40-48% for sensitivity.

4. **Li-6 enrichment supply chain**: ITER tritium breeding reports cover Li-6 enrichment requirements and costs. Search ITER Organization technical reports or FED journal — published, accessible.

5. **ICRH in dipole/closed-field-line geometry**: Search IAEA FEC proceedings for RF heating in magnetic mirrors or dipole experiments. LDX program publications (MIT, J. Kesner et al.) may include ECRH heating results applicable to Junior's 2.45 GHz system — `unverified — confirm existence before searching`.

6. **Independent power plant study**: No independent study of levitated dipole power plant economics exists yet. The arXiv 2602.20564 paper is the only source. Flag this explicitly in the analysis.

---

## Summary

**Proceed to full analysis.** The two arXiv preprints provide an unusually detailed technical foundation for a TRL 4-5 concept: plasma equilibria, magnet engineering, neutron shielding with Monte Carlo results, cryogenic budgets, and power balance. The data is sufficient to write all five D1+ sections with high confidence on physics and subsystem maturity, and moderate confidence on LCOE with stated assumptions.

**The two material gaps** are (1) absolute capital cost and LCOE values — explicitly withheld by OpenStar pending their own model — and (2) confinement scaling validation, which awaits Tahi (~2028). Both must be flagged prominently in the analysis. For the LCOE model, use the published thermal efficiency, availability, and power balance with parametric capital cost assumptions (e.g., vary overnight cost from $2B-$6B) to derive a cost-of-electricity sensitivity, noting the assumption explicitly.

**Do not wait for additional sources before proceeding.** The gaps are either proprietary (won't be resolved by more searching) or derivable (can be calculated from available data).
