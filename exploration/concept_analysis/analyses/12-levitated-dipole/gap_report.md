Now I have everything I need. Let me write the assessment.

---

# Gap Assessment: Levitated Dipole (D-T)

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: OpenStar has published an unusually detailed power plant design paper for a private company at this stage (arXiv 2602.20564), providing solid nuclear island physics, neutronics, and heating system parameters. The dossier is thorough and high-confidence on physics/taxonomy columns. However, the paper deliberately scopes to the nuclear island and omits balance-of-plant, thermal cycle, and all cost data — meaning LCOE parameter extraction requires heavy analogical reasoning with no published anchors. The concept is ready for a qualitative write-up (D1) and a parametric LCOE model with well-labeled uncertainty, but not for a cost-grounded analysis.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate

**Available**:
- **arXiv 2602.20564** (Simpson et al., 2026): Power plant design at 0D level — plasma physics, neutronics, heating systems, TBR, vacuum vessel geometry, duty cycle, net electrical output (208 MW), fusion power (667 MW). The most detailed primary source; authored by the OpenStar team itself.
- **arXiv 2508.17691**: Junior prototype specs — magnet design, achieved field, first plasma results, flux pump performance (170 kJ stored energy record), ECRH setup, cost ($<10M, built in <2 years).
- **OpenStar website/roadmap**: Prototype timeline (Junior → Tahi ~2028 → Maui ~2031 → Tama Nui commercial), funding ($NZD 35M from NZ government, ~USD 21M), key milestones.
- **News sources** (Bloomberg, RNZ, World Nuclear News, NucNet): Feb 2026 levitated plasma milestone, Tahi specs, funding details.
- **LDX/RT-1 heritage**: Prior academic experiments provide physics validation context (inward turbulent pinch, high-beta quasi-steady discharges) referenced in dossier.

**Missing**:
- Peer-reviewed publication in a journal (all technical sources are arXiv preprints as of research date)
- Any published cost estimates, techno-economic study, or plant cost model
- Independent third-party analysis of the OpenStar design
- Balance-of-plant design details (thermal cycle, BOP efficiency)
- Explicit Q_sci value (paper states a "fixed Qsci" is assumed but does not give the number in accessible HTML)

**Gaps**:
- No cost data published anywhere — `truly-unknown` — **blocking** for quantitative LCOE grounding
- No peer-reviewed publication (preprint only) — `not-yet-sourced` (may be in journal review) — **nice-to-have**
- No independent techno-economic analysis — `truly-unknown` at this stage — **important** for credibility

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Physics basis well-described: Bohm-like confinement scaling (conservative), MHD interchange-mode stability, peaked pressure profiles (p₀ ∝ (R_lcfs/R₀)^(20/3)), local β₀ ~ 3 optimal
- Heating power balance explicit: ICRH ~70% RF efficiency, Paux as essential term, alpha heating fraction model (good-curvature alpha balanced by radiation)
- Neutron management geometry quantified: ~25% of neutrons intercept core magnet, 1 MW-year/m² fluence lifetime, 92% radiant heat transfer to first wall
- Sacrificial coil replacement cycle defined: ~1 year neutron lifetime for outer section
- Duty cycle: >95%, pulsed only by cryogen thermal limits (hours-to-days per pulse)

**Missing**:
- Confinement scaling validation at fusion-relevant parameters — Junior achieved only 42% of design field; Tahi (~2028) is needed to validate Bohm scaling claim
- Q_sci numerical value not stated
- Recirculating power fraction breakdown (auxiliary heating + cryogenics + other)
- Detailed docking/replacement system design (how fast, what automation, what downtime model)
- Neon slush cryocooling system design and parasitic power load

**Gaps**:
- Bohm confinement scaling unvalidated at fusion scale — `truly-unknown` (awaiting Tahi) — **blocking** for physics credibility assessment; must be flagged as a major uncertainty
- Q_sci value not stated in accessible sources — `proprietary` or omitted from paper — **important** (needed to compute recirculating power fraction)
- Cryogenic parasitic power load not quantified — `not-yet-sourced` — **important** for net efficiency
- Docking/replacement automation design not described — `proprietary` — **important** for availability/capacity factor modeling

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **Core HTS magnet (REBCO CICC)**: Junior demonstrated 2.35 T at 42% design current, 170 kJ stored energy via flux pump. TRL ~4. Tahi targets 20 T (~2028); power plant requires 23 T. Significant scaling step.
- **On-board flux pump (transformer-rectifier)**: Demonstrated at record energy levels in Junior (170 kJ). TRL ~4. First demonstration of this specific patented architecture at relevant scale.
- **Magnetic levitation system**: Junior demonstrated levitated plasma confinement Feb 2026 — first commercial company. TRL ~4. "Top magnet" provides levitation and position control.
- **ICRH heating**: Mature technology from tokamak programs. TRL ~8 in general; integration into dipole geometry is novel, TRL ~4-5 for this specific configuration.
- **Vacuum vessel (Inconel 718 + reinforced concrete dome)**: Conventional materials in novel geometry. TRL ~5-6.
- **Li₂O tritium breeding blanket (HCPB)**: Material well-characterized; this geometry and integration is early-stage. TRL ~3.
- **Tungsten/B₄C neutron shield**: Materials mature; two-temperature design (>2000 K hot shield) is technically demanding. TRL ~4.

**Missing**:
- Neon slush cryogenic reservoir system: described conceptually ("slushy pumped in/out"), no demonstration. TRL ~3.
- Sacrificial outer coil section fabrication and replacement procedure: design concept only. TRL ~2-3.
- Remote maintenance/docking system (magnet removal under neutron activation): concept described, no detail. TRL ~2.
- ICRH coupler design for dipole geometry: no published coupler design. TRL ~3.

**Gaps**:
- Neon slush cryogenic system at scale — `proprietary` or `not-yet-sourced` — **important**; if parasitic cryo loads are high, net efficiency drops significantly
- Annual sacrificial coil replacement procedure — `truly-unknown` at engineering detail level — **blocking** for OPEX modeling; replacement cost and downtime are major LCOE drivers
- Remote maintenance system — `truly-unknown` — **important** for availability estimate

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **REBCO HTS tape**: Identified as the core enabling material. 2nd-gen REBCO is commercially available (AMSC, SuNAM, Fujikura, SuperPower). Junior coil (550 kg) already fabricated. CICC architecture for 23 T power plant represents a significant manufacturing scale-up.
- **Tungsten**: Available commercially; used in fusion programs (ITER first wall). No supply bottleneck identified.
- **Boron carbide (B₄C)**: Industrial material with existing supply chains. Sufficient for the neutron shield application.
- **Neon**: Industrial gas, not scarce.
- **Inconel 718**: Well-characterized aerospace/nuclear material.

**Missing** (derivable from known fusion supply chain context):
- REBCO tape volume requirements for power plant scale (23 T CICC) — not stated in sources
- Li₂O blanket material supply chain details (lithium-6 enrichment requirements, enriched Li supply)
- Tritium supply chain (external procurement vs. self-sufficient breeding timeline)
- Cost of REBCO tape at power plant scale — no published estimate

**Gaps**:
- Li-6 enrichment requirements and supply — `not-yet-sourced` — **important**; Li₂O blanket with TBR 1.1 means a tritium-self-sufficient plant, but startup inventory requires external T supply
- REBCO tape volume and cost at 23 T CICC scale — `derivable` from coil geometry + commercial tape pricing, but not stated — **important** for magnet capital cost
- Tritium startup inventory cost and source — `not-yet-sourced` (applicable to all D-T concepts) — **important** but analogous to tokamak programs
- Annual sacrificial coil REBCO tape consumption cost — `derivable` from ~20% of coil mass per year — **blocking** for OPEX

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor for cost anchors; Partial for performance parameters

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electrical output | ~208 MW (Reactor A) | arXiv 2602.20564 | medium (0D model, conservative Bohm scaling) |
| Fusion power | ~667 MW | arXiv 2602.20564 | medium |
| Net plant efficiency | ~31% | arXiv 2602.20564 (derived: 208/667) | medium |
| Duty cycle | >95% | arXiv 2602.20564 | medium |
| Heating system efficiency | ~70% (ICRH RF source) | arXiv 2602.20564 | high |
| Peak magnet field | 23 T (power plant) | arXiv 2602.20564 | medium |
| Sacrificial coil replacement interval | ~1 year | arXiv 2602.20564 | medium |
| Sacrificial coil fraction | ~20% of coil mass | arXiv 2602.20564 | medium |
| TBR target | 1.1 | arXiv 2602.20564 | medium |
| Neutron fluence lifetime (W shield) | 1 MW-year/m² | arXiv 2602.20564 | medium |
| Junior prototype build cost | <$10M | arXiv 2508.17691 | high |
| Development funding | ~NZD 55M total raised | News sources | high |
| Estimated total development need | $500M–$1B | News sources | low |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q_sci value (plasma gain) | proprietary / omitted | blocking | Paper states "fixed Q_sci assumed" but does not give the number; needed to compute recirculating power fraction |
| Thermal/electrical cycle type and efficiency | truly-unknown | blocking | No cycle specified (Rankine vs. sCO2 vs. other); paper stops at thermal power output |
| Capital cost breakdown (by subsystem) | truly-unknown | blocking | No cost data in any published source; no cost model published |
| Core magnet capital cost (23 T CICC, full plant) | derivable | blocking | Can be estimated from REBCO tape volume × commercial pricing, but requires geometry details not in sources |
| Sacrificial coil annual replacement cost (OPEX) | derivable | blocking | ~20% of coil mass per year × REBCO pricing; major OPEX item |
| Blanket and shield replacement cost/interval | truly-unknown | important | Tungsten 1 MW-year/m² lifetime gives interval; cost not estimated |
| Balance of plant capital cost | derivable (by analogy) | important | Analogous to fission or tokamak BOP; no dipole-specific estimate |
| Recirculating power fraction breakdown | not-yet-sourced | important | 208 MW net from 667 MW fusion implies large recirculating fraction; cryogenic load not quantified separately |
| Staffing and O&M cost | truly-unknown | important | Novel maintenance regime (annual magnet docking); no staffing model |
| Plant capital cost (overnight) | truly-unknown | blocking | No published estimate; must be fully constructed by analogy |
| Capacity factor (accounting for magnet replacement downtime) | derivable | important | >95% duty cycle stated; downtime for magnet docking not quantified in hours per year |
| Tritium startup inventory cost | not-yet-sourced | important | Applicable to all D-T concepts; established in ITER literature |

---

## Source Recommendations

1. **Q_sci and recirculating power fraction**: Re-read arXiv 2602.20564 full text (not just the HTML extract) — the numerical Q_sci value may appear in equations or supplementary material. Search strategy: `site:arxiv.org openstar levitated dipole Q_sci OR "scientific gain"`. *Unverified — confirm before searching.*

2. **Thermal cycle efficiency**: Search for fusion balance-of-plant analogues (tokamak, FRC) using sCO2 Brayton or steam Rankine. The specific cycle for this concept is genuinely unpublished; use assumed efficiency range (35–45%) with clear labeling. No specific search likely to help here.

3. **REBCO tape cost and volume at power plant scale**: Commonwealth Fusion Systems (SPARC) and Tokamak Energy have published HTS tape volume estimates and cost projections for their magnets. These provide a credible cost analogue for 23 T CICC. Search: `REBCO tape cost $/kA-m 2024 2025 fusion magnet`. *Unverified — use as analogue, not direct source.*

4. **Coil replacement OPEX**: Derive from (coil mass × sacrificial fraction × $/kg REBCO tape). Junior coil is 550 kg; scale to power plant. REBCO tape pricing is publicly available from manufacturers (~$50–200/m depending on spec).

5. **Blanket and first wall replacement costs**: ITER and US DEMO blanket cost studies (ARIES, EUROfusion) provide per-m² cost estimates for ceramic breeding blankets that could serve as analogues. Search OSTI: `ceramic breeder blanket cost estimate ARIES`. *Unverified — confirm source existence before using.*

6. **LDX experimental data (physics validation)**: Garnier et al. (2012) *Physics of Plasmas* papers on LDX confinement scaling would provide the academic physics basis for Bohm-like scaling claims. Darren Garnier (OpenStar CSO) is an author. Search: `Garnier LDX levitated dipole confinement scaling Physics of Plasmas`. *Likely exists — unverified.*

7. **Tritium startup inventory cost**: ITER Organization and Zucchetti et al. papers on tritium supply and startup costs for D-T reactors. Applicable to all D-T concepts. Not dipole-specific. *Likely exists — unverified.*

---

## Summary

**Proceed to full analysis with caveats.** The physics and operational parameters are well enough characterized to write a credible qualitative section and build a parametric LCOE model. The key action is to be explicit about what the model is doing: OpenStar published a nuclear island design without costs or BOP, so the LCOE model must be constructed almost entirely from analogical reasoning and stated assumptions.

The three hardest gaps are: (1) **no published cost data** — the entire capital cost structure must be built from analogy; (2) **thermal cycle unspecified** — net electrical efficiency has a real uncertainty range; (3) **Q_sci not stated** — recirculating power fraction is partially uncertain. All three should be prominent uncertainty disclosures in the write-up, not buried caveats.

The concept's transparency is actually high relative to its stage — a preprint power plant design from a company that just levitated its first plasma is unusual. The gaps are not from opacity but from the natural boundary of what a nuclear-island-focused paper covers. A well-labeled parametric model with ±50% capital cost uncertainty ranges and a sensitivity sweep on Q and BOP efficiency would be honest and useful.
